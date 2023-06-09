from typing import List
from ninja import Router
from apps.authentication.models import UserModel
from .schema import *
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from uuid import UUID
from .models import *
from ninja.files import UploadedFile
from ninja import File

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
                role=payload.role
            )
            return 200, {"message": "successfully created account."}
        except:
            return 500, {"message": "error on creating user!"}
        
    @router.post('/create-admin', response={200: Success, 500: Error}, auth=None)
    def create_admin(request, payload: CreateAdminInputSchema):
        """
        This function creates an admin user with the given email, password, and role, and returns a
        success message or an error message.
        
        :param request: The request object contains information about the incoming HTTP request, such as
        the HTTP method, headers, and body
        :param payload: The payload parameter is an instance of the CreateAdminInputSchema class, which
        contains the input data for creating a new admin user. This input schema likely includes fields
        such as email and password
        :type payload: CreateAdminInputSchema
        :return: A tuple is being returned, containing an integer and a dictionary. The integer
        represents the HTTP status code, and the dictionary contains a message indicating whether the
        operation was successful or not.
        """
        try:
            UserModel.objects.create(
                email=payload.email,
                password=make_password(payload.password),
                role='ADMIN'
            )
            return 200, {"message": "successfully created admin account."}
        except:
            return 500, {"message": "error on creating admin user!"}
        
    @router.get("/admin", response=List[UserOutputSchema])
    def get_admin_list(request):
        """
        This function returns a list of all users with the role "ADMIN" or a message if no such users
        are found.
        
        :param request: The request object is not used in the given code snippet. It is likely that this
        function is a part of a Django view and the request object is passed as an argument to the view
        function
        :return: If the UserModel objects with role "ADMIN" are found, they will be returned. If no
        UserModel objects with role "ADMIN" are found, a dictionary with a message "no admin users
        found!" will be returned along with a status code of 200.
        """
        try:
            users=UserModel.objects.all().filter(role="ADMIN")
            return users
        except UserModel.DoesNotExist as e:
            return 200, {"message": "no admin users found!"}
        
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
        
    @router.post('/upload-picture', response=UploadProfileOutputPictureSchema)
    def upload_picture(request, payload: UploadProfileInputPictureSchema, profile_picture: UploadedFile = File(...)):
        profile_picture = request.FILES.get('profile_picture')
        profile_pict_data = ProfilePictureModel.objects.create(
            user_id_id=payload.user_id,
            desc=payload.desc,
            profile_picture = profile_picture,
            modified_by=payload.modified_by
        )
        return profile_pict_data
    
    @router.get("profile-picture-lists/", response ={200: List[UploadProfileOutputPictureSchema], 404: Error})
    def get_profile_picture_lists(request):
        """
        This function retrieves all profile pictures from the ProfilePictureModel and returns them with
        a success status code, or returns a message with a 404 status code if no profile pictures are
        found.
        
        :param request: The request parameter is an object that represents the HTTP request made by the
        client to the server. It contains information such as the HTTP method used, the URL requested,
        any query parameters, headers, and the request body
        :return: A tuple is being returned, containing an HTTP status code and either a queryset of
        ProfilePictureModel objects or a dictionary with a "message" key if no ProfilePictureModel
        objects are found.
        """
        try:
            profile_pict = ProfilePictureModel.objects.all()
            return 200,  profile_pict
        except ProfilePictureModel.DoesNotExist as e:
            return 404, {"message": "No profile picture found!"}
    

    @router.get("profile-picture/{user_id}", response ={200: List[UploadProfileOutputPictureSchema], 404: Error})
    def get_specific_profile_picture(request, user_id: int):
        """
        This function retrieves a specific profile picture for a given user ID and returns a 200 status
        code with the picture if it exists, or a 404 status code with an error message if it does not.
        
        :param request: The request object contains information about the current HTTP request, such as
        the HTTP method, headers, and body
        :param user_id: An integer representing the ID of the user whose profile picture is being
        requested
        :type user_id: int
        :return: A tuple is being returned, containing an HTTP status code and either a
        ProfilePictureModel object or a dictionary with a "message" key and value.
        """
        try:
            profile_pict = ProfilePictureModel.objects.all().filter(user_id=user_id)
            return 200,  profile_pict
        except ProfilePictureModel.DoesNotExist as e:
            return 404, {"message": "No profile picture found!"}
           
        
    @router.delete("/{public_id}")
    def delete_user(request, public_id: UUID):
        """
        This function deletes a user with a given public ID and returns a success message or a 404 error
        message if the user is not found.
        
        :param request: The request object represents the HTTP request that was made by the client
        :param public_id: UUID
        :type public_id: UUID
        :return: If the user with the given public_id exists and is successfully deleted, the function
        returns a dictionary with the key "success" set to True. If the user does not exist, the
        function returns a tuple with the HTTP status code 404 and a dictionary with the key "message"
        set to "User not found!".
        """
        try:
            user = get_object_or_404(UserModel, public_id=public_id)
            user.delete()
            return {"success": True}
        except UserModel.DoesNotExist as e:
            return 404, {"message": "User not found!"}