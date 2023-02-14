from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main_logic.models import Category, Question, Team, Tournament
from main_logic.serializer import CategorySerializer, QuestionSerializer, TeamSerializer, TeamsSerializer, TournamentSerializer
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.


@swagger_auto_schema(method='get', responses={200: TeamsSerializer(many=True)})
@api_view(['GET'])
def get_teams(request) -> Response:
    """
    Retrieve the data of all teams.

    This function retrieves the data of all teams stored in the database. The returned data includes the name of the team,
    the leader's ID, the team's avatar URL, and a list of team members' IDs, names, and avatar URLs.

    Returns:
        JSON: A JSON response containing the following information:
            team_name (str): The name of the team.
            team_leader (int): The leader's ID.
            team_avatar (str): The URL of the team's avatar.
            members (list): A list of dictionaries, each containing the following information for a team member:
                id (int): The team member's ID.
                name (str): The team member's name.
                avatar (str): The URL of the team member's avatar.

    Example:
        Request: GET /api/teams/
        Response:
        [
            {
                "team_name": "Team A",
                "team_leader": 1,
                "team_avatar": "https://example.com/team-a-avatar.jpg",
                "members": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "avatar": "https://example.com/john-doe-avatar.jpg"
                    },
                    {
                        "id": 2,
                        "name": "Jane Doe",
                        "avatar": "https://example.com/jane-doe-avatar.jpg"
                    }
                ]
            },
            {
                "team_name": "Team B",
                "team_leader": 3,
                "team_avatar": "https://example.com/team-b-avatar.jpg",
                "members": [
                    {
                        "id": 3,
                        "name": "John Smith",
                        "avatar": "https://example.com/john-smith-avatar.jpg"
                    },
                    {
                        "id": 4,
                        "name": "Jane Smith",
                        "avatar": "https://example.com/jane-smith-avatar.jpg"
                    }
                ]
            }
        ]
    """
    teams = Team.objects.all()
    serializer = TeamsSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=TeamSerializer)
@api_view(['POST'])
def add_team(request):
    """
    Add a new team using the POST method.

    This function is used to create a new team.
    Args:   
        team_name,
        team_leader,
        team_avatar,
        members
    """
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "created"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


team_param = openapi.Parameter(
    'team', openapi.IN_QUERY, description="team manual param", type=openapi.TYPE_BOOLEAN)
user_response = openapi.Response('response description', TeamSerializer)


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

    Args:
        team_name (str): The name of the team.
        team_leader (int): An account ID for the leader of the team.
        members (list, optional): A list of account IDs for team members.

    Returns:
        JSON: A JSON response indicating the result of the request, with the following format:
            Data:
                id (int),
                team_name (str),
                team_leader (int),
                team_avatar (str),
                members (list).
            message (str):
                if a new team was created, "updated" if an existing team was updated,
                or "deleted" if the team was deleted.

    Examples:
    PUT Request: /api/teams/<id>/get-or-update/
    Data:
        {
            "team_name": "Team A",
            "team_leader": 1,
            "members": [2, 3]
        }
    Response:
        {
            "message": "created"
        }

    GET Request: /api/teams/<id>/get-or-update/
    Response:
    {
        "id": 8,
        "team_name": "Team A",
        "team_leader": 1,
        "team_avatar": "/teams.jpg",
        "members": [2, 3]
    }

    DELETE Request: /api/teams/<id>/get-or-update/
    Response:
    {
        "message": "deleted"
    }
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
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "updated"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        team.delete()
        return Response({"message": "deleted"}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='get', responses={200: CategorySerializer(many=True)})
@api_view(['GET'])
def get_categories(request):
    """
    Retrieve the data of all categories.
    """
    catagories_obj = Category.objects.all()
    serializer = CategorySerializer(catagories_obj, many=True)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: QuestionSerializer(many=True)})
@api_view(['GET'])
def get_questions(request):
    """
    Retrieve the data of all questions.
    """
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: TournamentSerializer(many=True)})
@api_view(['GET'])
def get_tournaments(request):
    """
    Retrieve the data of all tournaments.
    """
    tournaments = Tournament.objects.all()
    serializer = TournamentSerializer(tournaments, many=True)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_tournament(request, id):

    return Response({"data": None})
