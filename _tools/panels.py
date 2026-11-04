"""Generate the six Presence Sync story panels and the overview sheet."""
import os, sys

OUT = sys.argv[1]
FONT = "'Segoe Print','Comic Sans MS','Chalkboard SE','Comic Neue',cursive"
INK, MUTED, BLUE, RED, GREEN = "#1f2a37", "#566476", "#2f5fd0", "#d64545", "#2f9e5b"
PW, PH = 570, 480          # panel size
SW, SH = PW + 30, PH + 30  # single-panel canvas

DEFS = f"""<defs>
<filter id="rough" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="3.5"/>
</filter>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#e8eef5" stroke-width="1"/></pattern>
<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker>
<marker id="arb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{RED}"/></marker>
<marker id="arg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{GREEN}"/></marker>
<symbol id="person" viewBox="-30 -30 60 90" width="60" height="90" overflow="visible">
  <g fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"><circle cx="0" cy="-12" r="16" fill="#fff"/><path d="M0 4V38M-20 18L0 10L20 18M0 38L-14 58M0 38L14 58"/></g>
</symbol>
<symbol id="phone" viewBox="0 0 64 100" width="64" height="100" overflow="visible">
  <g stroke="{INK}" stroke-width="3"><rect x="2" y="2" width="60" height="96" rx="10" fill="#fff"/><rect x="10" y="14" width="44" height="60" rx="3" fill="#e6eefc"/><circle cx="32" cy="86" r="5" fill="#fff"/></g>
</symbol>
</defs>"""


def frame(num, title):
    return (f'<rect width="{PW}" height="{PH}" rx="14" fill="#fff" stroke="{INK}" stroke-width="3" filter="url(#rough)"/>'
            f'<circle cx="36" cy="38" r="17" fill="{BLUE}"/>'
            f'<text x="36" y="45" text-anchor="middle" font-size="18" fill="#fff" font-weight="700">{num}</text>'
            f'<text x="64" y="46" font-size="22" font-weight="700">{title}</text>')


def caption(bullets, y0=None):
    """bullets: list of lists of lines. Renders bullet markers and indents continuation lines."""
    lines = sum(len(b) for b in bullets)
    y = y0 if y0 else PH - 24 - (lines - 1) * 22
    out = []
    for b in bullets:
        for i, line in enumerate(b):
            if i == 0:
                out.append(f'<text x="30" y="{y}" font-size="15">•</text>')
            out.append(f'<text x="46" y="{y}" font-size="15">{line}</text>')
            y += 22
    return "".join(out)


def t(x, y, s, size=13, weight=None, fill=None, anchor="middle", extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    f = f' fill="{fill}"' if fill else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"{w}{f}{extra}>{s}</text>'


P = {}

P[1] = ("1-two-phones", frame(1, "Two phones that never talk") + f"""
<g filter="url(#rough)">
  <use href="#person" x="16" y="140"/>
  <path d="M76 190 H112" stroke="{INK}" stroke-width="3" marker-end="url(#ar)"/>
  <use href="#phone" x="118" y="126"/>
  <use href="#phone" x="480" y="126"/>
  <use href="#person" x="262" y="140"/>
  <path d="M186 176 Q222 150 258 176" fill="none" stroke="{RED}" stroke-width="3" marker-end="url(#arr)"/>
  <path d="M332 114 h124 a12 12 0 0 1 12 12 v38 a12 12 0 0 1 -12 12 h-84 l-22 22 l3 -22 h-21 a12 12 0 0 1 -12 -12 v-38 a12 12 0 0 1 12 -12z" fill="#fff" stroke="{INK}" stroke-width="2.5"/>
  <path d="M220 290 l46 28 M266 290 l-46 28" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>
</g>
{t(94, 178, "calls in", 11, fill=MUTED)}
{t(46, 252, "Customer", 13, "700")}
{t(150, 252, "Customer line", 14, "700")}
{t(150, 270, "contact center", 13, fill=MUTED)}
{t(292, 252, "Priya", 14, "700")}
{t(292, 270, "the agent", 13, fill=MUTED)}
{t(512, 252, "Work phone", 14, "700")}
{t(512, 270, "Teams, Zoom...", 13, fill=MUTED)}
{t(222, 128, '"New customer!"', 14, fill=RED)}
{t(400, 140, "On a Teams call", 13)}
{t(400, 158, "with my manager", 13)}
{t(282, 312, "Double-booked!", 20, "700", RED, "start")}
""" + caption([["Priya has a customer line and a work phone."],
               ["Neither knows what the other is doing, so a",
                "customer reaches her while she's already busy",
                "on another call."]]))

P[2] = ("2-translator", frame(2, "A translator in the middle") + f"""
<g filter="url(#rough)">
  <rect x="24" y="150" width="130" height="80" rx="10" fill="#fff" stroke="{INK}" stroke-width="3"/>
  <rect x="210" y="135" width="150" height="110" rx="12" fill="#e6eefc" stroke="{BLUE}" stroke-width="3.5"/>
  <rect x="416" y="150" width="130" height="80" rx="10" fill="#fff" stroke="{INK}" stroke-width="3"/>
  <path d="M156 168 H206" stroke="{BLUE}" stroke-width="3" marker-end="url(#arb)"/>
  <path d="M362 168 H412" stroke="{BLUE}" stroke-width="3" marker-end="url(#arb)"/>
  <path d="M412 214 H364" stroke="{GREEN}" stroke-width="3" marker-end="url(#arg)"/>
  <path d="M206 214 H158" stroke="{GREEN}" stroke-width="3" marker-end="url(#arg)"/>
</g>
{t(89, 186, "Customer", 14, "700")}{t(89, 204, "line", 14, "700")}
{t(285, 184, "Presence", 17, "700", BLUE)}{t(285, 206, "Sync", 17, "700", BLUE)}
{t(481, 186, "Work", 14, "700")}{t(481, 204, "phone", 14, "700")}
{t(285, 116, '"She is busy, hold her calls"', 15, fill=BLUE)}
{t(285, 278, '"She is free again"', 15, fill=GREEN)}
""" + caption([["When one side sees Priya get busy or free,",
                "Presence Sync tells the other side right away."],
               ["Both directions, in real time, for many",
                "companies at once."]]))

P[3] = ("3-echo", frame(3, "The echo") + f"""
<g filter="url(#rough)">
  <use href="#person" x="20" y="92"/>
  <rect x="100" y="100" width="124" height="58" rx="10" fill="#fff" stroke="{INK}" stroke-width="3"/>
  <rect x="290" y="100" width="124" height="58" rx="10" fill="#fff" stroke="{INK}" stroke-width="3"/>
  <use href="#person" x="474" y="92"/>
  <path d="M80 129 H96" stroke="{INK}" stroke-width="3" marker-end="url(#ar)"/>
  <path d="M226 129 H286" stroke="{INK}" stroke-width="3" marker-end="url(#ar)"/>
  <path d="M416 129 H470" stroke="{INK}" stroke-width="3" marker-end="url(#ar)"/>
  <path d="M262 200 h200 a12 12 0 0 1 12 12 v30 a12 12 0 0 1 -12 12 h-200 a12 12 0 0 1 -12 -12 v-30 a12 12 0 0 1 12 -12z M352 200 l0 -24 l20 24" fill="#fff" stroke="{RED}" stroke-width="2.5"/>
  <path d="M320 256 Q292 276 254 290" fill="none" stroke="{RED}" stroke-width="3" marker-end="url(#arr)"/>
  <rect x="64" y="270" width="186" height="64" rx="12" fill="#e6eefc" stroke="{BLUE}" stroke-width="3.5"/>
  <g transform="rotate(-6 360 312)"><rect x="268" y="272" width="190" height="84" fill="#ffe27a" stroke="#b8941a" stroke-width="2"/></g>
</g>
{t(50, 200, "Customer", 13, "700")}
{t(162, 125, "Customer", 13, "700")}{t(162, 143, "line", 13, "700")}
{t(352, 125, "rings through", 13, "700")}{t(352, 143, "work phone", 13, "700")}
{t(504, 200, "Priya", 13, "700")}
{t(362, 233, '"Priya is on a call!"', 15, fill=RED)}
{t(157, 308, "Presence Sync", 16, "700", BLUE)}
<g transform="rotate(-6 360 312)">
{t(363, 298, "Sticky note:", 14, "700")}{t(363, 320, '"That call is ours.', 14)}{t(363, 340, 'Ignore it."', 14)}
</g>
""" + caption([["The customer line rings through Priya's work",
                "phone, so the phone reports our own call back."],
               ["A sticky note on Priya says: that echo is ours."]]))

P[4] = ("4-late-sticky-note", frame(4, "When the sticky note is late") + f"""
<g filter="url(#rough)">
  <circle cx="92" cy="160" r="46" fill="#fff" stroke="{INK}" stroke-width="3"/>
  <path d="M92 160 V128 M92 160 L116 172" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>
  <rect x="172" y="96" width="370" height="60" rx="10" fill="#fff" stroke="{INK}" stroke-width="2.5"/>
  <rect x="172" y="170" width="370" height="60" rx="10" fill="#fff" stroke="{INK}" stroke-width="2.5"/>
  <rect x="172" y="244" width="370" height="60" rx="10" fill="#eaf7ef" stroke="{GREEN}" stroke-width="3"/>
  <path d="M510 114 l14 14 M524 114 l-14 14" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>
  <path d="M508 200 l8 9 l14 -18" fill="none" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>
</g>
{t(92, 234, "a split second", 13, fill=MUTED)}
{t(188, 122, "1. Sticky note on Priya?", 15, "700", anchor="start")}
{t(188, 144, "Not there yet: the alert came first", 13, fill=MUTED, anchor="start")}
{t(188, 196, "2. Whose number is on the call?", 15, "700", anchor="start")}
{t(188, 218, "One of the customer-line numbers", 13, fill=MUTED, anchor="start")}
{t(188, 270, "So it's ours: ignore the echo", 15, "700", GREEN, "start")}
{t(188, 292, "Priya stays correctly booked", 13, fill=MUTED, anchor="start")}
""" + caption([["Sometimes the phone's alert arrives a split",
                "second before the sticky note."],
               ["Backup check: a customer-line number on the",
                "call means it's our own call."]]))

rows = ["RingCentral", "Fuze", "Zoom", "MS Teams", "Google Meet", "Atos"]
p5 = []
for i, name in enumerate(rows):
    y = 78 + i * 42
    p5.append(f'<rect x="28" y="{y}" width="130" height="32" rx="8" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
              f'<rect x="196" y="{y+1}" width="80" height="30" rx="6" fill="#ffe27a" stroke="#b8941a" stroke-width="2"/>'
              f'<path d="M160 {y+16}H192" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>'
              f'<path d="M278 {y+16} Q330 {(y+16+208)/2} 380 {200+i*3}" fill="none" stroke="{BLUE}" stroke-width="2.5"'
              + (' marker-end="url(#arb)"' if i in (0, 5) else "") + '/>')
P[5] = ("5-one-brain", frame(5, "Six phone companies, one brain") + '<g filter="url(#rough)">' + "".join(p5) +
        f'<rect x="384" y="160" width="160" height="96" rx="12" fill="#e6eefc" stroke="{BLUE}" stroke-width="3.5"/></g>' +
        "".join(t(93, 78 + i * 42 + 21, n, 14, "700") + t(236, 78 + i * 42 + 21, "translator", 12) for i, n in enumerate(rows)) +
        t(464, 202, "One shared", 16, "700", BLUE) + t(464, 224, "brain", 16, "700", BLUE) +
        caption([["Every company reports calls in its own way."],
                 ["Each gets a small translator into one common",
                  "language, and one shared brain decides."],
                 ["A new partner = a new translator."]]))

P[6] = ("6-respect-the-person", frame(6, "Respect the person") + f"""
<g filter="url(#rough)">
  <rect x="30" y="86" width="100" height="40" rx="20" fill="#fff4cf" stroke="#b8941a" stroke-width="2.5"/>
  <rect x="200" y="86" width="110" height="40" rx="20" fill="#fde8e8" stroke="{RED}" stroke-width="2.5"/>
  <rect x="380" y="86" width="100" height="40" rx="20" fill="#fff4cf" stroke="#b8941a" stroke-width="2.5"/>
  <path d="M132 106H196" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>
  <path d="M312 106H376" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>
  <path d="M206 232 H496" stroke="{INK}" stroke-width="3" stroke-dasharray="8 6"/>
  <use href="#person" x="200" y="202" width="44" height="66"/>
  <use href="#person" x="310" y="202" width="44" height="66"/>
  <use href="#person" x="420" y="202" width="44" height="66"/>
</g>
{t(80, 111, "Lunch", 14, "700")}{t(255, 111, "On a call", 14, "700")}{t(430, 111, "Lunch", 14, "700")}
{t(30, 156, "After a call, Priya goes back to what she was doing.", 14, fill=MUTED, anchor="start")}
{t(30, 176, "The system only undoes changes it made itself.", 14, fill=MUTED, anchor="start")}
{t(92, 234, "Conference", 14, "700")}{t(92, 254, "or transfer", 14, "700")}
{t(222, 296, "Priya", 13, "700")}{t(222, 314, "hangs up: free", 13, "700", GREEN)}
{t(332, 314, "still busy", 13, fill=RED)}{t(442, 314, "still busy", 13, fill=RED)}
""" + caption([["On calls with several people, each person is",
                "tracked separately."],
               ["When Priya hangs up, only Priya becomes free."],
               ["Manual choices like Lunch always win."]]))


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="{FONT}" fill="{INK}">{DEFS}'
            f'<rect width="{w}" height="{h}" fill="#ffffff"/><rect width="{w}" height="{h}" fill="url(#grid)"/>{body}</svg>')


os.makedirs(OUT, exist_ok=True)
for k, (name, body) in P.items():
    open(f"{OUT}/{name}.svg", "w").write(svg(SW, SH, f'<g transform="translate(15,15)">{body}</g>'))

# Overview: 2 columns x 3 rows
OW, top, gap = 2 * PW + 90, 110, 30
OH = top + 3 * PH + 2 * gap + 60
body = (f'<text x="{OW/2}" y="56" text-anchor="middle" font-size="34" font-weight="700">Presence Sync: keeping two phones in agreement</text>'
        f'<text x="{OW/2}" y="84" text-anchor="middle" font-size="16" fill="{MUTED}">The story of a real-time sync system, told with one agent named Priya</text>')
for k, (name, pbody) in P.items():
    col, row = (k - 1) % 2, (k - 1) // 2
    body += f'<g transform="translate({30 + col * (PW + 30)},{top + row * (PH + gap)})">{pbody}</g>'
body += (f'<text x="{OW/2}" y="{OH-22}" text-anchor="middle" font-size="14" fill="{MUTED}">'
         'Manohar Patil · Presence Sync, NICE inContact (2017-2022) · Founding engineer, then Tech Lead</text>')
open(f"{OUT}/0-overview.svg", "w").write(svg(OW, OH, body))
print("ok", OW, OH)
