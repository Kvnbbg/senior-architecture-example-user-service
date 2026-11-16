"""
Repository pattern pour l'accès aux données.
Séparation claire des responsabilités : le service métier ne connaît pas
l'implémentation de stockage.
"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.models.user import User, UserCreate, UserInDB, UserUpdate


class UserRepository(ABC):
    """Contrat abstrait du repository — permet de mocker facilement en tests."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[UserInDB]:
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        ...

    @abstractmethod
    async def create(self, user_in: UserCreate) -> UserInDB:
        ...

    @abstractmethod
    async def update(self, user_id: UUID, user_in: UserUpdate) -> Optional[UserInDB]:
        ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[UserInDB]:
        ...


class InMemoryUserRepository(UserRepository):
    """Implémentation en mémoire pour démonstration et tests isolés.
    En production, remplacer par une implémentation PostgreSQL (SQLAlchemy/asyncpg).
    """

    def __init__(self) -> None:
        self._users: dict[UUID, UserInDB] = {}

    async def get_by_id(self, user_id: UUID) -> Optional[UserInDB]:
        return self._users.get(user_id)

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        return next((u for u in self._users.values() if u.email == email), None)

    async def create(self, user_in: UserCreate) -> UserInDB:
        user = UserInDB(**user_in.model_dump())
        self._users[user.id] = user
        return user

    async def update(self, user_id: UUID, user_in: UserUpdate) -> Optional[UserInDB]:
        existing = self._users.get(user_id)
        if not existing:
            return None
        update_data = user_in.model_dump(exclude_unset=True)
        updated = existing.model_copy(update=update_data)
        self._users[user_id] = updated
        return updated

    async def delete(self, user_id: UUID) -> bool:
        return self._users.pop(user_id, None) is not None

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[UserInDB]:
        users = list(self._users.values())
        return users[skip : skip + limit]
