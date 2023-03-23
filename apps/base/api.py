from ninja_extra import NinjaExtraAPI
from apps.authentication.api import router as authentication_router
from apps.users.api import router as users_router
from apps.folders.api import router as folder_router
from apps.modules.api import router as module_router
from apps.files.api import router as file_router
from ninja.security import HttpBearer

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == token:
            return token

api = NinjaExtraAPI(auth=GlobalAuth())
api.add_router('/', authentication_router)
api.add_router('/users', users_router)
api.add_router('/folder', folder_router)
api.add_router('/modules', module_router)
api.add_router('/files', file_router)