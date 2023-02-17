from rest_framework import serializers
from .models import Account, Following
from main_logic.serializer import TeamsSerializer, TeamMembershipsSerializer


class FollowingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ['user', 'follower']


class FollowingSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(read_only=True)

    class Meta:
        model = Following
        fields = ['user', 'follower', 'avatar']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['avatar'] = str(instance.user.avatar)
        return representation


class PlayersSerializer(serializers.ModelSerializer):
    followings_count = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'phone_number',
            'username',
            'date_joined',
            'last_login',
            'followings_count',
            'followers_count',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['followings_count'] = instance.following.count()
        representation['followers_count'] = instance.followers.count()
        return representation


class PlayerSerializer(serializers.ModelSerializer):
    followings_count = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    joined_team = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'phone_number',
            'username',
            'date_joined',
            'last_login',
            'followings_count',
            'followers_count',
            'joined_team',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['followings_count'] = instance.following.count()
        representation['followers_count'] = instance.followers.count()
        representation['joined_team'] = TeamMembershipsSerializer(
            instance.get_team_membership()).data
        return representation


class PlayerFriendshipSerializer(serializers.ModelSerializer):
    followings = FollowingSerializer(many=True, read_only=True)
    followers = FollowingSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            'followings',
            'followers',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['followings'] = FollowingSerializer(
            instance.following.all(), many=True).data
        representation['followers'] = FollowingSerializer(
            instance.followers.all(), many=True).data
        return representation
