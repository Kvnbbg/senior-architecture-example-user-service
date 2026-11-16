"""
Point d'entrée FastAPI — configuration minimale et propre.
"""
from fastapi import FastAPI

from app.api.users import router as users_router

app = FastAPI(
    title="Senior Architecture Example — User Service",
    description="Exemple de brique API avec typage strict, modèles étanches et séparation des responsabilités.",
    version="1.0.0",
)

app.include_router(users_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
