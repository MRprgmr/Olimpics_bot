from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .filters import RegisteredUsers
from .models import User, Subject, Class, Olympiad


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['name', 'username']
    list_filter = [RegisteredUsers, 'is_poorly_supplied']
    list_per_page = 50


@admin.register(Subject)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Olympiad)
class OlympiadAdmin(admin.ModelAdmin):
    fields = ('title', 'subject', 'description', 'participating_classes', 'scheduled_date', 'status')
    list_display = ['title', 'subject']
    list_filter = ['subject']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
