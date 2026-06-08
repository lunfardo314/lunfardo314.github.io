#!/usr/bin/env python3
import re, sys, html

TEAL = "#0B7285"   # chain IDs $/...
BLUE = "#1F5FCC"   # dashed tx/output IDs
GRAY = "#9AA0A6"   # de-emphasised long hex / signatures
DARK = "#2B2B2B"   # default text

src = open("printout_full.txt").read().splitlines()

out_lines = []
for line in src:
    # drop raw serialization dumps; they are noise for a conceptual figure
    if re.match(r"\s*bytes \(\d+\):", line):
        continue
    # collapse the long zero run in the produced-amounts vector
    line = re.sub(r"(?:, 0){3,}\]", ", …]", line)

    esc = html.escape(line, quote=False)

    # protect matches behind placeholders, most specific first
    store = []
    def stash(markup):
        store.append(markup)
        return f"\x00{len(store)-1}\x00"

    def t(s, h=6, k=6):
        return s if len(s) <= h + k + 1 else s[:h] + "…" + s[-k:]

    # chain IDs $/<hex> (full 48 or already-shortened)  (truncate the hex)
    esc = re.sub(r"\$/([0-9a-f]{6,})",
                 lambda m: stash(f'<span foreground="{TEAL}">$/{t(m.group(1))}</span>'), esc)
    # dashed tx / output IDs  [s]slot-tick-<hex>[#idx]  (truncate the hash part)
    esc = re.sub(r"\b([s]?\d+-\d+-)([0-9a-f]{6,})(#\d+)?",
                 lambda m: stash(f'<span foreground="{BLUE}">{m.group(1)}{t(m.group(2))}{m.group(3) or ""}</span>'), esc)
    # prefixed hashes / signatures  32x.. 64x.. sig=64x..  (truncate)
    esc = re.sub(r"((?:sig=)?(?:32x|64x))([0-9a-f]+)",
                 lambda m: stash(f'<span foreground="{GRAY}">{m.group(1)}{t(m.group(2))}</span>'), esc)
    # any remaining bare long hex blob (holder IDs, compound index values)  (truncate)
    esc = re.sub(r"[0-9a-f]{40,}",
                 lambda m: stash(f'<span foreground="{GRAY}">{t(m.group(0))}</span>'), esc)

    # bold the top-level field/section lines (no leading whitespace)
    if line and not line[0].isspace():
        esc = f"<b>{esc}</b>"

    for i, mk in enumerate(store):
        esc = esc.replace(f"\x00{i}\x00", mk)
    out_lines.append(esc)

markup = f'<span foreground="{DARK}">' + "\n".join(out_lines) + "</span>"
open("printout.pango", "w").write(markup)
print("lines:", len(out_lines))
