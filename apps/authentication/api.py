import json
from ninja import Router
from apps.authentication.models import UserModel
from .schema import AuthSchema, JWTPairSchema, Error, Success, ChangePasswordUserInputSchema, ForgotPasswordSchema
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from uuid import UUID
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException

router = Router()

# It's a subclass of the `HttpBearer` class that comes with the `flask-jwt-extended` library
class AuthenticationMethodView:
    @router.post('authentication/login', response={200: JWTPairSchema, 401: Error}, auth=None)
    def login(request, auth: AuthSchema):
        """
        It takes a request and an AuthSchema object, authenticates the user, and returns a refresh token
        and an access token
        
        :param request: The request object
        :param auth: AuthSchema
        :type auth: AuthSchema
        :return: A dictionary with two keys: refresh and access.
        """
        user = authenticate(**auth.dict())
        if user is None:
            return 401, {"message": "invalid username or password!"}
        else:
            access = RefreshToken.for_user(user)
            print(user.public_id)
            return {
                'access': str(access.access_token),
                'user': {
                    'id': user.id,
                    'public_id': str(user.public_id),
                    'email': str(user),
                    'role': str(user.role)
                }
            }

    @router.put('authentication/change-password/{public_id}', response={200: Success, 500: Error})
    def change_password(request, public_id: UUID, payload: ChangePasswordUserInputSchema):
        """
        It takes a request, a public_id, and a payload, and then it tries to get the user_data, decode
        the request body, load the json data, check the old password, check if the new password and the
        confirm password are the same, check if the password is correct, and if the password is correct
        and the new password and the confirm password are the same, then it updates the password
        
        :param request: The request object
        :param public_id: UUID
        :type public_id: UUID
        :param payload: ChangePasswordUserInputSchema
        :type payload: ChangePasswordUserInputSchema
        """
        try:
            user_data = UserModel.objects.get(public_id=public_id)
            body_unicode   = request.body.decode('utf-8')
            json_data = json.loads(body_unicode)
            old_password = json_data['old_password']
            password_check = check_password(old_password ,user_data.password)
            if json_data['new_password'] != json_data['confirm_password']:
                return 500, {"message": "the password is not matched!"}
            elif not password_check:
                return 500, {"message": "the password is incorrect!"}
            elif password_check and json_data['new_password'] == json_data['confirm_password']:
                UserModel.objects.filter(public_id=public_id).update(email=user_data.email, password = make_password(json_data['new_password']))
                return 200, {"message": "password successfully changed."}
        except:
            return 500, {"message": "error on changing password!"}
        

    @router.post('authentication/forgot-password', response={200: Success, 401: Error}, auth=None)
    def forgot_password(request, payload: ForgotPasswordSchema):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['username']
        letters = string.ascii_lowercase
        new_password = ''.join(random.choice(letters) for i in range(6))
        email_sent = False
        if UserModel.objects.filter(email=username).exists():
            user = UserModel.objects.get(email=username)
            subject = "Request for Forgot Password"
            message = "Hi user, here is your new password, {}".format(new_password.upper())
            email = settings.EMAIL_HOST_USER
            recipient = [user.email]
            try:
                send_mail(subject=subject, message=message, from_email=email, recipient_list=recipient)
                print("successfully email send")
                email_sent = True
            except SMTPException as err:
                print("error on sending email" + err)
                email_sent = False

            if email_sent == True:
                UserModel.objects.filter(email=username).update(email=username, password = make_password(new_password.upper()))

                return 200, {"message": "password successfully reset."}
            else:
                return 500, {"message": "error on forgot password!"}

            ## to decrypt ##
            #decMessage = fernet.decrypt(encrypt_token).decode()
            
