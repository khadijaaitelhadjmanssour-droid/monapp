# -*- coding: utf-8 -*-
"""Dream Wardrobe : achats futurs chiffrés, prix cibles, promos simulées,
alternatives moins chères (articles démo)."""

import hashlib
from datetime import date

import streamlit as st

from core import ai_engine, state, theme
from core.demo_data import PRODUCTS_BY_ID
from core.format import dh, dh0
from ui import assets
from ui.components import tile_html


def render():
    theme.hero("Dream Wardrobe ✦",
               "Tes achats futurs, intelligemment : prix cible, watchlist promotions et "
               "alternatives moins chères suggérées par l'agent IA. Les promo sont "
               "calculées sur le catalogue « démo » (badge DÉMO).")

    dw = st.session_state.dream_wardrobe
    if not dw:
        st.info("Aucune envie enregistrée. Ajoute des pièces depuis le fil, le styliste "
                "ou les recommandations (bouton « ✦ Dream Wardrobe »).", icon="✨")
        return

    # ── En-tête chiffré ─────────────────────────────────────────────────────
    total, cible, eco_count = _totals(dw)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        theme.stat_card(f"{len(dw)}", "pièces rêvées")
    with c2:
        theme.stat_card(dh(total), "coût total (prix démo, DH)")
    with c3:
        theme.stat_card(dh(cible), "prix cible visé")
    with c4:
        theme.stat_card(f"{eco_count}/{len(dw)}", "pièces éthiques ✓")

    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

    # ── Lignes de watchlist ────────────────────────────────────────────────
    st.caption("La veille est une simulation locale (promo recalculée chaque jour à partir "
               "du catalogue démo). Une API prix/promo se branchera au même endroit.")
    for it in list(dw):
        prod = PRODUCTS_BY_ID.get(it["id"])
        if prod is None:  # pièce venue d'une source de démo plus ancienne
            continue
        _dream_row(it, prod)

    # ── Vidange à double confirmation (pas de suppression accidentelle) ───
    if st.session_state.get("dw_clear_confirm"):
        cw1, cw2, gold = st.columns([1.2, 1.2, 2.6])
        gold.markdown("<span class='demo-chip'>DÉMO</span> Les envies démo se "
                      "régénèrent depuis le fil ou le styliste.",
                      unsafe_allow_html=True)
        if cw1.button("✅ Oui, tout vider", key="dw_clear_yes", type="primary",
                      use_container_width=True):
            st.session_state.dream_wardrobe = []
            st.session_state["dw_clear_confirm"] = False
            state.persist()
            st.rerun()
        if cw2.button("↩️ Annuler", key="dw_clear_no", use_container_width=True):
            st.session_state["dw_clear_confirm"] = False
            st.rerun()
        st.warning("Tu vas supprimer toutes tes envies — cette action est définitive "
                   "dans cette session.", icon="🗑️")
    elif st.button("🗑️ Vider le Dream Wardrobe"):
        st.session_state["dw_clear_confirm"] = True
        st.rerun()

    state.consume_notif()


def _totals(dw):
    total = sum(it["price"] for it in dw)
    cible = sum(it["target_price"] for it in dw)
    eco = sum(1 for it in dw if PRODUCTS_BY_ID[it["id"]]["ethical"] >= 4)
    return total, cible, eco


def _reduction_du_jour(pid: str) -> int:
    """Promo déterministe sur « aujourd'hui » (0–25 %) — DÉMO, aucune vraie API."""
    seed = f"{pid}{date.today().isoformat()}"
    return int(hashlib.md5(seed.encode()).hexdigest(), 16) % 26


def _dream_row(it, prod):
    red = _reduction_du_jour(it["id"])
    alt = ai_engine.alternative_moins_chere(prod)
    c1, c2, c3, c4 = st.columns([1.05, 1.15, 1.25, .9])

    with c1:
        img = assets.bg_deck([("products", it["id"])])
        st.markdown(tile_html(f"dw_{it['id']}", "", "", "", height=120, img=img),
                    unsafe_allow_html=True)
        if red >= 10:
            st.markdown(f"<span class='chip chip-second'>🔥 PROMO démo −{red} %"
                        f"</span>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"**{it['name']}**")
        st.caption(f"{it['brand']} · étiquette {dh(it['price'])}")
        tp = st.number_input("Prix cible (DH)", 0, int(it["price"]), key=f"tp_{it['id']}",
                             value=int(it["target_price"]))
        if tp != it["target_price"]:
            it["target_price"] = float(tp)
            state.persist()
        if st.button("✕ Retirer de mes envies", key=f"dr_{it['id']}", use_container_width=True):
            st.session_state.dream_wardrobe.remove(it)
            state.persist()
            st.rerun()

    with c3:
        prix_auj = it["price"] * (1 - red / 100)
        ok_achat = (prix_auj <= it["target_price"] or red >= 15)
        st.markdown("État de la veille (démo)")
        if prix_auj <= it["target_price"]:
            st.success(f"Signal ! Prix du jour : **{dh0(prix_auj)}** — sous ton prix cible "
                       f"({dh0(it['target_price'])})." +
                       (" 🔔 Alerte active." if it.get("alerte") else ""))
        elif red >= 15:
            st.warning(f"Bonne promo du jour (−{red} %) : **{dh0(prix_auj)}**. "
                       f"Encore au-dessus de ta cible ({dh0(it['target_price'])}) — "
                       "l'agent continue de guetter.")
        else:
            st.info(f"Prix au jour le jour (démo) : **{dh0(prix_auj)}** vs cible "
                    f"{dh0(it['target_price'])}. On continue de veiller 👀")
        if ok_achat and not it.get("alerte"):
            if st.button("🔔 Créer l'alerte (démo)", key=f"al_{it['id']}"):
                it["alerte"] = True
                state.notif(f"Alerte promo active sur {it['name']} (démo)")
                st.rerun()

    with c4:
        if alt:
            st.markdown("<span class='chip'>alternative IA</span>", unsafe_allow_html=True)
            st.markdown(tile_html(f"alt_{alt['id']}", "", "", "", height=64,
                                  img=assets.bg_deck([("products", alt["id"])])),
                        unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-size:.8rem'>{alt['name']}<br>"
                f"<b>{dh(alt['price'])}</b> "
                f"<span style='opacity:.6'>(−{dh0(it['price'] - alt['price'])})</span></div>",
                unsafe_allow_html=True,
            )
            if st.button(f"✦ Rêver {alt['name'][:14]}…", key=f"alt_{it['id']}",
                         use_container_width=True):
                st.session_state.dream_wardrobe.append({
                    "id": alt["id"], "name": alt["name"], "brand": alt["brand"],
                    "price": alt["price"], "target_price": round(alt["price"] * .7, 2),
                    "colors": alt["colors"], "year": "—",
                })
                state.notif(f"{alt['name']} ajoutée au Dream Wardrobe (moitié moins chère !)")
                st.rerun()
