"""
Modèles de domaine étanches pour l'entité User.
Utilisation de Pydantic v2 avec ConfigDict pour interdire les champs extras
et garantir l'étanchéité des données.
"""
from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Modèle de base partagé."""
    model_config = ConfigDict(
        frozen=True,  # Immutabilité
        extra="forbid",  # Refuse les champs inconnus
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    """Modèle pour la création — pas d'ID ni timestamps."""
    pass


class UserUpdate(BaseModel):
    """Modèle pour la mise à jour partielle — tous les champs optionnels."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None


class User(UserBase):
    """Modèle de lecture complet — étanche et immuable."""
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        from_attributes=True,
    )


class UserInDB(User):
    """Modèle interne (peut contenir des champs sensibles à l'avenir)."""
    pass
