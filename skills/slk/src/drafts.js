/**
 * Slack drafts — uses the undocumented drafts.* API to create real Slack drafts
 * that appear in the Slack editor UI.
 */

import { randomUUID } from "crypto";
import { slackApi } from "./api.js";

/**
 * Create a draft for a channel.
 */
export async function draftChannel(channel, message) {
  const channelId = await resolveChannelId(channel);
  const data = await createDraft(channelId, null, null, message);
  if (data.ok) {
    console.log(`📝 Draft saved → #${channel} (${data.draft.id})`);
    console.log(`   Check Slack — draft icon should appear.`);
  } else {
    console.error(`❌ Failed: ${data.error}`);
    process.exit(1);
  }
}

/**
 * Create a draft thread reply.
 */
export async function draftThread(channel, threadTs, message) {
  const channelId = await resolveChannelId(channel);
  const data = await createDraft(channelId, threadTs, null, message);
  if (data.ok) {
    console.log(`📝 Draft saved → #${channel} thread ${threadTs} (${data.draft.id})`);
    console.log(`   Check Slack — draft icon should appear.`);
  } else {
    console.error(`❌ Failed: ${data.error}`);
    process.exit(1);
  }
}

/**
 * Create a draft DM.
 */
export async function draftUser(userId, message) {
  // Open a DM conversation to get the channel ID
  const conv = await slackApi("conversations.open", { users: userId });
  if (!conv.ok) {
    console.error(`❌ Can't open DM with ${userId}: ${conv.error}`);
    process.exit(1);
  }
  const channelId = conv.channel.id;
  const data = await createDraft(channelId, null, null, message);
  if (data.ok) {
    console.log(`📝 Draft saved → DM @${userId} (${data.draft.id})`);
    console.log(`   Check Slack — draft icon should appear.`);
  } else {
    console.error(`❌ Failed: ${data.error}`);
    process.exit(1);
  }
}

/**
 * List all drafts.
 */
export async function listDrafts() {
  const data = await slackApi("drafts.list");
  if (!data.ok) {
    console.error(`Error: ${data.error}`);
    process.exit(1);
  }

  const drafts = (data.drafts || []).filter((d) => !d.is_deleted && !d.is_sent);
  if (drafts.length === 0) {
    console.log("No active drafts.");
    return;
  }

  for (const d of drafts) {
    const dest = d.destinations?.[0];
    const target = dest?.channel_id || "?";
    const thread = dest?.thread_ts ? ` (thread ${dest.thread_ts})` : "";
    const text = extractText(d.blocks);
    const age = timeSince(d.date_created * 1000);
    console.log(`${d.id}  → ${target}${thread}  (${age})`);
    console.log(`   ${text.substring(0, 120)}${text.length > 120 ? "..." : ""}`);
    console.log();
  }
}

/**
 * Delete a draft.
 */
export async function dropDraft(draftId) {
  // Need client_last_updated_ts to delete — fetch it first
  const list = await slackApi("drafts.list", {});
  if (!list.ok) {
    console.error(`❌ Failed to list drafts: ${list.error}`);
    process.exit(1);
  }

  const draft = (list.drafts || []).find((d) => d.id === draftId);
  if (!draft) {
    console.error(`❌ Draft ${draftId} not found.`);
    process.exit(1);
  }

  const data = await slackApi("drafts.delete", {
    draft_id: draftId,
    client_last_updated_ts: draft.last_updated_ts,
  });
  if (data.ok) {
    console.log(`🗑  Draft ${draftId} deleted.`);
  } else {
    console.error(`❌ Failed: ${data.error}`);
    process.exit(1);
  }
}

// ── Helpers ──────────────────────────────────────────────

async function resolveChannelId(nameOrId) {
  if (/^[CDG]/.test(nameOrId)) return nameOrId;

  const name = nameOrId.replace(/^#/, "");
  const data = await slackApi("conversations.list", {
    types: "public_channel,private_channel,mpim,im",
    limit: 200,
  });
  if (!data.ok) throw new Error(`Failed to list channels: ${data.error}`);
  const ch = data.channels.find(
    (c) => c.name === name || c.name_normalized === name
  );
  if (!ch) throw new Error(`Channel not found: ${nameOrId}`);
  return ch.id;
}

async function createDraft(channelId, threadTs, userIds, text) {
  const destination = { channel_id: channelId };
  if (threadTs) {
    destination.thread_ts = threadTs;
    destination.broadcast = false;
  }
  if (userIds) {
    destination.user_ids = userIds;
  }

  return slackApi("drafts.create", {
    client_msg_id: randomUUID(),
    is_from_composer: false,
    file_ids: [],
    destinations: [destination],
    blocks: [
      {
        type: "rich_text",
        elements: [
          {
            type: "rich_text_section",
            elements: [{ type: "text", text }],
          },
        ],
      },
    ],
  });
}

function extractText(blocks) {
  if (!blocks?.length) return "(empty)";
  const parts = [];
  for (const block of blocks) {
    for (const el of block.elements || []) {
      for (const item of el.elements || []) {
        if (item.type === "text") parts.push(item.text);
        if (item.type === "emoji") parts.push(`:${item.name}:`);
        if (item.type === "link") parts.push(item.url);
      }
    }
  }
  return parts.join("") || "(empty)";
}

function timeSince(ms) {
  const diff = Date.now() - ms;
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}
