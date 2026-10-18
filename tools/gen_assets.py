# -*- coding: utf-8 -*-
"""Générateur d'illustrations locales STYLEMIND (démo).

Produit des SVG déterministes — une illustration par produit, look, créateur,
celeb, style et catégorie — stockées dans assets/ et commitées avec le code.
Zéro réseau, zéro photo inventée de vraies personnes : des flat-illustrations
démo cohérentes avec la palette de l'app. Regénérer : python tools/gen_assets.py
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
sys.path.insert(0, str(ROOT))

from core.demo_data import (  # noqa: E402
    CELEB_LOOKS, CREATORS, FEED, PRODUCTS_BY_ID, STYLES,
)

PALETTES = [
    ("#E8B4B8", "#B34168", "#5B4B8A"), ("#F1D1B8", "#C96F4A", "#7C2D3A"),
    ("#DCE4D8", "#9CAF88", "#48503F"), ("#E6DDF7", "#9C8BC4", "#3E3262"),
    ("#F2E8D5", "#D9C5A0", "#8A6D4C"), ("#D9E4F1", "#5B7A9D", "#2E3A59"),
    ("#FBD9DC", "#D68BA0", "#5B1F32"), ("#F4ECD2", "#BFA23E", "#6B5830"),
]


def _h(s: str) -> int:
    return int(hashlib.md5(str(s).encode()).hexdigest(), 16)


def darken(hexcol, f=.72):
    h = hexcol.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"#{int(r*f):02X}{int(g*f):02X}{int(b*f):02X}"


def lighten(hexcol, f=.5):
    h = hexcol.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    mix = lambda c: int(c + (255 - c) * f)
    return f"#{mix(r):02X}{mix(g):02X}{mix(b):02X}"


def svg(body, w, h, uid, cols):
    a0, a1, a2 = cols
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">'
        f'<defs><linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{a0}"/><stop offset=".55" '
        f'stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/>'
        f'</linearGradient></defs>{body}</svg>'
    )


# ── Silhouettes canoniques 200×200 (flat, stylisées) ────────────────────────
GLYPHS = {
    "Hauts": '<path d="M62 52 L88 40 Q100 52 112 40 L138 52 L152 84 L132 94 '
             'L132 152 L68 152 L68 94 L48 84 Z"/><path d="M62 52 L130 52" '
             'stroke="{STROKE}" stroke-width="5" fill="none" stroke-linecap="round"/>',
    "Bas": '<path d="M64 44 L136 44 L142 158 L114 158 L100 96 L86 158 L58 158 Z"/>'
           '<path d="M64 44 L136 44 L137 60 L63 60 Z" fill="#FFFFFF" opacity=".18"/>',
    "Vestes": '<path d="M58 48 L86 38 L100 56 L114 38 L142 48 L152 106 L136 112 '
              'L136 152 L64 152 L64 112 L48 106 Z"/>'
              '<path d="M100 56 L100 152" stroke="{STROKE}" stroke-width="5" fill="none"/>',
    "Robes": '<path d="M82 42 L118 42 L126 86 L140 156 L60 156 L74 86 Z"/>'
             '<path d="M78 92 L122 92" stroke="{STROKE}" stroke-width="5" '
             'fill="none" stroke-linecap="round"/>',
    "Chaussures": '<path d="M68 40 L94 40 L96 100 Q134 106 148 128 L149 146 '
                  'Q102 156 60 144 Z"/>'
                  '<path d="M62 138 L149 139" stroke="{STROKE}" stroke-width="5" '
                  'fill="none" stroke-linecap="round"/>',
    "Accessoires": '<path d="M64 96 H136 L142 152 Q100 166 58 152 Z"/>'
                   '<path d="M82 96 Q100 52 118 96" stroke="{STROKE}" '
                   'stroke-width="7" fill="none" stroke-linecap="round"/>',
}
HAND = '<path d="M110 40 L70 115 L95 115 L85 165 L136 90 L110 90 Z"/>'


def glyph_grp(cat, x, y, scale, opacity=1.0, fill="#FFFFFF"):
    g = GLYPHS.get(cat, HAND).replace("{STROKE}", fill)
    return (f'<g transform="translate({x},{y}) scale({scale})" '
            f'fill="{fill}" opacity="{opacity}">{g}</g>')


def sparkles(uid, n=6, w=420, hgt=560):
    out = []
    for i in range(n):
        x = (_h(f"{uid}s{i}") % (w - 40)) + 20
        y = (_h(f"{uid}t{i}") % (hgt - 60)) + 30
        s = 8 + (_h(f"{uid}u{i}") % 10)
        op = 0.10 + (_h(f"{uid}v{i}") % 14) / 100
        out.append(f'<text x="{x}" y="{y}" font-size="{s}" fill="#FFFFFF" '
                   f'opacity="{op:.2f}" font-family="Georgia,serif">✦</text>')
    return "".join(out)


def backdrop(uid, cols, w, hgt):
    return (f'<rect width="{w}" height="{hgt}" fill="url(#bg{uid})"/>'
            f'<circle cx="{w // 2}" cy="{hgt * 30 // 100}" r="{w * 38 // 100}" '
            f'fill="#FFFFFF" opacity=".08"/>'
            f'<circle cx="{w * 18 // 100}" cy="{hgt * 80 // 100}" r="{w * 22 // 100}" '
            f'fill="#FFFFFF" opacity=".06"/>')


def prod_colors(pid):
    p = PRODUCTS_BY_ID.get(pid)
    return (p["colors"], p["category"]) if p else (["#C9A227"], "Vestes")


def palette_for(uid, extra_colors=None):
    if extra_colors:
        # teinte la palette à partir de la couleur dominante de l'item
        c = extra_colors[0]
        return (lighten(c, .28), c, darken(c, .62))
    return PALETTES[_h(uid) % len(PALETTES)]


# ── Produits : tuile produit avec silhouette + swatches ────────────────────
def prod_svg(pid):
    colors, cat = prod_colors(pid)
    cols = palette_for(pid, colors)
    uid = pid
    body = backdrop(uid, cols, 420, 520)
    body += glyph_grp(cat, 100, 60, 1.35, .95)          # grande silhouette
    body += glyph_grp(cat, 250, 260, 1.0, .28)          # écho fantôme
    body += sparkles(uid, 5)
    for i, c in enumerate(colors[:4]):
        cx = 150 + i * 34
        body += (f'<circle cx="{cx}" cy="470" r="12" fill="{c}" '
                 f'stroke="#FFFFFF" stroke-width="3"/>')
    return svg(body, 420, 520, uid, cols)


# ── Looks du fil : collage de 3 silhouettes ────────────────────────────────
def look_svg(fid):
    f = next((x for x in FEED if x["id"] == fid), None)
    cats, cols = [], []
    if f:
        for pid in f["products"][:3]:
            c, cat = prod_colors(pid)
            cats.append(cat); cols.append(c[0])
    uid = fid
    body = backdrop(uid, palette_for(uid, cols) if cols else PALETTES[_h(uid) % len(PALETTES)],
                    420, 560)
    pos = [(20, 20, 1.15), (185, 130, 1.35), (55, 330, 1.05)]
    for i, (x, y, s) in enumerate(pos):
        cat = cats[i] if i < len(cats) else "Vestes"
        fill = "#FFFFFF"
        body += (f'<rect x="{x-14}" y="{y-14}" width="{int(200*s)+28}" '
                 f'height="{int(200*s)+28}" rx="34" fill="#FFFFFF" opacity=".13"/>')
        body += glyph_grp(cat, x, y, s, .92, fill)
    body += sparkles(uid, 7)
    return svg(body, 420, 560, uid, palette_for(uid, cols) if cols
               else PALETTES[_h(uid) % len(PALETTES)])


def celeb_svg(sid):
    look = next((x for x in CELEB_LOOKS if x["id"] == sid), CELEB_LOOKS[0])
    cols = [prod_colors(p)[0][0] for p in look["products"][:3]] or ["#7C2D3A"]
    uid = sid
    rays = "".join(
        f'<path d="M210 200 L{x} {y} L{x+16} {y+10} Z" fill="#FFFFFF" opacity=".05"/>'
        for x, y in [(40, 30), (380, 20), (20, 500), (390, 520), (60, 260), (360, 300)])
    body = backdrop(uid, (darken(cols[0], .55), cols[0], darken(cols[0], .35)),
                    420, 560)
    body += rays
    body += ('<circle cx="210" cy="185" r="120" fill="#FFFFFF" opacity=".10"/>'
             '<circle cx="210" cy="185" r="120" fill="none" stroke="#C9A227" '
             'stroke-width="3" opacity=".5"/>')
    body += '<text x="210" y="215" font-size="110" text-anchor="middle" ' \
            'fill="#FFFFFF" opacity=".9" font-family="Georgia,serif">✦</text>'
    body += glyph_grp(prod_colors(look["products"][0])[1], 250, 330, .85, .85)
    body += sparkles(uid, 6)
    return svg(body, 420, 560, uid, (darken(cols[0], .55), cols[0], darken(cols[0], .35)))


# ── Créateurs : avatar monogramme ──────────────────────────────────────────
def creator_svg(cid):
    c = next((x for x in CREATORS if x["id"] == cid), CREATORS[0])
    cols = PALETTES[_h(cid) % len(PALETTES)]
    uid = cid
    initials = "".join(w[0] for w in c["name"].split()[:2]).upper()
    body = backdrop(uid, cols, 240, 240)
    body += ('<circle cx="120" cy="118" r="86" fill="none" stroke="#FFFFFF" '
             'stroke-width="3" opacity=".55"/>'
             '<circle cx="120" cy="118" r="74" fill="#FFFFFF" opacity=".14"/>')
    body += (f'<text x="120" y="138" font-size="62" text-anchor="middle" '
             f'font-family="Georgia,serif" font-style="italic" font-weight="700" '
             f'fill="#FFFFFF" opacity=".95">{initials}</text>')
    body += '<text x="196" y="52" font-size="26" fill="#FFFFFF" ' \
            'opacity=".8" font-family="Georgia,serif">✦</text>'
    return svg(body, 240, 240, uid, cols)


# ── Styles du quiz : pictogrammes ──────────────────────────────────────────
STYLE_ICONS = {
    "minimaliste": '<circle cx="100" cy="100" r="34" fill="none" stroke="#FFFFFF" stroke-width="8"/>',
    "chic parisien": "".join(f'<rect x="40" y="{70+i*18}" width="120" height="9" '
                             f'rx="4" fill="#FFFFFF"/>' for i in range(4)),
    "bohème": "".join(f'<path d="M40 {70+i*22} Q70 {52+i*22} 100 {70+i*22} '
                      f'T160 {70+i*22}" stroke="#FFFFFF" stroke-width="7" '
                      f'fill="none" stroke-linecap="round"/>' for i in range(3)),
    "romantique": '<path d="M100 140 C60 110 55 75 80 62 C95 55 100 70 100 72 '
                  'C100 70 105 55 120 62 C145 75 140 110 100 140 Z" fill="#FFFFFF"/>',
    "streetwear": '<polygon points="100,45 118,82 158,82 126,108 138,148 100,124 '
                  '62,148 74,108 42,82 82,82" fill="#FFFFFF"/>',
    "rock": HAND,
    "vintage": '<circle cx="100" cy="100" r="40" fill="none" stroke="#FFFFFF" '
               'stroke-width="7"/><circle cx="100" cy="100" r="18" fill="#FFFFFF"/>'
               '<path d="M100 42 L100 54 M158 100 L146 100 M100 158 L100 146 '
               'M42 100 L54 100" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>',
    "business": '<path d="M92 42 L108 42 L112 62 L100 150 L88 62 Z"/>'
                '<rect x="90" y="34" width="20" height="12" rx="3"/>',
    "casual": '<path d="M62 90 Q100 132 138 90" stroke="#FFFFFF" stroke-width="9" '
              'fill="none" stroke-linecap="round"/>'
              '<circle cx="75" cy="68" r="7" fill="#FFFFFF"/>'
              '<circle cx="125" cy="68" r="7" fill="#FFFFFF"/>',
    "éthique": '<path d="M100 152 Q58 100 100 46 Q142 100 100 152 Z" fill="#FFFFFF"/>'
               '<path d="M100 152 L100 60" stroke="{STROKE}" stroke-width="5"/>',
}


def style_svg(name):
    uid = f"st_{name}"
    cols = PALETTES[_h(uid) % len(PALETTES)]
    body = backdrop(uid, cols, 240, 240)
    icon = STYLE_ICONS.get(name, STYLE_ICONS["minimaliste"]).replace(
        "{STROKE}", "#FFFFFF")
    body += icon.replace("{STROKE}", "#FFFFFF")
    body += '<text x="120" y="212" font-size="17" text-anchor="middle" ' \
            'fill="#FFFFFF" opacity=".95" font-family="Georgia,serif" ' \
            'font-style="italic">✦</text>'
    return svg(body, 240, 240, uid, cols)


# ── Catégories (fallback garde-robe / états vides) ─────────────────────────
CAT_COLORS = {
    "Hauts": ("#F4ECD2", "#D9C5A0", "#8A6D4C"),
    "Bas": ("#D9E4F1", "#5B7A9D", "#2E3A59"),
    "Vestes": ("#E6DDF7", "#9C8BC4", "#3E3262"),
    "Robes": ("#FBD9DC", "#D68BA0", "#5B1F32"),
    "Chaussures": ("#F1D1B8", "#C96F4A", "#7C2D3A"),
    "Accessoires": ("#DCE4D8", "#9CAF88", "#48503F"),
}


def category_svg(cat):
    uid = f"cat_{cat}"
    cols = CAT_COLORS.get(cat, PALETTES[0])
    body = backdrop(uid, cols, 300, 300)
    body += glyph_grp(cat, 50, 30, 1.05, .95)
    return svg(body, 300, 300, uid, cols)


def main():
    OUT.mkdir(exist_ok=True)
    n = 0
    for pid in PRODUCTS_BY_ID:
        (OUT / "products").mkdir(exist_ok=True)
        (OUT / "products" / f"{pid}.svg").write_text(prod_svg(pid), encoding="utf-8")
        n += 1
    for f in FEED:
        (OUT / "looks").mkdir(exist_ok=True)
        (OUT / "looks" / f"{f['id']}.svg").write_text(look_svg(f["id"]), encoding="utf-8")
        n += 1
    for s in CELEB_LOOKS:
        (OUT / "celebs").mkdir(exist_ok=True)
        (OUT / "celebs" / f"{s['id']}.svg").write_text(celeb_svg(s["id"]), encoding="utf-8")
        n += 1
    for c in CREATORS:
        (OUT / "creators").mkdir(exist_ok=True)
        (OUT / "creators" / f"{c['id']}.svg").write_text(creator_svg(c["id"]), encoding="utf-8")
        n += 1
    for s in STYLES:
        (OUT / "styles").mkdir(exist_ok=True)
        (OUT / "styles" / f"{s}.svg").write_text(style_svg(s), encoding="utf-8")
        n += 1
    for cat in ["Hauts", "Bas", "Vestes", "Robes", "Chaussures", "Accessoires"]:
        (OUT / "categories").mkdir(exist_ok=True)
        (OUT / "categories" / f"{cat}.svg").write_text(category_svg(cat), encoding="utf-8")
        n += 1
    print(f"OK — {n} SVG générés dans {OUT}")


if __name__ == "__main__":
    main()
