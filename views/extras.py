# -*- coding: utf-8 -*-
"""Extras : mode éthique, seconde main, looks de célébrités, assistant cadeaux."""

import streamlit as st

from core import ai_engine, state, theme
from core.demo_data import CELEB_LOOKS, PRODUCTS_BY_ID
from ui.components import gradient_for, product_card, tile_html

STYLES_GIFT = ["minimaliste", "chic parisien", "bohème", "romantique", "streetwear",
               "rock", "vintage", "business", "casual", "éthique", "cozy"]
RELATIONS = ["Mère", "Père", "Ami·e", "Collègue", "Sœur / frère", "Grand-parent",
             "Avec moi-même 🙂"]


def render():
    theme.hero(
        "Extras ✦",
        "Mode éthique, friperie, looks de célébrités décryptés et assistant cadeaux. "
        "Ces quatre modules utilisent le catalogue « démo » : tout est simulé en "
        "attendant les vraies intégrations.",
        theme.demo_chip(),
    )

    t1, t2, t3, t4 = st.tabs(["🌿 Mode éthique", "♻️ Seconde main",
                              "🌟 Célébrités", "🎁 Assistant cadeaux"])
    with t1:
        _ethique()
    with t2:
        _fripes()
    with t3:
        _celebrites()
    with t4:
        _cadeaux()

    state.consume_notif()


def _ethique():
    p = st.session_state.profile
    ecos = [prod for prod in PRODUCTS_BY_ID.values() if prod["ethical"] >= 4]
    c1, c2, c3 = st.columns(3)
    c1.metric("Pièces avec impact ≥ 4/5", len(ecos))
    c2.metric("Impact moyen catalogue", round(sum(
        prod["ethical"] for prod in PRODUCTS_BY_ID.values()) / len(PRODUCTS_BY_ID), 1))
    c3.metric("Compatibles avec ton budget", len([x for x in ecos if x["price"] <= p["budget"]]))
    st.caption("Scores « éthique » locaux (DÉMO) — à remplacer par des notations de "
               "référence (Cleancloth, Textile Exchange…) quand la brique sera branchée.")
    cols = st.columns(3)
    for i, prod in enumerate(ecos[:9]):
        product_card(prod, cols[i % 3], height=140, key_suffix="eth")


def _fripes():
    fripes = [prod for prod in PRODUCTS_BY_ID.values() if prod["secondhand"]]
    st.markdown("**Pourquoi la friperie change ta garde-robe :** échappée du jetable, "
                "prix bradés, pièces qui ont déjà traversé le temps.")
    st.markdown(theme.chips([p["name"] for p in fripes]) + theme.demo_chip(),
                unsafe_allow_html=True)
    cols = st.columns(3)
    for i, prod in enumerate(fripes):
        product_card(prod, cols[i % 3], height=150, key_suffix="fri")
    st.info("Tu cherches **plus près de toi** ? L'IA pourra analyser les inventaires "
            "des friperies et de Vinted autour de toi à l'étape suivante (simulation "
            "elle aussi, pour l'instant).")


def _celebrites():
    p = st.session_state.profile
    cols = st.columns(3)
    for i, look in enumerate(CELEB_LOOKS):
        col = cols[i % 3]
        col.markdown(tile_html(
            look["id"],
            look["celeb"],
            look["vibe"],
            '<span class="t-badge badge-demo">CÉLÉBRITÉ DÉMO</span>',
            height=150,
            swatches=[PRODUCTS_BY_ID[q]["colors"][0] for q in look["products"]],
        ), unsafe_allow_html=True)
        col.markdown(f"**{look['desc']}**")
        col.caption(f"Prix presse « dark-line » ~{look['price_celeb']:.0f} € "
                    "(chiffre imagé, DÉMO)")
        if col.button("✧ Adapter à mon style & budget", key=f"adapt_{look['id']}",
                      use_container_width=True):
            st.session_state["look_adapte"] = look["id"]
        if st.session_state.get("look_adapte") == look["id"]:
            adapter_look(look, col)


def adapter_look(look, col):
    """Recompose le look selon budget : friperie ou alternative quand d'un chiffre
    « star » trop élevé. Explication ligne par ligne."""
    adapted, total, notes = [], 0.0, []
    for pid in look["products"]:
        prod = PRODUCTS_BY_ID[pid]
        if prod["price"] > st.session_state.profile["budget"] * 1.25:
            alt = ai_engine.alternative_moins_chere(prod)
            if alt:
                adapted.append(alt)
                total += alt["price"]
                notes.append(f"« {prod['name']} » ({prod['price']:.0f} €) → {alt['name']} "
                             f"({alt['price']:.0f} €, plus accessible)")
                continue
        adapted.append(prod)
        total += prod["price"]

    col.markdown("**Ton adaptation :**")
    col.markdown(theme.chips([q["name"] for q in adapted]), unsafe_allow_html=True)
    col.markdown(f"Total ≈ **{total:.0f} €** vs {look['price_celeb']:.0f} € version star "
                 f"– économie ≈ {look['price_celeb'] - total:.0f} € 🎉")
    if notes:
        col.caption("Choix remplacés : " + " · ".join(notes))
    if col.button("💾 Enregistrer cette adaptation", key=f"saveadapt_{look['id']}",
                  use_container_width=True):
        st.session_state["looks_sauvegardes"].append(f"adapt_{look['id']}")
        state.notif("Adaptation enregistrée dans tes épings ✧")
        st.rerun()


def _cadeaux():
    p = st.session_state.profile
    st.markdown("Décris la personne et laisse l'agent proposer 💚 *(moteur de règles "
                "local — un LLM enrichira les mots doux du cadeau quand il sera branché)*")
    c1, c2, c3 = st.columns(3)
    rel = c1.selectbox("Qui ?", RELATIONS, index=2)
    age = c2.slider("Âge approximatif", 5, 95, 35)
    styles = c3.multiselect("Son style", STYLES_GIFT, default=["casual"],
                            placeholder="choisir…")
    budget = st.slider("Budget (€)", 10, 300, int(p["budget"]), step=5)

    if st.button("🎁 Trouver des idées", type="primary"):
        gifts = ai_engine.cadeaux(budget, styles, rel)
        st.session_state["gift_result"] = (rel, age, gifts, budget)

    res = st.session_state.get("gift_result")
    if res:
        rel, age, gifts, budget = res
        st.markdown(f"#### Propositions pour : {rel}, ~{age} ans · budget {budget:.0f} €")
        cols = st.columns(4)
        for i, prod in enumerate(gifts):
            col = cols[i % 4]
            product_card(prod, col, height=140, cta="💌 Garder", key_suffix="gift")
            why = []
            if set(prod["styles"]) & set(styles):
                why.append("son style")
            if prod["price"] <= budget * .5:
                why.append("prix doux")
            if prod["ethical"] >= 4:
                why.append("éthique ✓")
            col.caption("Choix : " + (", ".join(why) or "la valeur sûre de son panier"))
