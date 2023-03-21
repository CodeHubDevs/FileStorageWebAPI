from ninja import Schema
from uuid import UUID
from typing import Optional
from ninja import Schema
from apps.users.schema import UserOutputSchema

class FolderInputSchema(Schema):
    user_id_id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    modified_by: Optional[str] = None

class FolderOutputSchema(Schema):
    public_id: Optional[UUID] = None
    user_id: Optional[UserOutputSchema] = None
    name: Optional[str] = None
    desc: Optional[str] = None

class Error(Schema):
    message: str

class Success(Schema):
    message: str