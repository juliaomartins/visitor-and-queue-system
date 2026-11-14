/**
 * The assistant's mark: a speech bubble with two sparkles, on a navy tile.
 *
 * RECOGNISABLE BEATS ORIGINAL HERE, on the owner's instruction. The first mark
 * was the tais key -- a squared spiral from the woven strip -- and it was
 * distinctive and meant nothing to the person looking for "the AI": admins did
 * not read it as something to click. A chat bubble says "conversation" and the
 * sparkles say "AI" in the vocabulary every product now shares, so the mark is
 * understood before the label is read. The tais stays where it is understood
 * as cloth: the panel's top edge.
 *
 * The sparkles are cut out in the tile's own colour (`assistant-mark-tile`),
 * so the mark follows the theme's accent in light and dark. Never gold: gold
 * means VIP on this console. Measured at 112, 34, 24 and 22px; the second
 * sparkle is what keeps it from reading as a plain "new message" badge.
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
        d="M9.5 8.5h13a3.2 3.2 0 0 1 3.2 3.2v7.3a3.2 3.2 0 0 1-3.2 3.2h-6l-4.6 3.6v-3.6h-2.4A3.2 3.2 0 0 1 6.3 19v-7.3a3.2 3.2 0 0 1 3.2-3.2Z"
        fill="#fff"
      />
      <path
        d="M14.6 10.6c.45 2.2 1.55 3.3 3.75 3.75-2.2.45-3.3 1.55-3.75 3.75-.45-2.2-1.55-3.3-3.75-3.75 2.2-.45 3.3-1.55 3.75-3.75Z"
        className="assistant-mark-tile"
      />
      <path
        d="M20.4 15.2c.2.95.65 1.4 1.6 1.6-.95.2-1.4.65-1.6 1.6-.2-.95-.65-1.4-1.6-1.6.95-.2 1.4-.65 1.6-1.6Z"
        className="assistant-mark-tile"
      />
    </svg>
  );
}
