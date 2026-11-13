/**
 * The assistant's mark: the tais key, a squared spiral, on a navy tile.
 *
 * The spiral that winds inward is the motif woven through the tais strip the
 * printed card ends in (and the panel's top edge), so the assistant wears the
 * event's own cloth rather than the stock sparkle or robot face every chat
 * widget carries. White on the console's navy; never gold, which on this
 * console means VIP.
 *
 * Drawn upright as a square spiral and turned 45 degrees, which is how the
 * weave sets it. Two turns and no more: a third closes up below 24px. A
 * hooked lozenge was tried first and read as a "b" at small sizes.
 *
 * Drawn, not shipped as a file, like every icon in this dashboard: it takes
 * the theme's accent and stays sharp at any pixel ratio.
 */
export function AssistantMark({
  size = 28,
  className = "",
}: {
  size?: number;
  className?: string;
}) {
  return (
    <svg
      viewBox="0 0 32 32"
      width={size}
      height={size}
      className={`assistant-mark ${className}`}
      aria-hidden
    >
      <rect width="32" height="32" rx="9" className="assistant-mark-tile" />
      <path
        d="M10 22V10h12v9h-8v-5h4.5v2.2"
        transform="rotate(45 16 16)"
        fill="none"
        stroke="#fff"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
