from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from apps.modules.models import ModuleModel
from .schema import *

router = Router()

class ModuleMethodView:
    @router.post('/create-module', response=ModuleOutputSchema)
    def create_module(request, payload: ModuleInputSchema):
        """
        It creates a module in the database
        
        :param request: The request object
        :param payload: ModuleInputSchema
        :type payload: ModuleInputSchema
        :return: The module_data is being returned.
        """
        module_data = ModuleModel.objects.create(
            folder_id_id=payload.folder_id_id,
            name=payload.name,
            desc=payload.desc,
            modified_by=payload.modified_by
        )
        return module_data
        
    @router.get("/get-module-lists", response=List[ModuleOutputSchema])
    def get_module_lists(request):
        """
        It returns all the modules in the database.
        
        :param request: The request object
        :return: A list of ModuleModel objects.
        """
        try:
            folder_data=ModuleModel.objects.all()
            return folder_data
        except ModuleModel.DoesNotExist as e:
            return 200, {"message": "no modules found!"}
        
    @router.get("/{public_id}", response ={200: ModuleOutputSchema, 404: Error})
    def get_specific_module(request, public_id: UUID):
        """
        This function retrieves a specific module based on its public ID and returns either the module
        or a "Module not found" message.
        
        :param request: The HTTP request object that contains information about the incoming request,
        such as headers, query parameters, and request body
        :param public_id: public_id is a parameter of type UUID (Universally Unique Identifier) used to
        identify a specific module in the system. It is a unique identifier assigned to each module and
        is used to retrieve the module from the database
        :type public_id: UUID
        :return: A tuple is being returned, containing an HTTP status code and either the requested
        module object or a dictionary with an error message if the module is not found.
        """
        try:
            module = get_object_or_404(ModuleModel, public_id=public_id)
            return 200,  module
        except ModuleModel.DoesNotExist as e:
            return 404, {"message": "Module not found!"}
        
    @router.put("/{public_id}", response={200: ModuleOutputSchema, 404: Error})
    def update_module(request, public_id: UUID, payload: ModuleInputSchema):
        """
        This function updates a module object with the given payload data and returns the updated module
        object or a "Module not found" message.
        
        :param request: The request object contains metadata about the HTTP request that triggered this
        function, such as headers, query parameters, and the request body
        :param public_id: public_id is a parameter of type UUID that represents the unique identifier of
        a ModuleModel object. It is used to retrieve the specific module that needs to be updated
        :type public_id: UUID
        :param payload: The `payload` parameter is a `ModuleInputSchema` object, which is likely a
        Pydantic model representing the data that is being updated for a `ModuleModel` instance. It
        contains the updated values for the attributes of the `ModuleModel` instance
        :type payload: ModuleInputSchema
        :return: A tuple containing the HTTP status code and either the updated ModuleModel object or a
        dictionary with a "message" key if the ModuleModel does not exist.
        """
        try:
            module = get_object_or_404(ModuleModel, public_id=public_id)
            for attr, value in payload.dict().items():
                print(attr)
                setattr(module, attr, value)
            module.save()
            return 200, module
        except ModuleModel.DoesNotExist as e:
            return 404, {"message": "Module not found!"}
        

    @router.delete("/{public_id}")
    def delete_modules(request, public_id: UUID):
        """
        This function deletes a module file with a given public ID and returns a success message or a
        404 error message if the file is not found.
        
        :param request: The request object represents the HTTP request that was made by the client to
        the server
        :param public_id: UUID (Universally Unique Identifier) is a 128-bit number used to identify
        information in computer systems. In this case, public_id is a UUID that is used to identify a
        specific module in the ModuleModel database
        :type public_id: UUID
        :return: If the file with the given public_id exists and is successfully deleted, the function
        returns a dictionary with a "success" key set to True. If the file does not exist, the function
        returns a tuple with a 404 status code and a dictionary with a "message" key set to "File not
        found!".
        """
        try:
            file = get_object_or_404(ModuleModel, public_id=public_id)
            file.delete()
            return {"success": True}
        except ModuleModel.DoesNotExist as e:
            return 404, {"message": "File not found!"}