# -*- coding: utf-8 -*-
"""Garde-robe numérique : ajout de vêtements (photos optionnelles,
stockées localement), composition de tenues avec ses propres pièces."""

import base64
import io
import uuid
from pathlib import Path

import streamlit as st
from PIL import Image

from core import state, theme
from core.format import dh0
from ui import assets
from ui.components import tile_html

CATEGORIES = ["Hauts", "Bas", "Vestes", "Robes", "Chaussures", "Accessoires"]
COULEURS = ["crème", "beige", "kaki", "marine", "bordeaux", "lilas",
            "noir", "sauge", "terracotta", "blanc"]
STYLES_GR = ["minimaliste", "chic parisien", "bohème", "romantique", "streetwear",
             "rock", "vintage", "business", "casual", "éthique", "cozy",
             "marinière"]

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "data" / "uploads"


def render():
    st.session_state.setdefault("selection_outfit", [])
    st.session_state.setdefault("up_count", 0)
    theme.hero("Garde-robe numérique 🧺",
               "Ajoute tes pièces (photo optionnelle), compose des tenues avec ce que tu "
               "possèdes déjà. Le styliste IA s'en sert pour ne jamais te suggérer "
               "ce que tu as déjà.")

    _ajout_piece_block()
    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

    if not st.session_state.garde_robe:
        st.info("Ta garde-robe est encore vide. Clique sur **+ Ajouter un vêtement** "
                "au-dessus pour commencer.", icon="🧺")
        return

    st.markdown(f"#### Mes pièces ({len(st.session_state.garde_robe)})")
    _render_pieces()

    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    _outfit_builder()
    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    _mes_tenues()

    state.consume_notif()


# ─────────────────────────────────────────────────────────────────────────────
def _ajout_piece_block():
    exp = st.expander("➕ Ajouter un vêtement", expanded=not st.session_state.garde_robe)
    with exp:
        name = st.text_input("Nom de la pièce", placeholder="ex. Chemise blanche froissée")
        c1, c2 = st.columns(2)
        cat = c1.selectbox("Catégorie", CATEGORIES)
        coupling_color = c2.multiselect("Couleurs", COULEURS, placeholder="choisir…")
        c3, c4 = st.columns(2)
        styles = c3.multiselect("Styles", STYLES_GR[:10], placeholder="choisir…")
        price = c4.number_input("Prix payé (DH)", 0.0, 2000.0, 50.0, step=5.0)
        occ = st.multiselect("Occasions", ["Quotidien", "Travail", "Week-end", "Soirée",
                                           "Événement", "Vacances"], placeholder="choisir…")
        photo = st.file_uploader("Photo (optionnelle)", type=["jpg", "jpeg", "png"],
                                 key=f"photo_{st.session_state.up_count}")

        if st.button("Enregistrer la pièce", type="primary",
                     key="save_piece", use_container_width=False):
            if not name.strip():
                st.warning("Donne un nom à la pièce 🙂")
            else:
                _ajout_piece(name, cat, coupling_color, styles, price, occ, photo)
                state.notif(f"« {name} » ajoutée à ta garde-robe 🧺")
                st.rerun()


def _ajout_piece(name, cat, colors, styles, price, occ, photo):
    item = {
        "id": str(uuid.uuid4())[:8],
        "name": name.strip(),
        "category": cat,
        "colors": colors or ["noir"],
        "styles": styles or ["casual"],
        "price": float(price),
        "occasions": occ or ["Quotidien"],
        "photo": None,
    }
    if photo is not None:
        try:
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            fname = f"{st.session_state.user_id}_{item['id']}.jpg"
            img = Image.open(photo).convert("RGB")
            img.thumbnail((520, 520))
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=82)
            (UPLOAD_DIR / fname).write_bytes(buf.getvalue())
            item["photo"] = fname
        except Exception as e:  # noqa: BLE001 — démo : on tolère l'échec photo
            st.warning(f"Photo non stockée ({e.__class__.__name__}) — la pièce reste aperçu.")
    st.session_state.garde_robe.append(item)
    st.session_state.up_count += 1
    state.persist()


def _piece_tile(item) -> str:
    """Aperçu de la pièce : photo utilisateur → illustration catégorie → dégradé.
    Les images sont TOUJOURS des <img> (l'assainisseur Streamlit supprime
    les url(data:…) en CSS inline)."""
    if item.get("photo") and (UPLOAD_DIR / item["photo"]).exists():
        fpath = UPLOAD_DIR / item["photo"]
        b64 = base64.b64encode(fpath.read_bytes()).decode()
        return (f'<div class="tile" style="height:150px;">'
                f'<img class="tile-img" src="data:image/jpeg;base64,{b64}" '
                f'alt="Photo de {item["name"]}"/></div>')
    img = assets.bg_deck([("categories", item["category"])])
    sw = "".join(f'<div class="sw" style="background:{_couleur_hex(c)}"></div>'
                 for c in item["colors"][:3])
    return tile_html(f"gr_{item['id']}", "", "", '', height=150, img=img,
                     extra_inner=f'<div class="swatches" style="top:auto; bottom:10px;">{sw}</div>')


COULEUR_HEX = {
    "crème": "#F5EBDD", "beige": "#D9C5A0", "kaki": "#9CAF88", "marine": "#2E3A59",
    "bordeaux": "#7C2D3A", "lilas": "#C9B8DB", "noir": "#1A1523", "sauge": "#9CAF88",
    "terracotta": "#C96F4A", "blanc": "#FFFFFF",
}


def _couleur_hex(c: str) -> str:
    return COULEUR_HEX.get(c, "#C9A227")


def _render_pieces():
    sel = st.session_state.selection_outfit
    cols = st.columns(4)
    for i, it in enumerate(list(st.session_state.garde_robe)):
        c = cols[i % 4]
        styles_chips = "".join(
            f'<span class="chip">{s}</span>' for s in it["styles"][:2])
        c.markdown(
            _piece_tile(it)
            + f"<div style='font-size:.86rem; font-weight:600'>{it['name']}</div>"
            f"<div style='font-size:.74rem; opacity:.6'>{it['category']}"
            f" · {dh0(it['price'])}</div>"
            f"<div style='margin:4px 0'>{styles_chips}</div>",
            unsafe_allow_html=True,
        )
        b1, b2 = c.columns(2)
        checked = it["id"] in sel
        if b1.button(("✓ " if checked else "") + "Sélection", key=f"sel_{it['id']}",
                     use_container_width=True):
            if checked:
                sel.remove(it["id"])
            else:
                sel.append(it["id"])
            st.rerun()
        if b2.button("✕", key=f"del_{it['id']}", use_container_width=True):
            st.session_state.garde_robe.remove(it)
            if it["id"] in sel:
                sel.remove(it["id"])
            state.persist()
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
def _outfit_builder():
    sel = st.session_state.selection_outfit
    n = len(sel)
    if n < 2:
        st.caption("Sélectionne **2 pièces ou plus** ci-dessus pour composer une tenue.")
        return
    by_id = {it["id"]: it for it in st.session_state.garde_robe}
    pieces = [by_id[i] for i in sel if i in by_id]
    st.markdown(f"#### Composer une tenue ({n} pièces)")
    st.markdown(theme.chips([p["name"] for p in pieces]), unsafe_allow_html=True)
    nom = st.text_input("Nom de la tenue", placeholder="ex. Céline bureau", key="outfit_name")
    c1, c2, _ = st.columns([1, 1, 2])
    if c1.button("💾 Enregistrer la tenue", type="primary"):
        if not nom.strip():
            st.warning("Un nom pour retrouver la tenue plus tard 🙂")
        else:
            st.session_state.tenues.append({
                "id": str(uuid.uuid4())[:8], "nom": nom.strip(), "occasion": "Mes tenues",
                "pieces": sel[:], "source": "ma garde-robe",
            })
            state.notif(f"Tenue « {nom.strip()} » enregistrée ✧")
            st.session_state["selection_outfit"] = []
            st.rerun()
    if c2.button("Annuler la sélection"):
        st.session_state["selection_outfit"] = []
        st.rerun()


def _mes_tenues():
    if not st.session_state.tenues:
        st.caption("Aucune tenue enregistrée pour l'instant.")
        return
    st.markdown(f"#### Mes tenues ({len(st.session_state.tenues)})")
    from core.demo_data import PRODUCTS_BY_ID

    def nom_piece(pid: str) -> str:
        gr = {it["id"]: it for it in st.session_state.garde_robe}
        if pid in gr:
            return gr[pid]["name"]
        p = PRODUCTS_BY_ID.get(pid)
        return p["name"] if p else f"pièce {pid[:6]}"

    cols = st.columns(3)
    for i, t in enumerate(list(st.session_state.tenues)):
        c = cols[i % 3]
        noms = [nom_piece(pid) for pid in t["pieces"]]
        c.markdown(
            f'<div class="outfit-card"><h4>{t["nom"]}</h4>'
            f"<div style='font-size:.8rem'>"
            f"{(' · '.join(noms)) if noms else '—'}</div></div>",
            unsafe_allow_html=True,
        )
        if c.button("✕ Retirer", key=f"delout_{t['id']}", use_container_width=True):
            st.session_state.tenues.remove(t)
            state.persist()
            st.rerun()
