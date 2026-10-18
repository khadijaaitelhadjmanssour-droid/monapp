# -*- coding: utf-8 -*-
"""
STYLEMIND ✦ — application de mode propulsée par l'IA (Streamlit).

Point d'entrée unique : `streamlit run app.py`
Toutes les données d'affichages externes sont des DONNÉES DE DÉMO
(catalogue, créateurs, prix, promos) — voir README.md.
"""

import streamlit as st

from core import state, theme

st.set_page_config(
    page_title="STYLEMIND ✦",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

state.init()
theme.inject()

# ─────────────────────────────────────────────────────────────────────────────
# Import des pages (lazy-friendly : chaque module est léger)
# ─────────────────────────────────────────────────────────────────────────────
from views import communaute, dream, extras, fil, garde_robe, premium, quiz, styliste_ia  # noqa: E402

PAGES = {
    "fil": ("✧", "Le fil"),
    "styliste": ("✨", "Styliste IA"),
    "quiz": ("🧠", "Profil & Style"),
    "robe": ("🧺", "Garde-robe"),
    "dream": ("🌙", "Dream Wardrobe"),
    "communaute": ("👥", "Communauté"),
    "extras": ("🌿", "Extras"),
    "premium": ("✦", "Premium & Offres"),
}
RENDERERS = {
    "fil": fil.render,
    "styliste": styliste_ia.render,
    "quiz": quiz.render,
    "robe": garde_robe.render,
    "dream": dream.render,
    "communaute": communaute.render,
    "extras": extras.render,
    "premium": premium.render,
}

current = st.session_state.get("page", "fil")
if current not in PAGES:
    current = "fil"
    st.session_state["page"] = current
p = st.session_state.profile

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar : identité + navigation
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="display:flex; align-items:center; gap:10px; margin:2px 0 6px 0;">'
        '<div style="background:linear-gradient(135deg,#EBB9C9,#B34168); width:40px;'
        'height:40px; border-radius:14px; display:flex; align-items:center;'
        'justify-content:center; color:#fff; font-weight:800; font-size:1.05rem;">SM</div>'
        '<div><div style="font-weight:800; font-size:1.05rem; line-height:1">STYLEMIND'
        '</div><div style="font-size:.7rem; opacity:.7">styliste IA · communauté'
        ' de mode</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:.8rem; padding:6px 4px 0 4px">'
        f'<div style="margin-bottom:4px"><span style="opacity:.8">{p["pseudo"]}</span>'
        ' <span class="demo-chip">DÉMO</span></div>'
        + ('<div style="margin-bottom:4px"><span class="chip chip-premium">'
           'Premium ✦ (démo)</span></div>' if p.get("premium") else "")
        + ("" if p["quiz_done"] else
           '<div style="margin-bottom:4px"><span class="chip" style='
           '"background:#FFE3EE; color:#B34168; font-size:.62rem; padding:2px 8px">'
           'profil IA à activer</span></div>')
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

    for key, (icon, label) in PAGES.items():
        if st.button(f"{icon}  {label}",
                     key=f"nav_{key}",
                     type="primary" if key == current else "secondary",
                     use_container_width=True):
            st.session_state["page"] = key
            st.rerun()

    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    st.caption(
        f"♥ épinglés {len(st.session_state.looks_sauvegardes)} · "
        f"✦ suivis {len(st.session_state.follows)} · "
        f"🌙 envies {len(st.session_state.dream_wardrobe)} · "
        f"🧺 garde-robe {len(st.session_state.garde_robe)}"
    )

    if st.button("↺ Réinitialiser la démo", key="reset_demo", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Rendu de la page courante
# ─────────────────────────────────────────────────────────────────────────────
RENDERERS[current]()

st.markdown(
    '<div style="text-align:center; opacity:.55; font-size:.75rem; margin:26px 0 10px">'
    "STYLEMIND ✦ — démonstrateur d'interface : "
    "les produits, créateurs et prix visibles sont des <b>données de démo</b> ; "
    "les fonctions IA tournent sur un moteur de règles local, prête à être "
    "branchée sur un LLM. Voir README.md.</div>",
    unsafe_allow_html=True,
)
state.consume_notif()
