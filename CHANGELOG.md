# Changelog

Toutes les évolutions notables du projet sont consignées dans ce fichier.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le projet respecte le [versionnage sémantique](https://semver.org/lang/fr/).

## [Non publié]

## [0.3.0] - 2026-11-10

### Ajouté

- L'onglet du navigateur affiche le nom du produit sur la page détail d'un drop.

## [0.2.0] - 2026-11-10

### Ajouté

- Image Docker multi-stage de l'API, lancée par un utilisateur non-root sur le port 8000.
- Image Docker du front : build Node puis nginx non-root sur le port 8080.
- `compose.yml` : stack complète (PostgreSQL 16 avec volume et healthcheck, API, front) lancée en une commande.
- `.env.example` avec toutes les variables de la stack.
- Intégration continue GitHub Actions : lint, tests backend, tests frontend, puis E2E Playwright sur la stack Docker ; badge dans le README.
- Tests des commandes côté API, test du composant `DropCard`, scénarios E2E « commander décrémente le stock » et « un drop épuisé désactive le bouton ».
- Déploiement continu sur tag `v*` : images `dropzone-api` et `dropzone-front` publiées sur ghcr.io, front publié sur GitHub Pages, release GitHub avec notes générées.
- `compose.release.yml` : lancement d'une version publiée depuis les images du registre, et procédure de retour à la version précédente.

### Modifié

- `AUDIT.md` suit la grille d'audit du cours (13 points).

## [0.1.0] - 2026-11-09

### Ajouté

- API FastAPI : liste des drops avec filtre par statut, détail d'un drop, création d'un drop, commande avec décrément atomique du stock.
- Endpoints de santé `GET /health` et `GET /health/ready`.
- Front React : liste des drops, compte à rebours avant ouverture, page détail avec bouton « Commander ».
- Données de démonstration insérées au premier démarrage.
- Tests pytest et Vitest, un scénario Playwright, lint Ruff et ESLint.
- Documentation du dépôt : `AUDIT.md`, `CONTRIBUTING.md`, ce `CHANGELOG.md`, modèle de pull request.

[Non publié]: https://github.com/LucasChaudet/dropzone/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/LucasChaudet/dropzone/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/LucasChaudet/dropzone/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/LucasChaudet/dropzone/releases/tag/v0.1.0
