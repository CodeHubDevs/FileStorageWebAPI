from typing import List
from ninja import Router
from apps.authentication.models import UserModel
from .schema import CreateUserInputSchema, UserOutputSchema, Success, Error
from django.contrib.auth.hashers import make_password

router = Router()

class UsersMethodView:
    @router.post('/create-user', response={200: Success, 500: Error})
    def create_user(request, payload: CreateUserInputSchema):
        """
        It creates a user with the given email and password
        
        :param request: The request object
        :param payload: CreateUserInputSchema
        :type payload: CreateUserInputSchema
        :return: A tuple of two values.
        """
        try:
            UserModel.objects.create(
                email=payload.email,
                password=make_password(payload.password),
            )
            return 200, {"message": "successfully created account."}
        except:
            return 500, {"message": "error on creating user!"}
        
    @router.get("/", response=List[UserOutputSchema])
    def get_user_list(request):
        """
        It returns a list of all users in the database
        
        :param request: The request object
        :return: A list of users
        """
        try:
            users=UserModel.objects.all()
            return users
        except UserModel.DoesNotExist as e:
            return 200, {"message": "no users found!"}