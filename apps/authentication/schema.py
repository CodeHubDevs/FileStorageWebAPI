from ninja import Schema
from uuid import UUID
from typing import List, Optional
from ninja import Schema, Field
from ninja_schema import ModelSchema, model_validator

from .models import UserModel

class CreateUserInputSchema(Schema):
    public_id: Optional[UUID] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @model_validator('email')
    def validate_unique_username(cls, value_data: str) -> str:
        if UserModel.objects.filter(email__icontains=value_data).exists():
            raise ValueError('Email already exists')
        return value_data
    
class UserOutputSchema(Schema):
    public_id: Optional[UUID] = None
    email: Optional[str] = None
    password: Optional[str] = None

class ChangePasswordUserInputSchema(Schema):
    old_password: Optional[str] = None
    new_password: Optional[str] = None
    confirm_password: Optional[str] = None

class AuthSchema(Schema):
    username: str
    password: str

class JWTPairSchema(Schema):
    refresh: str
    access: str

class Error(Schema):
    message: str

class Success(Schema):
    message: str