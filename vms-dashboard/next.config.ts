import path from "node:path";

import type { NextConfig } from "next";

/**
 * The backend is a separate origin (uvicorn on :8000) and emits no CORS headers —
 * django-cors-headers is not installed. Rather than ask the backend to change,
 * the dashboard proxies to it, so every browser request is same-origin:
 *
 *   - no CORS preflight on the Authorization header
 *   - the httpOnly refresh cookie is set and sent as a first-party cookie
 *   - visitor photos resolve, since DRF builds absolute URLs from the Host header
 *     and would otherwise point at :3000 with no route behind it
 *
 * Set VMS_BACKEND_ORIGIN to the server's LAN address for the event.
 */
const BACKEND_ORIGIN = process.env.VMS_BACKEND_ORIGIN ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  /*
    Dev-only cross-origin asset allowance. Literal IPs here are the same trap as
    a hardcoded backend address: wrong the next time the network changes. Match
    the private ranges instead - that covers any LAN this runs on, and nothing
    beyond it.
  */
  allowedDevOrigins: [
    "192.168.*.*",
    "10.*.*.*",
    "172.16.*.*",
    "172.17.*.*",
    "172.18.*.*",
    "172.19.*.*",
    "172.2*.*.*",
    "172.20.*.*",
    "172.30.*.*",
    "172.31.*.*",
    "*.local",
  ],

  // @vms/contracts ships TypeScript source, not a build.
  transpilePackages: ["@vms/contracts"],

  experimental: {
    /*
      How long the /api rewrite waits for the backend. Next's default is 30s
      (`proxyTimeout || 30000` in router-utils/proxy-request.js), and the
      assistant can take longer: one OpenAI call may run 60s plus a retry, and
      an answer can take several. At 30s the browser got a 500 while Django
      went on to save the answer, and Retry saved the question twice. Three
      minutes covers a slow answer; the request id the assistant sends makes a
      retry safe even past that.
    */
    proxyTimeout: 180_000,
  },

  // The contracts package is a file: dependency symlinked to ../vms-contracts.
  // Without the monorepo root, the bundler refuses to follow a symlink that
  // leaves the app directory and cannot resolve it at all.
  turbopack: {
    root: path.resolve(process.cwd(), ".."),
  },

  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${BACKEND_ORIGIN}/api/:path*` },
      { source: "/media/:path*", destination: `${BACKEND_ORIGIN}/media/:path*` },
    ];
  },
};

export default nextConfig;
