from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from apps.quizzes.models import QuizQuestionsModel, QuizChoicesModel
from .schema import *

router = Router()

class QuizzesMethodView:
    @router.post('/create-questions', response=QuizzesOutputSchema)
    def create_questions(request, payload: QuizzesInputSchema):
        """
        This function creates a new quiz question in the database using the provided payload data.
        
        :param request: The request object is an instance of the HttpRequest class, which represents an
        incoming HTTP request from a client. It contains information about the request, such as the HTTP
        method, headers, and body
        :param payload: QuizzesInputSchema, which is likely a schema or data structure that defines the
        expected format and data types for the input payload of a quiz question. It likely includes
        fields such as "question" (the actual question being asked), "desc" (a description or additional
        information about the question), and
        :type payload: QuizzesInputSchema
        :return: The function `create_questions` returns an instance of the `QuizQuestionsModel` class
        with the attributes `question`, `desc`, and `modified_by` set to the values provided in the
        `payload` parameter.
        """
        question_data = QuizQuestionsModel.objects.create(
            folder_id_id = payload.folder_id_id,
            question=payload.question,
            desc=payload.desc,
            modified_by=payload.modified_by
        )
        return question_data
    
    @router.post('/create-answer', response=ChoicesOutputSchema)
    def create_answer(request, payload: ChoicesInputSchema):
        """
        The function creates a new answer for a quiz question using the input payload data.
        
        :param request: The request object contains information about the current HTTP request, such as
        the user making the request, the HTTP method used, and any data sent in the request
        :param payload: The parameter `payload` is of type `ChoicesInputSchema`, which is likely a
        custom schema or data class that defines the structure of the data being passed in. It likely
        contains information about a user's answer to a quiz question, including the question ID, the
        user's answer choice, a description
        :type payload: ChoicesInputSchema
        :return: The function `create_answer` returns an instance of the `QuizChoicesModel` class with
        the data provided in the `payload` parameter.
        """
        answer_data = QuizChoicesModel.objects.create(
            question_id_id = payload.question_id_id,
            answer=payload.answer,
            desc=payload.desc,
            modified_by=payload.modified_by
        )
        return answer_data
    
    @router.get("/get-answer-lists/{question_id}", response=List[ChoicesOutputSchema])
    def get_answer_lists_by_question_id(request, question_id: int):
        """
        This function retrieves answer lists by a given question ID from a database table.
        
        :param request: The HTTP request object that contains information about the current request,
        such as the user making the request, the HTTP method used, and any data sent with the request
        :param question_id: an integer representing the ID of the question for which we want to retrieve
        the answer choices
        :type question_id: int
        :return: This function returns a queryset of answer choices related to a specific question ID.
        If no answer choices are found for the given question ID, it returns a response with a status
        code of 200 and a message indicating that no questions were found.
        """
        try:
            answer_data=QuizChoicesModel.objects.all().filter(question_id=question_id)
            return answer_data
        except QuizChoicesModel.DoesNotExist as e:
            return 200, {"message": "no questions found!"}
        
    @router.put("answer/{public_id}", response={200: ChoicesOutputSchema, 404: Error})
    def update_specific_answer(request, public_id: UUID, payload: ChoicesInputSchema):
        """
        This function updates a specific answer in a quiz using the provided payload.
        
        :param request: The HTTP request object containing metadata about the request being made
        :param public_id: The public_id parameter is a UUID (Universally Unique Identifier) that is used
        to identify a specific QuizChoicesModel object in the database
        :type public_id: UUID
        :param payload: The `payload` parameter is an instance of the `ChoicesInputSchema` class, which
        is expected to be a dictionary-like object containing the updated values for the
        `QuizChoicesModel` instance identified by the `public_id` parameter. The `dict()` method is
        called on the `payload` object
        :type payload: ChoicesInputSchema
        :return: A tuple containing an HTTP status code and either the updated QuizChoicesModel object
        or a dictionary with an error message.
        """
        try:
            answer = get_object_or_404(QuizChoicesModel, public_id=public_id)
            for attr, value in payload.dict().items():
                print(attr)
                setattr(answer, attr, value)
            answer.save()
            return 200, answer
        except QuizChoicesModel.DoesNotExist as e:
            return 404, {"message": "Answer not found!"}
        
    @router.delete("/{public_id}")
    def delete_answer(request, public_id: UUID):
        """
        This function deletes a QuizChoicesModel object with a given public_id and returns a success
        message or a 404 error message if the object does not exist.
        
        :param request: The HTTP request object containing metadata about the request, such as headers
        and user information
        :param public_id: UUID
        :type public_id: UUID
        :return: If the file with the given public_id exists and is successfully deleted, the function
        returns a dictionary with a "success" key set to True. If the file does not exist, the function
        returns a tuple with a 404 status code and a dictionary with a "message" key set to "File not
        found!".
        """

        try:
            file = get_object_or_404(QuizChoicesModel, public_id=public_id)
            file.delete()
            return {"success": True}
        except QuizChoicesModel.DoesNotExist as e:
            return 404, {"message": "File not found!"}
        
    
    @router.get("/get-question-lists", response=List[QuizzesOutputSchema])
    def get_question_lists(request):
        """
        This function retrieves all quiz questions data or returns a message if no questions are found.
        
        :param request: The request parameter is not being used in the given code snippet. It is likely
        that this function is a part of a Django view and the request parameter is being passed
        automatically by the framework
        :return: If the try block is successful, the function will return all the data from the
        QuizQuestionsModel. If the try block raises a DoesNotExist exception, the function will return a
        tuple containing the HTTP status code 200 and a dictionary with a message indicating that no
        questions were found.
        """
        try:
            quizzes_data=QuizQuestionsModel.objects.all()
            return quizzes_data
        except QuizQuestionsModel.DoesNotExist as e:
            return 200, {"message": "no questions found!"}
        
    @router.get("/get-question-lists/{folder_id}", response=List[QuizzesOutputSchema])
    def get_question_lists_by_folder_id(request, folder_id: int):
        """
        This function retrieves a list of quiz questions based on a given folder ID.
        
        :param request: The request object contains information about the current HTTP request, such as
        the user making the request, the HTTP method used, and any data sent with the request
        :param folder_id: an integer representing the ID of the folder for which the list of questions
        is being requested
        :type folder_id: int
        :return: If the `QuizQuestionsModel` objects are found for the given `folder_id`, then the
        `quizzes_data` variable containing the filtered objects is returned. If no objects are found,
        then a tuple containing the HTTP status code 200 and a dictionary with a "message" key-value
        pair indicating that no questions were found is returned.
        """
        
        try:
            quizzes_data=QuizQuestionsModel.objects.all().filter(folder_id=folder_id)
            return quizzes_data
        except QuizQuestionsModel.DoesNotExist as e:
            return 200, {"message": "no questions found!"}
        
    @router.get("/{public_id}", response ={200: QuizzesOutputSchema, 404: Error})
    def get_specific_question(request, public_id: UUID):
        """
        This function retrieves a specific quiz question by its public ID and returns either the
        question or a 404 error message.
        
        :param request: The request object represents the HTTP request that the client has made to the
        server
        :param public_id: public_id is a parameter of type UUID (Universally Unique Identifier) which is
        used to identify a specific quiz question in the database. It is passed as an argument to the
        function get_specific_question() which retrieves the question with the matching public_id from
        the QuizQuestionsModel table. If the question is
        :type public_id: UUID
        :return: a tuple with two values: an HTTP status code (either 200 or 404) and either the
        requested quiz question object or a dictionary with an error message if the question is not
        found.
        """
        try:
            question = get_object_or_404(QuizQuestionsModel, public_id=public_id)
            return 200,  question
        except QuizQuestionsModel.DoesNotExist as e:
            return 404, {"message": "Question not found!"}
        
    @router.put("/{public_id}", response={200: QuizzesOutputSchema, 404: Error})
    def update_question(request, public_id: UUID, payload: QuizzesInputSchema):
        """
        This function updates a quiz question object with the given payload data.
        
        :param request: The HTTP request object containing information about the request being made
        :param public_id: UUID - This is a unique identifier for the quiz question that is being
        updated. It is used to retrieve the specific question from the database
        :type public_id: UUID
        :param payload: The payload parameter is an instance of the QuizzesInputSchema class, which is
        expected to be a dictionary-like object containing the updated values for the QuizQuestionsModel
        instance identified by the public_id parameter
        :type payload: QuizzesInputSchema
        :return: a tuple containing an HTTP status code and either the updated QuizQuestionsModel object
        or a dictionary with an error message if the object is not found.
        """
        try:
            question = get_object_or_404(QuizQuestionsModel, public_id=public_id)
            for attr, value in payload.dict().items():
                print(attr)
                setattr(question, attr, value)
            question.save()
            return 200, question
        except QuizQuestionsModel.DoesNotExist as e:
            return 404, {"message": "Question not found!"}
        
    @router.delete("/{public_id}")
    def delete_question(request, public_id: UUID):
        """
        This function deletes a file with a given public ID and returns a success message or a 404 error
        message if the file is not found.
        
        :param request: The request object represents the HTTP request that was made by the client to
        the server
        :param public_id: public_id is a parameter of type UUID that is used to identify a specific
        FolderModel object to be deleted. It is passed as an argument to the delete_question function
        :type public_id: UUID
        :return: If the file with the given public_id exists and is successfully deleted, the function
        returns a dictionary with a key "success" and value True. If the file does not exist, the
        function returns a tuple with a status code of 404 and a dictionary with a key "message" and
        value "File not found!".
        """
        
        try:
            file = get_object_or_404(QuizQuestionsModel, public_id=public_id)
            file.delete()
            return {"success": True}
        except QuizQuestionsModel.DoesNotExist as e:
            return 404, {"message": "File not found!"}
        