from rest_framework import serializers

from .models import (
    Category,
    Question,
    Team,
    Tournament,
    TeamMembership,
    Option
)


class TeamMembershipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = ['team', 'member']


class TeamsSerializer(serializers.ModelSerializer):
    members = serializers.CharField(read_only=True)

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
        representation['members'] = TeamMembershipsSerializer(
            instance.team.all(), many=True).data
        return representation


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.CharField(read_only=True)

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
        # [instance.members.add(i.id) for i in validated_data.get('members')]
        instance.team_name = validated_data.get(
            'team_name', instance.team_name)
        instance.team_leader = validated_data.get(
            'team_leader', instance.team_leader)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['members'] = TeamMembershipsSerializer(
            instance.team.all(), many=True).data
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = [
            'question',
            'option_text',
            'is_correct'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = [
            'question_text',
            'category',
            'options'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['options'] = QuestionOptionSerializer(
            instance.options.all(), many=True).data
        return representation


class TournamentSerializer(serializers.ModelSerializer):
    tournament_teams = TeamSerializer(read_only=True)

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tournament_teams'] = TeamSerializer(
            instance.tournament_teams.all(), many=True).data
        return representation
