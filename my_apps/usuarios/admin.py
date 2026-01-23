from django.contrib import admin
from my_apps.usuarios.models import Profile, Organization, Membership
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ('user__username', 'location')
    list_per_page = 10
    
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_per_page = 10
    
    
@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('profile', 'organization', 'role', 'joined_at')
    search_fields = ('profile__user__username', 'organization__name', 'role')
    list_filter = ('role',)
    list_per_page = 10