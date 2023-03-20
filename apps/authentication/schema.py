from ninja import Schema
from typing import Optional
from ninja import Schema

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