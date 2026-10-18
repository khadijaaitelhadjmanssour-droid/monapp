# -*- coding: utf-8 -*-
"""Découverte du style personnel : quiz en 5 étapes + portrait IA."""

import streamlit as st

from core import state, theme
from core.demo_data import PRODUCTS_BY_ID, STYLES

COULEURS = ["crème", "beige", "kaki", "marine", "bordeaux", "lilas",
            "noir", "sauge", "terracotta", "blanc"]

LIFESTYLES = [
    "Bureau & rendez-vous", "Parents en mouvement", "Créatif·ve & artiste",
    "Étudiant·e dynamique", "Soirées & événements", "Tranquille au week-end",
]
LIFE_BONUS = {
    "Bureau & rendez-vous": "business",
    "Parents en mouvement": "casual",
    "Créatif·ve & artiste": "bohème",
    "Étudiant·e dynamique": "streetwear",
    "Soirées & événements": "rock",
    "Tranquille au week-end": "casual",
}
OCC_BONUS = {"Travail": "business", "Soirée": "rock", "Événement": "romantique",
             "Week-end": "casual", "Vacances": "bohème", "Quotidien": "minimaliste"}

OCCASIONS = ["Quotidien", "Travail", "Week-end", "Soirée", "Événement", "Vacances"]


def render():
    p = st.session_state.profile
    qa = st.session_state.quiz_answers

    if p.get("quiz_done"):
        _portait(p)
        return

    theme.hero("Ton style en 5 questions ✦",
               "L'agent IA se construit à partir de tes réponses : goûts, couleurs, "
               "mode de vie, budget. Tu pourras tout relancer à tout moment.")

    total_steps = 5
    st.progress((st.session_state.quiz_step) / (total_steps - 1),
                text=f"Étape {st.session_state.quiz_step + 1} / {total_steps}")

    step = st.session_state.quiz_step
    nxt = None
    if step == 0:
        qa["pseudo"] = st.text_input("Comment veux-tu être appelé(e) ?",
                                     value=qa.get("pseudo", ""), placeholder="ex. Zoé")
        qa["taille"] = st.text_input("Tes tailles habituelles",
                                     value=qa.get("taille", ""), placeholder="ex. M / 38 / 42")
        nxt = st.button("Continuer →", type="primary")
    elif step == 1:
        st.markdown("**Quels styles te parlent ?** (jusqu'à 4)")
        qa["styles"] = st.multiselect("Styles", STYLES, default=qa.get("styles", []),
                                      max_selections=4, label_visibility="collapsed",
                                      placeholder="jusqu'à 4 styles…")
        nxt = st.button("Continuer →", type="primary",
                        disabled=len(qa.get("styles", [])) == 0)
    elif step == 2:
        st.markdown("**Tes couleurs amies** 🎨")
        qa["couleurs_amies"] = st.multiselect(
            "Couleurs que tu portes sans réfléchir",
            COULEURS, default=qa.get("couleurs_amies", []), label_visibility="collapsed")
        st.markdown("**Tes couleurs bannies** ⛔")
        qa["couleurs_bannies"] = st.multiselect(
            "Couleurs que tu ne porteras jamais",
            COULEURS, default=qa.get("couleurs_bannies", []), label_visibility="collapsed")
        nxt = st.button("Continuer →", type="primary")
    elif step == 3:
        sl = st.slider("Budget moyen par pièce (€)", 10, 500,
                       value=int(qa.get("budget", p["budget"])), step=10)
        qa["budget"] = sl
        qa["occasions"] = st.multiselect("Quand t'habilles-tu le plus ?",
                                         OCCASIONS, default=qa.get("occasions", []),
                                         placeholder="choisir…")
        qa["lifestyle"] = st.selectbox("Ton mode de vie ressemble à…",
                                       LIFESTYLES, index=0)
        nxt = st.button("Continuer →", type="primary")
    elif step == 4:
        _recap(qa)
        nxt = st.button("✨ Activer mon profil IA", type="primary")

    _, b = st.columns([6, 1])
    if b.button("←", key="prev"):
        st.session_state.quiz_step = max(0, step - 1)
        st.rerun()
    if nxt:
        if step == 0 and not qa.get("pseudo", "").strip():
            st.warning("Donne-moi au moins un prénom/pseudo 🙂")
        else:
            st.session_state.quiz_step = step + 1
        if step == 4:
            _activer_profil(qa)
        st.rerun()


def _recap(qa):
    st.markdown("#### Récapitulatif")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"**Pseudo ·** {qa.get('pseudo') or '—'}  \n"
            f"**Tailles ·** {qa.get('taille') or '—'}  \n"
            f"**Styles ·** {', '.join(qa.get('styles', []) or ['—'])}"
        )
    with c2:
        st.markdown(
            f"**Budget ·** {qa.get('budget', 0):.0f} €/pièce  \n"
            f"**Occasions ·** {', '.join(qa.get('occasions', []) or ['—'])}  \n"
            f"**Couleurs ·** {', '.join(qa.get('couleurs_amies', []) or ['—'])}"
        )
    st.info("L'IA utilisera ces informations pour trier le fil, générer des tenues "
            "et te recommander des pièces compatibles.", icon="🧠")


def _activer_profil(qa):
    p = st.session_state.profile
    scores = {s: 2 for s in qa.get("styles", [])}
    bonus_l = LIFE_BONUS.get(qa.get("lifestyle"))
    if bonus_l:
        scores[bonus_l] = scores.get(bonus_l, 0) + 1
    for occ in qa.get("occasions", []):
        bs = OCC_BONUS.get(occ)
        if bs:
            scores[bs] = scores.get(bs, 0) + 1
    p.update({
        "pseudo": qa.get("pseudo") or p["pseudo"],
        "taille": qa.get("taille", ""),
        "styles_scores": {k: v for k, v in scores.items() if v > 0},
        "budget": qa.get("budget", 120),
        "occasions": qa.get("occasions", []),
        "lifestyle": qa.get("lifestyle", ""),
        "couleurs_amies": qa.get("couleurs_amies", []),
        "couleurs_bannies": qa.get("couleurs_bannies", []),
        "quiz_done": True,
    })
    state.notif("Profil IA activé — le styliste est réglé sur toi ✨")
    st.session_state.quiz_step = 0
    state.persist()


def _portait(p):
    theme.hero(f"Ton portrait IA, {p['pseudo']} ✦",
               "Généré localement par le moteur explicite STYLEMIND — chaque facteur "
               "est expliqué. Il évoluera avec tes épings, tenues et décisions dans l'app.")
    top = sorted(p["styles_scores"].items(), key=lambda kv: -kv[1]) or [("à définir", 0)]
    c1, c2, c3 = st.columns(3)
    with c1:
        theme.stat_card(f"{p['budget']:.0f} €", "budget moyen / pièce")
    with c2:
        total = sum(v for _, v in top)
        pct = round(top[0][1] / total * 100) if total else 0
        theme.stat_card(f"{pct} %", f"signature « {top[0][0]} »")
    with c3:
        affordable = sum(1 for x in PRODUCTS_BY_ID.values() if x["price"] <= p["budget"])
        theme.stat_card(f"{affordable}/{len(PRODUCTS_BY_ID)}",
                        "articles compatibles budget")

    st.markdown("#### Ta signature de style")
    for s, v in top:
        from ui.components import style_bar
        style_bar(s.capitalize(), round(v / (sum(x[1] for x in top) or 1) * 230))

    st.markdown("#### Palette & occasions")
    st.markdown(theme.chips(p["couleurs_amies"], cls="chip")
                + theme.chips(p["couleurs_bannies"], cls="chip chip-second")
                + theme.chips(p["occasions"], cls="chip chip-follow"),
                unsafe_allow_html=True)

    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    st.info("🧠 **Analyse IA explicite** : votre portrait combine styles du quiz, "
            "mode de vie et occasions. Cette version utilise le moteur de règles "
            "local ; un LLM (OpenAI…) peut être branché au même endroit pour "
            "enrichir la prose.", icon="✨")

    a, b, c = st.columns([1, 1, 1])
    with a:
        if st.button("🔄 Relancer le quiz", use_container_width=True):
            p["quiz_done"] = False
            st.session_state.quiz_step = 0
            state.persist()
            st.rerun()
    with b:
        if st.button("👔 Voir le styliste IA", type="primary", use_container_width=True):
            st.session_state["page"] = "styliste"
            st.rerun()
    with c:
        if st.button("↩️ Retour au fil", use_container_width=True):
            st.session_state["page"] = "fil"
            st.rerun()
