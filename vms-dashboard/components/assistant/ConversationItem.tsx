"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useRef, useState, type MouseEvent } from "react";

import {
  PencilIcon,
  RowContextMenu,
  TrashIcon,
} from "@/components/visitors/RowContextMenu";
import {
  assistantKeys,
  deleteConversation,
  renameConversation,
  type ConversationDetail,
  type ConversationSummary,
} from "@/lib/assistant";
import { useErrorText, useFormat, useT } from "@/lib/i18n";

/**
 * One saved conversation as a row: open it, or right-click to rename or delete.
 *
 * ONE COMPONENT FOR BOTH LISTS, the recent three in the empty state and the
 * full History view, so the two can never disagree about what a right-click
 * does. The menu is the visitor list's own `RowContextMenu`, so it looks and
 * behaves the same as everywhere else in the console: right-click, or the Menu
 * key / Shift+F10 on a focused row, which anchors to the row because that
 * event carries no pointer position.
 *
 * Right-click does not exist on a touch screen, so the History variant also
 * shows a "More actions" button that opens the same menu. The recent rows keep
 * their chevron instead; History is one tap away from them.
 *
 * Rename edits in place: Enter or leaving the field saves, Escape cancels.
 * Delete asks once more in the row itself -- it cannot be undone, and a
 * browser `confirm()` would block the page.
 */
export function ConversationItem({
  conversation,
  variant,
  active = false,
  now,
  onOpen,
  onDeleted,
}: {
  conversation: ConversationSummary;
  variant: "recent" | "history";
  active?: boolean;
  now: number;
  onOpen: (id: string) => void;
  onDeleted: (id: string) => void;
}) {
  const t = useT();
  const format = useFormat();
  const errorText = useErrorText();
  const queryClient = useQueryClient();

  const [menu, setMenu] = useState<{ x: number; y: number } | null>(null);
  const [mode, setMode] = useState<"idle" | "renaming" | "confirmDelete">("idle");
  const [draft, setDraft] = useState(conversation.title);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);
  // Set once Enter or Escape has decided the edit. Unmounting the field fires
  // a blur, and without this an Escape would save the text it meant to throw
  // away, and an Enter would send the rename twice.
  const settled = useRef(false);

  const title = conversation.title || t("assistant.untitled");

  useEffect(() => {
    if (mode === "renaming") {
      settled.current = false;
      inputRef.current?.select();
    }
  }, [mode]);

  const openMenuAt = (event: MouseEvent<HTMLElement>) => {
    event.preventDefault();
    // The Menu key and Shift+F10 report 0,0; anchor to the row instead.
    if (event.clientX === 0 && event.clientY === 0) {
      const box = event.currentTarget.getBoundingClientRect();
      setMenu({ x: box.left + 24, y: box.bottom - 8 });
      return;
    }
    setMenu({ x: event.clientX, y: event.clientY });
  };

  const saveRename = async () => {
    if (settled.current) return;
    settled.current = true;
    const next = draft.trim();
    if (!next || next === conversation.title) {
      setMode("idle");
      setDraft(conversation.title);
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const saved = await renameConversation(conversation.id, next);
      // Both caches carry the title: the list, and the open conversation.
      queryClient.setQueryData<ConversationSummary[]>(assistantKeys.conversations, (rows) =>
        rows?.map((row) => (row.id === saved.id ? { ...row, title: saved.title } : row)),
      );
      queryClient.setQueryData<ConversationDetail>(
        assistantKeys.conversation(saved.id),
        (detail) => (detail ? { ...detail, title: saved.title } : detail),
      );
      setMode("idle");
    } catch (caught) {
      setError(caught);
      settled.current = false; // let them correct it and try again
    } finally {
      setBusy(false);
    }
  };

  const confirmDelete = async () => {
    setBusy(true);
    setError(null);
    try {
      await deleteConversation(conversation.id);
      queryClient.removeQueries({ queryKey: assistantKeys.conversation(conversation.id) });
      await queryClient.invalidateQueries({ queryKey: assistantKeys.conversations });
      onDeleted(conversation.id);
    } catch (caught) {
      setError(caught);
      setMode("idle");
    } finally {
      setBusy(false);
    }
  };

  const menuElement = menu ? (
    <RowContextMenu
      x={menu.x}
      y={menu.y}
      heading={title}
      onClose={() => setMenu(null)}
      items={[
        {
          label: t("assistant.rename"),
          icon: <PencilIcon />,
          onSelect: () => {
            setDraft(conversation.title);
            setMode("renaming");
          },
        },
        {
          label: t("assistant.deleteConversation"),
          icon: <TrashIcon />,
          danger: true,
          onSelect: () => setMode("confirmDelete"),
        },
      ]}
    />
  ) : null;

  const errorLine = error ? (
    <p className="px-3 pb-2 text-xs text-revoked" role="alert">
      {errorText(error, "assistant.error.unexpected")}
    </p>
  ) : null;

  if (mode === "renaming") {
    return (
      <div className={`assistant-convo is-${variant} is-editing`}>
        <input
          ref={inputRef}
          className="assistant-convo-input"
          value={draft}
          maxLength={120}
          disabled={busy}
          aria-label={t("assistant.renameLabel")}
          onChange={(event) => setDraft(event.target.value)}
          onBlur={saveRename}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              event.preventDefault();
              saveRename();
            }
            if (event.key === "Escape") {
              // Escape here cancels the edit, not the whole panel.
              event.stopPropagation();
              settled.current = true;
              setDraft(conversation.title);
              setMode("idle");
            }
          }}
        />
        {errorLine}
      </div>
    );
  }

  if (mode === "confirmDelete") {
    return (
      <div className={`assistant-convo is-${variant} is-confirming`} role="group" aria-label={title}>
        <span className="assistant-convo-title min-w-0 flex-1">{title}</span>
        <button
          type="button"
          className="assistant-convo-cancel"
          disabled={busy}
          onClick={() => setMode("idle")}
          // Focus lands on the safe choice: a reflexive Enter must not delete
          // a conversation for good.
          autoFocus
        >
          {t("assistant.cancel")}
        </button>
        <button
          type="button"
          className="assistant-convo-delete"
          disabled={busy}
          onClick={confirmDelete}
        >
          {t("assistant.confirmDelete")}
        </button>
      </div>
    );
  }

  return (
    <>
      <div className={`assistant-convo is-${variant}`} onContextMenu={openMenuAt}>
        <button
          type="button"
          className="assistant-convo-open"
          aria-current={active ? "true" : undefined}
          title={t("assistant.rowHint")}
          onClick={() => onOpen(conversation.id)}
        >
          {variant === "recent" ? <IconChat className="assistant-recent-icon" /> : null}
          <span className="min-w-0 flex-1">
            <span className="assistant-convo-title">{title}</span>
            <span className="assistant-convo-meta">
              {format.relative(conversation.updated_at, now)}
            </span>
          </span>
          {variant === "recent" ? <IconChevron className="assistant-recent-chevron" /> : null}
        </button>
        {variant === "history" ? (
          <button
            type="button"
            className="assistant-convo-more"
            aria-label={`${t("assistant.moreActions")}: ${title}`}
            title={t("assistant.moreActions")}
            onClick={(event) => {
              const box = event.currentTarget.getBoundingClientRect();
              setMenu({ x: box.left, y: box.bottom + 4 });
            }}
          >
            <IconDots className="size-[1.05rem]" />
          </button>
        ) : null}
      </div>
      {errorLine}
      {menuElement}
    </>
  );
}

function IconChat({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden>
      <path
        d="M6.5 5.5h11a2.5 2.5 0 0 1 2.5 2.5v6a2.5 2.5 0 0 1-2.5 2.5h-5.2L8.5 19.5v-3h-2A2.5 2.5 0 0 1 4 14V8a2.5 2.5 0 0 1 2.5-2.5Z"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconChevron({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden>
      <path d="m9.5 6 6 6-6 6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconDots({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={className} aria-hidden>
      <circle cx="6" cy="12" r="1.6" />
      <circle cx="12" cy="12" r="1.6" />
      <circle cx="18" cy="12" r="1.6" />
    </svg>
  );
}
