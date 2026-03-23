/**
 * Slack auth — extracts session credentials from the Slack desktop app on macOS.
 *
 * 1. Keychain → "Slack Safe Storage" password
 * 2. Cookies SQLite → encrypted `d` cookie → AES-128-CBC decrypt
 * 3. LevelDB files → `xoxc-` token (string scan)
 */

import { execSync, spawnSync } from "child_process";
import { readFileSync, readdirSync, copyFileSync, unlinkSync, writeFileSync } from "fs";
import { join } from "path";
import { homedir, tmpdir } from "os";
import { pbkdf2Sync } from "crypto";

import { existsSync, mkdirSync } from "fs";

const SLACK_DIR_DIRECT = join(homedir(), "Library", "Application Support", "Slack");
const SLACK_DIR_APPSTORE = join(
  homedir(),
  "Library", "Containers", "com.tinyspeck.slackmacgap",
  "Data", "Library", "Application Support", "Slack"
);

function resolveSlackDir() {
  if (existsSync(SLACK_DIR_DIRECT)) return SLACK_DIR_DIRECT;
  if (existsSync(SLACK_DIR_APPSTORE)) return SLACK_DIR_APPSTORE;
  console.error(
    "Could not find Slack data directory.\n" +
    "Checked:\n" +
    `  ${SLACK_DIR_DIRECT}\n` +
    `  ${SLACK_DIR_APPSTORE}\n` +
    "Is Slack installed?"
  );
  process.exit(1);
}

const SLACK_DIR = resolveSlackDir();
const LEVELDB_DIR = join(SLACK_DIR, "Local Storage", "leveldb");
const COOKIES_DB = join(SLACK_DIR, "Cookies");
const CACHE_DIR = join(homedir(), ".local", "slk");
const TOKEN_CACHE = join(CACHE_DIR, "token-cache.json");

let cachedCreds = null;

function getKeychainKey() {
  // Mac App Store Slack uses account "Slack App Store Key", direct download uses "Slack" or "Slack Key"
  const accounts = SLACK_DIR === SLACK_DIR_APPSTORE
    ? ["Slack App Store Key", "Slack Key", "Slack"]
    : ["Slack Key", "Slack", "Slack App Store Key"];

  for (const account of accounts) {
    try {
      return Buffer.from(
        execSync(
          `security find-generic-password -s "Slack Safe Storage" -a "${account}" -w`,
          { encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] }
        ).trim()
      );
    } catch {}
  }

  console.error("Could not find Slack Safe Storage key in Keychain.");
  process.exit(1);
}

function decryptCookie() {
  const tmpDb = join(tmpdir(), `slk_cookies_${Date.now()}.db`);
  copyFileSync(COOKIES_DB, tmpDb);

  try {
    const hex = execSync(
      `sqlite3 "${tmpDb}" "SELECT hex(encrypted_value) FROM cookies WHERE name='d' AND host_key='.slack.com' LIMIT 1;"`,
      { encoding: "utf-8" }
    ).trim();

    if (!hex) throw new Error("No 'd' cookie found in Slack cookie store");

    const encrypted = Buffer.from(hex, "hex");

    if (encrypted.subarray(0, 3).toString() !== "v10") {
      throw new Error("Unknown cookie encryption format");
    }

    const data = encrypted.subarray(3);
    const aesKey = pbkdf2Sync(getKeychainKey(), "saltysalt", 1003, 16, "sha1");
    const iv = Buffer.alloc(16, " ");

    // Decrypt via openssl using spawnSync for clean binary output
    const tmpEnc = join(tmpdir(), `slk_enc_${Date.now()}.bin`);
    writeFileSync(tmpEnc, data);

    const result = spawnSync("openssl", [
      "enc", "-aes-128-cbc", "-d", "-nopad",
      "-K", aesKey.toString("hex"),
      "-iv", iv.toString("hex"),
      "-in", tmpEnc,
    ]);
    const decrypted = result.stdout;

    unlinkSync(tmpEnc);

    if (!decrypted || decrypted.length === 0) {
      throw new Error("Cookie decryption failed");
    }

    // Remove PKCS7 padding
    const padLen = decrypted[decrypted.length - 1];
    const unpadded = padLen <= 16 ? decrypted.subarray(0, -padLen) : decrypted;
    const text = unpadded.toString("utf-8");

    const idx = text.indexOf("xoxd-");
    if (idx < 0) throw new Error("No xoxd- found in decrypted cookie");
    return text.substring(idx);
  } finally {
    try { unlinkSync(tmpDb); } catch {}
  }
}

function extractToken() {
  const files = readdirSync(LEVELDB_DIR).filter(
    (f) => f.endsWith(".ldb") || f.endsWith(".log")
  );

  const tokens = new Set();

  for (const file of files) {
    try {
      const raw = readFileSync(join(LEVELDB_DIR, file));
      const content = raw.toString("latin1");

      // Method 1: direct regex (works for uncompressed entries)
      for (const m of content.matchAll(/xoxc-[a-zA-Z0-9_-]{20,}/g)) {
        tokens.add(m[0]);
      }

      // Method 2: Snappy-compressed LevelDB blocks mangle tokens.
      // Use Python to properly decompress and extract from the JSON structure.
      // Skip here — handled in extractTokenPython() below.
    } catch {}
  }

  // Method 2: Use Python to extract tokens from Snappy-compressed LevelDB
  // Python's regex on binary-stripped data handles compression artifacts better
  try {
    const pyResult = spawnSync("python3", ["-c", `
import os, re
path = ${JSON.stringify(LEVELDB_DIR)}
for f in os.listdir(path):
    if not (f.endswith(".ldb") or f.endswith(".log")): continue
    data = open(os.path.join(path, f), "rb").read()
    # Find all xoxc- positions and extract by reading the hex tail
    pos = 0
    while True:
        idx = data.find(b"xoxc-", pos)
        if idx < 0: break
        pos = idx + 5
        chunk = data[idx:idx+200]
        # Find the 64-char hex tail
        text = chunk.decode("latin1")
        hm = re.search(r'[a-f0-9]{64}', text)
        if not hm: continue
        # Get all bytes from xoxc- to end of hex tail
        end = text.index(hm.group()) + 64
        raw = chunk[:end]
        # Keep only printable token chars
        clean = bytes(b for b in raw if chr(b) in '0123456789abcdef-xoc').decode()
        # Validate structure
        if re.match(r'^xoxc-\\d+-\\d+-\\d+-[a-f0-9]{64}$', clean):
            print(clean)
`], { encoding: "utf-8", timeout: 5000 });
    if (pyResult.stdout) {
      for (const line of pyResult.stdout.trim().split("\n")) {
        if (line.startsWith("xoxc-")) tokens.add(line);
      }
    }
  } catch {}

  if (tokens.size === 0) {
    throw new Error("No xoxc- token found. Is Slack running?");
  }

  // Return all candidates sorted by length desc; caller will validate
  return [...tokens]
    .filter((t) => t.length > 50) // filter truncated tokens
    .sort((a, b) => b.length - a.length);
}

function loadTokenCache() {
  try {
    if (existsSync(TOKEN_CACHE)) {
      return JSON.parse(readFileSync(TOKEN_CACHE, "utf-8"));
    }
  } catch {}
  return null;
}

function saveTokenCache(token) {
  try {
    mkdirSync(CACHE_DIR, { recursive: true });
    writeFileSync(TOKEN_CACHE, JSON.stringify({ token, ts: Date.now() }));
  } catch {}
}

function validateToken(token, cookie) {
  try {
    const result = spawnSync("curl", [
      "-s", "https://slack.com/api/auth.test",
      "-H", `Authorization: Bearer ${token}`,
      "-b", `d=${cookie}`,
    ], { encoding: "utf-8", timeout: 10000 });
    const data = JSON.parse(result.stdout);
    return data.ok;
  } catch {
    return false;
  }
}

export function getCredentials(forceRefresh = false) {
  if (cachedCreds && !forceRefresh) return cachedCreds;

  const cookie = decryptCookie();

  // Try cached token first (fastest path)
  if (!forceRefresh) {
    const cache = loadTokenCache();
    if (cache?.token && validateToken(cache.token, cookie)) {
      cachedCreds = { token: cache.token, cookie };
      return cachedCreds;
    }
  }

  // Extract fresh tokens from LevelDB
  const candidates = extractToken();

  // Validate each candidate
  for (const token of candidates) {
    if (validateToken(token, cookie)) {
      saveTokenCache(token);
      cachedCreds = { token, cookie };
      return cachedCreds;
    }
  }

  // Fallback: return first candidate
  cachedCreds = { token: candidates[0], cookie };
  return cachedCreds;
}

export function refresh() {
  cachedCreds = null;
  return getCredentials(true);
}
