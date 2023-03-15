from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .utils import handle_uploaded_file
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .forms import UploadFileForm

from django.core.files.storage import FileSystemStorage

from main_logic.models import (
    Category,
    Question,
    Team,
    Tournament,
    Option
)

from main_logic.serializer import (
    CategorySerializer,
    QuestionSerializer,
    TeamSerializer,
    TeamsSerializer,
    TournamentSerializer
)
# views below.


@swagger_auto_schema(method='get', responses={200: TeamsSerializer(many=True)})
@api_view(['GET'])
def get_teams(request) -> Response:
    """
    Retrieve the data of all teams.

    This function retrieves the data of all teams stored in the database. The returned data includes the name of the team,
    the leader's ID, the team's avatar URL, and a list of team members' IDs, names, and avatar URLs.
    """
    teams = Team.objects.all()
    serializer = TeamsSerializer(teams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['team_name', 'token'],
        properties={
            'team_name': openapi.Schema(type=openapi.TYPE_STRING),
            'token': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
)
@api_view(['POST'])
def add_team(request):
    """
    Add a new team using the POST method.

    This function is used to create a new team.
    """
    try:
        team_credentials = {}
        team_credentials['team_name'] = request.data['team_name']
        got_token = request.data['token']
        token = Token.objects.get(key=got_token)
        user = token.user
        team_credentials['team_leader'] = user.id

        serializer = TeamSerializer(data=team_credentials)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist:
        return Response({'error': "Object does not exist!"}, status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(method='get', manual_parameters=[team_param], responses={200: user_response})
@swagger_auto_schema(methods=['put', 'delete'], request_body=TeamSerializer)
@api_view(['PUT', 'GET', 'DELETE'])
def get_or_update_team(request, id) -> Response:
    """
    Update or retrieve a team using the PUT, GET, or DELETE methods.

    This function allows you to either retrieve the data of an existing team by GET request.
    If the specified team already exists, you can update its data by sending a PUT request.
    To delete a team, send a DELETE request.
    The required parameters for either getting or updating a team are the name of the team and the ID of the team leader.
    Optionally, a list of IDs for team members can be included in the request.
    """

    try:
        team = Team.objects.get(id=id)
    except ObjectDoesNotExist:
        message = {
            "message": "The object does not exist, please use post method to create it."
        }
        return Response(message)

    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        team.delete()
        return Response({"message": "deleted"}, status=status.HTTP_202_ACCEPTED)


@swagger_auto_schema(method='get', responses={200: CategorySerializer(many=True)})
@api_view(['GET'])
def get_categories(request):
    """
    Retrieve the data of all categories.
    """
    catagories_obj = Category.objects.all()
    serializer = CategorySerializer(catagories_obj, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', responses={200: QuestionSerializer(many=True)})
@api_view(['GET'])
def get_questions(request, id):
    """
    Retrieve the data of all questions.
    """
    try:
        categories = Category.objects.get(id=id)
        questions = categories.category_questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', responses={200: TournamentSerializer(many=True)})
@api_view(['GET'])
def get_tournaments(request):
    """
    Retrieve the data of all tournaments.
    """
    try:
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', responses={200: TournamentSerializer})
@api_view(['GET'])
def get_tournament(request, id):
    try:
        tournament = Tournament.objects.get(id=id)
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def upload_doc(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        category = Category.objects.get(id=request.POST['catagory'])
        if form.is_valid():
            questions = handle_uploaded_file(request.FILES['file'])
            for k, v in questions.items():
                question = Question.objects.create(
                    question_text=v[0]['question'], category=category)
                options = v[1:]
                options_to_create = [Option(question=question, option_text=option.get(
                    'option', ''), is_correct='answer' in option) for option in options]
                Option.objects.bulk_create(options_to_create)

            return render(request, 'upload_doc.html')
    else:
        catagories = Category.objects.all()
        form = UploadFileForm()
    return render(request, 'upload_doc.html', {'form': form, 'catagories': catagories})
