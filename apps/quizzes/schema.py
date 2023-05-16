from ninja import Schema
from uuid import UUID
from typing import Optional
from ninja import Schema
from apps.folders.schema import FolderOutputSchema
from datetime import date, datetime, time, timedelta

class QuizzesInputSchema(Schema):
    folder_id_id: Optional[int] = None
    question: Optional[str] = None
    desc: Optional[str] = None
    modified_by: Optional[str] = None

class QuizzesOutputSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    folder_id: Optional[FolderOutputSchema] = None
    question: Optional[str] = None
    desc: Optional[str] = None
    type: Optional[str] = None
    date_created: Optional[date] = None

class ChoicesInputSchema(Schema):
    question_id_id: Optional[int] = None
    answer: Optional[str] = None
    desc: Optional[str] = None
    modified_by: Optional[str] = None

class ChoicesOutputSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    question_id: Optional[QuizzesOutputSchema] = None
    answer: Optional[str] = None
    desc: Optional[str] = None
    type: Optional[str] = None
    date_created: Optional[date] = None

class Error(Schema):
    message: str