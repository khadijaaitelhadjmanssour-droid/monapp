# -*- coding: utf-8 -*-
"""Données de DÉMONSTRATION STYLEMIND.

⚠️ TOUTES les données de ce fichier sont des DONNÉES DE DÉMO :
   produits, créateurs, stylistes, prix, marques, looks de célébrités...
   Rien de ceci n'est de vraies données d'un vrai catalogue e-commerce.
   Elles simulent ce que renverraient des API externes (affiliation,
   catalogue produits, réseaux sociaux) quand les intégrations seront branchées.
"""

# ─────────────────────────────────────────────────────────────────────────────
# Palette démo (codes couleur des produits)
# ─────────────────────────────────────────────────────────────────────────────
CREAM = "#F5EBDD"
NOIR = "#1A1523"
TERRACOTTA = "#C96F4A"
SAUGE = "#9CAF88"
LILAS = "#C9B8DB"
BLANC = "#FFFFFF"
BORDEAUX = "#7C2D3A"
CHAMOIS = "#D9C5A0"
MARINE = "#2E3A59"
OR = "#C9A227"
JEAN = "#5B7A9D"

# ─────────────────────────────────────────────────────────────────────────────
# Catalogue produits (DÉMO)
# ─────────────────────────────────────────────────────────────────────────────
PRODUCTS = [
    {"id": "P01", "name": "Chemise oversize lin", "brand": "Maison Lumen",
     "category": "Hauts", "styles": ["minimaliste", "bohème", "chic parisien"],
     "colors": [CREAM, BLANC], "price": 89.0, "occasions": ["Travail", "Quotidien"],
     "ethical": 4, "secondhand": False},
    {"id": "P02", "name": "Blazer structuré épaulé", "brand": "Atelier Volta",
     "category": "Vestes", "styles": ["chic parisien", "business", "minimaliste"],
     "colors": [NOIR, MARINE], "price": 165.0, "occasions": ["Travail", "Soirée"],
     "ethical": 3, "secondhand": False},
    {"id": "P03", "name": "Jean droit brut", "brand": "Indigo Social Club",
     "category": "Bas", "styles": ["casual", "streetwear", "vintage"],
     "colors": [JEAN], "price": 95.0, "occasions": ["Quotidien", "Week-end"],
     "ethical": 3, "secondhand": False},
    {"id": "P04", "name": "Midi plissée satin", "brand": "Rue Sérénité",
     "category": "Robes", "styles": ["romantique", "chic parisien", "bohème"],
     "colors": [LILAS, CREAM], "price": 120.0, "occasions": ["Soirée", "Événement"],
     "ethical": 2, "secondhand": False},
    {"id": "P05", "name": "Pull maille alpaga", "brand": "Brume Studio",
     "category": "Hauts", "styles": ["minimaliste", "casual", "cozy"],
     "colors": [SAUGE, CREAM], "price": 110.0, "occasions": ["Week-end", "Quotidien"],
     "ethical": 5, "secondhand": False},
    {"id": "P06", "name": "Trench classique", "brand": "Atelier Volta",
     "category": "Vestes", "styles": ["chic parisien", "business", "minimaliste"],
     "colors": [CHAMOIS, NOIR], "price": 240.0, "occasions": ["Quotidien", "Travail"],
     "ethical": 3, "secondhand": False},
    {"id": "P07", "name": "Mocassins cuir cognac", "brand": "Piedra",
     "category": "Chaussures", "styles": ["chic parisien", "vintage", "minimaliste"],
     "colors": [TERRACOTTA, CHAMOIS], "price": 150.0, "occasions": ["Travail", "Quotidien"],
     "ethical": 3, "secondhand": False},
    {"id": "P08", "name": "Sneakers blanches retro", "brand": "Studio 7",
     "category": "Chaussures", "styles": ["casual", "streetwear", "minimaliste"],
     "colors": [BLANC, CREAM], "price": 85.0, "occasions": ["Quotidien", "Week-end"],
     "ethical": 2, "secondhand": False},
    {"id": "P09", "name": "Maxi fleurie coton bio", "brand": "Ondine",
     "category": "Robes", "styles": ["bohème", "romantique", "vintage"],
     "colors": [TERRACOTTA, CHAMOIS], "price": 98.0, "occasions": ["Week-end", "Vacances"],
     "ethical": 5, "secondhand": False},
    {"id": "P10", "name": "Veste moto vintage", "brand": "Fripe Élite",
     "category": "Vestes", "styles": ["streetwear", "rock", "vintage"],
     "colors": [NOIR], "price": 70.0, "occasions": ["Quotidien", "Week-end", "Soirée"],
     "ethical": 4, "secondhand": True},
    {"id": "P11", "name": "Tailleur pantalon souple", "brand": "Maison Lumen",
     "category": "Bas", "styles": ["business", "chic parisien", "minimaliste"],
     "colors": [NOIR, MARINE], "price": 115.0, "occasions": ["Travail"],
     "ethical": 3, "secondhand": False},
    {"id": "P12", "name": "Sac cabas cuir recyclé", "brand": "Ciclo",
     "category": "Accessoires", "styles": ["minimaliste", "chic parisien", "éthique"],
     "colors": [CHAMOIS, NOIR], "price": 130.0, "occasions": ["Travail", "Quotidien"],
     "ethical": 5, "secondhand": False},
    {"id": "P13", "name": "Crop maille côtelée", "brand": "Fripe Élite",
     "category": "Hauts", "styles": ["streetwear", "romantique", "casual"],
     "colors": [LILAS, CREAM], "price": 28.0, "occasions": ["Week-end", "Soirée"],
     "ethical": 3, "secondhand": True},
    {"id": "P14", "name": "Jupe cuir vegan", "brand": "Ondine",
     "category": "Bas", "styles": ["rock", "streetwear", "minimaliste"],
     "colors": [NOIR], "price": 76.0, "occasions": ["Soirée", "Quotidien"],
     "ethical": 5, "secondhand": False},
    {"id": "P15", "name": "Chemisier soie froide", "brand": "Rue Sérénité",
     "category": "Hauts", "styles": ["chic parisien", "romantique", "business"],
     "colors": [LILAS, BLANC], "price": 105.0, "occasions": ["Travail", "Événement"],
     "ethical": 2, "secondhand": False},
    {"id": "P16", "name": "Bottines chelsea cuir", "brand": "Piedra",
     "category": "Chaussures", "styles": ["rock", "minimaliste", "casual"],
     "colors": [NOIR, TERRACOTTA], "price": 175.0, "occasions": ["Quotidien", "Travail", "Soirée"],
     "ethical": 3, "secondhand": False},
    {"id": "P17", "name": "Foulard soie vintage", "brand": "Fripe Élite",
     "category": "Accessoires", "styles": ["vintage", "romantique", "bohème"],
     "colors": [OR, BORDEAUX], "price": 22.0, "occasions": ["Quotidien", "Travail"],
     "ethical": 4, "secondhand": True},
    {"id": "P18", "name": "Hoodie coton bio", "brand": "Urban Roots",
     "category": "Hauts", "styles": ["streetwear", "casual", "cozy"],
     "colors": [SAUGE, CREAM], "price": 65.0, "occasions": ["Week-end", "Quotidien"],
     "ethical": 5, "secondhand": False},
    {"id": "P19", "name": "Robe portefeuille", "brand": "Rue Sérénité",
     "category": "Robes", "styles": ["romantique", "chic parisien", "minimaliste"],
     "colors": [BORDEAUX, NOIR], "price": 132.0, "occasions": ["Travail", "Événement"],
     "ethical": 3, "secondhand": False},
    {"id": "P20", "name": "Short tailleur", "brand": "Maison Lumen",
     "category": "Bas", "styles": ["minimaliste", "business", "chic parisien"],
     "colors": [CREAM, CHAMOIS], "price": 82.0, "occasions": ["Vacances", "Quotidien"],
     "ethical": 3, "secondhand": False},
    {"id": "P21", "name": "Caraco velvet", "brand": "Fripe Élite",
     "category": "Hauts", "styles": ["romantique", "rock", "vintage"],
     "colors": [BORDEAUX, LILAS], "price": 18.0, "occasions": ["Soirée", "Événement"],
     "ethical": 4, "secondhand": True},
    {"id": "P22", "name": "Trench vintage beige", "brand": "Fripe Élite",
     "category": "Vestes", "styles": ["vintage", "chic parisien", "minimaliste"],
     "colors": [CHAMOIS], "price": 55.0, "occasions": ["Quotidien", "Travail"],
     "ethical": 5, "secondhand": True},
    {"id": "P23", "name": "Pull oversize rayé", "brand": "Urban Roots",
     "category": "Hauts", "styles": ["casual", "marinière", "minimaliste"],
     "colors": [CREAM, MARINE], "price": 72.0, "occasions": ["Week-end", "Vacances"],
     "ethical": 4, "secondhand": False},
    {"id": "P24", "name": "Lunettes œil-de-chat", "brand": "Studio 7",
     "category": "Accessoires", "styles": ["vintage", "rock", "chic parisien"],
     "colors": [NOIR], "price": 45.0, "occasions": ["Quotidien", "Vacances"],
     "ethical": 2, "secondhand": False},
]

PRODUCTS_BY_ID = {p["id"]: p for p in PRODUCTS}

# ─────────────────────────────────────────────────────────────────────────────
# Créateurs & stylistes (DÉMO)
# ─────────────────────────────────────────────────────────────────────────────
CREATORS = [
    {"id": "C01", "name": "Lou Marceau", "handle": "@lou.styles", "role": "Styliste",
     "specialty": "Garde-robe capsule minimalist", "followers": 21400,
     "styles": ["minimaliste", "chic parisien", "casual"], "shoppable": True},
    {"id": "C02", "name": "Inès Bakari", "handle": "@ines.moods", "role": "Créatrice",
     "specialty": "Moodboards bohème & vintage", "followers": 8900,
     "styles": ["bohème", "vintage", "romantique"], "shoppable": True},
    {"id": "C03", "name": "Studio 7th Sense", "handle": "@7thsense", "role": "Styliste",
     "specialty": "Streetwear & second main", "followers": 45200,
     "styles": ["streetwear", "rock", "casual"], "shoppable": True},
    {"id": "C04", "name": "Camille Rive", "handle": "@camille.rive", "role": "Créatrice",
     "specialty": "Mode éthique & marques durables", "followers": 12300,
     "styles": ["éthique", "minimaliste", "cozy"], "shoppable": True},
    {"id": "C05", "name": "Théo Nardone", "handle": "@theo.nardone", "role": "Styliste",
     "specialty": "Business & chic parisien", "followers": 17800,
     "styles": ["business", "chic parisien", "minimaliste"], "shoppable": True},
    {"id": "C06", "name": "Yasmin Delay", "handle": "@yasmin.d", "role": "Créatrice",
     "specialty": "Looks de célébrités décryptés", "followers": 30100,
     "styles": ["rock", "romantique", "vintage"], "shoppable": False},
]
CREATORS_BY_ID = {c["id"]: c for c in CREATORS}

# ─────────────────────────────────────────────────────────────────────────────
# Fil visuel (DÉMO) — looks publiés par les créateurs + placements sponsorisés
# ─────────────────────────────────────────────────────────────────────────────
FEED = [
    {"id": "F01", "title": "Tailleur souple + mocassins, bureau chic", "creator": "C05",
     "products": ["P11", "P07", "P12"], "styles": ["chic parisien", "business"],
     "sponsored": False, "size": 1.0},
    {"id": "F02", "title": "Veste moto fripée + jupe cuir vegan", "creator": "C03",
     "products": ["P10", "P14", "P16"], "styles": ["rock", "streetwear"],
     "sponsored": False, "size": 1.35},
    {"id": "F03", "title": "Lin oversize + jean droit, mars tranquille", "creator": "C01",
     "products": ["P01", "P03", "P05"], "styles": ["minimaliste", "casual"],
     "sponsored": False, "size": 1.15},
    {"id": "F04", "title": "Midi plissée lilas, soirée douce", "creator": "C02",
     "products": ["P04", "P16", "P17"], "styles": ["romantique", "bohème"],
     "sponsored": False, "size": 1.25},
    {"id": "F05", "title": "Capsule alpaga : 5 pièces = 15 tenues", "creator": "C01",
     "products": ["P05", "P03", "P08"], "styles": ["minimaliste", "casual"],
     "sponsored": False, "size": 0.9},
    {"id": "F06", "title": "Maison Lumen · collection lin printemps", "creator": "C01",
     "products": ["P01", "P20", "P11"], "styles": ["minimaliste", "chic parisien"],
     "sponsored": True, "size": 1.0},
    {"id": "F07", "title": "Hoodie bio + bottines, street soft", "creator": "C04",
     "products": ["P18", "P16", "P24"], "styles": ["éthique", "streetwear"],
     "sponsored": False, "size": 1.2},
    {"id": "F08", "title": "Maxi fleurie coton bio, vacances mode éthique", "creator": "C04",
     "products": ["P09", "P08", "P12"], "styles": ["éthique", "bohème"],
     "sponsored": False, "size": 1.4},
    {"id": "F09", "title": "Studio 7 · sneakers rétro coton", "creator": "C03",
     "products": ["P08", "P18", "P13"], "styles": ["streetwear", "casual"],
     "sponsored": True, "size": 0.95},
    {"id": "F10", "title": "Marinière rayée + trench vintage fripé", "creator": "C02",
     "products": ["P23", "P22", "P08"], "styles": ["vintage", "casual"],
     "sponsored": False, "size": 1.1},
    {"id": "F11", "title": "Soie froide + jupe short, power look léger", "creator": "C05",
     "products": ["P15", "P20", "P24"], "styles": ["business", "romantique"],
     "sponsored": False, "size": 1.3},
    {"id": "F12", "title": "Velvet bordeaux après minuit", "creator": "C06",
     "products": ["P21", "P14", "P16"], "styles": ["rock", "romantique"],
     "sponsored": False, "size": 1.05},
]
FEED_BY_ID = {f["id"]: f for f in FEED}

# ─────────────────────────────────────────────────────────────────────────────
# Looks de célébrités (DÉMO — noms de personnes réelles à titre d'inspiration)
# ─────────────────────────────────────────────────────────────────────────────
CELEB_LOOKS = [
    {"id": "S01", "celeb": "Une icône décontractée du samedi (avant-première)",
     "desc": "Hoodie oversize + legging cuir + sneakers + lunettes noires",
     "products": ["P18", "P14", "P08", "P24"], "vibe": "streetwear chic", "price_celeb": 940.0},
    {"id": "S02", "celeb": "Rouge tapis d'une soirée (look archive)",
     "desc": "Blazer épaulé sur caraco velvet + bottines chelsea",
     "products": ["P02", "P21", "P16"], "vibe": "rock couture", "price_celeb": 2100.0},
    {"id": "S03", "celeb": "Passage d'aéroport d'une actrice française",
     "desc": "Trench + maille + jeans droit + mocassins + cabas",
     "products": ["P06", "P05", "P03", "P07", "P12"], "vibe": "chic parisien", "price_celeb": 1480.0},
]

# ─────────────────────────────────────────────────────────────────────────────
# Styles du quiz (DÉMO)
# ─────────────────────────────────────────────────────────────────────────────
STYLES = ["minimaliste", "chic parisien", "bohème", "romantique", "streetwear",
          "rock", "vintage", "business", "casual", "éthique"]
