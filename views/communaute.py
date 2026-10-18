# -*- coding: utf-8 -*-
"""Communauté : créateurs & stylistes à suivre, moodboards, looks sauvegardés."""

import uuid

import streamlit as st

from core import state, theme
from core.demo_data import CREATORS, FEED_BY_ID
from ui.components import gradient_for

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
        col.markdown(
            f'<div class="outfit-card" style="display:flex; gap:12px;">'
            f'<div style="background:{gradient_for(c["id"])}; min-width:64px; '
            f'height:64px; border-radius:50%;"></div>'
            f"<div style='flex:1'>"
            f"<strong>{c['name']}</strong> <span style='opacity:.6'>{c['handle']}</span>"
            f"<div style='margin:3px 0'><span class='{ROLES_CHIP.get(c['role'], 'chip')}'>"
            f"{c['role']}</span></div>"
            f"<div style='font-size:.83rem; opacity:.85'>{c['specialty']}</div>"
            f"<div style='font-size:.78rem; opacity:.6'>{c['followers']:,} abonnés"
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
def _moodboards():
    mb = st.session_state.moodboards
    eligibles = _items_epinglables()
    labels = list(eligibles)

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
                cj.markdown(
                    f'<div class="tile" style="background:{gradient_for(str(item_id))};'
                    f'height:100px;"></div>'
                    f"<div style='font-size:.72rem; opacity:.75'>"
                    f"{eligibles.get(item_id, 'épin')}</div>",
                    unsafe_allow_html=True,
                )
                if cj.button("✕", key=f"mbun_{mid}_{j}", use_container_width=True):
                    board["items"].remove(item_id)
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
    for d in st.session_state.dream_wardrobe:
        e[f"Envie · {d['name']}"] = d["id"]
    for g in st.session_state.garde_robe:
        e[f"Pièce · {g['name']}"] = g["id"]
    return e


# ─────────────────────────────────────────────────────────────────────────────
def _epingles():
    saves = st.session_state.looks_sauvegardes
    if not saves:
        st.caption("Rien d'épinglé pour l'instant — garde des looks depuis le fil ♥")
    cols = st.columns(3)
    for i, fid in enumerate(list(saves)):
        f = FEED_BY_ID.get(fid)
        if not f:
            continue
        c = cols[i % 3]
        c.markdown(
            f'<div class="tile" style="background:{gradient_for(fid)}; height:150px;">'
            f'<div class="overlay"><div class="t-title">{f["title"]}</div>'
            f"<div class='t-sub'>{f['sponsored'] and 'Sponsorisé · ' or ''}"
            f"{theme.chips(f['styles'][:2])}</div></div></div>",
            unsafe_allow_html=True,
        )
        if c.button("✕ Désépingler", key=f"unpin_{fid}", use_container_width=True):
            saves.remove(fid)
            state.persist()
            st.rerun()
