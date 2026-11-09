# Contribuer à DropZone

## Workflow : GitHub Flow

- `main` est toujours dans un état livrable. Elle est **protégée** : aucun push direct, tout changement passe par une pull request.
- Chaque changement part d'une **branche** créée depuis `main` à jour, et revient dans `main` par une **pull request**.
- Une branche = un sujet. Elle est supprimée après le merge.

## Nommage des branches

`<type>/<description-courte-en-kebab-case>`, avec le même `type` que les commits :

| Exemple | Usage |
|---|---|
| `feat/filtre-par-prix` | nouvelle fonctionnalité |
| `fix/stock-negatif` | correction de bug |
| `docs/readme-lancement` | documentation |
| `chore/docker-compose` | outillage, configuration, conteneurs |
| `ci/workflow-tests` | intégration ou déploiement continu |
| `test/commandes-api` | ajout ou correction de tests |

## Format des commits : Conventional Commits

```text
<type>(<portée facultative>): <description à l'impératif, en minuscules, sans point final>
```

| Type | Quand | Effet sur la version |
|---|---|---|
| `feat` | nouvelle fonctionnalité visible | **mineure** (0.1.0 → 0.2.0) |
| `fix` | correction de bug | **patch** (0.1.0 → 0.1.1) |
| `docs` | documentation seule | aucun |
| `test` | tests seuls | aucun |
| `refactor` | réécriture sans changement de comportement | aucun |
| `ci` | workflows GitHub Actions | aucun |
| `chore` | outillage, dépendances, configuration | aucun |

Un changement incompatible (ex. une route d'API supprimée) se signale par `!` après le type (`feat(api)!: ...`) ou par un pied de commit `BREAKING CHANGE:` ; il fait monter la version **majeure** (1.0.0 → 2.0.0).

Exemples :

```text
feat(front): add price filter on drop list
fix(api): reject orders on sold-out drops
docs: describe local setup on Windows
```

## Cycle d'une pull request

1. Mettre `main` à jour : `git checkout main` puis `git pull`.
2. Créer la branche : `git checkout -b feat/ma-fonction`.
3. Développer, avec des commits conventionnels.
4. Vérifier en local avant de pousser :
   - API (`backend/`, venv activé) : `ruff check .`, `ruff format --check .`, `pytest` ;
   - front (`frontend/`) : `npm run lint`, `npm run typecheck`, `npm test`.
5. Pousser la branche : `git push -u origin feat/ma-fonction`.
6. Ouvrir la pull request vers `main` et remplir le modèle (quoi, pourquoi, comment tester).
7. Attendre que les vérifications soient vertes (la CI sera obligatoire à partir de la partie 3), puis merger.
8. Mettre à jour `CHANGELOG.md` dans la PR si le changement est visible pour l'utilisateur.

## Versions et tags

- Numérotation **semver** : `MAJEUR.MINEUR.PATCH`.
- Une version est publiée par un **tag annoté** sur `main` : `git tag -a v0.2.0 -m "v0.2.0"` puis `git push origin v0.2.0`.
- Le `CHANGELOG.md` suit le format *Keep a Changelog* : les changements s'accumulent dans « Non publié », puis passent sous le numéro de version au moment du tag.
