from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from apps.files.models import FileModel
from .schema import *
from ninja import File
from ninja.files import UploadedFile

router = Router()

class FileMehodView:
    @router.post('/insert-file', response=FileOutputSchema)
    def insert_file(request, payload: FileInputSchema, file: UploadedFile = File(...)):
        """
        This function creates a new file object in the database with the provided data.
        
        :param request: The HTTP request object that contains information about the incoming request,
        such as headers, cookies, and query parameters
        :param payload: The payload parameter is of type FileInputSchema, which is likely a custom
        schema or data class that defines the expected input data for this function. It probably
        includes fields such as module_id, name, desc, and modified_by, which are used to create a new
        FileModel object
        :type payload: FileInputSchema
        :param file: The `file` parameter is an instance of the `UploadedFile` class, which represents a
        file uploaded by a user through a form submission. It contains information about the file, such
        as its name, content, and content type. In this function, the `file` parameter is obtained from
        the
        :type file: UploadedFile
        :return: an instance of the `FileModel` class that has been created with the provided data.
        """
        file = request.FILES.get('file')
        file_data = FileModel.objects.create(
            module_id_id=payload.module_id_id,
            name=payload.name,
            desc=payload.desc,
            file = file,
            modified_by=payload.modified_by
        )
        return file_data
        
    @router.get("/get-file-lists", response=List[FileOutputSchema])
    def get_file_lists(request):
        """
        This function retrieves all file data from the FileModel database table and returns it, or
        returns an error message if no data is found.
        
        :param request: The function takes a request object as a parameter, but it is not used in the
        function body. It is likely that this parameter was intended to be used for some purpose, but it
        is not clear from the code provided
        :return: If the `FileModel` objects exist, the function will return the `file_data` queryset. If
        the `FileModel` objects do not exist, the function will return a tuple with a status code of 500
        and a dictionary with a "message" key indicating that no folders were found.
        """
        try:
            file_data=FileModel.objects.all()
            return file_data
        except FileModel.DoesNotExist as e:
            return 500, {"message": "no folders found!"}
        
    @router.get("/{public_id}", response ={200: FileOutputSchema, 404: Error})
    def get_specific_file(request, public_id: UUID):
        """
        This function retrieves a specific file based on its public ID and returns either the file or a
        "File not found" message.
        
        :param request: The request object represents the HTTP request that was made by the client
        :param public_id: public_id is a parameter of type UUID (Universally Unique Identifier) that is
        used to identify a specific file in the system. It is passed as an argument to the function
        get_specific_file() in a request object. The function then tries to retrieve the file with the
        given public_id from the database
        :type public_id: UUID
        :return: A tuple is being returned, containing an HTTP status code and either a FileModel object
        or a dictionary with a "message" key and a corresponding error message.
        """
        try:
            file = get_object_or_404(FileModel, public_id=public_id)
            return 200,  file
        except FileModel.DoesNotExist as e:
            return 404, {"message": "File not found!"}
        
    # @router.put("/{public_id}", response=FileOutputSchema)
    # def update_file(request, public_id: UUID, payload: FileInputSchema, file: UploadedFile = File(...)):
    #     """
    #     This function updates a file object with new data provided in the payload.
        
    #     :param request: The request object represents the HTTP request that triggered the view function
    #     :param public_id: The public_id parameter is a UUID (Universally Unique Identifier) that
    #     identifies a specific file in the database
    #     :type public_id: UUID
    #     :param payload: The `payload` parameter is a `FileInputSchema` object that contains the updated
    #     data for the file. It is used to update the attributes of the `FileModel` object with the given
    #     `public_id`. The `dict()` method is called on the `payload` object to convert it to
    #     :type payload: FileInputSchema
    #     :param file: The `file` parameter is an instance of the `UploadedFile` class, which represents a
    #     file uploaded by a user through a form. It contains information about the file, such as its
    #     name, content, and content type. This parameter is used to update the contents of the file in
    #     the database
    #     :type file: UploadedFile
    #     :return: an instance of the `FileModel` class after updating its attributes with the values
    #     provided in the `payload` parameter.
    #     """
    #     file = get_object_or_404(FileModel, public_id=public_id)
    #     for attr, value in payload.dict().items():
    #         print(attr)
    #         setattr(file, attr, value)
    #     file.save()
    #     return file
    
    @router.delete("/{public_id}")
    def delete_file(request, public_id: UUID):
        """
        This function deletes a file with a given public ID and returns a success message or a 404 error
        message if the file is not found.
        
        :param request: The request object represents the HTTP request that was made by the client
        :param public_id: UUID (Universally Unique Identifier) is a 128-bit number used to identify
        information in computer systems. In this case, the public_id is a UUID that is used to identify
        a specific file in the system
        :type public_id: UUID
        :return: If the file with the given public_id exists and is successfully deleted, the function
        returns a dictionary with a "success" key set to True. If the file does not exist, the function
        returns a tuple with a 404 status code and a dictionary with a "message" key set to "File not
        found!".
        """
        try:
            file = get_object_or_404(FileModel, public_id=public_id)
            file.delete()
            return {"success": True}
        except FileModel.DoesNotExist as e:
            return 404, {"message": "File not found!"}