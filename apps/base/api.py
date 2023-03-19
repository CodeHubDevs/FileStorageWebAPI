from ninja_extra import NinjaExtraAPI
from apps.authentication.api import router as authentication_router

api = NinjaExtraAPI()
api.add_router('/', authentication_router)