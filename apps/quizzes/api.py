from typing import List, Union
from django.shortcuts import get_object_or_404
from ninja import Router
from .schema import *
from .models import *
import json

router = Router()

class QuizzesMethodView:
    @router.post('/create-quiz', response=QuizOutputSchema)
    def create_quiz(request, payload: QuizInputSchema):
        """
        This function creates a quiz object with a given folder ID and modified by user, and adds a list
        of questions to the quiz.
        
        :param request: The HTTP request object containing information about the incoming request
        :param payload: The payload parameter is of type QuizInputSchema, which is likely a custom
        schema or class that defines the expected structure of the input data for creating a quiz. It
        likely contains information such as the folder ID where the quiz should be stored and the user
        who is modifying the quiz
        :type payload: QuizInputSchema
        :return: an instance of the QuizModel class that has been created and populated with the
        provided payload data and questions.
        """
        quiz = QuizModel.objects.create(
            folder_id_id=payload.folder_id_id,
            modified_by=payload.modified_by,
            name=payload.name,
            desc=payload.desc,
            questions=payload.questions  # Assign the questions directly
        )
        return quiz

    @router.get("/get-quiz-lists", response=List[QuizOutputSchema])
    def get_quiz_lists(request):
        """
        This function retrieves all quiz data from the QuizModel database table and returns it, or
        returns a message if no quiz data is found.
        
        :param request: The request parameter is not being used in the given code snippet. It is a
        common parameter in Django views and is used to represent an HTTP request that is sent to the
        server. It contains information such as the request method, headers, and data
        :return: If the try block is successful, the function will return all the quiz data from the
        QuizModel. If the QuizModel.DoesNotExist exception is raised, the function will return a tuple
        containing the HTTP status code 200 and a dictionary with a message indicating that no quiz was
        found.
        """
        quiz_data = QuizModel.objects.all()
        return quiz_data

    @router.put("/edit-quiz/{public_id}", response=QuizOutputSchema)
    def edit_quiz(request, public_id: UUID, payload: QuizInputSchema):
        try:
            quiz = get_object_or_404(QuizModel, public_id=public_id)
            quiz.folder_id_id = payload.folder_id_id
            quiz.modified_by = payload.modified_by
            quiz.name = payload.name
            quiz.desc=payload.desc
            quiz.questions = payload.questions  # Update the questions directly
            quiz.save()

            return quiz
        except QuizModel.DoesNotExist:
            return {"message": "Quiz not found!"}, 404

    @router.get("/get-specific-quiz/{public_id}", response=Union[QuizOutputSchema, dict])
    def get_specific_quiz(request, public_id: UUID):
        """
        This function retrieves a specific quiz by its public ID and returns either the quiz or a 404
        error message.
        
        :param request: The HTTP request object that contains information about the incoming request,
        such as the HTTP method, headers, and body
        :param public_id: public_id is a parameter of type UUID (Universally Unique Identifier) that is
        used to identify a specific quiz in the database. It is passed as an argument to the function
        get_specific_quiz() in a Django view. The function tries to retrieve the quiz with the given
        public_id from the QuizModel
        :type public_id: UUID
        :return: A tuple containing an HTTP status code and either the requested quiz object or a
        dictionary with an error message.
        """
        try:
            quiz = get_object_or_404(QuizModel, public_id=public_id)
            return quiz
        except QuizModel.DoesNotExist:
            return {"message": "Quiz not found!"}, 404

    @router.delete("/delete-quiz/{public_id}")
    def delete_quiz(request, public_id: UUID):
        """
        This function deletes a quiz with a given public ID and returns a success message or a 404 error
        message if the quiz is not found.
        
        :param request: The HTTP request object that contains information about the current request,
        such as the HTTP method, headers, and body
        :param public_id: UUID
        :type public_id: UUID
        :return: If the quiz with the given public_id exists and is successfully deleted, a dictionary
        with the key "success" and value True is returned. If the quiz does not exist, a tuple with the
        HTTP status code 404 and a dictionary with the key "message" and value "quiz not found!" is
        returned.
        """
        try:
            quiz = get_object_or_404(QuizModel, public_id=public_id)
            quiz.delete()
            return {"success": True}
        except QuizModel.DoesNotExist:
            return {"message": "Quiz not found!"}, 404
