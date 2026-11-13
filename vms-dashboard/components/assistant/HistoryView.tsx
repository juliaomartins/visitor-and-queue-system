"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import {
  assistantKeys,
  deleteConversation,
  deleteMemory,
  useConversations,
  useMemories,
} from "@/lib/assistant";
import { useNow } from "@/lib/devices";
import { useErrorText, useFormat, useT } from "@/lib/i18n";

/**
 * The assistant's saved conversations and memory notes, for this admin only.
 *
 * Deleting a conversation is permanent, so it takes two clicks: the first turns
 * the button into "Delete for good", the second does it. Forgetting a note is
 * one click — a note is one short line the admin can say again.
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
  const format = useFormat();
  const errorText = useErrorText();
  const now = useNow(30_000);
  const queryClient = useQueryClient();

  const conversations = useConversations(true);
  const memories = useMemories(true);

  const [confirming, setConfirming] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<unknown>(null);

  const removeConversation = async (id: string) => {
    if (confirming !== id) {
      setConfirming(id);
      return;
    }
    setBusy(id);
    setError(null);
    try {
      await deleteConversation(id);
      queryClient.removeQueries({ queryKey: assistantKeys.conversation(id) });
      await queryClient.invalidateQueries({ queryKey: assistantKeys.conversations });
      onDeleted(id);
    } catch (caught) {
      setError(caught);
    } finally {
      setBusy(null);
      setConfirming(null);
    }
  };

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
                <button
                  type="button"
                  className="assistant-history-open"
                  aria-current={conversation.id === activeId ? "true" : undefined}
                  onClick={() => onOpen(conversation.id)}
                >
                  <span className="assistant-history-title">
                    {conversation.title || t("assistant.untitled")}
                  </span>
                  <span className="assistant-history-meta">
                    {format.relative(conversation.updated_at, now)}
                  </span>
                </button>
                <button
                  type="button"
                  className={
                    confirming === conversation.id
                      ? "assistant-history-delete is-confirming"
                      : "assistant-history-delete"
                  }
                  disabled={busy === conversation.id}
                  onClick={() => removeConversation(conversation.id)}
                  onBlur={() =>
                    setConfirming((current) => (current === conversation.id ? null : current))
                  }
                  aria-label={
                    confirming === conversation.id
                      ? t("assistant.confirmDelete")
                      : `${t("assistant.deleteConversation")}: ${
                          conversation.title || t("assistant.untitled")
                        }`
                  }
                >
                  {confirming === conversation.id ? (
                    t("assistant.confirmDelete")
                  ) : (
                    <IconTrash className="size-[0.95rem]" />
                  )}
                </button>
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

function IconTrash({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden>
      <path
        d="M5 7h14M10 4h4M8 7l.7 11.2a2 2 0 0 0 2 1.8h2.6a2 2 0 0 0 2-1.8L16 7"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
