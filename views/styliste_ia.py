# -*- coding: utf-8 -*-
"""Styliste IA : agent conversationnel + tenues du jour + zone Premium."""

import streamlit as st

from core import ai_engine, state, theme
from core.demo_data import PRODUCTS_BY_ID
from ui.components import product_card, tile_html


def render():
    p = st.session_state.profile
    profile_ok = p.get("quiz_done")

    theme.hero(
        "Ton styliste personnel IA ✦",
        "Il apprend de ton profil, ton garde-robe et tes épings, puis recommande "
        "tenues, pièces, marques et stylistes. Moteur <b>explicite local</b> pour "
        "l'instant : un LLM prendra le relais sans changer l'interface (voir README).",
        "",
    )

    if not profile_ok:
        st.warning("Réponds d'abord au quiz (page « Profil & Style ») — sans profil, "
                   "les conseils restent génériques.", icon="✨")
        if st.button("✨ Ouvrir le quiz", type="primary"):
            st.session_state["page"] = "quiz"
            st.rerun()

    # ── Tenues du jour ───────────────────────────────────────────────────────
    a, b = st.columns([3, 1])
    a.markdown("#### Tenue proposée aujourd'hui")
    if st.session_state.get("tenues_jour") is None:
        st.session_state["tenues_jour"] = ai_engine.generer_tenues(p, n=3)
    if b.button("🎲 Nouvelles idées", key="regen", use_container_width=True):
        st.session_state["tenues_jour"] = ai_engine.generer_tenues(p, n=3)
        st.rerun()

    ncols = st.columns(1)
    for t in st.session_state["tenues_jour"]:
        _outfit_card(t, ncols[0])

    # ── Recommandations boutique ─────────────────────────────────────────────
    st.markdown("#### Recommandées pour toi")
    recos = ai_engine.recommandations(p, n=6)
    cols = st.columns(3)
    for i, (prod, meta) in enumerate(recos):
        c = cols[i % 3]
        product_card(prod, c, key_suffix="reco")
        c.caption(f"Match IA : {meta['match_pct']} % — "
                  f"style {meta['style']*100:.0f} % · budget {meta['budget']*100:.0f} %")

    # ── Premium (fonctions IA avancées) ─────────────────────────────────────
    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    _premium_block(p)

    # ── Chat agent ───────────────────────────────────────────────────────────
    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    st.markdown("#### Parle à ton styliste 💬")
    _chat(p, recos)

    state.consume_notif()


# ─────────────────────────────────────────────────────────────────────────────
def _outfit_card(t, col):
    """Carte à la tenue généré par l'IA."""
    pieces_lines = []
    for q in t["pieces"]:
        sw = "".join(f'<span class="sw" style="background:{c}; display:inline-block;'
                     f' width:11px; height:11px; border-radius:50%; margin-left:4px;"></span>'
                     for c in q["colors"][:3])
        pieces_lines.append(
            f"<div style='display:flex; justify-content:space-between; font-size:.82rem;"
            f" margin:2px 0;'><span>{q['name']} <span style='opacity:.6'>· {q['brand']}</span>"
            f"{sw}</span><b>{q['price']:.0f} €</b></div>"
        )
    sec_chip = ('<span class="chip chip-second"> principale en friperie possible</span>'
                if any(q["secondhand"] for q in t["pieces"]) else "")
    depasse = ('<span class="chip chip-second">au-dessus du budget ⇒ alternatives dans le '
               'Dream Wardrobe</span>' if t["depasse_budget"] else "")

    col.markdown(
        '<div class="outfit-card">'
        f"<h4>{t['nom']} <span style='opacity:.5; font-weight:400'>· {t['occasion']}</span></h4>"
        + theme.chips(t["styles"][:2], cls="chip")
        + "".join(pieces_lines)
        + f"<div style='margin-top:8px'><b>Total ≈ {t['prix_total']:.0f} €</b> · "
        f"éthique {t['eco_moyen']}/5 {sec_chip}</div>"
        + depasse
        + f"<div class='why'>👀 <b>Pourquoi ça marche :</b> {t['pourquoi']}</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = col.columns(3)
    if c1.button("💾 Enregistrer la tenue", key=f"save_t_{t['id']}",
                 use_container_width=True):
        st.session_state.tenues.append({
            "id": t["id"], "nom": t["nom"], "occasion": t["occasion"],
            "pieces": [q["id"] for q in t["pieces"]],
        })
        state.notif(f"Tenue « {t['nom']} » enregistrée dans ta garde-robe")
        st.rerun()
    if c2.button("✦ Ajouter au Dream Wardrobe", key=f"dw_t_{t['id']}",
                 use_container_width=True):
        for q in t["pieces"]:
            if not any(d["id"] == q["id"] for d in st.session_state.dream_wardrobe):
                prod = PRODUCTS_BY_ID[q["id"]]
                st.session_state.dream_wardrobe.append({
                    "id": q["id"], "name": q["name"], "brand": q["brand"],
                    "price": q["price"], "target_price": round(q["price"] * .75, 2),
                    "colors": q["colors"], "year": "—",
                })
        state.notif("Pièces ajoutées à ton Dream Wardrobe ✦")
        st.rerun()
    if c3.button("Pourquoi pas autre chose ?", key=f"why_t_{t['id']}", use_container_width=True):
        st.toast(t["pourquoi"], icon="🤔")
        st.rerun()


def _premium_block(p):
    if p.get("premium"):
        st.success("✦ **Premium activé (démo)** — analyse approfondie disponible.", icon="✨")
        _analyse_approfondie(p)
        if st.button("Désactiver (démo)"):
            p["premium"] = False
            state.persist()
            st.rerun()
        return

    st.markdown(
        '<div class="outfit-card" style="background:linear-gradient(120deg,#FFF7E0,#fff);">'
        "<h4>✦ Fonctions IA Premium <span class='chip chip-premium'>DÉMO</span></h4>"
        "Analyse complète de ta garde-robe, détection des pièces manquantes, "
        "alertes promo illimitées, styliste personnel récurrent…"
        "<div class='why'>Prix simulés dans cette démo — aucun paiement réel.</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    if c1.button("✦ Activer Premium (démo)", type="primary", use_container_width=True):
        p["premium"] = True
        state.notif("Premium activé pour cette démonstration ✨")
        st.rerun()
    c2.caption("Modèle économique : abonnement IA, commissions d'affiliation, "
               "placements sponsorisés, commissions sur les ventes des stylistes.")
    if c3.button("📄 En savoir plus", use_container_width=True, key="premium_info"):
        st.session_state["page"] = "premium"
        st.rerun()


def _analyse_approfondie(p):
    """Analyse de garde-robe [Premium] : couverture par catégorie + trous visibles."""
    gr = st.session_state.garde_robe
    if not gr:
        st.info("Ta garde-robe numérique est vide. Ajoute tes pièces dans la page "
                "**Garde-robe** pour que l'analyse devienne concrète.", icon="🧺")
        return
    cats = {}
    for it in gr:
        cats[it.get("category", "?")] = cats.get(it.get("category", "?"), 0) + 1
    st.markdown("**Couverture de ta garde-robe :**")
    for cat, n in sorted(cats.items(), key=lambda kv: -kv[1]):
        theme.style_bar(cat, min(n * 25, 100))
    manquants = [c for c in ["Hauts", "Bas", "Vestes", "Chaussures", "Accessoires"]
                 if c not in cats]
    if manquants:
        st.warning(f"Pièces à compléter : {', '.join(manquants)} — je te suggère "
                   "d'étoffer ces catégories.", icon="🧵")
    else:
        st.info("Garde-robe bien équilibrée : l'agent continue à suivre tes usages.")
    tenues = st.session_state.tenues
    st.caption(f"Utilisation : {len(tenues)} tenue(s) gardée(s) · "
               f"{len(st.session_state.dream_wardrobe)} pièce(s) dans le Dream Wardrobe.")


def _chat(p, recos):
    for m in st.session_state.chat:
        with st.chat_message(m["role"], avatar=("🧑" if m["role"] == "user" else "✦")):
            st.markdown(m["content"])

    quick1, quick2, quick3, quick4 = st.columns(4)
    if quick1.button("Pourquoi ?", key="q1", use_container_width=True):
        _send("Pourquoi cette reco ?", p, recos)
    if quick2.button("Tenue bureau", key="q2", use_container_width=True):
        _send("Sors-moi une tenue pour le travail", p, recos)
    if quick3.button("Idée cadeau", key="q3", use_container_width=True):
        _send("Une idée cadeaux pour ma mère ?", p, recos)
    if quick4.button("Seconde main", key="q4", use_container_width=True):
        _send("Montre-moi une alternative seconde main", p, recos)

    if msg := st.chat_input("Dis à ton styliste ce qui te préoccupe…"):
        _send(msg, p, recos)


def _send(texte, p, recos):
    st.session_state.chat.append({"role": "user", "content": texte})
    rep = ai_engine.reponse_agent(texte, p, recos)
    st.session_state.chat.append({"role": "assistant", "content": rep})
    st.rerun()
