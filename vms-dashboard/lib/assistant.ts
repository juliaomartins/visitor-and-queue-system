/**
 * The chat assistant's data layer.
 *
 * The AI lives in the backend (`apps/assistant`): LangChain, the OpenAI key and
 * the retrieval from PostgreSQL. Nothing here talks to OpenAI, and the key
 * never reaches the browser — anything shipped to this bundle is readable by
 * whoever opens dev tools.
 *
 * CONVERSATIONS ARE STORED BY THE BACKEND, PER ADMIN. The browser sends one
 * message and the conversation id; the server loads the history itself and
 * saves the question with its answer. Nothing from a conversation is put in
 * localStorage or sessionStorage: answers carry visitor names, and the rule
 * for this app is that visitor data never lands in browser storage. The open
 * conversation's id is React state, so a reload starts at the panel's history
 * rather than mid-conversation — which is one click away.
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
import type { Locale, MessageKey } from "@/lib/locales";
import { downloadEntriesExport, type ReportFormat } from "@/lib/reports";
import { ApiError } from "@/lib/visitors";

export type ChatResponse = components["schemas"]["ChatResponse"];
export type ChatMessage = components["schemas"]["ChatMessage"];
export type ConversationSummary = components["schemas"]["ConversationSummary"];
export type ConversationDetail = components["schemas"]["ConversationDetail"];
export type MemoryNote = components["schemas"]["MemoryNote"];
export type DownloadOffer = components["schemas"]["DownloadOffer"];

/** Mirrors `MAX_MESSAGE_CHARS` in apps/assistant/serializers.py. */
export const MAX_CHARS = 4000;

export const assistantKeys = {
  status: ["assistant", "status"] as const,
  conversations: ["assistant", "conversations"] as const,
  conversation: (id: string) => ["assistant", "conversation", id] as const,
  memories: ["assistant", "memories"] as const,
};

function keyed(key: MessageKey): never {
  throw new ApiError(key, {}, key);
}

/**
 * A 404 with a JSON `detail` is the server answering about a resource ("No such
 * conversation"). A 404 without one is Django not knowing the route at all —
 * the backend is running code older than this page, and a restart fixes it.
 */
function notFound(error: unknown): never {
  const detail = (error as { detail?: unknown } | undefined)?.detail;
  if (typeof detail === "string" && detail) throw new ApiError(detail);
  keyed("assistant.error.stale");
}

export function useAssistantStatus(enabled: boolean) {
  return useQuery({
    queryKey: assistantKeys.status,
    enabled,
    staleTime: 60_000,
    queryFn: async ({ signal }) => {
      const { data, error, response } = await api.GET("/api/v1/assistant/status", {
        signal,
      });
      if (response.status === 404) notFound(error);
      if (error || !data) keyed("assistant.error.network");
      return data;
    },
  });
}

export function useConversations(enabled: boolean) {
  return useQuery({
    queryKey: assistantKeys.conversations,
    enabled,
    queryFn: async ({ signal }) => {
      const { data, error, response } = await api.GET(
        "/api/v1/assistant/conversations",
        { signal },
      );
      if (response.status === 404) notFound(error);
      if (error || !data) keyed("assistant.loadFailed");
      return data;
    },
  });
}

export function useConversation(id: string | null) {
  return useQuery({
    queryKey: assistantKeys.conversation(id ?? "none"),
    enabled: id !== null,
    queryFn: async ({ signal }) => {
      const { data, error, response } = await api.GET(
        "/api/v1/assistant/conversations/{id}",
        { params: { path: { id: id! } }, signal },
      );
      if (response.status === 404) notFound(error);
      if (error || !data) keyed("assistant.loadFailed");
      return data;
    },
  });
}

export function useMemories(enabled: boolean) {
  return useQuery({
    queryKey: assistantKeys.memories,
    enabled,
    queryFn: async ({ signal }) => {
      const { data, error, response } = await api.GET("/api/v1/assistant/memories", {
        signal,
      });
      if (response.status === 404) notFound(error);
      if (error || !data) keyed("assistant.loadFailed");
      return data;
    },
  });
}

/** Ask one question, in a conversation or (with `null`) a new one. */
export async function askAssistant(input: {
  conversation: string | null;
  message: string;
  locale: Locale;
}): Promise<ChatResponse> {
  // A request with a body cannot be replayed after a 401, so get a token first.
  await ensureAccessToken();

  let result;
  try {
    result = await api.POST("/api/v1/assistant/chat", {
      body: {
        conversation: input.conversation,
        message: input.message.slice(0, MAX_CHARS),
        locale: input.locale,
      },
    });
  } catch {
    keyed("assistant.error.network");
  }

  const { data, error, response } = result;
  if (data) return data;
  if (response.status === 404) notFound(error);
  if (response.status === 429) keyed("assistant.error.throttled");

  // 502/503 carry a sentence from the backend that says exactly what to fix
  // (no key, a rejected key, no internet). Shown as sent, like every other
  // backend `detail` in this app.
  const detail = (error as { detail?: unknown } | undefined)?.detail;
  if (typeof detail === "string" && detail) throw new ApiError(detail);
  keyed("assistant.error.unexpected");
}

export async function deleteConversation(id: string): Promise<void> {
  await ensureAccessToken();
  const { error, response } = await api.DELETE("/api/v1/assistant/conversations/{id}", {
    params: { path: { id } },
  });
  if (response.status === 404) notFound(error);
  if (!response.ok) keyed("assistant.error.unexpected");
}

export async function deleteMemory(id: string): Promise<void> {
  await ensureAccessToken();
  const { error, response } = await api.DELETE("/api/v1/assistant/memories/{id}", {
    params: { path: { id } },
  });
  if (response.status === 404) notFound(error);
  if (!response.ok) keyed("assistant.error.unexpected");
}

/** Fetch an offered file through the export view that already makes it. */
export async function downloadOffer(offer: DownloadOffer): Promise<void> {
  if (offer.report === "visitor_list") return downloadRoster();

  const { date_from, date_to, country, category, result } = offer.filters;
  if (!date_from || !date_to) keyed("assistant.downloadFailed");

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
