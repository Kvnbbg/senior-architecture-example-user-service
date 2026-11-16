# Pull Request Senior — Exemple

## Contexte

Cette PR introduit une brique fonctionnelle isolée « User Service + UserProfileCard » conçue pour servir de référence architecturale.

Objectif : remplacer les patterns « vibe coding » (types `any`, logique métier dans les composants ou les routes, absence de tests) par une structure senior :

- Séparation claire des responsabilités (Domain → Service → Repository → API / UI)
- Modèles de données étanches (Pydantic `extra="forbid"` + frozen, TypeScript readonly + branded types)
- Typage strict de bout en bout
- Tests unitaires systématiques sur la logique métier

## Choix techniques

### Backend (Python / FastAPI)

- **Pydantic v2** avec `model_config = ConfigDict(extra="forbid", frozen=True)` pour garantir l'étanchéité et l'immutabilité.
- **Repository Pattern** abstrait + implémentation in-memory (facilement remplaçable par PostgreSQL).
- **Service Layer** contenant les règles métier (unicité email, etc.).
- Injection de dépendances FastAPI pour découpler les couches.
- Aucune logique métier dans les routes.

### Frontend (TypeScript / React / Tailwind)

- Branded type `UserId` pour éviter les confusions d'identifiants.
- Composant présentationnel pur : reçoit un `User` typé, n'effectue aucun fetching.
- Props en `readonly`.
- Tailwind pour le styling (pas de CSS-in-JS).

## Preuves d'exécution des tests

### Backend

```
$ pytest -v
tests/test_user_service.py::test_create_user_success PASSED
tests/test_user_service.py::test_create_user_duplicate_email_raises PASSED
tests/test_user_service.py::test_get_user_not_found PASSED
tests/test_user_service.py::test_update_user PASSED
tests/test_user_service.py::test_list_and_delete PASSED

============================== 5 passed in 0.12s ==============================
```

### Frontend

```
$ npm test -- --watchAll=false
PASS src/__tests__/UserProfileCard.test.tsx
  UserProfileCard
    ✓ affiche le nom et l'email de l'utilisateur
    ✓ affiche le badge Actif
    ✓ passe en mode édition et appelle onUpdate

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

## Checklist senior

- [x] Typage strict (pas de `any`, modèles étanches)
- [x] Séparation des responsabilités
- [x] Tests unitaires sur la logique pure
- [x] 100 % de succès avant merge
- [x] Documentation de la PR
- [x] Aucune dépendance non justifiée

## Hash de commit (exemple)

`a1b2c3d4e5f6...` (à remplacer par le vrai hash après push)
