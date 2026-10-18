# -*- coding: utf-8 -*-
"""Fil visuel façon Pinterest."""

import streamlit as st

from core import state, theme
from core.demo_data import FEED, STYLES
from ui.components import feed_card, stat_card


def render():
    p = st.session_state.profile
    theme.hero(
        "Le fil ✦",
        "Regarde, épingle, suis. Le fil mélange les looks de la communauté et les "
        "placements sponsorisés du catalogue "
        f"<span class='demo-chip'>DÉMO</span>. Ton profil IA "
        f"({'actif ✓' if p['quiz_done'] else 'non activé'}) trie chaque tuile.",
        "",
    )

    if not p["quiz_done"]:
        st.info(
            "💡 Active ton **profil style IA** (page « Styliste IA ») pour que le fil "
            "soit trié selon tes goûts, ton mode de vie et ton budget.",
            icon="✨",
        )

    # ── Filtres ──────────────────────────────────────────────────────────────
    f1, f2, f3, f4 = st.columns([1.3, 1.3, 1, 1.2])
    sel_styles = f1.multiselect("Styles", STYLES, placeholder="Tous")
    sel_occ = f2.selectbox(
        "Occasion", ["Toutes", "Quotidien", "Travail", "Week-end", "Soirée",
                     "Événement", "Vacances"], index=0)
    hide_sponsored = f3.toggle("Masquer sponsorisés", value=False)
    sort_pop = f4.selectbox("Tri", ["Recommandé pour toi", "Populaire"], index=0)

    items = list(FEED)
    if sel_styles:
        items = [f for f in items if set(sel_styles) & {s.strip() for s in f["styles"]}]
    if sel_occ != "Toutes":
        # filtre par occasion : au moins un produit du look la couvre
        items = [f for f in items if sel_occ in _look_occasions(f)]
    if hide_sponsored:
        items = [f for f in items if not f["sponsored"]]
    if sort_pop == "Populaire":
        items.sort(key=lambda f: -f["size"])

    st.markdown(
        f"<div>{theme.chips(sorted({s.strip() for f in items for s in f['styles']}))}</div>",
        unsafe_allow_html=True,
    )

    # ── Murae masonry (répartition stable par id) ────────────────────────────
    ncols = 4
    cols = st.columns(ncols)
    for i, f in enumerate(items):
        feed_card(f, cols[i % ncols])

    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        stat_card(len(st.session_state.looks_sauvegardes), "looks épinglés")
    with c2:
        stat_card(len(st.session_state.moodboards), "moodboards")
    with c3:
        stat_card(len(st.session_state.follows), "créateurs suivis")


def _look_occasions(f) -> list:
    from core.demo_data import PRODUCTS_BY_ID
    occ = set()
    for pid in f["products"]:
        occ.update(PRODUCTS_BY_ID[pid]["occasions"])
    return sorted(occ)
