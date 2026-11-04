"""Presence Sync at a glance: high-level two-way diagram with the state-mapping table."""
import sys
OUT = sys.argv[1]
FONT = "'Segoe Print','Comic Sans MS','Chalkboard SE','Comic Neue',cursive"
INK, MUTED, BLUE, RED, GREEN, ORANGE, PURPLE = "#1f2a37", "#566476", "#2f5fd0", "#d64545", "#2f9e5b", "#e07b1a", "#7b4fd6"
W, H = 1200, 760

def mk(i, c):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            f'<path d="M0 0L10 5L0 10z" fill="{c}"/></marker>')

defs = ('<defs><filter id="rough" x="-5%" y="-5%" width="110%" height="110%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="5" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="3"/></filter>'
        '<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#e8eef5"/></pattern>'
        + mk("mg", GREEN) + mk("mo", ORANGE) + mk("mb", BLUE) + mk("mk", INK) +
        f'<symbol id="person" viewBox="-30 -30 60 90" width="60" height="90" overflow="visible">'
        f'<g fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"><circle cx="0" cy="-12" r="16" fill="#fff"/>'
        f'<path d="M0 4V38M-20 18L0 10L20 18M0 38L-14 58M0 38L14 58"/></g></symbol></defs>')

S, T = [], []  # shapes (roughened), texts

def text(x, y, s, size=14, fill=INK, weight=None, anchor="middle", halo=False):
    w = f' font-weight="{weight}"' if weight else ""
    h = ' stroke="#fff" stroke-width="5" paint-order="stroke"' if halo else ""
    T.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}"{w}{h}>{s}</text>')

def arrow(d, c, m, dash=None, w=3.2):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    S.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{ds} marker-end="url(#{m})"/>')

# --- Top: the agent and her two systems ---
S.append('<use href="#person" x="570" y="96"/>')
text(600, 212, "Priya", 15, weight="700")
text(600, 230, "one agent, two systems", 13, MUTED)
# contact-center desktop (monitor)
S.append(f'<rect x="232" y="112" width="124" height="80" rx="8" fill="#e6eefc" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M282 192 v14 M330 192 v14 M262 210 h88" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
text(294, 158, "MAX", 15, BLUE, "700")
text(294, 98, "Status: Working", 15, GREEN, "700")
# desk phone
S.append(f'<rect x="868" y="134" width="124" height="66" rx="14" fill="#fff" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M880 132 q50 -36 100 0" fill="none" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>'
         + "".join(f'<circle cx="{908+i*22}" cy="{156+j*20}" r="4" fill="{INK}"/>' for i in range(3) for j in range(2)))
text(930, 98, "Status: Busy - Contact Center", 15, RED, "700")
arrow("M562 150 H366", BLUE, "mb")
arrow("M640 150 H862", BLUE, "mb")

# --- Middle row ---
S.append('<use href="#person" x="22" y="292"/>')
text(52, 404, "Customer", 14, weight="700")
S.append(f'<rect x="160" y="300" width="200" height="86" rx="40" fill="#f1f3f6" stroke="#7a8797" stroke-width="3"/>')
text(260, 338, "Contact center", 16, weight="700")
text(260, 360, "NICE inContact ACD", 13, MUTED)
S.append(f'<rect x="498" y="296" width="204" height="94" rx="14" fill="#e6eefc" stroke="{BLUE}" stroke-width="3.5"/>')
text(600, 338, "Presence Sync", 18, BLUE, "700")
text(600, 362, "translates both ways", 13, MUTED)
S.append(f'<ellipse cx="902" cy="343" rx="118" ry="52" fill="#f3ecff" stroke="{PURPLE}" stroke-width="3"/>')
text(902, 338, "Phone platform", 16, weight="700")
text(902, 360, "Teams, RingCentral, Zoom...", 12, MUTED)
S.append('<use href="#person" x="1110" y="292"/>')
text(1140, 404, "Customer or", 14, weight="700")
text(1140, 422, "colleague", 14, weight="700")

arrow("M84 343 H154", GREEN, "mg"); text(118, 330, "calls", 12, GREEN, "700")
arrow("M250 298 L282 222", GREEN, "mg"); text(214, 262, "call delivered", 12, GREEN, "700", "middle", True)
arrow("M922 290 L936 214", GREEN, "mg")
# green: contact center -> PSA -> platform
arrow("M362 326 H494", GREEN, "mg"); text(428, 316, "Working (On Call)", 13, GREEN, "700", halo=True)
arrow("M704 326 H780", GREEN, "mg"); text(744, 284, "Busy - Contact Center", 13, GREEN, "700", halo=True)
# orange: platform -> PSA -> contact center
arrow("M782 362 H708", ORANGE, "mo"); text(752, 412, "on an internal call", 13, ORANGE, "700", halo=True)
arrow("M494 362 H366", ORANGE, "mo"); text(430, 384, "Unavailable-UC", 13, ORANGE, "700", halo=True)
# blocked call into the platform
arrow("M1104 343 H1026", INK, "mk")
S.append(f'<path d="M1052 330 l24 26 M1076 330 l-24 26" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>')
text(1064, 316, "can't get through", 12, RED, "700", halo=True)

# --- State mapping table ---
S.append(f'<rect x="150" y="458" width="900" height="232" rx="14" fill="#fff" stroke="{INK}" stroke-width="2.5"/>')
text(600, 492, "State mapping (rules)", 18, weight="700")
text(300, 528, "Contact center state", 14, MUTED, "700")
text(900, 528, "Phone platform status", 14, MUTED, "700")
rows = [("Working (On Call)", "Busy - Contact Center", GREEN, "mg", False, "Publisher rule"),
        ("Unavailable Meeting", "DND", GREEN, "mg", False, "Publisher rule"),
        ("Unavailable-UC", "On an internal call", ORANGE, "mo", True, "Subscriber rule")]
for i, (l, r, c, m, back, rule) in enumerate(rows):
    y = 572 + i * 46
    text(300, y + 5, l, 15, weight="700")
    text(900, y + 5, r, 15, weight="700")
    arrow(f"M{760} {y} H{440}" if back else f"M{440} {y} H{760}", c, m, dash="10 7", w=3)
    text(600, y - 8, rule, 12, c, "700", halo=True)
text(600, 734, "A Bidirectional rule applies both directions in the same call.", 14, MUTED)

title = (f'<text x="{W/2}" y="44" text-anchor="middle" font-size="28" font-weight="700">Presence Sync at a glance</text>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" fill="{INK}">'
       f'{defs}<rect width="{W}" height="{H}" fill="#fff"/><rect width="{W}" height="{H}" fill="url(#grid)"/>{title}'
       f'<g filter="url(#rough)">{"".join(S)}</g>{"".join(T)}</svg>')
open(OUT, "w").write(svg)
print("ok")
