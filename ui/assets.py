# -*- coding: utf-8 -*-
"""Chargeur d'illustrations locales (assets/ SVG générés par tools/gen_assets.py).

Toutes les images sont committées avec le code : elles fonctionnent à
l'identique en local et sur Streamlit Cloud (aucune URL externe).
Si un fichier est absent (ancien déploiement…), le composant retombe
gracieusement sur le dégradé déterministe existant.
"""
import base64
from functools import lru_cache
from pathlib import Path

from streamlit import cache_data

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


@lru_cache(maxsize=1)
def _available() -> bool:
    return ASSETS_DIR.exists()


def exists(kind: str, key: str) -> bool:
    return _available() and (ASSETS_DIR / kind / f"{key}.svg").exists()


@cache_data(show_spinner=False)
def data_uri(kind: str, key: str) -> str | None:
    """data:image/svg+xml;base64,… ou None si l'illustration est absente."""
    f = ASSETS_DIR / kind / f"{key}.svg"
    if not f.exists():
        return None
    b64 = base64.b64encode(f.read_bytes()).decode()
    return f"data:image/svg+xml;base64,{b64}"


def bg_deck(kind_key_pairs) -> str:
    """Retourne l'URI de la première illustration locale disponible.

    ⚠️ Streamlit assainit les styles inline des `st.markdown` HTML : les
    `url(data:…)` en CSS sont supprimés. On ne rend donc les images QUE via
    des balises <img> (jamais via background:url), d'où ce « pick » simple.
    """
    for kind, key in kind_key_pairs:
        if not key:
            continue
        uri = data_uri(kind, key)
        if uri:
            return uri
    return ""


# Ancien nom conservé le temps de la migration interne
pick = bg_deck


def img_tag(kind: str, key: str, size: int = 36, radius: int = 12, alt: str = "") -> str:
    """Petite vignette <img> intégrable dans du HTML markdown."""
    uri = data_uri(kind, key)
    if not uri:
        return ""
    return (f'<img src="{uri}" alt="{alt}" style="width:{size}px; height:{size}px;'
            f' border-radius:{radius}px; object-fit:cover; vertical-align:middle;" '
            f'loading="lazy"/>')
