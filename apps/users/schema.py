from ninja import Schema
from uuid import UUID
from typing import List, Optional
from ninja import Schema, Field
from ninja_schema import ModelSchema, model_validator
from apps.authentication.models import UserModel
from datetime import date, datetime, time, timedelta

class CreateUserInputSchema(Schema):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

    @model_validator('email')
    def validate_unique_username(cls, value_data: str) -> str:
        if UserModel.objects.filter(email__icontains=value_data).exists():
            raise ValueError('Email already exists')
        return value_data
    
class CreateAdminInputSchema(Schema):
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
    role: Optional[str] = None

class Error(Schema):
    message: str

class Success(Schema):
    message: str

class UploadProfileInputPictureSchema(Schema):
    user_id: Optional[int] = None
    profile_picture: Optional[str] = None
    desc: Optional[str] = None
    modified_by: Optional[str] = None

class UploadProfileOutputPictureSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    user_id: Optional[UserOutputSchema] = None
    desc: Optional[str] = None
    profile_picture: Optional[str] = None
    date_created: Optional[date] = None
