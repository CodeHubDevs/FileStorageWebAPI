from ninja import Schema
from uuid import UUID
from typing import Optional
from ninja import Schema
from apps.users.schema import UserOutputSchema
from datetime import date, datetime, time, timedelta

class FolderInputSchema(Schema):
    user_id_id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    modified_by: Optional[str] = None

class FolderOutputSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    user_id: Optional[UserOutputSchema] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    date_created: Optional[date] = None

class Error(Schema):
    message: str