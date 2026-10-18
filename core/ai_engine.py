# -*- coding: utf-8 -*-
"""Moteur d'IA STYLEMIND.

⚠️ Pour l'instant : moteur EXPLICITE (règles + score de similarité).
   Il est déterministe et explique ses choix. C'est la couche de repli,
   au même endroit qu'un modèle LLM (OpenAI/Azure...) se branchera quand
   la clé API sera configurée. Les points d'intégration sont marqués
   `# [LLM]` dans le code.
"""
import random

from .demo_data import PRODUCTS_BY_ID


def score_style(styles_item, scores) -> float:
    """Jaccard pondéré entre les styles de l'objet et les goûts de l'utilisateur."""
    styles_item = {s.strip() for s in styles_item}
    if not styles_item or not scores:
        return 0.35
    hit = sum(scores.get(s, 0) for s in styles_item)
    denom = sum(scores.values()) or 1
    return round(min(hit / denom + 0.15 * (len(styles_item) / 4), 1.0), 2)


def score_budget(prix, budget) -> float:
    if not prix or not budget:
        return 0.5
    if prix <= budget:
        return 1.0
    ratio = (prix - budget) / max(budget + 1, 1)
    return max(0.0, 1.0 - ratio * 2)


def score_occasion(occ_item, occ_user) -> float:
    if not occ_user:
        return 0.5
    inter = set(occ_item) & set(occ_user)
    return 1.0 if inter else 0.2


def produit_score_meta(prod, profile) -> dict:
    """Score global + sous-scores explicables."""
    s_style = score_style(prod["styles"], profile["styles_scores"])
    s_budget = score_budget(prod["price"], profile["budget"])
    s_occ = score_occasion(prod["occasions"], profile["occasions"])
    s_eco = prod["ethical"] / 5
    n_global = .5 * s_style + .25 * s_budget + .15 * s_occ + .10 * s_eco
    return {
        "global": round(n_global, 2), "style": s_style,
        "budget": s_budget, "occasion": s_occ,
        "ethique": s_eco,
        "match_pct": round(n_global * 100),
    }


def recommandations(profile, n=6) -> list:
    """Tri du catalogue selon le profil : [(prod, meta), ...]"""
    metas = [(prod, produit_score_meta(prod, profile))
             for prod in PRODUCTS_BY_ID.values()]
    metas.sort(key=lambda t: t[1]["global"], reverse=True)
    return metas[:n]


NOMS_TENUE = ["Éclair minimal", "Après-minuit", "Café + Trench",
              "Panache soft", "Corsaire doux", "Longueur Telline",
              "Marco singulier", "Élastique parfait", "Ligne fluide",
              "Coup de chapeau"]


def _pick(pool, filt, exclude):
    ok = [p for p in pool if filt(p) and p["id"] not in exclude]
    return random.choice(ok) if ok else None


def generer_tenues(profile, n=3, occasion=None):
    """Crée n tenues cohérentes avec le profil : même famille de style,
    contraire (haut/bas), chaussures, accessoire. Explication fournie."""
    pool = list(PRODUCTS_BY_ID.values())
    tenues = []
    for i in range(n):
        occ = occasion or (profile["occasions"][0] if profile["occasions"] else "Quotidien")
        scoring = [p for p in pool if occ in p["occasions"]]
        scoring.sort(key=lambda p: produit_score_meta(p, profile)["global"], reverse=True)
        if not scoring:
            scoring = pool[:]
        hero = scoring[0] if i == 0 else random.choice(scoring[:6])

        pieces = [hero]
        exclude = {hero["id"]}

        if hero["category"] != "Robes":
            bas = (_pick(pool, lambda p: p["category"] == "Bas", exclude)
                   or _pick(pool, lambda p: p["category"] == "Hauts", exclude))
            if bas:
                pieces.append(bas); exclude.add(bas["id"])
        veste = _pick(pool, lambda p: p["category"] == "Vestes", exclude)
        if veste and (hero["category"] != "Robes" or random.random() > .5):
            pieces.append(veste); exclude.add(veste["id"])
        chauss = _pick(pool, lambda p: p["category"] == "Chaussures", exclude)
        if chauss:
            pieces.append(chauss); exclude.add(chauss["id"])
        if random.random() > .45:
            acc = _pick(pool, lambda p: p["category"] == "Accessoires", exclude)
            if acc:
                pieces.append(acc); exclude.add(acc["id"])

        prix = sum(p["price"] for p in pieces)
        # petit arbitrage vers le budget : si dépassé, on propose l'alternative fripée
        depasse = prix > profile["budget"] * 1.2
        tenues.append({
            "id": f"T{random.randint(1000, 9999)}i",
            "nom": random.choice(NOMS_TENUE),
            "occasion": occ,
            "pieces": [{"id": p["id"], "name": p["name"], "brand": p["brand"],
                        "price": p["price"], "colors": p["colors"],
                        "category": p["category"],
                        "secondhand": p["secondhand"]} for p in pieces],
            "prix_total": round(prix, 2),
            "depasse_budget": depasse,
            "eco_moyen": round(sum(p["ethical"] for p in pieces) / len(pieces), 1),
            "styles": hero["styles"],
            "pourquoi": expliquer_tenue(pieces, profile, prix, depasse),
        })
    return tenues


def expliquer_tenue(pieces, profile, prix, depasse) -> str:
    hero = pieces[0]
    why = [f"style «{hero['styles'][0]}» aligné avec tes goûts"]
    if not depasse:
        why.append(f"dans ton budget ({prix:.0f} € ≤ {profile['budget']:.0f} €)")
    else:
        why.append(f"au-dessus du budget ({prix:.0f} € vs {profile['budget']:.0f} €) — "
                   "je cherche des alternatives dans le Dream Wardrobe")
    fripees = [p for p in pieces if p["secondhand"]]
    if fripees:
        names = ", ".join(p["name"] for p in fripees[:2])
        why.append(f"pieces fripées possibles ({names})")
    if sum(p["ethical"] for p in pieces) / len(pieces) >= 4:
        why.append("bon score éthique ✓")
    occ = hero["occasions"][0] if hero["occasions"] else "ton quotidien"
    why.append(f"pensé pour ton {occ.lower()}")
    return " · ".join(why)


# ─────────────────────────────────────────────────────────────────────────────
# Dream Wardrobe : alternatives moins chères
# ─────────────────────────────────────────────────────────────────────────────
def alternative_moins_chere(prod):
    """Trouve dans le catalogue DÉMO un article au style proche, moins cher."""
    cands = [p for p in PRODUCTS_BY_ID.values()
             if p["id"] != prod["id"] and p["price"] < prod["price"] * .8]
    best, best_s = None, -1
    for p in cands:
        style_hits = len(set(p["styles"]) & set(prod["styles"]))
        color_close = bool(set(p["colors"]) & set(prod["colors"]))
        s = style_hits + (1 if color_close else 0) - (p["price"] / prod["price"]) * 2
        if s > best_s:
            best, best_s = p, s
    return best


# ─────────────────────────────────────────────────────────────────────────────
# Assistant cadeaux (DÉMO)  [LLM]
# ─────────────────────────────────────────────────────────────────────────────
def cadeaux(budget, styles, relation) -> list:
    """Choix de cadeaux plausibles selon budget, styles et lien."""
    cands = [p for p in PRODUCTS_BY_ID.values() if p["price"] <= budget * 1.1]
    scored = []
    for p in cands:
        s = len(set(p["styles"]) & set(styles))
        if p["price"] <= budget * 0.5:
            s += .5                       # les petits prix font de bons cadeaux
        if relation.lower().startswith(("mère", "maman", "père", "papa", "tante", "oncle")):
            s += 1 if ("romantique" in p["styles"] or "chic parisien" in p["styles"]) else 0
        scored.append((p, s))
    scored.sort(key=lambda t: t[1], reverse=True)
    seen, res = set(), []
    for p, _ in scored:
        if p["category"] in seen:
            continue
        seen.add(p["category"])
        res.append(p)
        if len(res) >= 4:
            break
    return res


# ─────────────────────────────────────────────────────────────────────────────
# Agent conversationnel (règles locales — l'intégration LLM se branchera ici)
# [LLM] Si une clé API est configurée, remplacer la réponse par l'appel API.
# ─────────────────────────────────────────────────────────────────────────────
def reponse_agent(texte, profile, recos) -> str:
    t = (texte or "").lower()
    p = profile
    go2 = list(p["styles_scores"].keys())
    if any(m in t for m in ["bonjour", "salut", "hello", "coucou"]):
        return (f"Bonjour {p['pseudo']} ✨ Ton profil penche « {', '.join(go2[:2]) or '?'} ». "
                "Pose-moi tes questions : une tenue, un cadeau, une alternative "
                "seconde main, une explication sur une reco…")
    if "budget" in t:
        return (f"Ton budget enregistré : **{p['budget']:.0f} €** par pièce en moyenne. "
                "Avec l'option Premium je peux affiner par catégorie (chaussures, manteaux…). "
                "Tu peux le modifier directement dans le quiz.")
    if "cadeau" in t:
        return ("Va dans **Extras → Assistant cadeaux** 🎁 : je te prépare 4 propositions "
                "suivant la personne, son style et ton budget.")
    if "seconde" in t or ("occasion" in t and "main" in t):
        alt = next((r for r in recos if r[0]["secondhand"]), None)
        if alt:
            return (f"La friperie t'ouvre de belles portes : **{alt[0]['name']}** "
                    f"({alt[0]['price']:.0f} €), match de {alt[1]['match_pct']} % "
                    "avec ton style. Réserve-la dans ton Dream Wardrobe !")
        return "Les articles marqués « fripée » se trouvent dans Extras → Seconde main 🙂"
    if "pourquoi" in t and recos:
        r = recos[0]
        return (f"Top reco : **{r[0]['name']}** ({r[0]['price']:.0f} €) affiche "
                f"**{r[1]['match_pct']} %** — style {r[1]['style']*100:.0f} %, "
                f"budget {r[1]['budget']*100:.0f} %, occasion {r[1]['occasion']*100:.0f} %.")
    if any(m in t for m in ["tenue", "look", "habille", "porte", "sors"]):
        tenue = generer_tenues(p, n=1)[0]
        noms = ", ".join(q["name"] for q in tenue["pieces"])
        return (f"Je te propose **{tenue['nom']}** ({tenue['occasion'].lower()}) : {noms}. "
                f"Total ≈ {tenue['prix_total']:.0f} € · éthique {tenue['eco_moyen']}/5. "
                f"Pourquoi : {tenue['pourquoi']}")
    if "ethique" in t or "durable" in t:
        eco = [r for r in recos if r[0]["ethical"] >= 4]
        noms = ", ".join(f"**{r[0]['name']}** ({r[0]['price']:.0f} €)" for r in eco[:3]) or "—"
        return f"Les pièces durables (impact ≥ 4/5) : {noms}. Filtre-le depuis Extras → Mode éthique."
    if "premium" in t or "abonn" in t:
        etat = "actif ✦" if p["premium"] else "inactif (démo)"
        return (f"Tarif Premium : {etat} — analyse de garde-robe complète, alertes promo "
                "illimitées, styliste personnel. Page **Premium & Marques** pour activer.")
    if recos:
        r = recos[0]
        return (f"Je crois que **{r[0]['name']}** (match {r[1]['match_pct']} %, "
                f"{r[0]['price']:.0f} €) ferait de belles choses dans ta garde-robe. "
                "Précise ta demande — tenue, budget, cadeau, seconde main, éthique — "
                "pour que j'affine ✚")
    return "Rafraîchis ton profil dans le quiz, puis reviens me voir 💕"
