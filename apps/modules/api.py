from typing import List
from ninja import Router
from apps.modules.models import ModuleModel
from .schema import *

router = Router()

class ModuleMehodView:
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
            folder_id_id=payload.folder_id,
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