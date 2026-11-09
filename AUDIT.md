# Audit DevOps du dépôt DropZone

Audit réalisé le 09/11/2026 sur le dépôt de départ (commit `1bd9fe7`, « Initial commit »), avant toute modification.

Notes possibles : **OK** · **Partiel** · **Absent**

## Grille d'audit

### Git

| Critère | Note | Constat |
|---|:-:|---|
| Dépôt GitHub existant et accessible | OK | Dépôt `LucasChaudet/dropzone`, créé depuis le template, branche par défaut `main`. |
| `.gitignore` adapté à la stack | OK | Couvre `.env`, `.venv/`, `__pycache__/`, `*.db`, `node_modules/`, `dist/`, les rapports de tests et de couverture. Seules les variantes `.env.*` (ex. `.env.local`) n'étaient pas couvertes : ajoutées. |
| Historique de commits lisible | Partiel | Un seul commit (« Initial commit ») ; aucune convention de message. |
| Branche `main` protégée | Absent | L'API GitHub répond « Branch not protected » : un push direct sur `main` est possible. |
| Guide de contribution, changelog, modèle de PR | Absent | Ni `CONTRIBUTING.md`, ni `CHANGELOG.md`, ni `.github/pull_request_template.md`. |
| Versions taguées | Absent | La version `0.1.0` figure dans `pyproject.toml`, `package.json` et la réponse de `/health/ready`, mais aucun tag Git n'existe. |

### Build & Run

| Critère | Note | Constat |
|---|:-:|---|
| Démarrage documenté | OK | Le README décrit le lancement de l'API (venv + uvicorn) et du front (`npm ci`, `npm run dev`). Vérifié : l'API répond sur le port 8000, le front sur le port 5173 affiche les drops. |
| Dépendances listées et épinglées | OK | `requirements.txt` / `requirements-dev.txt` épinglés (`==`), `package-lock.json` versionné, `.npmrc` en `save-exact`. |
| Version des outils déclarée | OK | `requires-python = ">=3.12"`, `engines.node >= 22.12`, `.nvmrc`. |
| Démarrage en une commande | Absent | Deux terminaux et deux environnements (Python, Node) sont nécessaires. Aucun Dockerfile ni `compose.yml`. |
| Configuration par variables d'environnement | Partiel | Variables documentées dans le README, mais pas de fichier `.env.example`. |

### Tests et qualité

| Critère | Note | Constat |
|---|:-:|---|
| Des tests existent | Partiel | API : 26 tests pytest, couverture 94 % (minimum 85 % exigé). Front : 9 tests Vitest, 1 scénario Playwright. Manquent : les tests des commandes côté API, le test du composant `DropCard`, les scénarios E2E de commande. |
| Lint et format | OK | Ruff (API), ESLint et TypeScript (front) configurés et sans erreur. |
| Les tests s'exécutent automatiquement | Absent | Aucune intégration continue (pas de dossier `.github/workflows/`). |
| Tests E2E exécutables | Partiel | Playwright vise `http://localhost:8080`, une adresse qui n'existe pas tant que l'application n'est pas conteneurisée. |

### Déploiement

| Critère | Note | Constat |
|---|:-:|---|
| Méthode de déploiement connue | Absent | Ni image Docker, ni pipeline, ni hébergement. |
| Publication de versions | Absent | Ni release GitHub, ni image publiée sur un registre. |
| Retour à la version précédente | Absent | Aucune procédure. |

### Monitoring

| Critère | Note | Constat |
|---|:-:|---|
| Endpoints de santé | OK | `GET /health` (liveness) et `GET /health/ready` (readiness, `503` si la base ne répond pas). |
| Logs exploitables | Partiel | Logs texte sur la sortie standard, avec durée des requêtes ; pas de format structuré (JSON). |
| Métriques | Absent | Pas d'endpoint `/metrics`. |
| Supervision et alertes | Absent | Aucune sonde, aucune notification. |

## Bilan

| OK | Partiel | Absent |
|:-:|:-:|:-:|
| 7 | 5 | 10 |

## Ce qui est risqué

1. **`main` n'est pas protégée et rien ne vérifie le code** : un commit cassé peut être poussé directement sur `main` sans que personne ne s'en aperçoive.
2. **Aucune livraison reproductible** : l'application ne tourne que sur un poste configuré à la main ; impossible de livrer ni de revenir à une version précédente.
3. **Aucune supervision** : une panne de la base ou de l'API ne serait signalée par personne.
4. **Dépendances** : `npm audit` signale 10 vulnérabilités de gravité modérée dans les dépendances du front (aucune haute ni critique).
5. **Pas d'authentification** (choix assumé et documenté du projet pédagogique) : l'API ne doit pas être exposée publiquement avec des données réelles.

## Plan d'action

| Partie | Ce qui corrige l'audit |
|---|---|
| 1 | `AUDIT.md`, README, `CONTRIBUTING.md`, `CHANGELOG.md`, modèle de PR, protection de `main`, tag `v0.1.0` |
| 2 | Dockerfiles, `.dockerignore`, `compose.yml`, `.env.example` |
| 3 | Workflow CI (lint, tests, E2E), tests manquants, CI obligatoire sur `main` |
| 4 | Workflow CD : images sur ghcr.io, front sur GitHub Pages, release, procédure de rollback |
| 5 | Health checks Docker, logs JSON, `/metrics`, Uptime Kuma avec alerte |
