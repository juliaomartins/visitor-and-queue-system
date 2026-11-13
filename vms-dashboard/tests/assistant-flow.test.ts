import assert from "node:assert/strict";
import { describe, test } from "node:test";

import {
  createSendTracker,
  mergeReply,
  newRequestId,
} from "../lib/assistant-flow.ts";

const UUID_V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

const message = (id: number, role: "user" | "assistant", content: string) => ({
  id,
  role,
  content,
  downloads: [],
  created_at: "2026-11-13T09:00:00Z",
});

const summary = {
  id: "c1",
  title: "How many arrived?",
  locale: "en" as const,
  created_at: "2026-11-13T09:00:00Z",
  updated_at: "2026-11-13T09:05:00Z",
  message_count: 2,
};

const reply = {
  conversation: summary,
  question: message(3, "user", "And on the 3rd?"),
  answer: message(4, "assistant", "Two."),
  remembered: [],
};

describe("newRequestId", () => {
  test("is a v4 UUID even where crypto.randomUUID does not exist (LAN http)", () => {
    // Over http://<lan-ip> the page is not a secure context, so randomUUID is
    // absent -- which is every machine at the event but the server itself.
    const ids = new Set(Array.from({ length: 200 }, () => newRequestId({})));
    assert.equal(ids.size, 200);
    for (const id of ids) assert.match(id, UUID_V4);
  });

  test("uses crypto.randomUUID when the context offers it", () => {
    const fixed = "11111111-2222-4333-8444-555555555555";
    assert.equal(newRequestId({ randomUUID: () => fixed }), fixed);
  });
});

describe("mergeReply", () => {
  test("starts a conversation's cache from the reply", () => {
    const merged = mergeReply(undefined, reply);
    assert.deepEqual(merged.messages.map((m) => m.id), [3, 4]);
    assert.equal(merged.title, "How many arrived?");
  });

  test("appends to what is cached", () => {
    const old = { ...summary, messages: [message(1, "user", "q"), message(2, "assistant", "a")] };
    assert.deepEqual(mergeReply(old, reply).messages.map((m) => m.id), [1, 2, 3, 4]);
  });

  test("a retried send answered from the database does not duplicate messages", () => {
    const once = mergeReply(undefined, reply);
    assert.deepEqual(mergeReply(once, reply).messages.map((m) => m.id), [3, 4]);
  });
});

describe("createSendTracker", () => {
  test("a reply belongs to the view it was sent from", () => {
    const tracker = createSendTracker();
    const sent = tracker.begin();
    assert.equal(tracker.isCurrent(sent), true);
  });

  test("opening another conversation mid-question detaches the reply", () => {
    // Review finding: asking in A, opening B, and A's answer pulled the
    // panel back to A.
    const tracker = createSendTracker();
    const sent = tracker.begin();
    tracker.navigate();
    assert.equal(tracker.isCurrent(sent), false);
  });

  test("a newer send supersedes an older one", () => {
    const tracker = createSendTracker();
    const first = tracker.begin();
    const second = tracker.begin();
    assert.equal(tracker.isCurrent(first), false);
    assert.equal(tracker.isCurrent(second), true);
  });
});
