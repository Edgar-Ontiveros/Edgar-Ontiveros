"""SVG animado tipo terminal con ">_" naranja, tal como el typewriter de edgar-ontiveros.com.

Mismas frases y ritmo que el sitio (useTypewriter: 75 ms por letra, 2200 ms en pausa,
40 ms por letra al borrar, 400 ms entre frases; cursor que parpadea cada 1.1 s).
Lleva incrustado un subconjunto de JetBrains Mono (OFL) y textLength, para que cada letra
mida lo mismo aunque la fuente no cargue.
"""
import base64, io, sys
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONT, OUT = sys.argv[1], sys.argv[2]
LINES = ["Machine Learning Engineer", "Full Stack Developer", "Cloud Engineer"]
TYPE, HOLD, DELETE, GAP = 75, 2200, 40, 400
SIZE, CH = 20, 12.0                      # JetBrains Mono: avance de 0.6 em
PAD, PROMPT = 8, ">_"
THEMES = {"dark": ("#F59E0B", "#22D3EE"), "light": ("#D97706", "#0E7490")}

# Fuente: instancia de peso 400, recortada a las letras que se usan
f = TTFont(FONT)
f = instancer.instantiateVariableFont(f, {"wght": 400})
opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = []; opts.name_IDs = ["*"]
sub = subset.Subsetter(opts); sub.populate(text="".join(LINES) + PROMPT + " "); sub.subset(f)
buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
font_b64 = base64.b64encode(buf.getvalue()).decode()

tx = PAD + (len(PROMPT) + 1) * CH           # el texto empieza después de ">_ "
longest = max(len(l) for l in LINES)
W = int(tx + longest * CH + 4 + CH / 2 + PAD)
H = 36

# Línea de tiempo en ms: anchos visibles de cada frase
events = []  # (t, índice de frase, ancho)
t = 0
for i, line in enumerate(LINES):
    n = len(line)
    for k in range(1, n + 1):
        events.append((t + k * TYPE, i, k * CH))
    t += n * TYPE + HOLD
    for k in range(1, n + 1):
        events.append((t + k * DELETE, i, (n - k) * CH))
    t += n * DELETE + GAP
TOTAL = t

def animate(attr, timeline, fmt):
    """<animate> discreto a partir de [(t_ms, valor)] que empieza en t=0."""
    pts = []
    for tm, v in timeline:
        if pts and abs(pts[-1][0] - tm) < 1e-9:
            pts[-1] = (tm, v)
        else:
            pts.append((tm, v))
    kt = ";".join(f"{tm / TOTAL:.5f}" for tm, _ in pts)
    vals = ";".join(fmt(v) for _, v in pts)
    return (f'<animate attributeName="{attr}" dur="{TOTAL / 1000:.3f}s" repeatCount="indefinite" '
            f'calcMode="discrete" keyTimes="{kt}" values="{vals}"/>')

def svg(prompt_color, text_color):
    parts = []
    for i, line in enumerate(LINES):
        tl = [(0, 0.0)] + [(tm, w) for tm, j, w in events if j == i]
        parts.append(
            f'<clipPath id="c{i}"><rect x="{tx}" y="0" height="{H}" width="0">'
            f'{animate("width", tl, lambda v: f"{v:g}")}</rect></clipPath>'
            f'<text x="{tx}" y="25" fill="{text_color}" textLength="{len(line) * CH:g}" '
            f'lengthAdjust="spacingAndGlyphs" clip-path="url(#c{i})">{line}</text>')
    cur = [(0, tx + 4)] + [(tm, tx + 4 + w) for tm, _, w in events]
    cursor = (f'<rect y="6" width="{CH / 2:g}" height="22" fill="{prompt_color}" x="{tx + 4:g}">'
              f'{animate("x", cur, lambda v: f"{v:g}")}'
              f'<animate attributeName="opacity" dur="1.1s" repeatCount="indefinite" calcMode="discrete" '
              f'keyTimes="0;0.5" values="1;0"/></rect>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Machine Learning Engineer · Full Stack Developer · Cloud Engineer">
<style>@font-face{{font-family:"EO Mono";src:url(data:font/woff2;base64,{font_b64}) format("woff2");}}text{{font-family:"EO Mono","JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:{SIZE}px;}}</style>
<text x="{PAD}" y="25" fill="{prompt_color}" textLength="{len(PROMPT) * CH:g}" lengthAdjust="spacingAndGlyphs">&gt;_</text>
{"".join(parts)}
{cursor}
</svg>
'''

for name, (pc, tc) in THEMES.items():
    open(f"{OUT}/typing-{name}.svg", "w", encoding="utf-8").write(svg(pc, tc))
print(f"ok: {W}x{H}, ciclo {TOTAL} ms, fuente {len(buf.getvalue())} bytes")
