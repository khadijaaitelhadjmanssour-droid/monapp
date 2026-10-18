# -*- coding: utf-8 -*-
"""Composants visuels réutilisables : tuiles façon Pinterest, boutons, mini-stats.

Comme l'app n'a pas encore de vraies photos (API / uploads), les visuels
sont des tuiles à dégradé générées de façon déterministe — elles seront
remplacées par de vraies images quand les intégrations seront branchées.
"""
import hashlib

import streamlit as st

from core import state
from core.demo_data import CREATORS_BY_ID, PRODUCTS_BY_ID
from core.format import dh
from ui import assets


# ─────────────────────────────────────────────────────────────────────────────
# Cœur « image » : tuile dégradé déterministe
# ─────────────────────────────────────────────────────────────────────────────
def _hash(s: str) -> int:
    return int(hashlib.md5(str(s).encode()).hexdigest(), 16)


PALETTES = [
    ("#E8B4B8", "#B34168", "#5B4B8A"),
    ("#F1D1B8", "#C96F4A", "#7C2D3A"),
    ("#DCE4D8", "#9CAF88", "#48503F"),
    ("#E6DDF7", "#9C8BC4", "#3E3262"),
    ("#F2E8D5", "#D9C5A0", "#8A6D4C"),
    ("#D9E4F1", "#5B7A9D", "#2E3A59"),
    ("#FBD9DC", "#D68BA0", "#5B1F32"),
    ("#F4ECD2", "#BFA23E", "#6B5830"),
]


def gradient_for(key: str) -> str:
    a, b, c = PALETTES[_hash(key) % len(PALETTES)]
    angle = 100 + (_hash(key + "a") % 120)
    return (f"linear-gradient({angle}deg, {a} 0%, {b} 62%, {c} 100%)")


def tile_html(key, title, sub="", badges="", height=180, swatches=None,
              extra_inner="", img=None) -> str:
    """Tuile Pinterest : illustration locale en <img> de fond (fiable via
    l'assainisseur Streamlit) + dégradé déterministe en repli."""
    deck = gradient_for(key)
    media = f'<img class="tile-img" src="{img}" alt="" loading="lazy"/>' if img else ""
    sw = ""
    if swatches:
        sw = '<div class="swatches">' + "".join(
            f'<div class="sw" style="background:{c}"></div>' for c in swatches[:4]) + "</div>"
    return (
        f'<div class="tile" style="background:{deck}; height:{height}px;">'
        f"{media}{sw}{badges}"
        f'<div class="overlay"><div class="t-title">{title}</div>'
        f'{f"<div class=t-sub>{sub}</div>" if sub else ""}{extra_inner}</div></div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Badges (DÉMO, sponsorisé, éthique, friperie…)
# ─────────────────────────────────────────────────────────────────────────────
def badges_for_item(kind="look", sponsored=False, secondhand=False, ethical=0):
    out = ""
    # l'ensemble du catalogue / feed est de la donnée DÉMO → badge visible
    out += '<span class="t-badge badge-demo">DÉMO</span>'
    kind_lab = {"look": "Look", "produit": "Produit", "celeb": "Célébrité (démo)",
                "moodboard": "Moodboard"}.get(kind, "Look")
    if sponsored:
        out += '<span class="t-badge badge-sponsored">Sponsorisé</span>'
    else:
        out += (f'<span class="t-badge" '
                f'style="background:rgba(255,255,255,.72); margin-left:4px">'
                f'{kind_lab}</span>')
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Carte du fil (tuile + actions sauvegarde / suivi du créateur)
# ─────────────────────────────────────────────────────────────────────────────
def feed_card(f, col):
    creator = CREATORS_BY_ID.get(f["creator"], {})
    price_total = sum(PRODUCTS_BY_ID[p]["price"] for p in f["products"])
    swatches = []
    for pid in f["products"][:3]:
        swatches.extend(PRODUCTS_BY_ID[pid]["colors"][:2])
    badges = badges_for_item("look", sponsored=f["sponsored"])
    img_sources = [("looks", f["id"])]
    if f["products"]:
        img_sources.append(("products", f["products"][0]))
    img = assets.media_pick(f["id"], img_sources)
    col.markdown(
        tile_html(f["id"], f["title"], f"{creator.get('name','')} · "
                  f"{creator.get('specialty','')}", badges, height=int(200 * f["size"]),
                  swatches=swatches, img=img),
        unsafe_allow_html=True,
    )
    col.caption(f"≈ {dh(price_total)} · {len(f['products'])} pièces")
    if col.button("👁 Voir le look", key=f"see_{f['id']}",
                  use_container_width=True,
                  help="Ouvrir la page de détail complète de ce look"):
        st.session_state.look_page = f["id"]
        st.rerun()
    saved = f["id"] in st.session_state.looks_sauvegardes
    if col.button("♥ Épinglé ✓" if saved else "♥ Épingler",
                  key=f"save_{f['id']}", use_container_width=True,
                  help="Ajouter / retirer ce look de tes favoris ♥"):
        if saved:
            st.session_state.looks_sauvegardes.remove(f["id"])
        else:
            st.session_state.looks_sauvegardes.append(f["id"])
            state.notif("Look enregistré dans tes favoris ♥")
        st.rerun()
    follow = f["creator"] in st.session_state.follows
    if col.button("✓ Suivi ✓" if follow else "＋ Suivre le créateur",
                  key=f"fol_{f['id']}", use_container_width=True,
                  help=f"Suivre {creator.get('name', 'ce créateur')}"):
        if follow:
            st.session_state.follows.remove(f["creator"])
        else:
            st.session_state.follows.append(f["creator"])
            state.notif(f"Tu suis {creator.get('name', '')} ✦")
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Carte produit (tuile courte + bouton d'envie)
# ─────────────────────────────────────────────────────────────────────────────
def product_card(p, col, height=160, cta="✦ Dream Wardrobe", key_suffix=""):
    badges = badges_for_item("produit", sponsored=False, secondhand=p["secondhand"])
    tags = []
    if p["secondhand"]:
        tags.append('<span class="chip chip-second">Seconde main</span>')
    if p["ethical"] >= 4:
        tags.append('<span class="chip chip-eco">Éthique ✓</span>')
    img = assets.media_pick(p["id"], [("products", p["id"])])
    col.markdown(
        tile_html(p["id"], p["name"], f"{p['brand']} · {dh(p['price'])}",
                  badges, height=height, swatches=p["colors"], img=img)
        + f'<div style="margin:2px 0 6px 0">{"".join(tags)}</div>',
        unsafe_allow_html=True,
    )
    in_dw = any(d["id"] == p["id"] for d in st.session_state.dream_wardrobe)
    libelle = "Rêvé ✓" if in_dw else (cta or "Dream Wardrobe ✦")
    if col.button(libelle,
                  key=f"dw_{p['id']}_{key_suffix}", use_container_width=True,
                  help="Épingler / retirer cette pièce dans tes envies d'achat"):
        if in_dw:
            st.session_state.dream_wardrobe = [d for d in st.session_state.dream_wardrobe if d["id"] != p["id"]]
        else:
            st.session_state.dream_wardrobe.append({
                "id": p["id"], "name": p["name"], "brand": p["brand"],
                "price": p["price"], "target_price": round(p["price"] * .75, 2),
                "colors": p["colors"], "year": "—",
            })
            state.notif(f"{p['name']} ajouté(e) à ton Dream Wardrobe ✦")
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Barre d'activité de profil (mini-graph en CSS) — délégué au thème
# ─────────────────────────────────────────────────────────────────────────────
from core.theme import stat_card, style_bar  # noqa: F401, E402
