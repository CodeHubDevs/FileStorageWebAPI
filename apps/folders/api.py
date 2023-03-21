from typing import List
from ninja import Router
from apps.folders.models import FolderModel
from .schema import *

router = Router()

class FolderMehodView:
    @router.post('/create-folder', response=FolderOutputSchema)
    def create_folder(request, payload: FolderInputSchema):
        """
        It creates a folder in the database
        
        :param request: The request object
        :param payload: FolderInputSchema
        :type payload: FolderInputSchema
        :return: The return value is a FolderModel object.
        """
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
        It returns all the data from the FolderModel table.
        
        :param request: The request object
        :return: A list of FolderModel objects.
        """
        try:
            folder_data=FolderModel.objects.all()
            return folder_data
        except FolderModel.DoesNotExist as e:
            return 200, {"message": "no folders found!"}