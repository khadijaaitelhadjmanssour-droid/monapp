# -*- coding: utf-8 -*-
"""État de la session + persistance JSON (profil, garde-robe, moodboards...).

Le stockage est local (data/users/<id>.json). Aucune donnée n'est envoyée
en ligne : la brique « synchronisation cloud » sera branchée plus tard.
"""
import json
import os
import uuid
from pathlib import Path

import streamlit as st

USERS_DIR = Path(__file__).resolve().parent.parent / "data" / "users"


def default_profile() -> dict:
    return {
        "pseudo": "Invité.style",
        "quiz_done": False,
        "styles_scores": {},          # ex: {"minimaliste": 3, "bohème": 1}
        "budget": 120,                # int : utilisé dans plusieurs st.slider
        "taille": "",
        "occasions": [],
        "lifestyle": "",
        "couleurs_amies": [],
        "couleurs_bannies": [],
        "notes_agent": [],
        "premium": False,
    }


BASE_KEYS = {
    "user_id": lambda: "user_" + uuid.uuid4().hex[:10],
    "profile": default_profile,
    "quiz_step": lambda: 0,
    "quiz_answers": lambda: {},
    "garde_robe": lambda: [],        # vêtements numériques de l'utilisateur
    "tenues": lambda: [],            # outfits construits avec ses vêtements
    "dream_wardrobe": lambda: [],    # envies d'achats futurs
    "looks_sauvegardes": lambda: [], # ids du feed sauvegardés
    "moodboards": lambda: {},        # {id: {"name":..., "items":[itemIds]}}
    "follows": lambda: [],           # ids de créateurs/stylistes suivis
    "chat": lambda: [],
    "notif": lambda: None,
    "gift_result": lambda: None,
    "saved_flash": lambda: {},
}


def init():
    """Initialise la session et charge la persistance locale si elle existe."""
    for k, factory in BASE_KEYS.items():
        if k not in st.session_state:
            st.session_state[k] = factory()

    USERS_DIR.mkdir(parents=True, exist_ok=True)

    if "loaded_once" not in st.session_state:
        st.session_state["loaded_once"] = True
        path = USERS_DIR / f"{st.session_state.user_id}.json"
        if path.exists():  # ne devrait jamais se produire (id aléatoire), au cas où
            load(path)
            # normalisation (compatibilité ancien fichier : budget float → int)
            p = st.session_state.profile
            try:
                p["budget"] = int(float(p.get("budget", 120) or 120))
            except (TypeError, ValueError):
                p["budget"] = 120


def load(path):
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    st.session_state.user_id = payload.get("user_id", st.session_state.user_id)
    for key in ("profile", "garde_robe", "tenues", "dream_wardrobe",
                "looks_sauvegardes", "moodboards", "follows"):
        if key in payload:
            st.session_state[key] = payload[key]


def persist():
    """Sauvegarde l'utilisateur sur disque (appelée après chaque mutation)."""
    USERS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "user_id": st.session_state.user_id,
        "profile": st.session_state.profile,
        "garde_robe": st.session_state.garde_robe,
        "tenues": st.session_state.tenues,
        "dream_wardrobe": st.session_state.dream_wardrobe,
        "looks_sauvegardes": st.session_state.looks_sauvegardes,
        "moodboards": st.session_state.moodboards,
        "follows": st.session_state.follows,
    }
    try:
        (USERS_DIR / f"{st.session_state.user_id}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
    except OSError:
        pass


def notif(msg: str, type_: str = "info"):
    st.session_state["notif"] = (type_, msg)
    persist()


def consume_notif():
    n = st.session_state.get("notif")
    if n:
        st.session_state["notif"] = None
        kind, msg = n
        icon = "ℹ️" if kind == "info" else "✅"
        st.toast(msg, icon=icon)
