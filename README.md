# DropZone

[![CI](https://github.com/LucasChaudet/dropzone/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/LucasChaudet/dropzone/actions/workflows/ci.yml)

Plateforme de **drops** de sneakers en édition limitée : un drop met en vente un nombre fixe de paires à une heure précise, et les acheteurs commandent jusqu'à épuisement du stock.

> Projet pédagogique (BTS SIO SLAM, cours « Introduction DevOps »). L'application fonctionne ; il lui manque tout ce qui permet de la livrer et de l'exploiter : conteneurs, intégration continue, déploiement, monitoring. C'est l'objet du TP. L'application n'a pas d'authentification.

| Document | Contenu |
|---|---|
| [AUDIT.md](AUDIT.md) | état du dépôt avant le TP : présent, manquant, risqué |
| [CONTRIBUTING.md](CONTRIBUTING.md) | branches, format des commits, cycle d'une pull request, versions |
| [CHANGELOG.md](CHANGELOG.md) | évolutions de chaque version |

## Fonctionnalités

- Liste des drops avec leur statut (`upcoming`, `live`, `sold_out`), un filtre par statut et un compte à rebours avant l'ouverture.
- Page détail d'un drop avec un bouton « Commander ».
- Une commande décrémente le stock, sans jamais vendre deux fois la dernière paire (décrément atomique en base).
- Données de démonstration insérées au premier démarrage.

## Stack

| Partie | Technologies |
|---|---|
| API (`backend/`) | Python 3.12, FastAPI, SQLAlchemy 2, SQLite en local ou PostgreSQL, pytest, Ruff |
| Front (`frontend/`) | React 19, Vite, TypeScript, ESLint, Vitest + Testing Library, Playwright |
| Conteneurs | Docker, Docker Compose, PostgreSQL 16, nginx (image `nginxinc/nginx-unprivileged`) |

## Lancer avec Docker (recommandé)

Seul prérequis : Docker avec Docker Compose (Docker Desktop).

```bash
git clone https://github.com/LucasChaudet/dropzone.git
cd dropzone
cp .env.example .env          # Windows PowerShell : Copy-Item .env.example .env
docker compose up -d --build --wait
```

| Service | Image | Rôle | Adresse |
|---|---|---|---|
| `db` | `postgres:16-alpine` | base de données, données dans le volume `db-data` | interne (`db:5432`) |
| `api` | construite depuis `backend/Dockerfile` | API FastAPI, utilisateur non-root `app` | <http://localhost:8000> |
| `front` | construite depuis `frontend/Dockerfile` | front servi par nginx, `/api/` redirigé vers `api` | <http://localhost:8080> |

- `api` ne démarre que lorsque `db` est `healthy` (sonde `pg_isready`).
- Dans le réseau Compose, l'API joint la base par son nom de service, `db` : `localhost` désignerait le conteneur de l'API lui-même.
- Toutes les variables sont dans `.env.example` ; le vrai `.env` n'est jamais commité.

Commandes utiles :

```bash
docker compose ps                  # état des services (db doit être healthy)
docker compose logs -f api         # logs de l'API
docker compose exec api whoami     # affiche app : l'API ne tourne pas en root
docker compose down                # arrête la stack, les données restent dans le volume
docker compose down -v             # arrête la stack ET supprime les données
```

## Lancer le projet en local (sans Docker)

Prérequis : Git, Python 3.12 ou plus récent, Node.js 22.12 ou plus récent.

**API**, dans un premier terminal :

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate              # Windows : .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Sous Windows (PowerShell), créer l'environnement avec `py -m venv .venv`. Si `Activate.ps1` est bloqué par la politique d'exécution, lancer les outils sans activer le venv : `.venv\Scripts\python.exe -m uvicorn app.main:app --reload`.

Si le port 8000 est déjà utilisé (erreur `WinError 10013` sous Windows), une autre instance de l'API tourne déjà : l'arrêter, ou lancer celle-ci avec `--port 8001`.

- L'API répond sur <http://localhost:8000> ; documentation interactive sur <http://localhost:8000/docs>.
- Par défaut, elle utilise une base SQLite locale (fichier `backend/dropzone.db`, ignoré par Git), créée et remplie au premier démarrage.
- Pour utiliser une base PostgreSQL existante, définir la variable `DATABASE_URL` avant de lancer uvicorn :
  `DATABASE_URL=postgresql+psycopg://utilisateur:motdepasse@localhost:5432/dropzone`.

**Front**, dans un second terminal :

```bash
cd frontend
npm ci
npm run dev
```

Le front est servi sur <http://localhost:5173> ; les appels à `/api` sont redirigés vers l'API sur le port 8000.

## Qualité et tests

```bash
# backend/ (venv activé)
ruff check .              # lint
ruff format --check .     # format
pytest                    # tests + couverture (minimum 85 %)

# frontend/
npm run lint              # ESLint
npm run typecheck         # TypeScript
npm test                  # Vitest
npm run build             # build de production (dossier dist/)
npm run test:e2e          # Playwright : nécessite l'application complète sur http://localhost:8080
```

Les tests Playwright visent l'adresse `http://localhost:8080` (variable `E2E_BASE_URL` pour en viser une autre). Avant le premier lancement : `npx playwright install chromium`. Chaque scénario crée son propre drop par l'API : les tests ne dépendent ni des données de démo, ni les uns des autres.

## Intégration continue

Le workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) tourne sur chaque pull request vers `main` et sur chaque push sur `main`.

| Job | Contenu | Démarre |
|---|---|---|
| Lint | Ruff (lint + format) pour l'API, ESLint et TypeScript pour le front | tout de suite |
| Tests backend | pytest avec couverture (minimum 85 %) | tout de suite, en parallèle |
| Tests frontend | Vitest, puis le build de production | tout de suite, en parallèle |
| E2E | stack Docker Compose + Playwright ; rapport HTML gardé en artefact `playwright-report`, même en cas d'échec | seulement si les trois autres sont verts |

- Les dépendances pip et npm sont mises en **cache** (clé : `requirements-dev.txt` et `package-lock.json`).
- Le jeton du workflow n'a que le droit de **lire** le code (`permissions: contents: read`).
- Les quatre jobs sont des **vérifications obligatoires** de la protection de `main` : une PR rouge ne peut pas être mergée.

Lancer un job sur son poste avec [act](https://nektosact.com/) (Docker requis), par exemple :

```bash
act pull_request -j backend-tests
```

## Déploiement continu

Une version se publie en posant un **tag annoté** `vX.Y.Z` sur `main` (après avoir mis à jour le [CHANGELOG](CHANGELOG.md)) :

```bash
git checkout main
git pull
git tag -a v0.2.0 -m "v0.2.0"
git push origin v0.2.0
```

Le workflow [`.github/workflows/cd.yml`](.github/workflows/cd.yml) publie alors :

| Livrable | Où |
|---|---|
| Image de l'API, tags `0.2.0`, `0.2`, `sha-…` | `ghcr.io/lucaschaudet/dropzone-api` |
| Image du front, mêmes tags | `ghcr.io/lucaschaudet/dropzone-front` |
| Front statique | <https://lucaschaudet.github.io/dropzone/> |
| Release avec notes générées | [Releases](https://github.com/LucasChaudet/dropzone/releases), créée quand images et Pages sont publiées |

- Chaque job n'a que les droits dont il a besoin (`packages: write` pour les images, `pages: write` pour Pages, `contents: write` pour la release) ; ghcr.io est joint avec le jeton `GITHUB_TOKEN` du run, sans mot de passe.
- Le CD ne relance pas les tests : seul `main` est tagué, et la CI y est obligatoire.
- Sur Pages, il n'y a pas de nginx pour rediriger `/api` : le front appelle l'adresse donnée par la variable de dépôt `VITE_API_URL` (*Settings → Secrets and variables → Actions → Variables*), `http://localhost:8000` par défaut. Sans API joignable, la page affiche « L'API est injoignable ».
- Réglages GitHub : *Settings → Pages* : source « GitHub Actions » ; *Settings → Environments → github-pages* : règle de déploiement autorisant les tags `v*` ; packages `dropzone-api` et `dropzone-front` en visibilité publique.

### Lancer une version publiée

[`compose.release.yml`](compose.release.yml) lance la stack à partir des images du registre, sans aucun build. La version est la variable `DROPZONE_VERSION` (dans `.env`, sans le `v`).

```bash
docker compose down                              # arrête la stack de développement (données gardées)
docker compose -f compose.release.yml pull
docker compose -f compose.release.yml up -d --wait
docker compose -f compose.release.yml ps         # colonne IMAGE : …:0.2.0
```

### Retour à la version précédente (rollback)

1. Dans `.env`, remettre l'ancienne version, par exemple `DROPZONE_VERSION=0.2.0` (PowerShell, sans modifier le fichier : `$env:DROPZONE_VERSION="0.2.0"`).
2. Relancer : `docker compose -f compose.release.yml up -d --wait`. Compose remplace les conteneurs `api` et `front` par ceux de l'ancienne image, déjà publiée : rien n'est reconstruit.
3. Vérifier : `docker compose -f compose.release.yml ps` affiche les images `…:0.2.0`, et <http://localhost:8000/health/ready> renvoie la version `0.2.0`.

Le rollback ne revient pas sur les **données** : les commandes passées restent dans la base, et un changement de schéma fait par la nouvelle version n'est pas annulé.

## API

| Requête | Réponse |
|---|---|
| `GET /health` | `200` : le processus répond (liveness) |
| `GET /health/ready` | `200` si la base répond, `503` sinon (readiness) |
| `GET /drops?status=live` | `200` : la liste triée par id, filtre facultatif `upcoming`, `live` ou `sold_out` |
| `GET /drops/{id}` | `200` le drop · `404` |
| `POST /drops` | `201` le drop créé · `422` données invalides |
| `POST /drops/{id}/orders` | `201` la commande · `404` · `409` drop pas encore ouvert ou épuisé |

Un drop : `id`, `product`, `description`, `price_cents` (entier, en centimes), `stock`, `remaining`, `opens_at` (RFC 3339) et `status`, calculé à chaque lecture.

```bash
curl -X POST localhost:8000/drops -H 'Content-Type: application/json' \
  -d '{"product":"Air Max 1","price_cents":18000,"stock":100,"opens_at":"2026-01-01T09:00:00Z"}'
curl -X POST localhost:8000/drops/1/orders
```

## Configuration

La configuration passe par des variables d'environnement (ou un fichier `backend/.env`, jamais commité).

| Variable | Rôle | Défaut |
|---|---|---|
| `DATABASE_URL` | URL SQLAlchemy de la base | `sqlite:///./dropzone.db` |
| `LOG_LEVEL` | niveau des logs | `INFO` |
| `SEED_DEMO_DATA` | insérer les données de démo si la base est vide | `true` |
| `CORS_ORIGINS` | origines autorisées, séparées par des virgules (front servi depuis un autre domaine) | vide |
| `VITE_API_URL` | URL de l'API pour le front, fixée au build | `/api` |
| `API_PROXY_TARGET` | API vers laquelle `npm run dev` redirige `/api` | `http://localhost:8000` |

## Structure du projet

```text
.
├── compose.yml              stack Docker : db, api, front
├── .env.example             variables de la stack (copier en .env)
├── backend/                 API FastAPI
│   ├── app/                 code (routes, services, domaine, modèles)
│   ├── tests/               tests pytest (SQLite en mémoire)
│   ├── Dockerfile           image multi-stage de l'API (utilisateur non-root)
│   ├── pyproject.toml       configuration Ruff et pytest
│   └── requirements*.txt    dépendances épinglées
└── frontend/                application React
    ├── src/                 composants, pages et tests Vitest
    ├── e2e/                 tests Playwright
    ├── Dockerfile           build Node puis nginx non-root sur le port 8080
    ├── nginx.conf           configuration nginx pour servir le front dans un conteneur
    └── playwright.config.ts
```

## Contribuer

- `main` est protégée : pas de push direct, chaque changement passe par une branche et une pull request.
- Branches nommées `<type>/<description>` (ex. `feat/filtre-par-prix`), commits au format **Conventional Commits** (ex. `fix(api): reject orders on sold-out drops`).
- Avant de pousser : lint et tests de la partie modifiée (voir « Qualité et tests »).
- Les versions sont publiées par un tag annoté `vX.Y.Z` sur `main` et décrites dans le [CHANGELOG](CHANGELOG.md).

Le détail est dans [CONTRIBUTING.md](CONTRIBUTING.md).

## Feuille de route

Le détail des consignes est dans la fiche **« TP DropZone »**.

| Partie | Contenu | État |
|---|---|---|
| 1 | Dépôt d'aplomb : audit, README, `main` protégée, Conventional Commits, version `v0.1.0` | fait |
| 2 | Conteneuriser : images Docker de l'API et du front, `compose.yml` avec PostgreSQL, `.env.example` | fait |
| 3 | Intégration continue : workflow GitHub Actions (lint, tests, E2E), tests manquants, badge | fait |
| 4 | Déploiement continu : images sur ghcr.io, front sur GitHub Pages, release à chaque tag | fait |
| 5 | Observer : health checks Docker, logs structurés, métriques `/metrics`, Uptime Kuma | à faire |

## Licence

MIT.
