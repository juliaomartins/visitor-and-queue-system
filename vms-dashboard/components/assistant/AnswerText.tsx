import { Fragment, type ReactNode } from "react";

/**
 * The assistant's answer, typeset.
 *
 * The backend asks the model for paragraphs, short bulleted lists and **bold**
 * for the key figure, and nothing else. This renders exactly that subset into
 * React elements.
 *
 * NEVER `dangerouslySetInnerHTML`, and no markdown library either. The answer
 * quotes visitor names, and visitor names are typed by the public at
 * `/register` — a name containing `<img onerror>` must arrive as text. React
 * escapes every string below, so anything outside the subset simply shows as
 * the characters it is.
 */
export function AnswerText({ text }: { text: string }) {
  const blocks = text.trim().split(/\n{2,}/);
  return <>{blocks.map((block, index) => renderBlock(block, index))}</>;
}

const BULLET = /^\s*(?:[-*•]|\d+[.)])\s+/;

function renderBlock(block: string, key: number): ReactNode {
  const lines = block.split("\n").filter((line) => line.trim());
  const out: ReactNode[] = [];
  let items: string[] = [];
  let prose: string[] = [];

  const flushItems = () => {
    if (!items.length) return;
    out.push(
      <ul key={`ul-${out.length}`}>
        {items.map((item, i) => (
          <li key={i}>{inline(item)}</li>
        ))}
      </ul>,
    );
    items = [];
  };
  const flushProse = () => {
    if (!prose.length) return;
    out.push(
      <p key={`p-${out.length}`}>
        {prose.map((line, i) => (
          <Fragment key={i}>
            {i > 0 ? <br /> : null}
            {inline(line)}
          </Fragment>
        ))}
      </p>,
    );
    prose = [];
  };

  for (const line of lines) {
    if (BULLET.test(line)) {
      flushProse();
      items.push(line.replace(BULLET, ""));
    } else {
      flushItems();
      prose.push(line.replace(/^#+\s*/, ""));
    }
  }
  flushProse();
  flushItems();

  return <Fragment key={key}>{out}</Fragment>;
}

/**
 * The ONLY URLs an answer may turn into links: the author's, which the backend
 * prompt states when asked who built the system (AUTHOR_* in
 * apps/assistant/agent.py — change both together).
 *
 * An allowlist, not a linkifier. Answers quote visitor names typed by the
 * public, so a "name" carrying a phishing URL must stay inert text. Anything
 * not listed here renders as the characters it is.
 */
const TRUSTED_LINKS = [
  "https://github.com/juliaomartins",
  "https://juliaomartins.dev/",
];

const canonical = (url: string) => url.replace(/\/+$/, "").toLowerCase();
const TRUSTED = new Map(TRUSTED_LINKS.map((url) => [canonical(url), url]));

// `[label](url)` or a bare URL. Trailing sentence punctuation is not part of a
// bare URL: "see https://juliaomartins.dev/." must not link to "/.".
const LINK = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)|(https?:\/\/[^\s)\]]+?)(?=[.,;:!?)]*(?:\s|$))/g;

function linkify(text: string, keyPrefix: string): ReactNode[] {
  const out: ReactNode[] = [];
  let last = 0;

  for (const match of text.matchAll(LINK)) {
    const [whole, label, labelled, bare] = match;
    const href = TRUSTED.get(canonical(labelled ?? bare));
    if (!href) continue; // untrusted: leave it in the surrounding text

    const start = match.index;
    if (start > last) out.push(text.slice(last, start));
    out.push(
      <a
        key={`${keyPrefix}-${start}`}
        href={href}
        target="_blank"
        rel="noopener noreferrer"
      >
        {label ?? bare}
      </a>,
    );
    last = start + whole.length;
  }

  if (last < text.length) out.push(text.slice(last));
  return out;
}

/** `**bold**` becomes the figure; trusted links become links; nothing else. */
function inline(text: string): ReactNode[] {
  return text.split(/\*\*(.+?)\*\*/g).flatMap((part, index) =>
    index % 2 === 1 ? (
      <strong key={index}>{linkify(part, `b${index}`)}</strong>
    ) : (
      linkify(part, `t${index}`)
    ),
  );
}
