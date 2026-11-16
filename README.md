# Senior Architecture Example

Exemple de brique fonctionnelle isolée conçue avec une rigueur senior :

- **Backend** : FastAPI + Pydantic v2, modèles étanches (`extra="forbid"`, frozen), Repository Pattern, Service Layer.
- **Frontend** : React + TypeScript strict, branded types, composant présentationnel pur, Tailwind CSS.
- **Tests** : Pytest (backend) et Jest + React Testing Library (frontend).

## Objectif

Démontrer comment remplacer du code « vibe coding » jetable par une architecture maintenable, testable et typée de façon stricte.

## Structure

```
backend/
  app/
    models/          # Modèles Pydantic étanches
    services/        # Logique métier + Repository
    api/             # Couche transport FastAPI
  tests/             # Tests unitaires Pytest

frontend/
  src/
    types/           # Types TS stricts + branded
    components/      # Composants React purs
    __tests__/       # Tests Jest
```

## Lancer les tests backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## Lancer les tests frontend

```bash
cd frontend
npm install
npm test
```

## Pull Request type

Voir le fichier `PULL_REQUEST.md` pour un exemple de description senior.
