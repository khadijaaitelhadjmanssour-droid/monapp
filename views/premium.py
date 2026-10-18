# -*- coding: utf-8 -*-
"""Premium & Marques : monétisation illustrée (abonnements, affiliation,
sponsored placements, commissions stylistes).Tout est DÉMO."""

import streamlit as st

from core import state, theme


def render():
    p = st.session_state.profile
    theme.hero(
        "StyleMIND pour toi ✦ et pour l'industrie ✦",
        "Une communauté de mode d'abord, une monétisation ensuite. Les prix et "
        "pourcentages indiqués sont des données de démonstration.",
        theme.chips(["abonnement IA", "affiliation", "placements sponsorisés",
                     "commissions stylistes"]) + theme.demo_chip(),
    )

    # ── Abonnements ─────────────────────────────────────────────────────────
    st.markdown("#### Choisis ton niveau")
    c1, c2, c3 = st.columns(3)
    plan = "premium" if p.get("premium") else "standard"
    with c1:
        _plan_card(
            "Gratuit", "0 €",
            ["Quiz + profil style", "Fil & épings", "Tenues du jour limitées (2/jour)",
             "Dream Wardrobe : 5 places", "Assistant cadeaux de base"],
            "✅ Ton plan actuel" if plan != "premium" else "",
        )
    with c2:
        _plan_card(
            "Premium ✦", "9,99 €/mois (démo)",
            ["Analyse complète de ta garde-robe", "Alertes promo illimitées",
             "Génération de tenues illimitée", "Recommandations LLM avancées",
             "Assistant cadeaux « mots doux »", "Dream Wardrobe sans limite"],
            "✅ Ton plan actuel" if plan == "premium" else "",
        )
    with c3:
        _plan_card(
            "Styliste+", "24,99 €/mois (démo)",
            ["Tout Premium", "Un styliste humain vérifie tes looks chaque mois",
             "Sessions visio annales", "Accès aux ventes privées partenaires"],
            "",
        )
    a1, a2 = st.columns(2)
    if a1.button("✦ Activer Premium (démo)" if not p.get("premium")
                 else "↩︎ Redevenir gratuit (démo)",
                 type="primary" if not p.get("premium") else "secondary",
                 use_container_width=True):
        p["premium"] = not p.get("premium")
        state.notif("Premium activé (démo) ✨" if p["premium"]
                    else "Rétrogradé au plan gratuit (démo)")
        st.rerun()
    a2.caption("Aucun paiement réel : cette démonstration simule l'état du compte.")

    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

    # ── Modèle économique ───────────────────────────────────────────────────
    st.markdown("#### Pour les marques & les stylistes 🤝")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        theme.stat_card("Affiliation", "8-15 % commission / vente démo")
    with m2:
        theme.stat_card("Sponsorisés", "placements marqués dans le fil (DÉMO)")
    with m3:
        theme.stat_card("Stylistes", "10 % sur garde-robe achetable")
    with m4:
        theme.stat_card("2 plans ✦", "abonnements premium")
    st.info("Le fil public mélange du communautaire et du sponsorisé, toujours "
            "étiqueté (badge violet « Sponsorisé »). Aucune donnée réelle de marque "
            "n'est chargée ici.", icon="🧾")

    # ── Espace partenaire (démo) ────────────────────────────────────────────
    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    exp = st.expander("🚀 Devenir partenaire (formulaire démo)")
    # (Le formulaire démonstration ne donne sur aucune boîte mail : les intégrations
    #  de services backend viendront plus tard.)
    with exp:
        _ = st.text_input("Nom de la marque / du styliste")
        contact = st.text_input("Email", placeholder="coucou@marque.fr")
        typ = st.selectbox("Type de partenariat",
                           ["Affiliation produit", "Sponsoring du fil",
                            "Garde-robe achetable (styliste)", "Autre"])
        if st.button("Envoyer ma demande (démo)", type="primary"):
            state.notif("Demande enregistrée côté démo — aucun envoi réel effectué "
                        f"({contact or 'email manquant'} · {typ}) ✍️")
            st.rerun()

    state.consume_notif()


def _plan_card(nom, prix, bullets, badge):
    st.markdown(
        '<div class="outfit-card">'
        f"<h4>{nom} {(badge and f'<span class=chip>{badge}</span>' or '')}</h4>"
        f"<div class='stat-card' style='margin:6px 0; padding:10px 14px'>"
        f"<div class='v'>{prix}</div></div>"
        f"<ul style='font-size:.85rem; padding-left:1.1rem; margin:0'>"
        + "".join(f"<li>{b}</li>" for b in bullets) + "</ul></div>",
        unsafe_allow_html=True,
    )
