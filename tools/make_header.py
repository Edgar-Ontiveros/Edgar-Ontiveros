"""Encabezado animado para el perfil de GitHub: la constelación de edgar-ontiveros.com.

Replica src/components/Constellation.tsx: nodos cian de radio 1.2 a 2.2 y opacidad 0.45 a 0.9,
una deriva lenta de 4 a 16 px/s, enlaces por proximidad (gris #94a3b8, alfa 0.3 × cercanía,
distancia de 1.2 × el espaciado medio, entre 80 y 150) y atenuación al 40 % detrás del texto.
En SVG no hay física por cuadro, así que cada nodo sigue una trayectoria periódica (Lissajous)
y las posiciones y opacidades se calculan en K cuadros y se animan con SMIL en ciclo continuo.
El nombre va como trazos de Space Grotesk (la fuente de títulos del sitio, OFL), así no depende
de las fuentes de quien lo vea.
"""
import math, random, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT, OUT = sys.argv[1], sys.argv[2]
W, H = 900, 250
BG, BORDER, ACCENT, MUTED, TEXT = "#0A0E1A", "#1E293B", "#22D3EE", "#94A3B8", "#E8EAF0"
T, K = 60.0, 40                      # periodo del ciclo (s) y cuadros calculados
random.seed(20261014)

# ── Nombre en trazos ──
font = instancer.instantiateVariableFont(TTFont(FONT), {"wght": 600})
gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm
SIZE, TRACK, WORD_GAP = 34.0, 0.42, 0.55     # px, tracking y espacio extra entre palabras (en em)
scale = SIZE / upm
def advance(ch): return font["hmtx"][cmap[ord(ch)]][0] * scale
name = "EDGAR ONTIVEROS"
widths = [(WORD_GAP * SIZE + advance(" ")) if c == " " else advance(c) for c in name]
total = sum(widths) + TRACK * SIZE * (len(name) - 1)  # tracking solo entre letras
x, baseline = (W - total) / 2, 158
paths = []
for c, w in zip(name, widths):
    if c != " ":
        pen = SVGPathPen(gs)
        gs[cmap[ord(c)]].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        paths.append(pen.getCommands())
    x += w + TRACK * SIZE
name_x0, name_x1 = (W - total) / 2, (W - total) / 2 + total

# ── Monograma EO· (public/favicon.svg, viewBox 32) centrado sobre el nombre ──
MONO = 1.25                                   # 32 u → 40 px
mono_cx, mono_cy = W / 2, 82
gx, gy = 17.4, 18.0                           # centro óptico del glifo en el viewBox original
mono_tf = f"translate({mono_cx - gx * MONO:.2f} {mono_cy - gy * MONO:.2f}) scale({MONO})"

# ── Zona del texto (los nodos se atenúan al 40 % con un borde suave) ──
ZX0, ZX1, ZY0, ZY1 = name_x0 - 10, name_x1 + 10, 52, 186
FEATHER, ZMIN = 60.0, 0.4
def zone_fade(px, py):
    dx = max(ZX0 - px, 0, px - ZX1); dy = max(ZY0 - py, 0, py - ZY1)
    d = math.hypot(dx, dy)
    return 1.0 if d >= FEATHER else ZMIN + (1 - ZMIN) * (d / FEATHER)

# ── Nodos: rejilla con desplazamiento al azar para que queden repartidos ──
N = 30
cols, rows = 10, 3
spacing = math.sqrt(W * H / N)
LINK = max(80.0, min(150.0, 1.2 * spacing))
nodes = []
for r in range(rows):
    for c in range(cols):
        cx0 = (c + 0.5) * W / cols + random.uniform(-0.3, 0.3) * W / cols
        cy0 = (r + 0.5) * H / rows + random.uniform(-0.3, 0.3) * H / rows
        ax, ay = random.uniform(22, 48), random.uniform(10, 22)
        kx, ky = random.choice([1, 1, 2]), random.choice([1, 2])
        px, py = random.uniform(0, 2 * math.pi), random.uniform(0, 2 * math.pi)
        cx0 = min(max(cx0, 10 + ax), W - 10 - ax); cy0 = min(max(cy0, 10 + ay), H - 10 - ay)
        nodes.append(dict(cx=cx0, cy=cy0, ax=ax, ay=ay, kx=kx, ky=ky, px=px, py=py,
                          r=random.uniform(1.2, 2.2), a=random.uniform(0.45, 0.9)))
def pos(n, t):
    w = 2 * math.pi * t / T
    return (n["cx"] + n["ax"] * math.sin(n["kx"] * w + n["px"]), n["cy"] + n["ay"] * math.sin(n["ky"] * w + n["py"]))

times = [T * i / K for i in range(K + 1)]                 # el último cuadro repite el primero
P = [[pos(n, t) for t in times] for n in nodes]
kt = ";".join(f"{i / K:.4f}" for i in range(K + 1))
def anim(attr, vals):
    # Sin keyTimes: con cuadros equiespaciados SMIL los reparte igual y el archivo pesa la mitad
    return f'<animate attributeName="{attr}" dur="{T:g}s" repeatCount="indefinite" values="{";".join(vals)}"/>'
f1 = lambda v: f"{v:.1f}"
f2 = lambda v: f"{v:.2f}"

links = []
for i in range(N):
    for j in range(i + 1, N):
        op = []
        for k in range(K + 1):
            (xa, ya), (xb, yb) = P[i][k], P[j][k]
            d = math.hypot(xb - xa, yb - ya)
            close = max(0.0, 1 - d / LINK)
            op.append(0.3 * close * min(zone_fade(xa, ya), zone_fade(xb, yb)))
        if max(op) < 0.02:
            continue
        links.append(
            f'<line stroke="{MUTED}" stroke-width="1">'
            + anim("x1", [f1(P[i][k][0]) for k in range(K + 1)]) + anim("y1", [f1(P[i][k][1]) for k in range(K + 1)])
            + anim("x2", [f1(P[j][k][0]) for k in range(K + 1)]) + anim("y2", [f1(P[j][k][1]) for k in range(K + 1)])
            + anim("stroke-opacity", [f2(v) for v in op]) + "</line>")
dots = []
for n, pts in zip(nodes, P):
    dots.append(
        f'<circle r="{n["r"]:.2f}" fill="{ACCENT}">'
        + anim("cx", [f1(x) for x, _ in pts]) + anim("cy", [f1(y) for _, y in pts])
        + anim("fill-opacity", [f2(n["a"] * zone_fade(x, y)) for x, y in pts]) + "</circle>")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Edgar Ontiveros">
<title>Edgar Ontiveros</title>
<defs><clipPath id="card"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14"/></clipPath></defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>
<g clip-path="url(#card)">{"".join(links)}{"".join(dots)}</g>
<g transform="{mono_tf}"><g stroke="{ACCENT}" stroke-width="3.6" fill="none"><path d="M11.4 7.8H4.8v16.4h6.6M4.8 16h5.6"/><circle cx="22" cy="16" r="7.2"/></g><circle cx="29.4" cy="27.6" r="2.4" fill="{ACCENT}"/></g>
<path fill="{TEXT}" d="{" ".join(paths)}"/>
<line x1="{name_x0:.1f}" y1="190" x2="{name_x1:.1f}" y2="190" stroke="{MUTED}" stroke-opacity="0.55" stroke-width="1.1"/>
</svg>
'''
open(OUT, "w", encoding="utf-8").write(svg)
print(f"ok: {len(svg) / 1024:.0f} KB, {len(links)} enlaces, {N} nodos, nombre {total:.0f}px, LINK {LINK:.0f}px")
