# Deep research on arifOS MCP `init_anchor` session anchoring

## Executive summary

The UX requirement that you can authenticate by simply typing **“I’m Arif”** is compatible with strong security *only if “I’m Arif” is treated as an identifier and intent assertion* — not as a secret or factor. A name-assertion alone has essentially no security value against phishing, credential stuffing, replay, or agent automation. Strong assurance must come from **cryptographic proof-of-possession bound to the legitimate origin/session**, while preserving usability by ensuring the human never memorizes random secrets. citeturn17view0turn7view1turn14view0

The best design for `init_anchor` in an AI-agentic platform is therefore:

- Use **passkeys / WebAuthn (FIDO2)** as the default cryptographic authenticator (phishing-resistant via verifier-name binding; no passwords to memorize). citeturn7view1turn3view2turn4view0  
- Make **“I’m Arif”** a **required human assertion** for UX + audit, but bind it into the signed challenge so it cannot be swapped or replayed out of context. citeturn14view0turn7view1  
- Issue a **short-lived, scoped anchor token** that is **sender-constrained (proof-of-possession)** to reduce session token theft/replay, using standards like **DPoP** (`RFC 9449`) and/or **mTLS-bound tokens** (`RFC 8705`) plus JWT PoP semantics (`RFC 7800`). citeturn14view0turn2search0turn2search1turn18search0turn18search3  
- Require **step-up “signed human approval”** for privileged scopes (e.g., delegation grants, credential binding changes, vault sealing), aligning with NIST’s emphasis on phishing resistance, replay resistance, and explicit intent. citeturn7view1turn17view0turn19view0  
- Implement agent delegation as **explicit, constrained leases** (time-bounded, tool-bounded, risk-tier-bounded) with an **auditable delegation chain** (OAuth Token Exchange “act” claim pattern). citeturn2search2turn19view0turn17view0  

Primary standards referenced include guidance from entity["organization","NIST","us standards institute"], entity["organization","FIDO Alliance","authentication standards org"], entity["organization","W3C","web standards consortium"], entity["organization","IETF","internet standards org"], entity["organization","EMVCo","payments standards body"], and entity["organization","C2PA","content provenance coalition"]. citeturn7view0turn4view0turn3view2turn2search0turn4view2turn4view3  

## Problem framing for `init_anchor`

`init_anchor` is not just “login.” In a governed MCP runtime, it is the act of **binding authority** to a session and producing an `auth_context` that downstream policy enforcement will trust. That makes it closer to establishing a *root of control for a decision boundary* than to ordinary sign-in.

The key design implication is to separate (and log) three distinct claims:

1. **Identification & intent (UX)**: “I’m Arif” is a human-readable assertion that expresses who is attempting to anchor and that they intend to do so.  
2. **Authentication (security)**: proof that the claimant controls an authenticator bound to the Arif subscriber account (e.g., passkey). NIST frames authentication as validating authenticators and proving control of secrets bound to the subscriber account. citeturn17view0turn7view1  
3. **Authorization (governance)**: what scopes and risk tiers the anchored session is allowed to exercise (and what must trigger step-up). NIST explicitly anticipates “step-up authentication” when a higher assurance level is required. citeturn17view0turn14view0  

A modern threat model must assume:

- **Phishing and verifier/RP impersonation**, where the attacker tries to trick the user into producing a reusable output. NIST defines phishing resistance as preventing disclosure of secrets and valid authenticator outputs to an impostor verifier without depending on user vigilance; it also states that OTP/manual entry methods are *not* phishing-resistant because they can be relayed. citeturn7view1  
- **Replay of captured artifacts** (token replay, recorded challenge responses). NIST recommends replay resistance via nonces/challenges and specifies replay resistance as a property distinct from the protected channel itself. citeturn7view1turn14view0  
- **Session hijacking and token theft**, including browser/XSS risks, stolen bearer tokens, and long-lived API tokens. NIST session guidance emphasizes securely generated session secrets, cookie protections, and warns that access tokens are not proofs of user presence. citeturn14view0turn19view0  
- **Endpoint compromise**, where malware may attempt to drive authenticators or steal session secrets; NIST explicitly lists endpoint compromise and “authentication fatigue” as threats. citeturn19view0  
- **Collusion / intentional delegation**, where the real subscriber knowingly allows someone (or something) else to act. NIST is explicit that AAL protections are not intended to prevent willful disclosure and that there are few technical controls to stop such collusion. citeturn17view0turn19view0  

In an AI-agent platform, “collusion” includes: “I allow my agent to act as me.” Since you explicitly want delegation, the system must make delegation **explicit, scoped, logged, time-bounded**, and revocable—rather than trying (and failing) to prove “this was typed by human hands, no AI involved.”

## Comparative evaluation of candidate approaches

### High-level comparison table

| Approach | Core security properties | UX friction (human memory) | Phishing resistance | Replay resistance | Delegation model | Revocation & recovery | Privacy implications | Complexity | Best-fit use cases |
|---|---|---|---|---|---|---|---|---|---|
| Passkeys / WebAuthn (hardware-backed when available) | Origin-scoped public-key credentials; user consent & optional user verification; strong basis for AAL2/AAL3 patterns | No memorized random secrets; uses device unlock (biometric/PIN) | Strong (verifier-name binding); NIST cites WebAuthn as phishing-resistant example | Strong via challenge/nonce | Indirect: delegates via signed tokens you issue post-auth | Revoke credential ID; recover via additional passkeys/devices or recovery ceremony | Generally good; attestation can leak device model/identity if overused | Medium | Primary `init_anchor` authenticator, step-up approvals |
| User-controlled Verifiable Credentials / wallet | Issuer-signed claims; holder presentations; can support selective disclosure & short-lived presentations | Usually no memorized secrets; wallet activation via device unlock | Can be strong if presentation is origin/audience-bound and PoP | Strong if challenge-bound presentations | Natural for delegation via attribute bundles + presentation policy | Revocation via issuer status/validity windows; wallet replacement needed | Potential correlation if identifiers reused; selective disclosure mitigates | High | Cross-domain trust, proofing, regulated identity, portable “Arif credential” |
| Signed human-approval transactions | Binds explicit intent to high-risk actions; reduces “consent theater” | Extra step, but no memorized secrets required | High if signing is phishing-resistant and bound to real origin | High (transaction hash + nonce) | Enables explicit delegation grants | Clear audit trail; can invalidate approvals by policy | Minimal incremental data; but creates durable audit artifacts | Medium | High-risk operations (delegation, vault seal, policy changes) |
| Biometric local unlock | Good *activation factor*; not a remote authenticator by itself | Low friction; accessibility-dependent | Depends on underlying cryptographic authenticator | Depends on protocol | Not a delegation primitive | Needs fallback method; biometrics can fail for some users | Biometric templates should remain local; collecting biometrics raises privacy risk | Low–Medium | Local activation for passkeys/wallets; not standalone remote proof |
| Name assertion + server-side binding (no cryptographic proof) | At best: weak risk signals (device cookies, IP reputation) | Very low friction; matches “I’m Arif” | Weak; trivially phishable | Weak; replayable | Delegation indistinguishable from theft/automation | Recovery easy but insecure | Device fingerprinting can be privacy-invasive | Low | Low-risk read-only, pre-auth funnels, fallback *only with strict limits* |
| Social / attestation proofs (trusted referee, applicant reference) | Human attestation to identity or attributes; supports edge cases | High friction/time; no memorization | Not directly applicable | Not directly applicable | Delegation can be formalized via policy/role attestations | Useful for recovery and exceptions; slow but resilient | Sensitive PII; needs careful minimization & notice | Operationally high | Recovery, exception handling, regulated proofing, disputed identity cases |
| Device attestation | Verifies device/authenticator provenance/integrity claims | Usually silent; can add enrollment friction | Helps reduce some impersonation/clone risks | Indirect | Supports device-based policy (managed devices) | Revoke device posture or attested keys | Can enable tracking; enterprise attestation is privacy-sensitive | High | Enterprise/high-assurance anchors; managed fleets; compromised-device detection |
| mTLS | Strong channel binding; client cert proves key possession in TLS | Not human-usable directly | Strong (channel binding) | Strong | Good for service/agent identity; not for human intent | Cert rotation & revocation required | Certificates identify clients; careful scoping needed | Medium–High | Service-to-service, MCP component auth, internal agent calls |
| PKI (X.509) | Mature identity-to-key binding model; supports revocation lists/policies | Heavy for humans; manageable for services | Strong when used with mutual auth | Strong | Delegation via subordinate certs/roles or token exchange | Mature revocation/rotation patterns | Identity exposure depends on certificate contents | High | Enterprise/regulated environments, long-lived service identities |
| Risk-based silent auth | Uses telemetry to reduce friction; “frictionless” accept flow | Minimal friction | Not sufficient alone | Indirect | Supports adaptive step-up | Helps detect anomalies; not a root credential | Requires telemetry governance; privacy risk assessment | Medium | Adaptive step-up, session monitoring, fraud/automation throttling |

This comparison is grounded in: NIST definitions of phishing resistance, replay resistance, authentication intent, session management, and the separation between authentication events and sessions. citeturn7view1turn14view0turn17view0turn19view0 WebAuthn’s origin scoping and privacy model informs the passkey row. citeturn3view2turn9view2 VC and wallet properties come from VC Data Model v2.0 and NIST’s subscriber-controlled wallet model. citeturn3view3turn20search0turn10view0 “Frictionless” risk-based acceptance is analogous to EMV 3DS real-time risk assessment without user challenge. citeturn4view2turn1search14 Sender-constrained token options derive from DPoP, mTLS-bound tokens, and PoP semantics specs. citeturn2search0turn2search1turn18search0turn18search3  

### Key findings from the comparison

A name assertion is non-secret and non-unique; therefore it cannot provide replay resistance, phishing resistance, or protection against automation by itself. NIST’s model makes this explicit: authentication is about proving control of authenticators/secrets bound to an account, and phishing resistance requires cryptographic binding to the verifier/channel rather than manual copy/paste outputs. citeturn17view0turn7view1

Passkeys/WebAuthn best match your UX constraint because they remove password memorization and use the same device unlock the user already uses, while still providing a cryptographic challenge–response flow. citeturn4view0turn3view2turn7view1 WebAuthn also scopes credentials to relying parties and requires user consent for operations, which is structurally aligned with “init anchor” being a deliberate act. citeturn3view2

For agentic systems, delegation is the central security problem. NIST’s guidance on willful sharing/collusion implies the correct engineering response is **explicit delegation controls + auditability**, not trying to “detect AI.” citeturn17view0turn19view0 OAuth token exchange’s actor-chain pattern provides a standards-based way to express “agent acts on behalf of Arif” without collapsing identities. citeturn2search2turn2search3  

## Concrete `init_anchor` protocol proposal

This proposal is designed to satisfy: **Arif types only “I’m Arif”** (no memorized random tokens), while still achieving strong assurance through **phishing-resistant cryptographic authentication**, **replay-resistant challenge binding**, **sender-constrained sessions**, and **explicit delegation leases**.

### Design goals mapped to standards

- **Phishing resistance**: Use WebAuthn/passkeys; NIST explicitly cites WebAuthn as phishing resistant via verifier-name binding, and rejects manual OTP entry as phishing-resistant. citeturn7view1turn3view2turn4view0  
- **Replay resistance**: All assertions must be server-challenge-bound and time-bounded; NIST defines nonce/challenge freshness as a replay-resistance mechanism. citeturn7view1turn14view0  
- **Authentication intent**: Require explicit interaction per anchor and per step-up; NIST distinguishes intent and notes biometrics alone may not always establish it without an explicit action. citeturn7view1turn19view0  
- **Session security**: Derive session secrets from approved randomness, limit lifetime, protect cookies, and prefer proof-of-possession session mechanisms where feasible. citeturn14view0turn18search0turn2search0  
- **Delegation**: Issue constrained, auditable tokens using actor-chain patterns and sender constraints. citeturn2search2turn2search0turn18search3  
- **Auditability and provenance**: Store signed artifacts for the anchor and approvals; for content provenance, C2PA shows a long-lived verification model based on signer identity and revocation/time-stamps (useful as an analogy for durable audit trails). citeturn4view3  

### Protocol overview

#### Roles

- **Client UI**: where you type “I’m Arif.” (Could be the MCP host’s UI, a web console, or a local app wrapper.)
- **Anchor Verifier (arifOS MCP)**: verifies WebAuthn assertions, issues `auth_context`.
- **Agent Runtime(s)**: delegated AI agents that receive constrained delegation tokens.

#### Artifacts

- **AnchorChallenge**: canonical JSON object; hash becomes WebAuthn challenge.
- **WebAuthnAssertion**: standard WebAuthn authentication output.
- **AnchorContext Token (ACT)**: short-lived token representing the anchored session, sender-constrained.
- **Approval Token (APT)**: per-action step-up approval, scoped and one-time.
- **Delegation Lease Token (DLT)**: explicit, limited delegation to an agent.

### Message flow

```mermaid
sequenceDiagram
  autonumber
  participant U as User (Arif)
  participant C as Client UI / MCP Host
  participant S as arifOS MCP Anchor Verifier
  participant A as Agent Runtime

  U->>C: Type human_assertion = "I'm Arif"
  C->>S: POST /init_anchor/start {actor_hint:"Arif", human_assertion, requested_scope, device_signals}
  S-->>C: 200 {anchor_nonce, anchor_challenge, webauthn_options, policy, ttl}

  C->>U: Display summary (scope, ttl, device)
  C->>C: navigator.credentials.get(webauthn_options)
  U->>C: Local UV/consent (biometric/PIN)

  C->>S: POST /init_anchor/finish {anchor_nonce, webauthn_assertion, session_pubkey, dpop_pubthumb}
  S-->>C: 200 {ACT (sender-constrained), auth_context, session_limits}

  Note over C,S: Subsequent calls use ACT + DPoP proof (or mTLS) for replay/theft resistance

  C->>S: POST /stepup/request {action_digest, risk_tier, reason}
  S-->>C: 200 {approval_nonce, approval_challenge, ttl}

  C->>U: Display action preview; require "I'm Arif" re-entry (intent)
  U->>C: Re-type "I'm Arif" + confirm
  C->>C: WebAuthn get() again (step-up signing)
  C->>S: POST /stepup/confirm {approval_nonce, webauthn_assertion}
  S-->>C: 200 {APT (one-time), scope}

  C->>S: POST /delegate {agent_id, constraints, ttl} + APT
  S-->>C: 200 {DLT (subject=Arif, act=agent)}

  A->>S: Tool/API call + DLT + sender-constraining proof
  S-->>A: Allowed/Denied + audit log reference
```

The diagram’s structure follows NIST’s separation of authentication events from sessions, the need for reauthentication/step-up for higher assurance contexts, and secure session binding guidance. citeturn14view0turn17view0  

### Canonical objects and required fields

Below is a concrete, implementable shape. Field names are suggestions; the *important part* is what gets bound together cryptographically and what gets logged.

#### `AnchorChallenge` (server-constructed; hashed into WebAuthn challenge)

Key properties:

- `type`: `"arifOS.init_anchor"`
- `policy_version`: server policy hash/version
- `actor_hint`: `"Arif"` (display / identifier)
- `human_assertion`: exact string typed (display + audit)
- `requested_scope`: e.g., `["anchor:basic"]` or `["anchor:admin"]`
- `risk_tier`: `"low" | "med" | "high"`
- `aud`: relying party identifier (e.g., `arifos-mcp`)
- `nonce`: random server nonce (unique per request)
- `iat`, `exp`: issuance and expiry timestamps
- `client_context_hash`: hash of client-declared context (optional; see assumptions)
- `session_pop`: client-proposed proof-of-possession key thumbprint (optional but recommended)

**Security rationale:** This binds your typed assertion and requested scope into the WebAuthn-signed challenge, making the anchor transaction replay-resistant and preventing scope substitution after signing. This is consistent with NIST’s focus on challenge-based replay resistance and with WebAuthn’s challenge–response model. citeturn7view1turn3view2turn14view0  

#### WebAuthn requirements for `init_anchor`

- Require **user verification** (UV) where possible (biometric/PIN), to raise assurance and reduce the chance of “walk-up” signing. WebAuthn supports platform authenticators and secure-element/TPM-backed authenticators. citeturn3view2turn9view2  
- Treat attestation as **policy-dependent**:  
  - Default `attestation="none"` for privacy, unless you need device trust signals. WebAuthn’s privacy section notes that attestation can expose authenticator model information and correlatable identifiers. citeturn9view2turn8view0turn6search10  
  - Allow “enterprise” attestation only in managed contexts due to tracking risk. citeturn8view1turn6search14  

#### `AnchorContext Token (ACT)` format (JWT, PoP-bound)

Use JWT as a compact claims container per RFC 7519. citeturn2search3  
Bind the token to a proof-of-possession key using `cnf` semantics (RFC 7800) and the `jkt` thumbprint approach used by DPoP (RFC 9449). citeturn18search0turn18search3  

Suggested claims:

- `iss`: `"arifos-mcp"`
- `sub`: stable internal subject id for Arif (not necessarily “Arif” string)
- `aud`: `"arifos-mcp"`
- `iat`, `exp`
- `jti`: unique token id
- `aal`: `"AAL2-like"` or `"AAL3-like"` (do not overclaim; see assumptions)
- `scope`: anchored permissions
- `risk_ceiling`: `"low|med|high"`
- `session_id`
- `cnf`: `{ "jkt": "<thumbprint-of-session-pop-key>" }`
- `human_assertion_hash`: hash of the typed assertion (audit binding without storing raw string in token)

**Sender constraint:** Each request must include a DPoP proof signed with the session PoP key; the resource server checks the DPoP public key matches `cnf.jkt` to detect replay/token theft. citeturn2search0turn18search3  

This aligns with NIST’s recommendations to prefer session management over repeated credential presentation, and to consider proof-of-possession session secrets (device-bound mechanisms) rather than simple bearer tokens when feasible. citeturn14view0  

### TTLs and step-up rules

NIST requires session timeouts and reauthentication, while also acknowledging that limits depend on environment, endpoint type, and may be extended when stronger session maintenance technologies are used. citeturn14view0

A pragmatic policy for arifOS MCP is to separate session classes:

- **ACT-low (interactive governance UI, read/observe)**  
  - `exp`: 24 hours  
  - inactivity timeout: 60 minutes  
  - step-up required: no  
- **ACT-med (agent tooling, non-destructive actions)**  
  - `exp`: 8 hours  
  - inactivity timeout: 30 minutes  
  - step-up: required for delegation issuance and any “state mutation”  
- **ACT-high (sovereign / irreversible, high-impact)**  
  - `exp`: 60 minutes  
  - inactivity timeout: 10–15 minutes  
  - step-up: required for each high-impact action (one-time APT)

These values should be tuned using NIST’s session monitoring and risk management approach, not hardcoded dogma; NIST explicitly expects documented limits and allows coordinated session monitoring signals to trigger reauth or termination. citeturn14view0  

### Delegation token format and constraints

Use OAuth Token Exchange’s actor-chain concept for clarity and audit: subject remains the human (`sub`), while the agent is represented in `act`, and chains can be nested for multi-hop delegation. citeturn2search2  

Suggested **Delegation Lease Token (DLT)** claims:

- `iss`: `"arifos-mcp"`
- `sub`: Arif subject id
- `act`: `{ "sub": "agent:<agent_id>", "client_id": "<agent_runtime_id>" }`
- `aud`: `"arifos-mcp-tools"` (or specific tool audience)
- `scope`: exact tool set (allowlist)
- `risk_ceiling`: maximum allowed risk tier
- `constraints`:  
  - `max_calls`, `max_tokens`, `max_spend` (if applicable)  
  - `time_window`  
  - `data_domains` (e.g., “no external network”, “read-only files”)  
- `iat`, `exp` (usually short; e.g., 5–30 minutes unless continuously renewed)
- `jti`
- `cnf`: proof-of-possession binding:  
  - DPoP key thumbprint (`jkt`), or  
  - mTLS certificate hash (`x5t#S256`) for service runtimes (RFC 8705), depending on deployment. citeturn2search0turn2search1turn18search0turn18search3  

**Why this matters:** it prevents the most dangerous failure mode in agentic systems: an agent quietly inheriting sovereign authority with long-lived bearer credentials. NIST’s threat catalog highlights endpoint compromise, token theft, and the weakness of recovery processes; short-lived, sender-constrained delegation leases directly reduce blast radius. citeturn19view0turn14view0  

## Operational considerations for arifOS MCP

### Usability, accessibility, and “typed name” UX

- The typed name must be framed as **identity selection and intent capture**, not “proof.” NIST’s framing makes clear authentication depends on control of authenticators bound to the subscriber account. citeturn17view0  
- To preserve accessibility, do not require biometrics as the only activation method. NIST discusses biometric variability and the need for alternative methods when biometrics fail; WebAuthn also notes biometrics are used for user verification but are not revealed to the relying party. citeturn7view1turn9view2  
- If you use any “prove you’re human” challenges (CAPTCHA-like), ensure an accessible alternative. W3C’s CAPTCHA accessibility note documents that many CAPTCHAs fail to recognize disabled users as human and can be ineffective. citeturn6search0turn6search8  

### Anti-automation and AI-agent prompting

Because AI agents can generate the same text assertion, the security boundary must be grounded in **authentication intent + local user verification**:

- NIST defines “authentication intent” as requiring explicit claimant response to each authentication/reauth request, specifically to make it harder for malware to use authenticators without the claimant’s knowledge. citeturn7view1turn19view0  
- WebAuthn’s model requires user consent for authenticator operations and provides origin scoping, reducing phishing and automated credential re-use. citeturn3view2  

Practically, “anti-automation” should be implemented as:

- **No anchor issuance without UV/consent** (passkey prompt).  
- **Rate limits / velocity checks** on `/init_anchor/start` and `/finish`.  
- **Session monitoring** signals (typing cadence, device/browser changes) to trigger reauth or termination, with privacy assessment. citeturn14view0  
- **High-risk action gating** by step-up APT, preventing an agent from “walking” into privileged operations just because a base ACT exists.

This does not solve willful delegation (you can always choose to delegate). NIST explicitly states that nearly nothing can be done to prevent intentional collusion from an authentication perspective. The design goal shifts to: make delegation safe, visible, and bounded. citeturn17view0turn19view0  

### Recovery and revocation

NIST notes that recovery is often the weak point because it is expensive and pushed toward less secure backups; it also warns that one factor should not be usable to obtain a different factor. citeturn19view0turn7view1

For arifOS MCP, the recovery design that best matches your “no memorized random tokens” rule is:

- Require **multiple passkeys** bound to the Arif account (e.g., two devices + one roaming security key). This reduces reliance on memorized secrets while avoiding single-device lockout; FIDO passkeys are designed to avoid password memorization and can support cross-device sign-in. citeturn4view0turn5view0  
- Maintain an **offline, non-memorized recovery artifact** (e.g., a hardware key stored physically), used only for re-binding devices. This is still “no memorization,” but it is a ceremony. (Assumption: arifOS governance tolerates occasional ceremony for catastrophic recovery.)
- For exceptional recovery (lost all authenticators), use **attested recovery** (trusted referee / applicant reference patterns) as a human/legal process, especially if you want a defensible audit trail. NIST’s identity proofing guidance explicitly defines trusted referees and applicant references, and requires documentation of such processes. citeturn12view0turn3view0  

Revocation requirements:

- Revoke passkeys by credential ID; do not rely on deleting usernames.  
- Revoke ACT/DLT by `jti` (denylist) for emergency containment.  
- Rotate signing keys for the verifier and publish a JWKS with clear key lifecycle management (implementation detail; ensure audit logs retain verification ability for historical actions).

### Privacy and auditability

Privacy must be treated as an engineering constraint, not a legal footnote:

- WebAuthn notes that many design aspects are motivated by privacy and that public key credentials are scoped to relying parties; attestation and authenticator model data can increase correlation risk. citeturn9view2turn8view0  
- NIST requires privacy risk assessment when doing session monitoring because many signals (geolocation, device characteristics, behavioral biometrics) have privacy implications. citeturn14view0  
- VC/wallet approaches can improve privacy via selective disclosure and short-lived presentations, but must be designed to avoid persistent correlators. citeturn10view0turn10view1turn3view3  
- For durable auditability, store **signed anchor artifacts** and **signed approvals** with trusted timestamps where possible. C2PA’s model illustrates how signed claims plus timestamps allow validation “indefinitely” with revocation context—useful as a conceptual template for “audit receipts.” citeturn4view3  

## Assumptions and boundary conditions

This report necessarily assumes details that were not specified; altering any of these can change the recommendation:

- **Device capabilities**: At least one device you control supports passkeys/WebAuthn with user verification (biometric or PIN). If not, the design shifts toward external security keys or PKI-backed clients. citeturn3view2turn4view0  
- **Threat tolerance**: You want strong resistance to phishing, replay, and token theft, and accept that *endpoint compromise* and *willful delegation* cannot be fully solved by authentication alone. citeturn19view0turn17view0  
- **Regulatory environment**: No specific jurisdictional requirements (e.g., financial KYC, government eID mandates) were provided. If regulation requires identity proofing to a defined assurance level, incorporate NIST IAL-aligned proofing or an equivalent local scheme. citeturn12view0turn3view0  
- **MCP deployment topology**: This proposal assumes a central arifOS MCP verifier that can issue, revoke, and audit tokens. In a fully offline/airgapped design, you would favor local hardware roots and offline logs. citeturn14view0  
- **“Typing name only” interpretation**: “No memorized random tokens” is interpreted as “no passwords/OTPs/KBA,” not “no device unlock.” Passkeys rely on local unlock (biometric/PIN) that the user already uses; requiring a brand-new memorized secret would undermine the stated UX. citeturn4view0turn7view1  

## Primary specs and source links

The most relevant primary specifications and normative guidance used for this design are:

- NIST SP 800-63B-4 (Authentication & Authenticator Management), including phishing resistance, replay resistance, intent, and session management guidance. citeturn17view0turn7view1turn14view0  
- NIST SP 800-63A-4 (Identity Proofing & Enrollment), including trusted referee/applicant reference roles and proofing types. citeturn12view0turn3view0  
- W3C Web Authentication (WebAuthn) specification, including origin scoping and privacy considerations. citeturn3view2turn9view2  
- W3C Verifiable Credentials Data Model v2.0 and associated materials on privacy-respecting, machine-verifiable credentials and selective disclosure best practices. citeturn3view3turn10view0turn10view1  
- IETF RFC 7519 (JWT) for token claims structure. citeturn2search3  
- IETF RFC 7800 (JWT Proof-of-Possession semantics; `cnf` claim). citeturn18search0  
- IETF RFC 9449 (DPoP) for sender-constrained tokens and replay detection. citeturn2search0turn18search3  
- IETF RFC 8705 (OAuth mTLS client authentication and certificate-bound access tokens). citeturn2search1  
- IETF RFC 8693 (OAuth 2.0 Token Exchange; delegation/actor chain). citeturn2search2  
- EMV 3-D Secure documentation on frictionless (risk-based) acceptance as a model for minimizing user challenge while still controlling fraud risk. citeturn4view2turn1search14  
- C2PA Technical Specification (Content Credentials) for signer-identity-based trust decisions and long-lived verification with timestamps and revocation context. citeturn4view3