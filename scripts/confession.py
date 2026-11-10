"""Pick today's confession and write it into assets/terminal.svg."""
import datetime
import random
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "assets" / "terminal.svg"
LIST = ROOT / "scripts" / "confessions.txt"

lines = [l.strip() for l in LIST.read_text(encoding="utf-8").splitlines() if l.strip()]

# Shuffle once with a fixed seed, then walk through by date -> no repeats until the list is used up.
order = list(range(len(lines)))
random.Random(1402).shuffle(order)
today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).date()
confession = lines[order[today.toordinal() % len(lines)]]

svg = SVG.read_text(encoding="utf-8")
new_svg, n = re.subn(
    r'(<text id="confession"[^>]*>)(.*?)(</text>)',
    lambda m: m.group(1) + "&gt; " + escape(confession, {'"': "&quot;"}) + m.group(3),
    svg,
    flags=re.S,
)
if n != 1:
    raise SystemExit("confession placeholder not found")
SVG.write_text(new_svg, encoding="utf-8")
print(f"{today}: {confession}")
