from ninja import Schema
from uuid import UUID
from typing import Optional
from ninja import Schema
from apps.modules.schema import ModuleOutputSchema
from datetime import date, datetime, time, timedelta

class FileInputSchema(Schema):
    module_id_id: Optional[int] = None
    name: Optional[str] = None
    file: Optional[str]= None
    desc: Optional[str] = None
    modified_by: Optional[str] = None

class FileOutputSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    module_id: Optional[ModuleOutputSchema] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    file: Optional[str]= None
    date_created: Optional[date] = None

class CommentInputSchema(Schema):
    comment: Optional[str] = None
    desc: Optional[str] = None
    modified_by: Optional[str] = None

class CommentOutputSchema(Schema):
    id: Optional[int] = None
    public_id: Optional[UUID] = None
    file_id: Optional[FileOutputSchema] = None
    comment: Optional[str] = None
    desc: Optional[str] = None
    date_created: Optional[date] = None

class Error(Schema):
    message: str