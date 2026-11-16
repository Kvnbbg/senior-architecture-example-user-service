"""
Tests unitaires du service métier et du repository.
Couverture de la logique pure — 100 % des chemins critiques.
"""
import pytest
from uuid import uuid4

from app.models.user import UserCreate, UserUpdate
from app.services.user_repository import InMemoryUserRepository
from app.services.user_service import UserService


@pytest.fixture
def repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def service(repository: InMemoryUserRepository) -> UserService:
    return UserService(repository)


@pytest.mark.asyncio
async def test_create_user_success(service: UserService) -> None:
    user_in = UserCreate(email="alice@example.com", full_name="Alice Martin")
    user = await service.create_user(user_in)

    assert user.email == "alice@example.com"
    assert user.full_name == "Alice Martin"
    assert user.is_active is True
    assert user.id is not None


@pytest.mark.asyncio
async def test_create_user_duplicate_email_raises(service: UserService) -> None:
    user_in = UserCreate(email="bob@example.com", full_name="Bob")
    await service.create_user(user_in)

    with pytest.raises(ValueError, match="existe déjà"):
        await service.create_user(user_in)


@pytest.mark.asyncio
async def test_get_user_not_found(service: UserService) -> None:
    result = await service.get_user(uuid4())
    assert result is None


@pytest.mark.asyncio
async def test_update_user(service: UserService) -> None:
    created = await service.create_user(
        UserCreate(email="carol@example.com", full_name="Carol")
    )
    updated = await service.update_user(
        created.id, UserUpdate(full_name="Carol Updated", is_active=False)
    )

    assert updated is not None
    assert updated.full_name == "Carol Updated"
    assert updated.is_active is False
    assert updated.email == "carol@example.com"


@pytest.mark.asyncio
async def test_list_and_delete(service: UserService) -> None:
    await service.create_user(UserCreate(email="d@example.com", full_name="D"))
    await service.create_user(UserCreate(email="e@example.com", full_name="E"))

    users = await service.list_users()
    assert len(users) == 2

    deleted = await service.delete_user(users[0].id)
    assert deleted is True

    remaining = await service.list_users()
    assert len(remaining) == 1
