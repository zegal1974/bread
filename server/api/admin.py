from django.contrib import admin

from api.models.models import Actor


class ActorAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']


admin.site.register(Actor, ActorAdmin)
