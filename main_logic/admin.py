from django.contrib import admin
from .models import (
    Team,
    Tournament,
    Category,
    TeamMembership,
    Question
)


class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('team', 'member')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_type')


# Register your models here.
admin.site.register(Team)
admin.site.register(Tournament)
admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TeamMembership, TeamMembershipAdmin)
