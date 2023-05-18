from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from .schema import *
from .models import *
import json

router = Router()

class QuizzesMethodView:
    @router.post('/create-choice', response=ChoiceOutputSchema)
    def create_choice(request, payload: ChoiceInputSchema):
        """
        This function creates a new choice object in the database using the input data.
        
        :param request: The request object represents the HTTP request that triggered the view function.
        It contains information about the client's request, such as the HTTP method used, the headers,
        and the request body
        :param payload: The parameter `payload` is of type `ChoiceInputSchema`, which is likely a custom
        schema or data class that defines the structure of the data being passed in for creating a new
        choice. It likely contains information such as the text of the choice and the user who is
        modifying it
        :type payload: ChoiceInputSchema
        :return: The function `create_choice` is returning an instance of the `ChoiceModel` class that
        was created with the data provided in the `payload` parameter.
        """
        choice_data = ChoiceModel.objects.create(
            choice=payload.choice,
            modified_by=payload.modified_by
        )
        return choice_data
    
    @router.get("/get-choices-lists", response=List[ChoiceOutputSchema])
    def get_choices_lists(request):
        """
        The function retrieves all the choices from the ChoiceModel database table and returns them, or
        returns a message if no choices are found.
        
        :param request: The `request` parameter is not used in the given code snippet. It is likely that
        this function is not part of a view and does not require a request object
        :return: If the `ChoiceModel` objects exist, then the function will return the queryset of all
        `ChoiceModel` objects. If the `ChoiceModel` does not exist, then the function will return a
        tuple containing an HTTP status code of 200 and a dictionary with a message indicating that no
        choices were found.
        """
        try:
            choices_data=ChoiceModel.objects.all()
            return choices_data
        except ChoiceModel.DoesNotExist as e:
            return 200, {"message": "no choices found!"}
        
    @router.get("get-specific-choice/{public_id}", response ={200: ChoiceOutputSchema, 404: Error})
    def get_specific_choice(request, public_id: UUID):
        """
        This function retrieves a specific choice object based on its public ID and returns it with a
        200 status code, or returns a 404 status code with an error message if the choice does not
        exist.
        
        :param request: The request object represents the HTTP request that the client has made to the
        server
        :param public_id: public_id is a parameter of type UUID (Universally Unique Identifier) which is
        used to identify a specific ChoiceModel object. It is passed as an argument to the
        get_specific_choice function
        :type public_id: UUID
        :return: A tuple containing an HTTP status code and either the requested ChoiceModel object or a
        dictionary with an error message if the object does not exist.
        """
        try:
            choice = get_object_or_404(ChoiceModel, public_id=public_id)
            return 200,  choice
        except ChoiceModel.DoesNotExist as e:
            return 404, {"message": "Choice not found!"}
        
    @router.put("update-choice/{public_id}", response={200: ChoiceOutputSchema, 404: Error})
    def update_choice(request, public_id: UUID, payload: ChoiceInputSchema):
        """
        This function updates a choice object with the given payload data.
        
        :param request: The request object contains information about the current HTTP request, such as
        the HTTP method, headers, and body
        :param public_id: The public_id parameter is a UUID (Universally Unique Identifier) that is used
        to identify a specific ChoiceModel object in the database
        :type public_id: UUID
        :param payload: The `payload` parameter is an instance of the `ChoiceInputSchema` class, which
        is a Pydantic model used for validating and parsing incoming JSON data in the request body. It
        contains the updated values for the `ChoiceModel` instance identified by the `public_id`
        parameter
        :type payload: ChoiceInputSchema
        :return: A tuple containing an HTTP status code and either the updated ChoiceModel object or a
        dictionary with an error message.
        """
        try:
            choice = get_object_or_404(ChoiceModel, public_id=public_id)
            for attr, value in payload.dict().items():
                print(attr)
                setattr(choice, attr, value)
            choice.save()
            return 200, choice
        except ChoiceModel.DoesNotExist as e:
            return 404, {"message": "Choice not found!"}
        
######################################################################

    @router.post('/create-question', response=QuestionOutputSchema)
    def create_question(request, payload: QuestionInputSchema):
        """
        This function creates a new question object with choices and returns it.
        
        :param request: The HTTP request object containing information about the incoming request
        :param payload: The payload parameter is of type QuestionInputSchema, which is likely a custom
        schema or class that defines the structure of the data expected for creating a new question. It
        likely includes fields such as the question text and the user who modified the question
        :type payload: QuestionInputSchema
        :return: The function `create_question` is returning an instance of the `QuestionsModel` class
        that has been created with the provided `question` and `modified_by` data, and with the
        `choices` data added to it.
        """
        body_unicode=request.body.decode('utf-8')
        json_data = json.loads(body_unicode)
        choices_data = json_data['choices']
        question_data = QuestionsModel.objects.create(
            question=payload.question,
            modified_by=payload.modified_by
        )
        for indx in range(len(choices_data)):
            print(indx)
            question_data.choices.add(choices_data[indx])
        return question_data
    
    @router.get("/get-question-lists", response=List[QuestionOutputSchema])
    def get_question_lists(request):
        """
        This function retrieves all question data from the ChoiceModel database table or returns a
        message if no questions are found.
        
        :param request: The request parameter is not used in the given code snippet. It is likely that
        this function is a part of a Django view and the request parameter is included by default in all
        view functions
        :return: If there are questions in the database, the function will return a QuerySet containing
        all the questions. If there are no questions in the database, the function will return a tuple
        containing a status code of 200 and a dictionary with a message indicating that no questions
        were found.
        """
        try:
            question_data=QuestionsModel.objects.all()
            return question_data
        except QuestionsModel.DoesNotExist as e:
            return 200, {"message": "no question found!"}
        
    @router.get("get-specific-question/{public_id}", response ={200: QuestionOutputSchema, 404: Error})
    def get_specific_question(request, public_id: UUID):
        """
        This function retrieves a specific question by its public ID and returns either the question or
        a "Question not found" message.
        
        :param request: The HTTP request object containing metadata about the request, such as headers
        and query parameters
        :param public_id: public_id is a parameter of type UUID (Universally Unique Identifier) that is
        used to identify a specific question in the QuestionsModel database. It is passed as an argument
        to the get_specific_question function
        :type public_id: UUID
        :return: A tuple is being returned, with the first element being an HTTP status code (either 200
        or 404) and the second element being either the requested question object or a dictionary with
        an error message.
        """
        try:
            question = get_object_or_404(QuestionsModel, public_id=public_id)
            return 200,  question
        except QuestionsModel.DoesNotExist as e:
            return 404, {"message": "Question not found!"}
    
    @router.delete("delete-question/{public_id}")
    def delete_question(request, public_id: UUID):
        """
        This function deletes a question with a given public ID and returns a success message or a 404
        error message if the question is not found.
        
        :param request: The request object represents the HTTP request that was made by the client
        :param public_id: UUID
        :type public_id: UUID
        :return: If the question with the given public_id exists, it will be deleted and a dictionary
        with the key "success" and value True will be returned. If the question does not exist, a tuple
        with the HTTP status code 404 and a dictionary with the key "message" and value "Question not
        found!" will be returned.
        """
        try:
            question = get_object_or_404(QuestionsModel, public_id=public_id)
            question.delete()
            return {"success": True}
        except QuestionsModel.DoesNotExist as e:
            return 404, {"message": "Question not found!"}
        
######################################################################

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
        body_unicode=request.body.decode('utf-8')
        json_data = json.loads(body_unicode)
        questions = json_data['questions']
        quiz = QuizModel.objects.create(
            folder_id_id=payload.folder_id_id,
            modified_by=payload.modified_by
        )
        for indx in range(len(questions)):
            print(indx)
            quiz.questions.add(questions[indx])
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
        try:
            quiz_data=QuizModel.objects.all()
            return quiz_data
        except QuizModel.DoesNotExist as e:
            return 200, {"message": "no quiz found!"}
        
    @router.get("get-specific-quiz/{public_id}", response ={200: QuizOutputSchema, 404: Error})
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
            return 200,  quiz
        except QuizModel.DoesNotExist as e:
            return 404, {"message": "Quiz not found!"}
        
    @router.delete("delete-quiz/{public_id}")
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
        except QuizModel.DoesNotExist as e:
            return 404, {"message": "quiz not found!"}