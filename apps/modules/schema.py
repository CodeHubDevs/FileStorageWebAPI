from ninja import Schema
from uuid import UUID
from typing import Optional
from ninja import Schema
from apps.folders.schema import FolderOutputSchema
from datetime import date, datetime, time, timedelta

class ModuleInputSchema(Schema):
    folder_id_id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    modified_by: Optional[str] = None

class ModuleOutputSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    folder_id: Optional[FolderOutputSchema] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    date_created: Optional[date] = None

class Error(Schema):
    message: str