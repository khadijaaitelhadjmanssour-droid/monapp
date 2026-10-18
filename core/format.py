# -*- coding: utf-8 -*-
"""Formatage centralisé : DEVISE (dirham marocain, MAD/DH) et nombres.

Toute l'application LIT ses prix ici. Les valeurs numériques stockées
n'ont pas été converties : elles SONT des dirhams (démo).
Format uniforme : « 1 250,00 DH » (séparateur de milliers = espace,
décimales = virgule, 2 décimales par défaut).
"""


def _fr(nombre: str) -> str:
    """'1,250.00' → '1 250,00' (convention française)."""
    return nombre.replace(",", " ").replace(".", ",")


def dh(valeur, dec: int = 2) -> str:
    """Prix en dirhams : dh(1250) → '1 250,00 DH' ; dh(89) → '89,00 DH'."""
    try:
        v = float(valeur)
    except (TypeError, ValueError):
        v = 0.0
    return f"{_fr(f'{v:,.{dec}f}')} DH"


def dh0(valeur) -> str:
    """Prix rond pour les phrases courtes : dh0(89.4) → '89 DH'."""
    return dh(valeur, dec=0)


def nombre_fr(valeur) -> str:
    """21 400 (séparateur de milliers à la française)."""
    try:
        return _fr(f"{int(valeur):,d}")
    except (TypeError, ValueError):
        return str(valeur)
