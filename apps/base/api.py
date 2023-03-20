from ninja_extra import NinjaExtraAPI
from apps.authentication.api import router as authentication_router
from apps.users.api import router as users_router
from ninja.security import HttpBearer

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == token:
            return token

api = NinjaExtraAPI(auth=GlobalAuth())
api.add_router('/', authentication_router)
api.add_router('/users', users_router)