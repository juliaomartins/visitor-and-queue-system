"use client";

import {
  createContext,
  useContext,
  useId,
  useMemo,
  useRef,
  useState,
  type ReactNode,
  type RefObject,
} from "react";

/**
 * Whether the assistant panel is open, shared between its two halves.
 *
 * The launcher lives in the topbar and the panel docks beside the page in the
 * dashboard layout, so they are siblings with no common component of their
 * own. This is the smallest thing that joins them: one boolean, the
 * launcher's element (focus returns there on close) and the id that ties
 * `aria-controls` to the panel.
 */
type AssistantState = {
  open: boolean;
  setOpen: (open: boolean) => void;
  launcherRef: RefObject<HTMLButtonElement | null>;
  panelId: string;
};

const AssistantContext = createContext<AssistantState | null>(null);

export function AssistantProvider({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  const launcherRef = useRef<HTMLButtonElement | null>(null);
  const panelId = useId();

  const value = useMemo(
    () => ({ open, setOpen, launcherRef, panelId }),
    [open, panelId],
  );

  return <AssistantContext value={value}>{children}</AssistantContext>;
}

export function useAssistant(): AssistantState {
  const state = useContext(AssistantContext);
  if (!state) throw new Error("useAssistant needs <AssistantProvider>");
  return state;
}
