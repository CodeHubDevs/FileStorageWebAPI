from typing import List
from ninja import Router
from apps.folders.models import FolderModel
from .schema import *

router = Router()

class FolderMehodView:
    @router.post('/create-folder', response=FolderOutputSchema)
    def create_folder(request, payload: FolderInputSchema):
        
            folder_data = FolderModel.objects.create(
                user_id_id=payload.user_id_id,
                name=payload.name,
                desc=payload.desc,
                modified_by=payload.modified_by
            )
            return folder_data
        
    @router.get("/get-folder-lists", response=List[FolderOutputSchema])
    def get_folder_lists(request):
        """
        It returns a list of all users in the database
        
        :param request: The request object
        :return: A list of users
        """
        try:
            folder_data=FolderModel.objects.all()
            return folder_data
        except FolderModel.DoesNotExist as e:
            return 200, {"message": "no users found!"}