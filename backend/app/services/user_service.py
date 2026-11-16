"""
Service métier — logique pure, indépendante du transport HTTP et du stockage.
"""
from typing import Optional
from uuid import UUID

from app.models.user import User, UserCreate, UserUpdate
from app.services.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    async def get_user(self, user_id: UUID) -> Optional[User]:
        user = await self._repo.get_by_id(user_id)
        return User.model_validate(user) if user else None

    async def create_user(self, user_in: UserCreate) -> User:
        # Règle métier : email unique
        existing = await self._repo.get_by_email(user_in.email)
        if existing:
            raise ValueError(f"Un utilisateur avec l'email {user_in.email} existe déjà")
        created = await self._repo.create(user_in)
        return User.model_validate(created)

    async def update_user(self, user_id: UUID, user_in: UserUpdate) -> Optional[User]:
        updated = await self._repo.update(user_id, user_in)
        return User.model_validate(updated) if updated else None

    async def delete_user(self, user_id: UUID) -> bool:
        return await self._repo.delete(user_id)

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        users = await self._repo.list_all(skip, limit)
        return [User.model_validate(u) for u in users]
