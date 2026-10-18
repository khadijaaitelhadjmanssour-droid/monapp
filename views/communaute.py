# -*- coding: utf-8 -*-
"""Communauté : créateurs & stylistes à suivre, moodboards, looks sauvegardés."""

import uuid

import streamlit as st

from core import state, theme
from core.demo_data import CREATORS, FEED_BY_ID, PRODUCTS_BY_ID
from core.format import dh, nombre_fr
from ui import assets
from ui.components import gradient_for, tile_html

ROLES_CHIP = {"Styliste": "chip chip-follow", "Créatrice": "chip"}


def render():
    theme.hero(
        "La communauté ✦",
        "Suis des créateurs et des stylistes, explore leurs garde-robes achetables et "
        "organise ton inspiration en moodboards. Les profils et les stats affichés "
        "ici sont des données de démo.",
        theme.chips(["6 profils démo", "mises à jour locales"]) + theme.demo_chip(),
    )

    t1, t2, t3 = st.tabs(["👉 Créateurs & stylistes", "✧ Moodboards", "♥ Mes épings"])

    with t1:
        _creators()
    with t2:
        _moodboards()
    with t3:
        _epingles()

    state.consume_notif()


# ─────────────────────────────────────────────────────────────────────────────
def _creators():
    follows = st.session_state.follows
    cols = st.columns(2)
    ordered = sorted(CREATORS, key=lambda c: c["id"] not in follows)
    for i, c in enumerate(ordered):
        col = cols[i % 2]
        suivi = c["id"] in follows
        affili = ("<span class='chip chip-eco'>Garde-robe achetable · "
                  "commission affiliée (démo)</span>" if c["shoppable"]
                  else "<span class='chip'>Inspiration (sans vente)</span>")
        avatar = assets.data_uri("creators", c["id"])
        if avatar:
            avatar_html = (f'<img src="{avatar}" alt="Avatar (démo) de {c["name"]}" '
                           f'style="width:64px; height:64px; border-radius:50%;'
                           f' object-fit:cover; border:2px solid #EBB9C9; flex-shrink:0;"/>')
        else:
            avatar_html = (f'<div style="background:{gradient_for(c["id"])}; width:64px;'
                           f' height:64px; border-radius:50%; flex-shrink:0;"></div>')
        col.markdown(
            f'<div class="outfit-card" style="display:flex; gap:12px;">'
            f"{avatar_html}"
            f"<div style='flex:1'>"
            f"<strong>{c['name']}</strong> <span style='opacity:.6'>{c['handle']}</span>"
            f"<div style='margin:3px 0'><span class='{ROLES_CHIP.get(c['role'], 'chip')}'>"
            f"{c['role']}</span></div>"
            f"<div style='font-size:.83rem; opacity:.85'>{c['specialty']}</div>"
            f"<div style='font-size:.78rem; opacity:.6'>{nombre_fr(c['followers'])} abonnés"
            f"{' · suivi ✓' if suivi else ''}</div>"
            f"<div style='margin-top:4px'>{affili}</div>"
            "</div></div>",
            unsafe_allow_html=True,
        )
        if col.button(("✓ Ne plus suivre" if suivi else "✦ Suivre") + f" {c['handle']}",
                      key=f"folc_{c['id']}", use_container_width=True):
            if suivi:
                follows.remove(c["id"])
            else:
                follows.append(c["id"])
                state.notif(f"Tu suis {c['name']} ✦")
            state.persist()
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
def _items_epinglables():
    """{label unique → id} : looks sauvegardés, envies, pièces de garde-robe."""
    e = {}
    for fid in st.session_state.looks_sauvegardes:
        f = FEED_BY_ID.get(fid)
        if f:
            e[f"Look · {f['title']}"] = fid
    for aid, ad in st.session_state.get("adapted_looks", {}).items():
        e[f"Adaptation · {ad.get('celeb', aid)}"] = aid
    for d in st.session_state.dream_wardrobe:
        e[f"Envie · {d['name']}"] = d["id"]
    for g in st.session_state.garde_robe:
        e[f"Pièce · {g['name']}"] = g["id"]
    return e


def _source_image(item_id: str) -> list:
    """Résout la meilleure illustration locale pour un id épinglé."""
    if item_id in FEED_BY_ID:
        return [("looks", item_id)]
    if item_id in PRODUCTS_BY_ID:
        return [("products", item_id)]
    if item_id in st.session_state.get("adapted_looks", {}):
        sid = st.session_state.adapted_looks[item_id].get("source")
        if sid:
            return [("celebs", sid)]
    for g in st.session_state.garde_robe:
        if g["id"] == item_id:
            return [("categories", g["category"])]
    return []


def _moodboards():
    mb = st.session_state.moodboards
    eligibles = _items_epinglables()
    labels_by_id = {v: k for k, v in eligibles.items()}
    labels = list(eligibles)

    # Nettoyage (un tour en avance) : retire la sélection morte d'une épingle
    # supprimée, sinon la multiselect la ré-ajoutait automatiquement au rerun.
    pruned = st.session_state.pop("mb_prune", set())
    for mid in pruned:
        st.session_state.pop(f"mbadd_{mid}", None)

    c1, c2 = st.columns([2, 1])
    nom = c1.text_input("Nom du nouveau moodboard", placeholder="ex. Printemps doux")
    if c2.button("✨ Créer le moodboard", key="mb_new", use_container_width=True):
        if not nom.strip():
            st.warning("Donne un nom à ton moodboard 🙂")
        else:
            mid = str(uuid.uuid4())[:6]
            mb[mid] = {"name": nom.strip(), "items": []}
            state.notif(f"Moodboard « {nom.strip()} » créé ✧")
            state.persist()
            st.rerun()

    if not mb:
        st.caption("Aucun moodboard encore. Crée le premier pour organiser ton inspiration.")
        return

    for mid, board in list(mb.items()):
        with st.container(border=True):
            h1, h2, h3 = st.columns([3, 2, .4])
            h1.markdown(f"**✧ {board['name']}** · {len(board['items'])} épin(s)")
            add = h2.multiselect("Ajouter des épingles", labels, key=f"mbadd_{mid}",
                                 label_visibility="collapsed", placeholder="+ épingles…")
            if h3.button("🗑️", key=f"mbdel_{mid}", use_container_width=True):
                mb.pop(mid)
                state.persist()
                st.rerun()
            new_ids = [eligibles[lab] for lab in add if eligibles[lab] not in board["items"]]
            if new_ids:
                board["items"].extend(new_ids[:4])
                state.persist()
                st.rerun()

            cols = st.columns(4)
            for j, item_id in enumerate(list(board["items"])):
                cj = cols[j % 4]
                img = assets.bg_deck(_source_image(item_id))
                cj.markdown(
                    tile_html(f"mb_{item_id}", "", "", "", height=100, img=img)
                    + f"<div style='font-size:.72rem; opacity:.75'>"
                    f"{labels_by_id.get(item_id, 'épin')}</div>",
                    unsafe_allow_html=True,
                )
                if cj.button("✕", key=f"mbun_{mid}_{j}", use_container_width=True):
                    board["items"].remove(item_id)
                    pruned.add(mid)
                    st.session_state["mb_prune"] = pruned
                    state.persist()
                    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
def _epingles():
    saves = st.session_state.looks_sauvegardes
    adapted = st.session_state.get("adapted_looks", {})
    if not saves and not adapted:
        st.caption("Rien d'épinglé pour l'instant — épingle des looks depuis le fil ♥, "
                   "ou adapte un look de célébrité depuis Extras.")

    cols = st.columns(3)
    i = 0

    def next_col():
        nonlocal i
        c = cols[i % 3]
        i += 1
        return c

    for fid in list(saves):
        f = FEED_BY_ID.get(fid)
        if not f:
            continue
        c = next_col()
        c.markdown(
            tile_html(fid, f["title"],
                      ("Sponsorisé · " if f["sponsored"] else ""),
                      "", height=150,
                      img=assets.bg_deck([("looks", fid)])),
            unsafe_allow_html=True,
        )
        if c.button("✕ Désépingler", key=f"unpin_{fid}", use_container_width=True):
            saves.remove(fid)
            state.persist()
            st.rerun()

    for aid in list(adapted):
        ad = adapted[aid]
        c = next_col()
        c.markdown(
            tile_html(aid, ad.get("celeb", "Adaptation"),
                      f"Adaptation à ton budget · {dh(ad.get('total', 0))}", "", height=150,
                      img=assets.bg_deck([("celebs", ad.get("source", ""))])),
            unsafe_allow_html=True,
        )
        c.caption(" · ".join(ad.get("pieces", [])) or "—")
        if c.button("✕ Désépingler", key=f"unpinadapt_{aid}", use_container_width=True):
            adapted.pop(aid)
            if aid in st.session_state.looks_sauvegardes:
                st.session_state.looks_sauvegardes.remove(aid)
            state.persist()
            st.rerun()
