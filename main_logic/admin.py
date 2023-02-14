from django.contrib import admin
from .models import (
    Team,
    Tournament,
    Category,
    # Question
)

# Register your models here.
admin.site.register(Team)
admin.site.register(Tournament)
admin.site.register(Category)
# admin.site.register(Question)
