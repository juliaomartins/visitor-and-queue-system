"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState, type ReactNode } from "react";

import { AssistantPanel } from "@/components/assistant/AssistantDock";
import { AssistantProvider } from "@/components/assistant/assistant-context";
import { PageMetaProvider } from "@/components/page-meta";
import { Sidebar } from "@/components/sidebar";
import { Topbar } from "@/components/topbar";
import { restoreSession } from "@/lib/auth";
import { useT } from "@/lib/i18n";

/**
 * The dashboard shell, and the gate in front of it.
 *
 * The access token is held in memory, so a reload or a fresh tab arrives with
 * nothing. Before rendering anything that will immediately fetch, spend the
 * refresh cookie once to get a token back. Without this, every page would flash a
 * row of 401s on load and recover a moment later.
 */
export default function DashboardLayout({ children }: { children: ReactNode }) {
  const router = useRouter();
  const t = useT();
  const [state, setState] = useState<"checking" | "ready">("checking");

  useEffect(() => {
    let cancelled = false;

    restoreSession().then((ok) => {
      if (cancelled) return;
      if (ok) setState("ready");
      else router.replace("/login");
    });

    return () => {
      cancelled = true;
    };
  }, [router]);

  if (state === "checking") {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p
          className="mono text-xs tracking-[0.14em] text-ink-3 uppercase"
          role="status"
        >
          {t("shell.restoringSession")}
        </p>
      </div>
    );
  }

  return (
    <PageMetaProvider>
      <AssistantProvider>
        <div className="flex min-h-screen">
          <Sidebar />
          <div className="flex min-w-0 flex-1 flex-col">
            <Topbar />
            <main className="flex-1 px-4 py-5 sm:px-6 sm:py-6">{children}</main>
          </div>
          {/* A column of the layout, not an overlay: on a wide screen the page
              reflows beside it. Here rather than in a page, so the
              conversation survives navigation; behind the session gate above. */}
          <AssistantPanel />
        </div>
      </AssistantProvider>
    </PageMetaProvider>
  );
}
