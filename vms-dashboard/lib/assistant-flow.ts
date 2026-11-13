/**
 * The assistant panel's bookkeeping, as plain functions the tests can reach.
 *
 * No React and no imports that need the app's `@/` alias: `npm test` runs
 * these files directly under Node.
 */
import type { components } from "@vms/contracts";

type ChatResponse = components["schemas"]["ChatResponse"];
type ConversationDetail = components["schemas"]["ConversationDetail"];

/**
 * An id for one send, reused by its Retry. The backend stores it on the
 * question (unique), so a Retry after the proxy gave up -- while Django went on
 * to save the answer -- returns the saved pair instead of asking twice.
 *
 * `crypto.randomUUID` is secure-context only, and the event's LAN is plain
 * http (CLAUDE.md, hard constraint 9): on every machine but the server's own
 * localhost it does not exist. The fallback is a v4 UUID from Math.random --
 * not a secret, only a key that two sends of one admin will not share.
 */
export function newRequestId(
  cryptoImpl: { randomUUID?: () => string } = globalThis.crypto ?? {},
): string {
  if (typeof cryptoImpl.randomUUID === "function") return cryptoImpl.randomUUID();

  const hex = Array.from({ length: 32 }, () =>
    Math.floor(Math.random() * 16).toString(16),
  );
  hex[12] = "4";
  hex[16] = ((parseInt(hex[16], 16) & 0x3) | 0x8).toString(16);
  const s = hex.join("");
  return `${s.slice(0, 8)}-${s.slice(8, 12)}-${s.slice(12, 16)}-${s.slice(16, 20)}-${s.slice(20)}`;
}

/**
 * Write a reply into the conversation's cached detail. Messages are matched by
 * id, so a Retry answered from the database adds nothing that is already there.
 */
export function mergeReply(
  old: ConversationDetail | undefined,
  reply: ChatResponse,
): ConversationDetail {
  const messages = [...(old?.messages ?? [])];
  for (const message of [reply.question, reply.answer]) {
    if (!messages.some((m) => m.id === message.id)) messages.push(message);
  }
  return { ...reply.conversation, messages };
}

/**
 * Whether a reply still belongs to what the panel shows.
 *
 * A question can take half a minute. If the admin opens another conversation
 * or starts a new one meanwhile, the answer must still be saved and cached --
 * but it must not drag the panel back to where it was asked. `begin()` marks a
 * send, `navigate()` marks the admin moving away, and `isCurrent(token)` says
 * whether the panel is still where that send began.
 */
export function createSendTracker() {
  let epoch = 0;
  return {
    begin(): number {
      epoch += 1;
      return epoch;
    },
    navigate(): void {
      epoch += 1;
    },
    isCurrent(token: number): boolean {
      return token === epoch;
    },
  };
}
