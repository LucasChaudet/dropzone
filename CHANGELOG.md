# Changelog

Toutes les évolutions notables du projet sont consignées dans ce fichier.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le projet respecte le [versionnage sémantique](https://semver.org/lang/fr/).

## [Non publié]

## [0.1.0] - 2026-11-09

### Ajouté

- API FastAPI : liste des drops avec filtre par statut, détail d'un drop, création d'un drop, commande avec décrément atomique du stock.
- Endpoints de santé `GET /health` et `GET /health/ready`.
- Front React : liste des drops, compte à rebours avant ouverture, page détail avec bouton « Commander ».
- Données de démonstration insérées au premier démarrage.
- Tests pytest et Vitest, un scénario Playwright, lint Ruff et ESLint.
- Documentation du dépôt : `AUDIT.md`, `CONTRIBUTING.md`, ce `CHANGELOG.md`, modèle de pull request.

[Non publié]: https://github.com/LucasChaudet/dropzone/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/LucasChaudet/dropzone/releases/tag/v0.1.0
