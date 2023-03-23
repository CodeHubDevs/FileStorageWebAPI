from typing import List
from ninja import Router
from apps.files.models import FileModel
from .schema import *
from ninja import File
from ninja.files import UploadedFile

router = Router()

class FileMehodView:
    @router.post('/insert-file', response=FileOutputSchema)
    def insert_file(request, payload: FileInputSchema, file: UploadedFile = File(...)):
        file = request.FILES.get('file')
        file_data = FileModel.objects.create(
            module_id_id=payload.module_id,
            name=payload.name,
            desc=payload.desc,
            file = file,
            modified_by=payload.modified_by
        )
        return file_data
        
    @router.get("/get-file-lists", response=List[FileOutputSchema])
    def get_file_lists(request):
        try:
            file_data=FileModel.objects.all()
            return file_data
        except FileModel.DoesNotExist as e:
            return 500, {"message": "no folders found!"}