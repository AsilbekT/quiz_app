from rest_framework import serializers

from accounts.models import Account
from .models import Category, Question, Team, Tournament


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'avatar'
        ]


class TeamsSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'team_leader',
            'team_avatar',
            'members'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['members'] = MemberSerializer(
            instance.members.all(), many=True).data
        return representation


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'team_leader',
            'team_avatar',
            'members'
        ]

    def update(self, instance, validated_data):
        """
        Update and return an existing `TeamSerializer` instance, given the validated data.
        """
        [instance.members.add(i.id) for i in validated_data.get('members')]
        instance.team_name = validated_data.get(
            'team_name', instance.team_name)
        instance.team_leader = validated_data.get(
            'team_leader', instance.team_leader)

        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'type'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question',
            'question_type',
            'answer',
            'option1',
            'option2',
            'option3',
            'option4'
        ]


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = [
            'id',
            'tournament_code',
            'tournament_teams',
            'tournament_price',
            'categories',
            'is_active',
        ]
