# -*- coding: utf-8 -*-
"""Fil visuel façon Pinterest + page de détail d'un look."""

import streamlit as st

from core import state, theme
from core.demo_data import FEED, STYLES, CREATORS_BY_ID, FEED_BY_ID, PRODUCTS_BY_ID
from core.format import dh
from ui import assets
from ui.components import feed_card, product_card, stat_card, tile_html, badges_for_item


def render():
    look_page = st.session_state.get("look_page")
    if look_page and look_page in FEED_BY_ID:
        _render_detail(look_page)
        return
    _render_feed()


# ─────────────────────────────────────────────────────────────────────────────
# Le fil : mêmes filtres / recherche / styles que précédemment
# ─────────────────────────────────────────────────────────────────────────────
def _render_feed():
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
    f0, f1, f2, f3, f4 = st.columns([1.3, 1.05, 1.05, .9, 1])
    query = f0.text_input("🔎 Rechercher", placeholder="pièce, marque, créateur…")
    sel_styles = f1.multiselect("Styles", STYLES, placeholder="Tous")
    sel_occ = f2.selectbox(
        "Occasion", ["Toutes", "Quotidien", "Travail", "Week-end", "Soirée",
                     "Événement", "Vacances"], index=0)
    hide_sponsored = f3.toggle("Masquer sponsorisés", value=False)
    sort_pop = f4.selectbox("Tri", ["Recommandé pour toi", "Populaire"], index=0)

    items = list(FEED)
    if query.strip():
        q = query.strip().lower()

        def _match(f):
            creator = CREATORS_BY_ID.get(f["creator"], {})
            hay = [f["title"], creator.get("name", ""), creator.get("handle", ""),
                   creator.get("specialty", "")]
            for pid in f["products"]:
                prod = PRODUCTS_BY_ID.get(pid)
                if prod:
                    hay.extend([prod["name"], prod["brand"], prod["category"]])
            return q in " ".join(hay).lower()
        items = [f for f in items if _match(f)]
        if not items:
            st.info(f"Aucun look ne correspond à « {query.strip()} » — essaie un autre "
                    "mot-clé (pièce, marque, créateur).", icon="🔍")
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

    # ── Mur masonry (3 colonnes : boutons d'action jamais tronqués) ─────────
    ncols = 3
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
    occ = set()
    for pid in f["products"]:
        occ.update(PRODUCTS_BY_ID[pid]["occasions"])
    return sorted(occ)


# ─────────────────────────────────────────────────────────────────────────────
# Page de détail d'un look (ouverte par « 👁 Voir le look » sur une carte)
# ─────────────────────────────────────────────────────────────────────────────
def _render_detail(lid: str):
    f = FEED_BY_ID[lid]
    creator = CREATORS_BY_ID.get(f["creator"], {})
    pieces = [PRODUCTS_BY_ID[pid] for pid in f["products"]]
    total = sum(p["price"] for p in pieces)
    occasions = _look_occasions(f)
    styles = sorted({s.strip() for s in f["styles"]})

    # L'utilisateur atterrit ici via un clic ; "Retour" revient au fil.
    if st.button("← Retour au fil", key="back_to_feed",
                 help="Revenir à la découverte des looks"):
        st.session_state.look_page = None
        st.rerun()

    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    hero, infos = st.columns([1.15, 1])
    with hero:
        _hero_image(f)
    with infos:
        st.markdown(
            "<div>" + badges_for_item("look", sponsored=f["sponsored"])
            + "</div>", unsafe_allow_html=True)
        st.markdown(f"### {f['title']}")
        st.markdown(
            f"✦ **{creator.get('name', 'Créateur de la démo')}** · "
            f"{creator.get('role', 'Créateur')} · "
            f"*{creator.get('specialty', '')}*" if creator else "✦ Look de la démo")
        if styles:
            st.markdown(f"<div>{theme.chips(styles)}</div>",
                        unsafe_allow_html=True)
        if occasions:
            st.caption("Occasions : " + " · ".join(occasions))
        st.markdown(
            f"{len(pieces)} pièce(s) · **≈ {dh(total)} au total** "
            "(somme des pièces en DH)")
        _action_buttons(f)
        st.caption("Looks de données DÉMO : les créateurs, marques et prix sont "
                    "simulés ; les photos (Unsplash, licence libre) illustrent le "
                    "thème du look.")

    st.markdown("#### Les pièces du look")
    cols = st.columns(3)
    for i, p in enumerate(pieces):
        product_card(p, cols[i % 3], height=170, key_suffix="detail")


def _hero_image(f):
    """Grande photo du look : vraie photo locale si disponible, sinon tuile
    à dégradé déterministe (repli propre, jamais d'image cassée)."""
    photo = assets.photo_bytes(f["id"])
    if photo:
        st.image(photo, use_container_width=True)
        return
    img = assets.media_pick(f["id"], [("looks", f["id"])])
    if not img:
        st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
        st.info("Pas de visuel pour ce look.", icon="🖼")
        return
    creator = CREATORS_BY_ID.get(f["creator"], {})
    sub = f"{creator.get('name','')} · {creator.get('specialty','')}"
    st.markdown(
        tile_html(f["id"], "", sub, height=430, img=img),
        unsafe_allow_html=True,
    )


def _action_buttons(f):
    saved = f["id"] in st.session_state.looks_sauvegardes
    follow = f["creator"] in st.session_state.follows
    creator = CREATORS_BY_ID.get(f["creator"], {})
    b1, b2 = st.columns(2)
    if b1.button("★ Épinglé ✓" if saved else "★ Épingler le look",
                 key=f"det_save_{f['id']}", use_container_width=True,
                 help="Ajouter / retirer ce look de tes favoris ♥"):
        if saved:
            st.session_state.looks_sauvegardes.remove(f["id"])
        else:
            st.session_state.looks_sauvegardes.append(f["id"])
            state.notif("Look enregistré dans tes favoris ♥")
        st.rerun()
    if b2.button("✓ Suivi ✓" if follow else "+ Suivre",
                 key=f"det_fol_{f['id']}", use_container_width=True,
                 help=f"Suivre {creator.get('name', 'ce créateur')}"):
        if follow:
            st.session_state.follows.remove(f["creator"])
        else:
            st.session_state.follows.append(f["creator"])
            state.notif(f"Tu suis {creator.get('name', '')} ✦")
        st.rerun()
