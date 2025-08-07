from django.contrib import admin
from app_profile.models.options_model import ValueTagModel, HobbyTagModel, CommunicationTagModel
from app_profile.models.personality_model import PersonalityModel
from app_profile.models.profile_model import ProfileModel

class ValueTagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)

class HobbyTagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)

class CommunicationTagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)

class PersonalityAdmin(admin.ModelAdmin):
    list_display = ('account__account_id', 'organization__organization_id')
    search_fields = ('account__account_id', 'organization__organization_id')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('account__account_id', 'organization__organization_id')
    search_fields = ('account__account_id', 'organization__organization_id')


admin.site.register(ValueTagModel, ValueTagAdmin)
admin.site.register(HobbyTagModel, HobbyTagAdmin)
admin.site.register(CommunicationTagModel, CommunicationTagAdmin)
admin.site.register(PersonalityModel, PersonalityAdmin)
admin.site.register(ProfileModel, ProfileAdmin)