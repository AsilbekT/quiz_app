from django.contrib import admin
from .models import (
    Team,
    Tournament,
    QuestionType,
    Question
)

# Register your models here.
admin.site.register(Team)
admin.site.register(Tournament)
admin.site.register(QuestionType)
admin.site.register(Question)
