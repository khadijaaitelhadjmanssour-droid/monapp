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
              extra_inner="") -> str:
    sw = ""
    if swatches:
        sw = '<div class="swatches">' + "".join(
            f'<div class="sw" style="background:{c}"></div>' for c in swatches[:4]) + "</div>"
    return (
        f'<div class="tile" style="background:{gradient_for(key)}; height:{height}px;">'
        f"{sw}{badges}"
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
        out += f'<span class="t-badge" style="background:rgba(255,255,255,.72)">{kind_lab}</span>'
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
    col.markdown(
        tile_html(f["id"], f["title"], f"{creator.get('name','')} · "
                  f"{creator.get('specialty','')}", badges, height=int(200 * f["size"]),
                  swatches=swatches),
        unsafe_allow_html=True,
    )
    b1, b2 = col.columns(2)
    saved = f["id"] in st.session_state.looks_sauvegardes
    if b1.button("♡ Épingler" if not saved else "✓ Épinglé",
                 key=f"save_{f['id']}", use_container_width=True):
        if saved:
            st.session_state.looks_sauvegardes.remove(f["id"])
        else:
            st.session_state.looks_sauvegardes.append(f["id"])
            state.notif("Look enregistré dans tes favoris ♥")
        st.rerun()
    follow = f["id"] in st.session_state.follows
    if b2.button("✓ Suivi" if follow else "Suivre",
                 key=f"fol_{f['id']}", use_container_width=True):
        if follow:
            st.session_state.follows.remove(f["id"])
        else:
            st.session_state.follows.append(f["id"])
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
    col.markdown(
        tile_html(p["id"], p["name"], f"{p['brand']} · {p['price']:.0f} €",
                  badges, height=height, swatches=p["colors"])
        + f'<div style="margin:2px 0 6px 0">{"".join(tags)}</div>',
        unsafe_allow_html=True,
    )
    in_dw = any(d["id"] == p["id"] for d in st.session_state.dream_wardrobe)
    if col.button(("✓ Rêvé") if in_dw else cta,
                  key=f"dw_{p['id']}_{key_suffix}", use_container_width=True):
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
