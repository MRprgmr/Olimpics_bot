from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class User(models.Model):
    telegram_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=20, blank=False)
    username = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=40, blank=True, null=True)
    grade = models.ForeignKey(Class, on_delete=models.PROTECT, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Olympiad(models.Model):
    title = models.CharField(max_length=64)
    subject = models.ForeignKey(Subject, related_name='olympiads', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    scheduled_date = models.DateField()
    participating_classes = models.ManyToManyField(Class)
    registered_users = models.ManyToManyField(User, related_name='registered_olympiads')

    def __str__(self):
        return self.title
