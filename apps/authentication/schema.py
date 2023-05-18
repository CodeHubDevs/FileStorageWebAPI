from ninja import Schema
from typing import Optional
from ninja import Schema
from uuid import UUID

class UserOutputSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    email: Optional[str] = None
    role: Optional[str] = None

class ChangePasswordUserInputSchema(Schema):
    old_password: Optional[str] = None
    new_password: Optional[str] = None
    confirm_password: Optional[str] = None

class AuthSchema(Schema):
    username: str
    password: str

class JWTPairSchema(Schema):
    access: str
    user: Optional[UserOutputSchema] = None

class ForgotPasswordSchema(Schema):
    username: str

class Error(Schema):
    message: str

class Success(Schema):
    message: str