"use client";

import { useMutation } from "@tanstack/react-query";
import { useCallback, useEffect, useId, useRef, useState } from "react";

import { AnswerText } from "@/components/assistant/AnswerText";
import {
  askAssistant,
  downloadOffer,
  MAX_CHARS,
  useAssistantStatus,
  type ChatTurn,
  type DownloadOffer,
} from "@/lib/assistant";
import { useErrorText, useFormat, useT } from "@/lib/i18n";
import type { MessageKey } from "@/lib/locales";

/**
 * The data assistant: a labelled launcher, and a panel that sits beside the page.
 *
 * NON-MODAL ON PURPOSE. The point is to ask "how many from Indonesia?" while
 * looking at the visitor list, so the page behind stays live and clickable —
 * no backdrop, no focus trap. Escape closes it and focus returns to the
 * launcher, which is everything a keyboard user needs from a popover.
 *
 * Mounted once in the dashboard layout, so the conversation survives moving
 * between pages; it is React state and nothing else, so it does not survive a
 * reload — see `lib/assistant.ts` for why that is the rule.
 */

const SUGGESTIONS: MessageKey[] = [
  "assistant.suggest.dayOne",
  "assistant.suggest.vipAbsent",
  "assistant.suggest.refused",
  "assistant.suggest.excel",
];

export function AssistantDock() {
  const t = useT();
  const errorText = useErrorText();
  const panelId = useId();

  const [open, setOpen] = useState(false);
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [draft, setDraft] = useState("");

  const launcherRef = useRef<HTMLButtonElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const logRef = useRef<HTMLDivElement | null>(null);
  const nextId = useRef(1);

  const status = useAssistantStatus(open);
  const disabled = status.data?.enabled === false;

  const ask = useMutation({
    mutationFn: askAssistant,
    onSuccess: (reply) => {
      setTurns((current) => [
        ...current,
        {
          id: nextId.current++,
          role: "assistant",
          content: reply.answer,
          downloads: reply.downloads,
        },
      ]);
    },
  });

  const send = useCallback(
    (text: string) => {
      const content = text.trim().slice(0, MAX_CHARS);
      if (!content || ask.isPending || disabled) return;

      const next: ChatTurn[] = [
        ...turns,
        { id: nextId.current++, role: "user", content },
      ];
      setTurns(next);
      setDraft("");
      ask.mutate(next);
    },
    [ask, disabled, turns],
  );

  const retry = () => {
    if (turns.at(-1)?.role === "user") ask.mutate(turns);
  };

  const close = useCallback(() => {
    setOpen(false);
    // After the panel unmounts, so the launcher exists to receive it.
    requestAnimationFrame(() => launcherRef.current?.focus());
  }, []);

  const reset = () => {
    ask.reset();
    setTurns([]);
    setDraft("");
    inputRef.current?.focus();
  };

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  // Keep the newest message in view. Instant rather than smooth: the reader is
  // waiting for this exact line, and a glide only delays it.
  useEffect(() => {
    const log = logRef.current;
    if (log) log.scrollTop = log.scrollHeight;
  }, [turns, ask.isPending, ask.isError]);

  // Grow the composer with its content, up to about five lines.
  useEffect(() => {
    const input = inputRef.current;
    if (!input) return;
    input.style.height = "auto";
    input.style.height = `${Math.min(input.scrollHeight, 132)}px`;
  }, [draft, open]);

  if (!open) {
    return (
      <button
        ref={launcherRef}
        type="button"
        className="assistant-launcher"
        aria-expanded={false}
        aria-controls={panelId}
        onClick={() => setOpen(true)}
      >
        <IconSpark className="size-[1.15rem]" />
        <span>{t("assistant.launcher")}</span>
      </button>
    );
  }

  return (
    <section
      id={panelId}
      role="dialog"
      aria-modal="false"
      aria-labelledby={`${panelId}-title`}
      className="assistant-panel"
      onKeyDown={(event) => {
        if (event.key === "Escape") {
          event.stopPropagation();
          close();
        }
      }}
    >
      {/* One slice of the woven tais from the organisers' card. Drawn with
          `cover`, so it is a single copy of the photograph, never a tile. */}
      <div aria-hidden className="assistant-seam" />

      <header className="flex items-start gap-3 border-b border-line px-4 pt-3 pb-3">
        <div className="min-w-0 flex-1">
          <h2 id={`${panelId}-title`} className="display text-base leading-snug text-ink">
            {t("assistant.title")}
          </h2>
          <p className="mt-0.5 text-xs leading-relaxed text-ink-3">
            {t("assistant.subtitle")}
          </p>
        </div>
        {turns.length > 0 ? (
          <button
            type="button"
            className="assistant-icon-button"
            onClick={reset}
            disabled={ask.isPending}
            title={t("assistant.clear")}
            aria-label={t("assistant.clear")}
          >
            <IconRefresh className="size-[1.05rem]" />
          </button>
        ) : null}
        <button
          type="button"
          className="assistant-icon-button"
          onClick={close}
          title={t("assistant.close")}
          aria-label={t("assistant.close")}
        >
          <IconClose className="size-[1.05rem]" />
        </button>
      </header>

      <div
        ref={logRef}
        className="min-h-0 flex-1 overflow-y-auto overscroll-contain px-4 py-4"
        role="log"
        aria-live="polite"
        aria-busy={ask.isPending}
      >
        {disabled ? (
          <p className="assistant-notice">{t("assistant.disabled")}</p>
        ) : status.isError ? (
          <p className="assistant-notice">{errorText(status.error)}</p>
        ) : null}

        {turns.length === 0 && !disabled ? (
          <div>
            <p className="text-sm leading-relaxed text-ink-2">
              {t("assistant.emptyLead")}
            </p>
            <ul className="mt-3 flex flex-col items-start gap-2">
              {SUGGESTIONS.map((key) => (
                <li key={key}>
                  <button
                    type="button"
                    className="assistant-suggestion"
                    onClick={() => send(t(key))}
                  >
                    {t(key)}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ) : null}

        <ol className="flex flex-col gap-4">
          {turns.map((turn) => (
            <li key={turn.id}>
              {turn.role === "user" ? (
                <div className="flex justify-end">
                  <p className="assistant-question">
                    <span className="sr-only">{t("assistant.you")}: </span>
                    {turn.content}
                  </p>
                </div>
              ) : (
                <div className="assistant-answer">
                  <span className="sr-only">{t("assistant.bot")}: </span>
                  <AnswerText text={turn.content} />
                  {turn.downloads?.length ? (
                    <ul className="assistant-files">
                      {turn.downloads.map((offer, index) => (
                        <li key={index}>
                          <FileRow offer={offer} />
                        </li>
                      ))}
                    </ul>
                  ) : null}
                </div>
              )}
            </li>
          ))}
        </ol>

        {ask.isPending ? (
          <p className="assistant-thinking mt-4" role="status">
            {t("assistant.thinking")}
          </p>
        ) : null}

        {ask.isError ? (
          <div className="mt-4 flex flex-wrap items-center gap-x-3 gap-y-2">
            <p className="text-sm leading-relaxed text-revoked" role="alert">
              {errorText(ask.error, "assistant.error.unexpected")}
            </p>
            <button type="button" className="assistant-text-button" onClick={retry}>
              {t("assistant.retry")}
            </button>
          </div>
        ) : null}
      </div>

      <form
        className="border-t border-line px-3 pt-3 pb-2.5"
        onSubmit={(event) => {
          event.preventDefault();
          send(draft);
        }}
      >
        <div className="assistant-composer">
          <textarea
            ref={inputRef}
            rows={1}
            value={draft}
            maxLength={MAX_CHARS}
            disabled={disabled}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => {
              if (
                event.key === "Enter" &&
                !event.shiftKey &&
                !event.nativeEvent.isComposing
              ) {
                event.preventDefault();
                send(draft);
              }
            }}
            placeholder={t("assistant.placeholder")}
            aria-label={t("assistant.placeholder")}
            aria-describedby={`${panelId}-hint`}
            className="assistant-input"
          />
          <button
            type="submit"
            className="assistant-send"
            disabled={!draft.trim() || ask.isPending || disabled}
            aria-label={t("assistant.send")}
            title={t("assistant.send")}
          >
            <IconSend className="size-[1.05rem]" />
          </button>
        </div>
        <p id={`${panelId}-hint`} className="sr-only">
          {t("assistant.inputHint")}
        </p>
        <p className="mt-2 px-1 text-[0.7rem] leading-snug text-ink-3">
          {t("assistant.privacy")}
        </p>
      </form>
    </section>
  );
}

/** One offered file: what it is, which slice of the data, and the button. */
function FileRow({ offer }: { offer: DownloadOffer }) {
  const t = useT();
  const format = useFormat();
  const errorText = useErrorText();
  const [state, setState] = useState<"idle" | "busy" | "failed">("idle");
  const [error, setError] = useState<unknown>(null);

  const kind: Record<string, MessageKey> = {
    pdf: "reports.format.pdf",
    xlsx: "reports.format.xlsx",
    csv: "reports.format.csv",
  };

  const day = (iso: string) => {
    // Built from parts, not `new Date(iso)`: that parses as UTC midnight and a
    // browser west of Greenwich would label the 2nd as the 1st.
    const [y, m, d] = iso.split("-").map(Number);
    return format.date(new Date(y, m - 1, d));
  };

  const { date_from, date_to, country, category, result } = offer.filters;
  const scope =
    offer.report === "visitor_list"
      ? [t("assistant.file.allVisitors")]
      : [
          t("assistant.file.entrance"),
          date_from && date_to
            ? date_from === date_to
              ? t("assistant.file.oneDay", { day: day(date_from) })
              : t("assistant.file.range", { from: day(date_from), to: day(date_to) })
            : null,
          country,
          category === "vip" ? t("visitors.tab.vip") : null,
          result ? t(`scan.${result}` as MessageKey) : null,
        ].filter(Boolean);

  // The format leads because it is what differs between two offers in one
  // answer; what the file covers goes underneath, and wraps rather than
  // truncating, since a cut-off date range is a wrong date range.
  const title =
    offer.report === "visitor_list"
      ? t("assistant.file.visitors")
      : t(kind[offer.format]);

  const run = async () => {
    setState("busy");
    setError(null);
    try {
      await downloadOffer(offer);
      setState("idle");
    } catch (caught) {
      setError(caught);
      setState("failed");
    }
  };

  return (
    <div className="assistant-file">
      <span className="assistant-file-badge" aria-hidden>
        {offer.format.toUpperCase()}
      </span>
      <div className="min-w-0 flex-1">
        <p className="text-sm leading-snug font-medium text-ink">{title}</p>
        <p className="mt-0.5 text-xs leading-snug text-ink-3">{scope.join(", ")}</p>
        {state === "failed" ? (
          <p className="mt-1 text-xs text-revoked" role="alert">
            {errorText(error, "assistant.downloadFailed")}
          </p>
        ) : null}
      </div>
      <button
        type="button"
        className="assistant-file-button"
        onClick={run}
        disabled={state === "busy"}
      >
        {state === "busy" ? t("assistant.downloading") : t("assistant.download")}
      </button>
    </div>
  );
}

function IconSpark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden>
      <path
        d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7a2.5 2.5 0 0 1-2.5 2.5H11l-4.2 3.4c-.5.4-1.3 0-1.3-.6V16A2.5 2.5 0 0 1 4 13.5v-7Z"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
      <path
        d="M8.5 10h7M8.5 12.8h4.5"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
      />
    </svg>
  );
}

function IconClose({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden>
      <path
        d="M6 6l12 12M18 6 6 18"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
      />
    </svg>
  );
}

function IconRefresh({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden>
      <path
        d="M19 12a7 7 0 1 1-2.05-4.95M19 4.5V8h-3.5"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconSend({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden>
      <path
        d="M12 19V5M6 11l6-6 6 6"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
