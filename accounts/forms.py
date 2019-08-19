from django import forms
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
    AuthenticationForm)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from  django.contrib.auth import get_user_model, authenticate
from .models import Member, Profile
from django.contrib.auth.forms import PasswordChangeForm

#Important step. We need to get the user model
User = get_user_model()

class EmailChangeForm(forms.Form):
	email = forms.EmailField(max_length=100, required=False)
	alt_email = forms.EmailField(max_length=100, required=False)
	use_alt_email = forms.BooleanField(required=False)


class MemberUpdateForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = ('display_username', 'first_name', 
		'mid_initials', 'last_name',)
		labels = {'display_username':'Username',
		    'first_name':'First Name',
		    'mid_initials':'Middle Initials',
		    'last_name':'Last Name',}
	def __init__(self, *args, **kwargs):
		# We add the class "alpha" to username, first_name,
		# mid_initials and last_name. These fields are alpha only and
		# we use the class to validate the form with javascript
		list1 = ['display_username', 'first_name', 'mid_initials', 
		'last_name']
		super().__init__(*args, **kwargs)
		for f in self.visible_fields():
			if f.name in list1:
				f.field.widget.attrs['class'] = 'alpha'


class MemberPasswordChangeForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['new_password2'].label = 'Retype new password'


# We subclass the Django UserCreationForm
# Remember that password is not part of the Member model
# We add two fields, password1 & password2
# with labels "password" and "confirm password"

# The MemberCreationForm class has three functions:
# (1)   __init__
#
# (2)  clean_password2 that checks whether 
#      password1 = password2
#
# (3)  save which, inter alia, sets the password.
#      This tells Django what the password is 
#      which Django than hashes

class MemberCreationForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput,
	    label ='Password')
	password2 = forms.CharField(widget=forms.PasswordInput,
	    label='Confirm password')
	class Meta:
		model = User
		fields = ('email', 'password1', 'password2',
		'display_username', 'first_name', 'mid_initials', 'last_name',
		'alt_email')
		labels = {'email':'**Email',
		    'display_username':'**Username',
		    'first_name':'**First Name',
		    'mid_initials':'Middle Initials',
		    'last_name':'**Last Name',
		    'alt_email':'**Alternative Email Address'}
	def __init__(self, *args, **kwargs):
		# We add the class "alpha" to display_username, first_name,
		# mid_initials and last_name. These fields are alpha only and
		# we use the class to validate the form with javascript
		list1 = ['display_username', 'first_name', 'mid_initials', 
		'last_name']
		super().__init__(*args, **kwargs)
		for f in self.visible_fields():
			if f.name in list1:
				f.field.widget.attrs['class'] = 'alpha'
			
	def clean_password2(self):
		# Check that the two password entries match
		# We also do this client-side using Javascript
		# But this is how it's done in Django
		print('in forms clean_password2   ')
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		print('passwords did match $$$$$$$$$$$$$$$$$$$$$$$')
		return password2


	def save(self, commit=True):
		print('In forms save **************')
		# Save the provided password in hashed format
		user = super().save(commit=False)
		# sets the password 
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user	
		
class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile	
		fields = ('profile_pic', 'pic_caption', 'city', 'country', 
		'website', 'about')
		labels = {'profile_pic':'Profile Picture',
		    'pic_caption':'Caption', 
		    'city':'City',
		    'country':'Country',
		    'website':'Website', 'about':'Tell us about yourself'}
		widgets = {'about':forms.Textarea}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for f in self.visible_fields():
			if f.name == 'about':
				f.field.widget.attrs['class'] = 'slm-textarea'
			elif f.name == 'profile_pic':
				f.field.widget.attrs['class'] = 'slm-profile-pic'

		


class MemberChangeForm(UserChangeForm):
	class Meta:
		model = User
		fields = ('email', 'username', 'first_name', 'mid_initials',
		    'last_name')
		 
class MemberLoginForm(forms.Form):
	loginfield = forms.CharField(max_length = 120,
	    label='Login with username or email')
	    
	password1 = forms.CharField(widget=forms.PasswordInput,
	    label='Password')
	


		
		
