from typing import List
from ninja import Router
from apps.folders.models import FolderModel
from .schema import *
from django.shortcuts import get_object_or_404

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
        
    @router.get("/{public_id}", response ={200: FolderOutputSchema, 404: Error})
    def get_specific_folder(request, public_id: UUID):
        """
        This function retrieves a specific folder by its public ID and returns either the folder or a
        "Folder not found" message.
        
        :param request: The request object represents the HTTP request that was made by the client
        :param public_id: UUID
        :type public_id: UUID
        :return: A tuple containing an HTTP status code and either the requested folder object or a
        dictionary with an error message if the folder does not exist.
        """
        try:
            folder = get_object_or_404(FolderModel, public_id=public_id)
            return 200,  folder
        except FolderModel.DoesNotExist as e:
            return 404, {"message": "Folder not found!"}
        
    @router.put("/{public_id}", response={200: FolderOutputSchema, 404: Error})
    def update_folder(request, public_id: UUID, payload: FolderInputSchema):
        """
        This function updates a folder object with the given payload data and returns the updated folder
        or a 404 error message if the folder is not found.
        
        :param request: The request object contains metadata about the current HTTP request, such as
        headers, query parameters, and the request body
        :param public_id: UUID - This is a unique identifier for the folder that is being updated. It is
        used to retrieve the folder from the database
        :type public_id: UUID
        :param payload: The `payload` parameter is an instance of the `FolderInputSchema` class, which
        is expected to be a dictionary-like object containing the updated attributes and values for a
        `FolderModel` instance. The `dict()` method is called on the `payload` object to convert it to a
        standard Python
        :type payload: FolderInputSchema
        :return: A tuple containing an HTTP status code and either the updated folder object or a
        dictionary with an error message.
        """
        try:
            folder = get_object_or_404(FolderModel, public_id=public_id)
            for attr, value in payload.dict().items():
                print(attr)
                setattr(folder, attr, value)
            folder.save()
            return 200, folder
        except FolderModel.DoesNotExist as e:
            return 404, {"message": "Folder not found!"}
        
    @router.delete("/{public_id}")
    def delete_folder(request, public_id: UUID):
        """
        This function deletes a folder with a given public ID and returns a success message or a 404
        error message if the folder does not exist.
        
        :param request: The request object represents the HTTP request that was made by the client
        :param public_id: UUID
        :type public_id: UUID
        :return: If the file with the given public_id exists and is successfully deleted, the function
        returns a dictionary with a "success" key set to True. If the file does not exist, the function
        returns a tuple with a 404 status code and a dictionary with a "message" key set to "File not
        found!".
        """
        try:
            file = get_object_or_404(FolderModel, public_id=public_id)
            file.delete()
            return {"success": True}
        except FolderModel.DoesNotExist as e:
            return 404, {"message": "File not found!"}