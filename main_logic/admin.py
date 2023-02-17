from django.contrib import admin
from .models import (
    Team,
    Tournament,
    Category,
    TeamMembership
)


class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('team', 'member')


# Register your models here.
admin.site.register(Team)
admin.site.register(Tournament)
admin.site.register(Category)
admin.site.register(TeamMembership, TeamMembershipAdmin)
