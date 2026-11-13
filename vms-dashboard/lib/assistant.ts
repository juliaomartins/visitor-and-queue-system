/**
 * The chat assistant's data layer.
 *
 * The AI lives in the backend (`apps/assistant`): LangChain, the OpenAI key and
 * the retrieval from PostgreSQL. Nothing here talks to OpenAI, and the key
 * never reaches the browser — anything shipped to this bundle is readable by
 * whoever opens dev tools.
 *
 * THE CONVERSATION LIVES IN MEMORY ONLY. Answers carry visitor names, and the
 * rule for this app is that visitor data never lands in localStorage. A reload
 * starts a fresh conversation; that is the price, and it is a small one.
 *
 * Offered files are fetched from the EXISTING export views with the admin's
 * token — `downloadEntriesExport` and `downloadRoster` — so a file from the
 * chat is byte-for-byte the one the Reports and Visitors pages produce.
 */
import { useQuery } from "@tanstack/react-query";
import type { components } from "@vms/contracts";

import { api } from "@/lib/api";
import { ensureAccessToken } from "@/lib/auth";
import { downloadRoster } from "@/lib/badges";
import { downloadEntriesExport, type ReportFormat } from "@/lib/reports";
import { ApiError } from "@/lib/visitors";

export type ChatResponse = components["schemas"]["ChatResponse"];
export type DownloadOffer = components["schemas"]["DownloadOffer"];
export type ChatRole = components["schemas"]["RoleEnum"];

export type ChatTurn = {
  id: number;
  role: ChatRole;
  content: string;
  downloads?: DownloadOffer[];
};

/** Mirrors `MAX_MESSAGES` / `MAX_MESSAGE_CHARS` in apps/assistant/serializers.py. */
export const MAX_HISTORY = 20;
export const MAX_CHARS = 4000;

export function useAssistantStatus(enabled: boolean) {
  return useQuery({
    queryKey: ["assistant", "status"],
    enabled,
    staleTime: 60_000,
    queryFn: async ({ signal }) => {
      const { data, error, response } = await api.GET("/api/v1/assistant/status", {
        signal,
      });
      if (response.status === 404) {
        throw new ApiError("assistant.error.stale", {}, "assistant.error.stale");
      }
      if (error || !data) {
        throw new ApiError("assistant.error.network", {}, "assistant.error.network");
      }
      return data;
    },
  });
}

/**
 * Ask the question at the end of `turns`.
 *
 * Only the text of earlier turns is sent, never the offered files: the backend
 * re-retrieves on a follow-up rather than trusting rows from three questions
 * ago, and a smaller payload is a cheaper one on the admin's key.
 */
export async function askAssistant(turns: ChatTurn[]): Promise<ChatResponse> {
  await ensureAccessToken();

  const messages = turns
    .slice(-MAX_HISTORY)
    .map(({ role, content }) => ({ role, content: content.slice(0, MAX_CHARS) }));

  let result;
  try {
    result = await api.POST("/api/v1/assistant/chat", { body: { messages } });
  } catch {
    throw new ApiError("assistant.error.network", {}, "assistant.error.network");
  }

  const { data, error, response } = result;
  if (data) return data;

  if (response.status === 404) {
    throw new ApiError("assistant.error.stale", {}, "assistant.error.stale");
  }
  if (response.status === 429) {
    throw new ApiError("assistant.error.throttled", {}, "assistant.error.throttled");
  }
  // 502/503 carry a sentence from the backend that says exactly what to fix
  // (no key, a rejected key, no internet). Shown as sent, like every other
  // backend `detail` in this app.
  const detail = (error as { detail?: unknown } | undefined)?.detail;
  if (typeof detail === "string" && detail) throw new ApiError(detail);

  throw new ApiError("assistant.error.unexpected", {}, "assistant.error.unexpected");
}

/** Fetch an offered file through the export view that already makes it. */
export async function downloadOffer(offer: DownloadOffer): Promise<void> {
  if (offer.report === "visitor_list") return downloadRoster();

  const { date_from, date_to, country, category, result } = offer.filters;
  if (!date_from || !date_to) {
    throw new ApiError("assistant.downloadFailed", {}, "assistant.downloadFailed");
  }

  return downloadEntriesExport(
    {
      from: date_from,
      to: date_to,
      country: country ?? undefined,
      category: category ?? undefined,
      result: result ?? undefined,
    },
    offer.format as ReportFormat,
  );
}
