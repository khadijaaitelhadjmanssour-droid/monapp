# -*- coding: utf-8 -*-
"""Récupère de VRAIES photos de mode (Unsplash — licence gratuite, photos
réelles de photographes, aucune image générée) et les enregistre en LOCAL
dans assets/photos/<id>.jpg.

⇒ Chaque fichier est associé à un IDENTIFIANT UNIQUE (F01…F12 = looks du
   fil, P01…P24 = pièces du catalogue). Aucune association par position de
   liste : le tableau PHOTO_SOURCES choisit chaque photo en fonction du
   titre, des pièces, du style et de l'occasion du look correspondant.
⇒ Les visuels retenus ont été VÉRIFIÉS à l'œil (correspondance
   description ↔ contenu de la photo). Certains produits n'ont pas de
   photo : l'app retombe alors sur l'illustration SVG adaptée à SA
   catégorie (voir ui/assets.py) — jamais sur une image sans rapport.
⇒ Les images sont committées avec le code : elles fonctionnent à
   l'identique en local et sur Streamlit Cloud, sans URL externe.
⇒ Licence Unsplash (https://unsplash.com/license) : usage commercial et
   non-commercial autorisé, attribution non obligatoire mais appréciée.
   Photographies réelles illustrant des looks de DÉMO ; elles ne
   prétendent jamais représenter les créateurs fictifs de l'app.
"""
import sys
from pathlib import Path

BASE = "https://images.unsplash.com/"
QS = "?fm=jpg&q=80&w=900&fit=crop"
OUT = Path(__file__).resolve().parent.parent / "assets" / "photos"

# id (look / produit) → photo Unsplash. Mappage 1-à-1, jamais par position.
PHOTO_SOURCES = {
    # ── Looks du fil ──────────────────────────────────────────────────────
    # F01 Tailleur souple + mocassins, bureau chic → chemise rayée +
    #      tailleur beige, ambiance bureau (tenue professionnellement chic)
    "F01": "photo-1620012253295-c15cc3e65df4",
    # F02 Veste moto fripée + jupe cuir vegan → veste moto cuir zippée
    "F02": "photo-1551028719-00167b16eac5",
    # F03 Lin oversize + jean droit, mars tranquille → haut clair +
    #      jean droit, éditorial calme
    "F03": "photo-1519235106638-30cc49b5dbc5",
    # F04 Midi plissée lilas, soirée douce → robe midi plissée rose/lilas
    "F04": "photo-1581044777550-4cfa60707c03",
    # F05 Capsule alpaga : 5 pièces = 15 tenues → flat lay capsule
    #      (pull + jean + sneakers), esprit minimaliste cosy
    "F05": "photo-1620799140408-edc6dcb6d633",
    # F06 Maison Lumen · collection lin printemps → portant de vêtements
    #      beige/lin (ambiance collection boutique)
    "F06": "photo-1445205170230-053b83016050",
    # F07 Hoodie bio + bottines, street soft → hoodie porté, street soft
    "F07": "photo-1556821840-3a63f95609a7",
    # F08 Maxi fleurie coton bio, vacances mode éthique → robe maxi
    #      fleurie en bord de mer
    "F08": "photo-1496747611176-843222e1e57c",
    # F09 Studio 7 · sneakers rétro coton → sneaker en gros plan
    "F09": "photo-1549298916-b41d501d3772",
    # F10 Marinière rayée + trench vintage fripé → rayons de friperie
    #      vintage (esprit « fripé » du look)
    "F10": "photo-1520006403909-838d6b92c22e",
    # F11 Soie froide + jupe short, power look léger → blazer femme,
    #      power look léger en bureau vitré
    "F11": "photo-1573496359142-b8d87734a5a2",
    # F12 Velvet bordeaux après minuit → cuir noir + lunettes, tenue
    #      rock de nuit sur toit
    "F12": "photo-1520975954732-35dd22299614",
    # ── Pièces du catalogue (vues sur le fil et les pages de détail) ─────
    "P01": "photo-1596755094514-f87e34085b2c",  # Chemise oversize lin
    "P03": "photo-1542272604-787c3835535d",     # Jean droit brut
    "P04": "photo-1539008835657-9e8e9680c956",  # Midi plissée satin
    "P07": "photo-1593030761757-71fae45fa0e7",  # Mocassins cuir cognac
    "P08": "photo-1595950653106-6c9ebd614d3a",  # Sneakers blanches rétro
    "P11": "photo-1598033129183-c4f50c736f10",  # Tailleur pantalon souple
    "P12": "photo-1584917865442-de89df76afd3",  # Sac cabas cuir
    "P24": "photo-1572635196237-14b3f281503f",  # Lunettes noires
}
# NB : P02, P05, P06, P09, P10, P13…P23 n'ont pas de photo satisfaisante →
# l'app affiche leur illustration SVG de catégorie (comportement voulu).


def fetch_all() -> list:
    import urllib.request

    OUT.mkdir(parents=True, exist_ok=True)
    ok, bad = [], []
    for key, pid in PHOTO_SOURCES.items():
        dest = OUT / f"{key}.jpg"
        url = BASE + pid + QS
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
        except Exception as exc:  # noqa: BLE001 — rapport explicite sinon
            print(f"ECHEC {key}: {exc}")
            bad.append(key)
            continue
        if data[:2] != b"\xff\xd8":
            print(f"ECHEC {key}: réponse non-JPEG ({data[:16]!r})")
            bad.append(key)
            continue
        dest.write_bytes(data)
        print(f"OK    {key}: {dest.name} ({len(data)//1024} Ko)")
        ok.append(key)
    print(f"\nRésultat : {len(ok)} images OK, {len(bad)} échecs -> {bad or 'aucun'}")
    return bad


if __name__ == "__main__":
    sys.exit(1 if fetch_all() else 0)
