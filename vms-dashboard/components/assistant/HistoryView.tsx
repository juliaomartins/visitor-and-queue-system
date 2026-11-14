"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { ConversationItem } from "@/components/assistant/ConversationItem";
import { assistantKeys, deleteMemory, useConversations, useMemories } from "@/lib/assistant";
import { useNow } from "@/lib/devices";
import { useErrorText, useT } from "@/lib/i18n";

/**
 * The assistant's saved conversations and memory notes, for this admin only.
 *
 * Each conversation is a `ConversationItem`: open it, or right-click (or use
 * its "More actions" button) to rename or delete it -- the same row and the
 * same menu as the recent conversations in the empty state. Forgetting a note
 * is one click: a note is one short line the admin can say again.
 */
export function HistoryView({
  activeId,
  onOpen,
  onBack,
  onDeleted,
}: {
  activeId: string | null;
  onOpen: (id: string) => void;
  onBack: () => void;
  onDeleted: (id: string) => void;
}) {
  const t = useT();
  const errorText = useErrorText();
  const now = useNow(30_000);
  const queryClient = useQueryClient();

  const conversations = useConversations(true);
  const memories = useMemories(true);

  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<unknown>(null);

  const forget = async (id: string) => {
    setBusy(id);
    setError(null);
    try {
      await deleteMemory(id);
      await queryClient.invalidateQueries({ queryKey: assistantKeys.memories });
    } catch (caught) {
      setError(caught);
    } finally {
      setBusy(null);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <button type="button" className="assistant-text-button self-start" onClick={onBack}>
        {t("assistant.backToChat")}
      </button>

      {error ? (
        <p className="text-sm text-revoked" role="alert">
          {errorText(error, "assistant.error.unexpected")}
        </p>
      ) : null}

      <section aria-labelledby="assistant-history-title">
        <h3 id="assistant-history-title" className="assistant-section-title">
          {t("assistant.historyTitle")}
        </h3>
        <p className="mt-1 text-xs leading-relaxed text-ink-3">{t("assistant.rowHint")}</p>

        {conversations.isError ? (
          <p className="assistant-notice mt-2">{errorText(conversations.error)}</p>
        ) : conversations.data?.length === 0 ? (
          <p className="mt-2 text-sm leading-relaxed text-ink-3">
            {t("assistant.historyEmpty")}
          </p>
        ) : (
          <ul className="mt-2 flex flex-col">
            {(conversations.data ?? []).map((conversation) => (
              <li key={conversation.id} className="assistant-history-row">
                <ConversationItem
                  conversation={conversation}
                  variant="history"
                  active={conversation.id === activeId}
                  now={now}
                  onOpen={onOpen}
                  onDeleted={onDeleted}
                />
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-labelledby="assistant-memory-title">
        <h3 id="assistant-memory-title" className="assistant-section-title">
          {t("assistant.memoriesTitle")}
        </h3>
        <p className="mt-1 text-xs leading-relaxed text-ink-3">
          {t("assistant.memoriesHint")}
        </p>

        {memories.isError ? (
          <p className="assistant-notice mt-2">{errorText(memories.error)}</p>
        ) : memories.data?.length === 0 ? (
          <p className="mt-2 text-sm text-ink-3">{t("assistant.memoriesEmpty")}</p>
        ) : (
          <ul className="mt-2 flex flex-col gap-1.5">
            {(memories.data ?? []).map((note) => (
              <li key={note.id} className="assistant-memory-row">
                <span className="min-w-0 flex-1 text-sm leading-snug text-ink">
                  {note.text}
                </span>
                <button
                  type="button"
                  className="assistant-text-button"
                  disabled={busy === note.id}
                  onClick={() => forget(note.id)}
                >
                  {t("assistant.forget")}
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
