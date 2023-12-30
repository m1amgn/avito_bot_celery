from django.contrib import admin
from .models import Profiles, Users, Chats, AccessTokens

admin.site.register(Profiles)
admin.site.register(Users)


@admin.register(Chats)
class ChatsAdminDate(admin.ModelAdmin):
    readonly_fields = ('created_timestamp',)


@admin.register(AccessTokens)
class AccessTokensAdminDates(admin.ModelAdmin):
    readonly_fields = ('created_timestamp',)
