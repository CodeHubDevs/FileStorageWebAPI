from ninja import Schema
from uuid import UUID
from typing import Optional
from ninja import Schema
from apps.folders.schema import FolderOutputSchema
from datetime import date, datetime, time, timedelta
from typing import List

class ChoiceInputSchema(Schema):
    choice: Optional[str] = None
    modified_by: Optional[str] = None

class ChoiceOutputSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    choice: Optional[str] = None
    type: Optional[str] = None
    date_created: Optional[date] = None

########################################

class QuestionInputSchema(Schema):
    question: Optional[str] = None
    choices: Optional[List[int]] = None
    modified_by: Optional[str] = None

class QuestionOutputSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    question: Optional[str] = None
    choices: Optional[List[ChoiceOutputSchema]] = None
    type: Optional[str] = None
    date_created: Optional[date] = None

########################################

class QuizInputSchema(Schema):
    folder_id_id: Optional[int]= None
    questions: Optional[List[int]] = None
    modified_by: Optional[str] = None

class QuizOutputSchema(Schema):
    id : Optional[int] = None
    public_id: Optional[UUID] = None
    folder_id: Optional[FolderOutputSchema] = None
    questions: Optional[List[QuestionOutputSchema]] = None
    type: Optional[str] = None
    date_created: Optional[date] = None

class Error(Schema):
    message: str