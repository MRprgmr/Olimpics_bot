from django.contrib.admin import SimpleListFilter

from Bot.models import Olympiad


class RegisteredUsers(SimpleListFilter):
    title = "Olympiads"

    parameter_name = 'registered_olympiad'

    def lookups(self, request, model_admin):
        olympiads = Olympiad.objects.all()

        return ((olympiad.id, olympiad.title) for olympiad in olympiads)

    def queryset(self, request, queryset):
        if self.value() is not None:
            olympiad = Olympiad.objects.get(id=self.value())
            custom_list = [user.id for user in olympiad.registered_users.all()]
            return queryset.filter(id__in=custom_list)
