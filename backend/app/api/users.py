"""
Endpoints API — couche transport fine.
Toute la logique métier est déléguée au UserService.
"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import User, UserCreate, UserUpdate
from app.services.user_repository import InMemoryUserRepository, UserRepository
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repository() -> UserRepository:
    # En production : injecter un repository PostgreSQL
    return InMemoryUserRepository()


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repo)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    try:
        return await service.create_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return user


@router.get("/", response_model=list[User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    service: Annotated[UserService, Depends(get_user_service)],
) -> list[User]:
    return await service.list_users(skip, limit)


@router.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    user = await service.update_user(user_id, user_in)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
