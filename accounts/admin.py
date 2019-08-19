from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Member, Profile
from .forms import MemberCreationForm, MemberChangeForm

# Member is model for the custom user
class UserAdmin(BaseUserAdmin):
	add_form = MemberChangeForm
	form = MemberChangeForm
	model = Member
	list_display = ['email', 'alt_email', 
	'display_username', 
	'username', 'slug',  'create_dt', 'update_dt']

# Register your models here.
admin.site.register(Member, UserAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)  #we unregister group

