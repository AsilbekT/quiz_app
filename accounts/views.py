from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account
from .serializer import FollowingsSerializer, PlayerFriendshipSerializer, PlayerSerializer, PlayersSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


@api_view(['GET'])
def get_users(request) -> Response:
    players = Account.objects.filter(is_active=True)
    serializer = PlayersSerializer(players, many=True)
    serialized_players = serializer.data
    players_count = players.count()
    data = {
        'players_count': players_count,
        'all_players':  serialized_players
    }
    return Response(data)


@api_view(['GET'])
def get_user(request, id) -> Response:
    try:
        player = Account.objects.get(id=id)
        serializer = PlayerSerializer(player)
        serialized_players = serializer.data
    except ObjectDoesNotExist:
        serialized_players = {}
    return Response(serialized_players)


@api_view(['GET'])
def get_friendships(request, id) -> Response:
    try:
        player = Account.objects.get(id=id)
        serializer = PlayerFriendshipSerializer(player)
        serialized_players = serializer.data
    except ObjectDoesNotExist:
        serialized_players = {}
    return Response(serialized_players)


@api_view(['POST'])
def add_friendship(request) -> Response:
    data = {}
    if request.method == 'POST':
        if request.data['user'] != request.data['follower']:
            serializer = FollowingsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data['response'] = 'successfully registered new user.'
            else:
                data = serializer.errors
            return Response(data)
        else:
            return Response({'error': "users cannot follow themselves!"})
