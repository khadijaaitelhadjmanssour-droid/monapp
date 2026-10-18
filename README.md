# STYLEMIND ✦

Application de **mode propulsée par l'IA**, développée avec **Streamlit**.
Elle combine une communauté de mode façon Pinterest, un styliste personnel IA et
un shopping intelligent — et non un simple site e-commerce.

> ⚠️ **Résumé des données de démo** : tous les produits, créateurs, stylistes,
> prix, promos, looks de célébrités et chiffres d'abonnement visibles dans
> l'app sont **fabriqués pour la démonstration**. Ils simulent ce que
> renverront les vraies sources (API catalogue, réseaux de marque, LLM
> hébergé) une fois les intégrations branchées. Ces points sont toujours
> signalés dans l'interface par un badge **DÉMO**.

## Lancer l'application

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Dossier de rendu `mon_app` (Desktop)

Le projet est livré dans `C:\Users\pc\Desktop\mon_app` (lien d'annuaire NTFS
« junction » vers le dossier du même projet) :

- **Double-clic** sur `lancer_stylemind.bat` → démarre Streamlit et ouvre le navigateur ;
- **PowerShell** :
  ```powershell
  cd C:\Users\pc\Desktop\mon_app
  & "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m streamlit run app.py
  ```
- **CMD** :
  ```cmd
  cd /d "%USERPROFILE%\Desktop\mon_app" && "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m streamlit run app.py
  ```

Aucun fichier déplacé : `C:\Users\pc\Desktop\mon_app` et
`C:\Users\pc\Desktop\Monapp` désignent le même contenu.

Si `python`/`pip` ne sont pas dans le PATH (cas typique Windows), ajoutez
`%LOCALAPPDATA%\Programs\Python\Python312` puis `...\Python312\Scripts` au
PATH, ou appelez l'interpréteur en chemin absolu :

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m streamlit run app.py
```

## Fonctionnalités (ce qui tourne, ce qui est simulé)

- **Monnaie** : tous les prix de l'app (produits, tenues, célébrités,
  abonnements, cadeaux) sont affichés en **dirhams (DH)** via une fonction
  unique `core/format.dh()` — ex. `1 250,00 DH`. Les valeurs numériques
  du catalogue démo sont inchangées.
- **Illustrations** : `assets/` contient 61 SVG générés par
  `tools/gen_assets.py` (une illustration unique par produit, look, célébrité,
  créateur, style et catégorie). Ils sont committés avec le code et marchent
  donc identiquement en local et sur Streamlit Cloud, sans URL externe et
  sans photo inventée de vraie personne. Si un fichier manque, la tuile
  retombe sur son dégradé déterministe.

| Page | Fonctionnalités | État |
|---|---|---|
| **Le fil** | feed masonry filtrable (styles, occasion, sponsorisés), recherche texte, épingle, suivre des créateurs | contenu : données de démo |
| **Styliste IA** | tenues du jour générées (vignettes + détail DH), matching produit avec explication (style/budget/occasion/éthique), chat d'agent, déverrouillage Premium | IA = moteur de règles local *explicite*, chat = règles |
| **Profil & Style** | quiz 5 étapes — sélecteur de styles illustré en boutons (max 4), couleurs, budget (DH), occasions, mode de vie — portrait IA | IA = scoring local, prêt pour LLM |
| **Garde-robe** | ajout de pièces (photos resize localement via Pillow, repli illustration de catégorie), tenues à vos propres vêtements | persistance JSON locale reliée (`init()` reprend le dernier profil) |
| **Dream Wardrobe** | prix cible (DH), veille promo « du jour » (simulation), alternatives IA moins chères, vidange à double confirmation | prix simulés par hash daté |
| **Communauté** | créateurs/stylistes à suivre (avatars illustrés), moodboards avec illustrations, épings (y compris adaptations célébrités) | profils de démo |
| **Extras** | mode éthique (filtres impact), friperie, looks de célébrités + adaptation budget (enregistrable → Mes épings), assistant cadeaux | tout sur le catalogue DÉMO |
| **Premium & Offres** | plans en DH (gratuit / 9,99 / 24,99), modèle économique, formulaire partenaires | aucun paiement réel |

## Architecture (évolutive)

```
app.py                 # navigation + sidebar (routage léger)
core/
  state.py             # session + persistance JSON (data/users/<id>.json)
  theme.py             # design system (CSS, chips, hero, stats, tuiles)
  demo_data.py         # 100 % simulés : catalogue, créateurs, feed, célébrités
  format.py            # devise centralisée : prix en dirhams (DH)
  ai_engine.py         # moteur IA explicite : scoring, tenues, cadeaux, chat
views/                 # écrans de l'app (nommé volontairement pas « pages » :
  fil.py, quiz.py, styliste_ia.py, garde_robe.py, dream.py,   # Streamlit
  communaute.py, extras.py, premium.py                        # auto-page)
ui/
  components.py        # tuiles Pinterest-like, cartes, boutons d'action
  assets.py            # chargeur d'illustrations locales (cache + repli)
assets/                # 61 illustrations SVG committées (voir gen_assets)
tools/gen_assets.py    # régénération des illustrations
.streamlit/config.toml # thème clair bord pink/violet
data/                  # uploads + persistance utilisateur (créés à l'exécution)
```

### Où brancher les vraies APIs / un LLM

- `core/ai_engine.py` — moteur local ; les points `# [LLM]` marquent
  exactement où appeler un modèle (OpenAI, Anthropic, Azure…). L'interface
  n'a pas besoin de changer : renvoyer une chaîne depuis `reponse_agent()`
  ou `generer_tenues()` suffit.
- `core/demo_data.py` — remplacer les listes `PRODUCTS`, `FEED`, `CREATORS`,
  `CELEB_LOOKS` par des appels API d'affiliation/catalogue, tout le reste
  (scoring, tuiles, boutons Dream Wardrobe) continue de fonctionner.
- `core/state.py` — `persist()` sauvegarde localement en JSON ; à remplacer
  par un vrai backend (auth, cloud) plus tard.
- Promos du Dream Wardrobe (`pages/dream.py`) — la veille est simulée par un
  hash du jour ; branchez votre API prix/promo à la même place.

### Choix techniques

- **Streamlit** : itération rapide, widget chat natif, déploiement immédiat.
- **Moteur explicite** avant LLM : le même produit tourne sans clé API, et
  l'IA « explique » ses recommandations (style ×, budget ×, occasion ×,
  éthique ×) — une bonne base d'intégration pour un LLM afterwards.
- **Persistance JSON** par utilisateur : aucune base de données requise
  pour la démonstration ; le schéma passe tel quel vers SQLite/Postgres.

## Nettoyage de la démo

Un bouton **« ↺ Réinitialiser la démo »** en bas de la sidebar repart d'un
profil vierge ; le rafraîchissement de la page reprend le dernier profil
enregistré. Pour tout effacer : supprimer `data/users/` et `data/uploads/`.
Sur Streamlit Cloud le disque est éphémère : chaque session redémarre à vide,
ce qui correspond au principe « données de démo ».
