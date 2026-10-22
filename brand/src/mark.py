"""Vector Translation mark: Leonardo's octahedron from Pacioli's De divina proportione (1509), drawn twice.

The source copy is pale ink. The translated copy, displaced by a vector, is electric blue, with visible
edges (those bordering a face turned to the eye) bold and hidden edges thin and pale, by the same rule
as the Vector Humanities mark (brand/src/poly.py in the VH kit). A vermilion arrow joins the top vertex
of the source copy to the top vertex of the translated copy.

Levels: 'full' draws every edge of both copies; 'front' draws visible edges only, heavier; 'icon' draws
the outlines only, heavier still. Usage: python3 mark.py <brand dir> <assets dir>
"""
import math, itertools, os, sys

DIST = 11.0
AZ, EL = math.radians(15), math.radians(22)      # three-quarter view; the VH mark's 23 degrees turns the octahedron into a kite
SHIFT = (0.55, 0.28)                             # displacement of the translated copy, in copy widths

def octa():
    vs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    edges = [(i, j) for i in range(6) for j in range(i + 1, 6) if abs(math.dist(vs[i], vs[j]) - math.sqrt(2)) < 1e-9]
    faces = []
    for n in itertools.product((1, -1), repeat=3):
        faces.append((n, [q for q in range(6) if sum(n[k] * vs[q][k] for k in range(3)) == 1]))
    return vs, edges, faces

def rot(p, ax, ay):
    x, y, z = p
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    return (x, y, z)

def project(spin=None, tilt=None):
    """Unit-scale 2D points, depth, edges and visibility for one copy."""
    spin = AZ if spin is None else spin; tilt = EL if tilt is None else tilt
    vs, edges, faces = octa()
    turn = lambda v: rot(v, tilt, spin)
    R = [turn(v) for v in vs]
    count = {e: 0 for e in edges}                    # faces turned to the eye, per edge
    for n, fv in faces:
        nr = turn(n)
        c = [sum(R[q][k] for q in fv) / 3 for k in range(3)]
        if nr[0] * c[0] + nr[1] * c[1] + nr[2] * (c[2] + DIST) < 0:
            for e in edges:
                if e[0] in fv and e[1] in fv:
                    count[e] += 1
    P = [(v[0] * DIST / (DIST + v[2]), -v[1] * DIST / (DIST + v[2])) for v in R]
    return P, R, edges, [count[e] > 0 for e in edges], [count[e] == 1 for e in edges]

def layout(box=(8.0, 8.0, 92.0, 92.0), spin=None, tilt=None):
    """Both copies fitted together into box. Returns (source points, translated points, R, edges, vis)."""
    P, R, edges, vis, sil = project(spin, tilt)
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    w = max(xs) - min(xs); h = max(ys) - min(ys)
    dx, dy = SHIFT[0] * w, SHIFT[1] * w
    x0, y0, x1, y1 = box
    sc = min((x1 - x0) / (w + dx), (y1 - y0) / (h + dy))
    ox = (x0 + x1) / 2 - (min(xs) + (w + dx) / 2) * sc
    oy = (y0 + y1) / 2 - (min(ys) + (h + dy) / 2) * sc
    A = [(x * sc + ox, y * sc + oy) for x, y in P]
    B = [(x + dx * sc, y + dy * sc) for x, y in A]
    return A, B, R, edges, vis, sil

def mix(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(ca, cb))

PALETTES = {
    'paper':    dict(bg='#f6f2e9', beam='#1a1aff', ink='#141518', accent='#ff4a24'),
    'night':    dict(bg='#0c0e1c', beam='#8a90ff', ink='#e8e6f0', accent='#ff6a45'),
    'electric': dict(bg='#1a1aff', beam='#ffffff', ink='#ffffff', accent='#ff6a45'),
}

def level_for(px):
    return 'full' if px >= 80 else 'front' if px >= 28 else 'icon'

def arrow(a, b, col, w, head):
    """Shaft from a to b, ending in an open head at b."""
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    tip = b
    base = (tip[0] - head * math.cos(ang), tip[1] - head * math.sin(ang))
    l = (base[0] + head * 0.55 * math.sin(ang), base[1] - head * 0.55 * math.cos(ang))
    r = (base[0] - head * 0.55 * math.sin(ang), base[1] + head * 0.55 * math.cos(ang))
    return (f'<path d="M{a[0]:.2f},{a[1]:.2f} L{base[0]:.2f},{base[1]:.2f}" stroke="{col}" stroke-width="{w:.2f}" stroke-linecap="round"/>'
            f'<path d="M{tip[0]:.2f},{tip[1]:.2f} L{l[0]:.2f},{l[1]:.2f} L{r[0]:.2f},{r[1]:.2f} Z" fill="{col}" stroke="{col}" stroke-width="{w * 0.6:.2f}" stroke-linejoin="round"/>')

def body(c, level='full', px=400, box=None, weight=1.0, cls=False):
    """SVG elements for the mark in a 100x100 box. cls=True emits class names for CSS theming."""
    A, B, R, edges, vis, sil = layout(box or (8.0, 8.0, 92.0, 92.0))
    if level == 'icon':                              # at 16 to 28 px only the outlines survive
        vis = sil
    u = 100.0 / px
    if level == 'full':
        wf, wb, ws, wa, hd = 1.5 * weight, 0.55 * weight, 0.7 * weight, 1.1 * weight, 4.2 * weight
    elif level == 'front':
        wf, wb, ws, wa, hd = max(3.0, 1.7 * u), None, max(1.6, 1.0 * u), max(2.4, 1.4 * u), 8.0
    else:
        wf, wb, ws, wa, hd = max(6.0, 2.0 * u), None, max(3.4, 1.2 * u), max(4.4, 1.6 * u), 13.0
    src_vis = mix(c['ink'], c['bg'], 0.62)
    src_hid = mix(c['ink'], c['bg'], 0.82)
    back = mix(c['beam'], c['bg'], 0.6)
    st = (lambda k, col: f'class="{k}"') if cls else (lambda k, col: f'stroke="{col}"')
    order = sorted(range(len(edges)), key=lambda n: -(R[edges[n][0]][2] + R[edges[n][1]][2]))
    out = []
    for n in order:                                  # the source copy
        i, j = edges[n]
        if vis[n] or level == 'full':
            col, k = (src_vis, 's') if vis[n] else (src_hid, 'sh')
            out.append(f'<path d="M{A[i][0]:.2f},{A[i][1]:.2f} L{A[j][0]:.2f},{A[j][1]:.2f}" {st(k, col)} stroke-width="{ws if vis[n] else ws * 0.7:.2f}" stroke-linecap="round"/>')
    for n in order:                                  # hidden edges of the translated copy
        i, j = edges[n]
        if not vis[n] and wb:
            out.append(f'<path d="M{B[i][0]:.2f},{B[i][1]:.2f} L{B[j][0]:.2f},{B[j][1]:.2f}" {st("bh", back)} stroke-width="{wb:.2f}" stroke-linecap="round"/>')
    top = 2                                          # vertex (0, 1, 0)
    a = arrow(A[top], B[top], c['accent'], wa, hd)
    if cls:
        a = a.replace(f'stroke="{c["accent"]}"', 'class="a"').replace(f'fill="{c["accent"]}"', '')
    out.append(a)
    for n in order:                                  # visible edges of the translated copy
        i, j = edges[n]
        if vis[n]:
            out.append(f'<path d="M{B[i][0]:.2f},{B[i][1]:.2f} L{B[j][0]:.2f},{B[j][1]:.2f}" {st("b", c["beam"])} stroke-width="{wf:.2f}" stroke-linecap="round"/>')
    return ''.join(out)

def mark_svg(c, px=400, level=None, bg=True, title='Vector Translation'):
    level = level or level_for(px)
    rect = f'<rect width="100" height="100" fill="{c["bg"]}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="{px}" height="{px}">'
            f'<title>{title}</title>{rect}{body(c, level, px)}</svg>')

def favicon():
    css = ('<style>.b{stroke:#1a1aff}.s{stroke:#8f8f93}.a{stroke:#ff4a24;fill:#ff4a24}'
           '@media (prefers-color-scheme: dark){.b{stroke:#8a90ff}.s{stroke:#6d6c78}.a{stroke:#ff6a45;fill:#ff6a45}}</style>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">' + css
            + body(PALETTES['paper'], 'icon', 32, box=(4.0, 4.0, 96.0, 96.0), cls=True) + '</svg>')

def css_body(level, px, box=None, weight=1.0):
    """Mark for inline use in the site, coloured by CSS classes (.b .bh .s .sh .a)."""
    return body(PALETTES['paper'], level, px, box=box, weight=weight, cls=True)

FONT = ("@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600"
        "&family=IBM+Plex+Mono&display=swap');")

def card_svg():
    """1200 x 630 social card: mark on the left, wordmark on the right, paper ground."""
    c = PALETTES['paper']
    m = body(c, 'full', 1200, box=(6.0, 6.0, 94.0, 94.0), weight=0.9)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">'
            f'<style>{FONT}</style><rect width="1200" height="630" fill="{c["bg"]}"/>'
            f'<g transform="translate(70 75) scale(4.8)">{m}</g>'
            f'<text x="630" y="300" font-family="Cormorant Garamond" font-weight="600" font-size="62" letter-spacing="9" fill="{c["ink"]}">VECTOR</text>'
            f'<text x="630" y="372" font-family="Cormorant Garamond" font-weight="600" font-size="62" letter-spacing="9" fill="{c["beam"]}">TRANSLATION</text>'
            f'<text x="633" y="430" font-family="IBM Plex Mono" font-size="19" letter-spacing="3" fill="#5b5d66">A VECTOR HUMANITIES METHOD</text>'
            f'</svg>')

def avatar_svg():
    c = PALETTES['paper']
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="1024" height="1024">'
            f'<rect width="100" height="100" fill="{c["bg"]}"/>'
            + body(c, 'full', 1024, box=(13.0, 13.0, 87.0, 87.0), weight=1.5) + '</svg>')

def sheet():
    cells = []
    for name in ('paper', 'night', 'electric'):
        c = PALETTES[name]
        cells.append(f'<div class="c"><div class="t">{name}</div>{mark_svg(c, 300)}'
                     f'<div class="sm">' + ''.join(mark_svg(c, s) for s in (128, 64, 48, 32, 24, 16)) + '</div></div>')
    return ('<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:18px;background:#d8d4ca}'
            '.g{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.c{background:#fff;border-radius:10px;padding:14px;'
            'display:flex;flex-direction:column;gap:12px;align-items:center}.t{align-self:flex-start;font:12px Menlo,monospace;'
            'letter-spacing:.12em;text-transform:uppercase;color:#555}.sm{display:flex;gap:12px;align-items:flex-end}</style>'
            '<div class="g">' + ''.join(cells) + '</div>')

if __name__ == '__main__':
    BR, AS = sys.argv[1:3]
    w = lambda p, t: open(p, 'w').write(t)
    for name, c in PALETTES.items():
        for lv in ('full', 'front', 'icon'):
            w(os.path.join(BR, f'mark-{lv}-{name}.svg'), mark_svg(c, 400, lv))
    fav = favicon()
    w(os.path.join(BR, 'favicon.svg'), fav); w(os.path.join(AS, 'favicon.svg'), fav)
    w(os.path.join(BR, 'avatar.svg'), avatar_svg())
    w(os.path.join(BR, 'social-card.svg'), card_svg())
    w(os.path.join(BR, 'src', 'sheet.html'), sheet())
    w(os.path.join(BR, 'src', 'header-mark.txt'), css_body('front', 36, box=(4.0, 4.0, 96.0, 96.0)))
    print('ok')
