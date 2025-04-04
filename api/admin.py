from django.contrib import admin

# Register your models here.
from .models import Games, Details

admin.site.register(Games)
admin.site.register(Details)