"""Hand-drawn Presence Sync architecture diagram with color-coded flows."""
import sys
OUT = sys.argv[1]
FONT = "'Segoe Print','Comic Sans MS','Chalkboard SE','Comic Neue',cursive"
INK, MUTED, BLUE = "#1f2a37", "#566476", "#2f5fd0"
GREEN, ORANGE, PURPLE, GRAY, RED, GOLD = "#2f9e5b", "#e07b1a", "#7b4fd6", "#7a8797", "#d64545", "#b8941a"
W, H = 1240, 1000

def marker(i, c):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            f'<path d="M0 0L10 5L0 10z" fill="{c}"/></marker>')

defs = ('<defs><filter id="rough" x="-5%" y="-5%" width="110%" height="110%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="7" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="3"/></filter>'
        '<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#e8eef5"/></pattern>'
        + marker("mg", GREEN) + marker("mo", ORANGE) + marker("mp", PURPLE) + marker("mk", GRAY) + marker("mr", RED) + '</defs>')

shapes, texts = [], []

def zone(x, y, w, h, fill, stroke, title, ty=None):
    shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2.5" stroke-dasharray="10 6"/>')
    texts.append(f'<text x="{x+16}" y="{ty or y+h-14}" font-size="15" font-weight="700" fill="{stroke}">{title}</text>')

def box(x, y, w, h, title, sub=None, fill="#fff", stroke=INK, tc=INK, num=None):
    shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2.6"/>')
    cx = x + w / 2
    if sub:
        texts.append(f'<text x="{cx}" y="{y+h/2-3}" text-anchor="middle" font-size="14" font-weight="700" fill="{tc}">{title}</text>')
        texts.append(f'<text x="{cx}" y="{y+h/2+16}" text-anchor="middle" font-size="12" fill="{MUTED}">{sub}</text>')
    else:
        texts.append(f'<text x="{cx}" y="{y+h/2+5}" text-anchor="middle" font-size="14" font-weight="700" fill="{tc}">{title}</text>')
    if num:
        shapes.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{BLUE}" stroke="#fff" stroke-width="2"/>')
        texts.append(f'<text x="{x}" y="{y+4.5}" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">{num}</text>')

def line(d, color, mk=None, start=False, dash=None, w=3):
    a = f' marker-end="url(#{mk})"' if mk else ""
    s = f' marker-start="url(#{mk})"' if start else ""
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    shapes.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"{ds}{a}{s}/>')

def label(x, y, s, color, size=12, anchor="middle", weight="700"):
    texts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}" '
                 f'stroke="#fff" stroke-width="4" paint-order="stroke">{s}</text>')

# Zones
zone(24, 96, 248, 610, "#f3f5f8", "#7a8797", "Contact center (inContact)")
zone(298, 96, 618, 610, "#f2f6fe", BLUE, "Presence Sync")
zone(944, 96, 272, 610, "#f7f2ff", PURPLE, "Phone platforms (partners)")
zone(298, 730, 618, 120, "#fffaea", GOLD, "Platform and delivery", ty=754)

# Contact center
box(50, 150, 196, 60, "MAX agent desktop", "agent sets their state")
box(50, 262, 196, 70, "ACD routing engine", "routes customer calls")
box(50, 400, 196, 70, "Agent event stream", "Kafka to Kinesis")
box(50, 540, 196, 64, "Agent directory", "users and extensions")

# PSA
PSF, PST = "#e6eefc", BLUE
box(322, 140, 170, 64, "PresenceSyncUI", "Angular admin console", PSF, PST, num="03")
box(516, 140, 186, 64, "PartnerOnboarding", "Scala REST APIs", PSF, PST, num="06")
box(726, 140, 170, 64, "Config and rules DB", "tenants, mappings, rules")
box(330, 262, 200, 70, "Subscriber", "partner to contact center", PSF, PST, num="01")
box(712, 262, 180, 70, "Per-partner adapters", "one translator each", PSF, PST)
box(570, 352, 112, 62, "Redis", "state, call tags")
box(330, 400, 200, 70, "Publisher", "contact center to partner", PSF, PST, num="02")
box(712, 516, 180, 64, "DirectorySync", "contacts, both ways", PSF, PST, num="04")
box(330, 606, 230, 64, "SyntheticMonitor", "spots upstream event changes", PSF, PST, num="08")

# Platform band
box(322, 770, 172, 60, "PSA-SSL", "DigiCert certificates", "#fff", GOLD, num="07")
box(512, 770, 214, 60, "CICD-DevOps", "Docker, Kubernetes, Terraform", "#fff", GOLD, num="09")
box(744, 770, 156, 60, "PSAPerformance", "Gatling load tests", "#fff", GOLD, num="05")

# Partners
for i, n in enumerate(["RingCentral", "Fuze", "Zoom", "MS Teams", "Google Meet", "Atos"]):
    box(970, 150 + i * 70, 220, 46, n, None, "#fff", PURPLE)

# Flows
line("M148 210 V258", GRAY, "mk", w=2.5)                                   # MAX -> ACD
line("M148 332 V396", GREEN, "mg"); label(156, 370, "agent events", GREEN, anchor="start")
line("M246 435 H326", GREEN, "mg")
line("M530 444 H962", GREEN, "mg"); label(760, 464, "set presence: Busy or DND", GREEN)
line("M962 297 H896", ORANGE, "mo"); label(918, 254, "call and", ORANGE); label(918, 268, "presence events", ORANGE)
line("M712 297 H534", ORANGE, "mo")
line("M330 297 H250", ORANGE, "mo"); label(290, 324, "set state", ORANGE); label(290, 338, "(gRPC)", ORANGE)
line("M892 548 H962", PURPLE, "mp", start=True, dash="8 6")
line("M712 572 H250", PURPLE, "mp", start=True, dash="8 6"); label(470, 592, "contacts and availability, both ways", PURPLE)
line("M492 172 H512", GRAY, "mk", dash="6 5", w=2.5)
line("M702 172 H722", GRAY, "mk", dash="6 5", w=2.5)
line("M810 204 V258", GRAY, "mk", dash="6 5", w=2.5); label(818, 236, "rules, mappings", GRAY, anchor="start")
line("M609 140 V114 H1080 V146", GRAY, "mk", dash="6 5", w=2.5); label(840, 108, "register tenant, create subscriptions", GRAY)
line("M530 312 Q560 330 570 362", GRAY, w=2.5)                            # Subscriber - Redis
line("M530 416 Q556 410 570 400", GRAY, w=2.5)                            # Publisher - Redis
line("M246 458 C300 470 290 640 326 640", RED, "mr", dash="2 6", w=3.5)

# Legend
lg = [(GREEN, None, "Publisher flow: contact center to phone platform"),
      (ORANGE, None, "Subscriber flow: phone platform to contact center"),
      (PURPLE, "8 6", "Directory Sync: both ways"),
      (GRAY, "6 5", "Configuration"),
      (RED, "2 6", "Event-change monitoring")]
for i, (c, d, s) in enumerate(lg):
    col, row = i % 2, i // 2
    x, y = 60 + col * 600, 892 + row * 30
    ds = f' stroke-dasharray="{d}"' if d else ""
    shapes.append(f'<path d="M{x} {y} H{x+50}" stroke="{c}" stroke-width="3.5" stroke-linecap="round"{ds}/>')
    texts.append(f'<text x="{x+62}" y="{y+5}" font-size="14" fill="{INK}">{s}</text>')

title = (f'<text x="{W/2}" y="48" text-anchor="middle" font-size="30" font-weight="700">Presence Sync architecture</text>'
         f'<text x="{W/2}" y="74" text-anchor="middle" font-size="15" fill="{MUTED}">Numbered boxes are the nine components; colors show which way each flow runs</text>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" fill="{INK}">'
       f'{defs}<rect width="{W}" height="{H}" fill="#fff"/><rect width="{W}" height="{H}" fill="url(#grid)"/>{title}'
       f'<g filter="url(#rough)">{"".join(shapes)}</g>{"".join(texts)}</svg>')
open(OUT, "w").write(svg)
print("ok")
