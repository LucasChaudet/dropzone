# Grille d'audit DevOps

**Projet audité :** DropZone (dépôt de départ, commit `1bd9fe7` « Initial commit », audit du 09/11/2026)
**Stack :** API Python 3.12 / FastAPI / SQLAlchemy (SQLite en local, PostgreSQL prévu) · front React 19 / Vite / TypeScript

Notation : ✅ OK · ⚠️ partiel · ❌ absent. La colonne « Constat » indique ce qui a été vu (fichier, commande, lien).

## Git

| Point vérifié | ✅ | ⚠️ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| Dépôt GitHub existant et accessible | ✅ | | | `https://github.com/LucasChaudet/dropzone`, créé depuis le template, branche par défaut `main`. |
| `.gitignore` adapté à la stack (pas de `node_modules`, `vendor`, `.env`…) | ✅ | | | Ignore `.env`, `.venv/`, `__pycache__/`, `*.db`, `node_modules/`, `dist/`, rapports de tests. Complété ensuite pour toutes les variantes `.env.*`. |
| Historique de commits lisible (pas de « fix », « wip », « aaaa ») | | ⚠️ | | Un seul commit, « Initial commit » : lisible, mais aucune convention de message. |
| Branche `main` protégée (pas de push direct) | | | ❌ | `gh api repos/LucasChaudet/dropzone/branches/main/protection` → « Branch not protected ». |

## Build et lancement

| Point vérifié | ✅ | ⚠️ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| L'application démarre en une seule commande documentée | | ⚠️ | | Lancement documenté dans le README, mais en plusieurs commandes, dans deux terminaux (venv + `uvicorn`, puis `npm ci` + `npm run dev`). Aucun Dockerfile ni `compose.yml`. |
| Les dépendances sont listées (`package.json`, `requirements.txt`…) | ✅ | | | `backend/requirements.txt` et `requirements-dev.txt` épinglés, `frontend/package.json` + `package-lock.json`. |
| Aucun chemin absolu codé en dur (ex. `C:\Users\moi\...`) | ✅ | | | Recherche dans le code : aucun chemin absolu ; la base SQLite est relative (`sqlite:///./dropzone.db`). |

## Tests

| Point vérifié | ✅ | ⚠️ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| Des tests existent | ✅ | | | API : 26 tests pytest (couverture 94 %). Front : 9 tests Vitest et 1 scénario Playwright. |
| Les tests s'exécutent en une seule commande | | ⚠️ | | Une commande par partie (`pytest` dans `backend/`, `npm test` dans `frontend/`), chacune dans son environnement ; Playwright exige l'application complète sur le port 8080. Aucune CI. |

## Déploiement

| Point vérifié | ✅ | ⚠️ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| La méthode de déploiement actuelle est connue et documentée | | | ❌ | Aucune : ni image Docker, ni pipeline, ni hébergement. |
| Un environnement de staging existe (différent de la prod) | | | ❌ | Seul le poste du développeur existe. |

## Monitoring

| Point vérifié | ✅ | ⚠️ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| L'URL de production est surveillée | | | ❌ | Pas d'URL de production, aucune sonde. L'API expose déjà `/health` et `/health/ready`. |
| Les logs sont accessibles | | ⚠️ | | Logs texte sur la sortie standard du terminal (`backend/app/logging_config.py`) ; non structurés, non conservés. |

## Bilan

**Total : 5 ✅ · 4 ⚠️ · 4 ❌ (sur 13 points)**

**Mes 3 priorités d'amélioration (les ❌ les plus bloquants) :**

1. **Protéger `main`** : pull request obligatoire, puis CI obligatoire. Sans cela, un code cassé arrive directement sur la branche livrée. *(Fait en partie 1.)*
2. **Rendre le déploiement reproductible** : conteneuriser l'application (partie 2), puis publier chaque version automatiquement (partie 4).
3. **Surveiller l'application** : health checks, logs structurés, métriques et sonde avec alerte (partie 5).

## Présent, manquant, risqué

- **Présent** : une application fonctionnelle et testée, des dépendances épinglées, une configuration par variables d'environnement, des endpoints de santé.
- **Manquant** : conteneurs, `.env.example`, intégration continue, déploiement, versions taguées, supervision, guide de contribution et changelog.
- **Risqué** :
  - `main` non protégée et aucune CI : un commit cassé peut atteindre la branche livrée sans que personne ne s'en aperçoive ;
  - l'application ne tourne que sur un poste configuré à la main : impossible de livrer ou de revenir en arrière ;
  - aucune alerte en cas de panne ;
  - `npm audit` signale 10 vulnérabilités modérées dans les dépendances du front (aucune haute ni critique) ;
  - pas d'authentification (choix du projet pédagogique) : l'API ne doit pas être exposée avec des données réelles.
