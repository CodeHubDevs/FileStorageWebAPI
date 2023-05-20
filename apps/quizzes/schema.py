from ninja import Schema
from uuid import UUID
from ninja import Schema
from apps.folders.schema import FolderOutputSchema
from datetime import date, datetime, time, timedelta
from typing import List, Dict, Optional

class QuizInputSchema(Schema):
    folder_id_id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    questions: Optional[List[Dict]] = None
    modified_by: Optional[str] = None

class QuizOutputSchema(Schema):
    id: Optional[int] = None
    public_id: Optional[UUID] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    folder_id: Optional[FolderOutputSchema] = None
    questions: Optional[List[Dict]] = None
    type: Optional[str] = None
    date_created: Optional[date] = None

class Error(Schema):
    message: str
