import datetime as dt
import sys
from django.contrib import messages
from django.contrib.auth.hashers import check_password #use to check password manually
from django.contrib.auth import (get_user_model, login, 
    update_session_auth_hash)
    
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import (PasswordChangeView, 
    PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView,
    PasswordResetDoneView, LoginView, LogoutView)

from django.core.mail import send_mail
    
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text

from django.utils.http import (urlsafe_base64_encode, 
   urlsafe_base64_decode)

from django.utils.http import (urlsafe_base64_decode,)


from django.utils.text import slugify
    
from django.views.generic import (TemplateView, CreateView, View, 
    DetailView, ListView, FormView, UpdateView)

from .forms import (MemberCreationForm, ProfileUpdateForm,
    MemberPasswordChangeForm, MemberLoginForm, MemberUpdateForm,
    EmailChangeForm)

from .models import Member, Profile

from home.utils import (account_activation_token, sendmail_utility,
    generate_random_str)


# A valuable resource:
# Classy Class-Based Views.
# https://ccbv.co.uk/


#IMPORTANT!
#This points Django to the user model which, in this case, is
#accounts.member

User = get_user_model()

#This information is restricted to the owner of the data
#In URLs you will see "login_required" but that is not enough
class MemberDetailView(DetailView):
	template_name = 'accounts/member_detail.html'
	model = Member
	context_object_name = 'member'
	
	def dispatch(self, request, *args, **kwargs):
		context = super().dispatch(request, *args, **kwargs)
		logged_in_user_pk = request.user.pk  #this is pk of the logged in user
		owner_pk = context.context_data['member'].pk # this is pk of the owner of the data
		
		#Only the owner of this data is allowed a view
		#If owner's pk != logged in user's pk we redirect
		#to "unauthorised access attempted"
		#Also see comment on permissions below
		
		if str(owner_pk) != str(logged_in_user_pk): 
			url = reverse_lazy('accounts:unauthorised_access')
			return HttpResponseRedirect(url)
		return context	
	
# PERMISSIONS
# We have a simple permission system. With the exception of a
# super user only the owner may view or alter certain data.
# In a large, multi-user installation there will be groups
# of people with different levels of access and different powers
# to addm change or delete data. Django has a powerful permissions
# system.
# See: 
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication


	
#This allows changes to most member details
#There is a separate protocol for changing email address
class MemberUpdateView(UpdateView):
	model = Member
	template_name = 'accounts/member_update.html'
	form_class = MemberUpdateForm
	success_url = reverse_lazy('home:index')
	def dispatch(self, request, *args, **kwargs):
		context = super().dispatch(request, *args, **kwargs)
	
		logged_in_user_pk = request.user.pk
		
		#Only the owner of this data may modify it
		#So, again if owner's pk does not match user's pk
		#we redirect to "unauthorised access attempted"

		#This class is used twice, first for "get" and 
		#then for "post". Only the "get" access has the 
		#"context_data" attribute
		
		if hasattr(context, 'context_data'):
			owner_pk = context.context_data['member'].pk
			if str(owner_pk) != str(logged_in_user_pk):
				url = reverse_lazy('accounts:unauthorised_access')
				return HttpResponseRedirect(url)
			return context 
			
		#We send an email to the user confirming that changes 
		#have been made
		#If we get this far we know that logged in user is the
		#owner of the data.
		
		user = User.objects.get(pk=logged_in_user_pk)
		to_email = user.email

		#setup email
		
		from_email = 'support@site.com'
		username = user.display_username
		msg = 'Hi ' + username + ' changes were made to your login '
		msg+= ' details. If this was not you contact user support '
		msg+= 'immediately!'
		print('msg= ' + msg)
		mail_subject = 'Changes to your login detail'
		
		send_mail(mail_subject, msg, from_email, [to_email,])

		url = reverse_lazy('accounts:member_detail', \
		    args=[request.user.pk])
		return HttpResponseRedirect(url)


# This allows the member to change email addresses
# We send a confirmation email to the CURRENT addresses
# NOT the new addresses
# The account is decativated until confirmation is received

class EmailChangeView(UpdateView):
	def get(self, request, pk):
		print('in get of EmailChangeView')
		
		# first check that logged in user matches owner of data
		logged_in_user_pk = request.user.pk
		if logged_in_user_pk != pk:
			url = reverse_lazy('accounts:unauthorised_access')
			return HttpResponseRedirect(url)
			
		form = EmailChangeForm
		
		#Setup context
		email = request.user.email
		alt_email = request.user.alt_email
		x = {'email':email, 'alt_email':alt_email}
		# context name is tstuff, short for template stuff
		context = {'tstuff':x} 
		return render(request, 'accounts/email_change.html', context)

	def post(self, request, pk):
		print()
		print('in post of EmailChangeView')
		form = EmailChangeForm(data=request.POST)
		#checking whether form is valid triggers cleaning data
		if form.is_valid():
			email = form.clean().get('email')
			alt_email = form.clean().get('alt_email')
			use_alt_email = form.clean().get('use_alt_email')
			
			#update member record
			user = User.objects.get(pk=pk)
			user.is_active = False  #account inactivated
			
			# we set to_email address for confirmatory email
			to_email = user.email
			if use_alt_email == True:
				to_email = user.alt_email
			
			if email != '':
				user.email = email
			if alt_email != '':
				user.alt_email = alt_email 
			user.save()
			
			mail_subject = 'Re-activate.' 
			msg1 = "Hello"
			msg2 = 'Please confirm your NEW email address by activating '
			msg2+= 'this link:'
			domplus = '/accounts/activate'
			
			sendmail_utility(mail_subject, domplus, msg1, msg2, 
			to_email, request.user, account_activation_token,
			request)
			
			#return to home page
			url = reverse_lazy('home:index')
			return HttpResponseRedirect(url)
		else:
			print('form is not valid WERTYUIOP{')
			print()	# this is a deliberate lose end	


# We use the "vanilla" subclass 
class MemberPasswordChangeView(PasswordChangeView):
	template_name = 'accounts/password_change.html'
	form_class = MemberPasswordChangeForm #We do not use the default
	success_url = reverse_lazy('home:index')


# Anyone may view profile information 
# But only the owner can change it (See below)
class ProfileDetailView(DetailView):
	model = Profile
	template_name = 'accounts/profile_detail.html'
	context_object_name = 'profile'
	


# Only the owner may change profile data

class ProfileUpdateView(UpdateView):
	template_name = 'accounts/profile_update.html'
	form_class = ProfileUpdateForm
	model = Profile
	
	def dispatch(self, *args, **kwargs):
		
		print('entering dispatch of ProfileUpdateView')
		
		context = super().dispatch(*args, **kwargs)
		
		#We hit this code twice, first during the "get phase" and 
		#then during the "post phase". During the "get phase" 
		#context will have the attribute "_request"
		
		#We could split this view into a "def get" and "def post" 
		#which is probably better practice but I wanted to
		#demonstrate that we could do it all in dispatch

		if hasattr(context, '_request'):
			logged_in_user_pk = context._request.user.pk
			profile_user_pk = context.context_data['object'].user.pk
			# check that logged in user is owner of data
			if logged_in_user_pk != profile_user_pk:
				url = reverse_lazy('accounts:unauthorised_access')
				return HttpResponseRedirect(url)
		return context



# We direct users who attempt unauthorised access here
class UnauthAccessView(TemplateView):
	template_name = 'accounts/unauthorised_access.html'



#This is the hard part - registering a new user
#We subclass the most basic generic view 
#from django.views.generic import View
#It supports the following http methods:
#'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'
#Which means so do all its subclasses
#In RegisterView we shall change 'get' and 'post'			

# process is as follows:
# 1)  We display the registration form using RegisterView

# 2)  After a successful form submission the prospective user
#     Is redirected to a "confirm registration page" using
#     ConfirmRegistrationView

# 3)  On clicking the confirmatory link or pasting it into
#     The URL box the user is directed to the welcome page
#     using the ActivateView

# So the progression is RegisterView -> ConfirmRegistrationView ->
# -> ActivateView
# In addition the validate_user view is used by Ajax in form validation

# As much form validation as possible is done
# using javascript


class RegisterView(View):  
	def get(self, request):
		form = MemberCreationForm
		context = {'form':form}
		return render(request, 'accounts/register.html', context)
	def post(self, request):
		form = MemberCreationForm(request.POST)
		
		if form.is_valid():
			user = form.save(commit=False)
			#We create the synthetic username and slug
			z = slugify(user.display_username + ' ' + user.email)
			user.slug = z
			curr_dt = dt.datetime.now()
			fmt = '%d %b %Y %H %M %S'
			curr_dt_fmt = curr_dt.strftime(fmt)
			z = slugify(z + ' ' + curr_dt_fmt)
			z+= generate_random_str()
			
			#The synthetic username comprising the slugified
			#display_username, email date, time and 32 random
			#characters has now been generated 
			user.username = z
			
			#The default as defined in the Member model is
			#is_active = 'True'
			#However as we require an authentication email we set
			#is_active = False 
			user.is_active = False
			user.save()

			#generate the confirmation email
			#msg1 and msg2 are two parts of the message
			#to be included in the confirmatory email
			mail_subject = 'Activate.' 
			msg1 = "Hello"
			msg2 = 'Please confirm your email address by activating '
			msg2+= 'this link:'
			domplus = '/accounts/activate'
			to_email = form.cleaned_data.get('email') #only access cleaned data
			#We use sendmail_utility 
			#See util.py in the home app folder
			sendmail_utility(mail_subject, domplus, msg1, msg2,
			to_email, user, account_activation_token, request) 
			# The user is directed here after completing the 
			# registration form
			url = reverse_lazy('accounts:confirm_registration')
			return HttpResponseRedirect(url)
		else:
			# If submission fails go back to the form
			context = {'form':form}
			return render(request, 'accounts/register.html', context)


#The prospective user is directed here after completing
#The registration form

class ConfirmRegistrationView(TemplateView):
	template_name = 'accounts/confirm_registration.html'
	
#The prospective user is directed to the Activate View on clicking
#the link in the confirmatory email
#We override the get method
#(This is the really tricky bit)  
class ActivateView(View):
	# We try to decode the activation link we generate in 
	# the RegisterView
	def get(self, request, uidb64, token):

		try:
			uid = force_text(urlsafe_base64_decode(uidb64))

			#If we have correctly decoded uid we get the id of the
			# User object
			user = User.objects.get(pk = uid)
			
		except(TypeError, ValueError, OverflowError, User.DoesNotExist):
			print('bombed out!!!!!!!!!!!!!!!!!!!!!!!!')
			print()
			user = None
	
		z = account_activation_token.check_token(user, token)

		if user is not None:
			# the token and the user match
			#activate user and login
			user.is_active = True
			user.save()
			#Login the user NB: Many websites require user to login
			#manually. 
			login(request, user)
			return render(request, 'accounts/welcome.html', {})

			
class IndexView(TemplateView):
	template_name = 'accounts/index.html'

#We use the standard Django classes for this
#The progression is:
# MemberPasswordResetView -> MemberPasswordResetDone
# -> MemberPasswordResetConfirm
class MemberPasswordResetView(PasswordResetView):
	template_name = 'accounts/password_reset.html'
	email_template_name = 'accounts/password_reset_email.html'
	subject_template_name = 'accounts/password_reset_subject.txt'
	from_email = 'meyer@meyer.com'	
	success_url = reverse_lazy('accounts:password_reset_done')
	
	
class MemberPasswordResetConfirm(PasswordResetConfirmView):
	template_name = 'accounts/password_reset_confirm.html'	
	success_url = reverse_lazy('accounts:login')


class MemberPasswordResetDone(TemplateView):
	template_name = 'accounts/password_reset_done.html'


# THE AJAX FUNCTION
def validate_user(request):
	
	#In this function we check whether a particular
	#email or username already exists on the database
	#If a match is found we set a boolean variable,
	#x = True
	#If there is no match we set
	#x = False 

	print('in validate_use')
	print()
	
	# This is used by the jQuery Ajax function
	# See regFormAjax.js in static/js folder
	# It is used to prevent duplication of 
	# email addresses and display_usernames
	
	#testvar is the variable, either an email or
	#a username, to be checked
	
	testvar = request.GET.get('testvar', None)
	print('testvar')
	print(testvar)
	print()
	#check var has the values 'email' or 'username'
	checkvar = request.GET.get('checkvar', None)
	print('checkvar')
	print(checkvar)
	
	x = False #default for x is false
	print('x')
	print(x)
	print()
	
	if checkvar == 'email': #We are checcking if email exists
		
		# Here we check that the email in the form
		# is not equal to any other primary email 
		
		x1 = Member.objects.filter(email__iexact=testvar)
		print('x1')
		print(x1.exists()) #Will be true if record with email exists
		print()
		
		# Here we check that the email in the form is not equal
		# to any other alternate email on the database

		x2 = Member.objects.filter(alt_email__iexact=testvar)
		print('x2')
		print(x2.exists()) # cf x1
		print()
		# ALL email addresses on the database must be unique

		# x is a boolean. If it is true the Javascript 
		# routine know that a duplicate has been found on 
		# the database.
		
		#Not the OR condition
		
		if x1.exists() or x2.exists(): #if either email exists x = True
			x = True
			print('x')
			print(x)
			print()
		
	elif checkvar == 'username': #We are checking if display username exists
		x1 = Member.objects.filter(display_username__iexact=testvar)
		if x1.exists():
			x=True

	# if x = True then email or display_username already
	# exists on the database
	
	print('x again')
	print(x)

	data = {
	    'is_taken':x
	}
	return JsonResponse(data) #return the data to javascript in Json format


# I have checked password manually just to demonstrate
# how it is done. In a live implmenetation leave it
# to Django
class MemberLoginView(View):
	
	def get(self, request):
		form = MemberLoginForm
		context = {'form':form}
		z = render(request, 'accounts/login.html', context)
		return z
		
	def post(self, request):
		form = MemberLoginForm(request.POST)
		if form.is_valid(): #testing whether form is valid produces cleaned data
			password1 = form.cleaned_data.get('password1')
			xlogin = form.cleaned_data.get('loginfield')
		# member can login with username or email
		# first try with display_username
		try:
			print('first try')
			print()
			memb = Member.objects.get(display_username=xlogin)
		# next try with email address
		except Exception as e:
			try:
				print('2nd try')
				print()
				memb = Member.objects.get(email=xlogin)
			except Exception as e:
				# if both attempts fail go back to login form
				print('2nd except')
				print()
				url = reverse_lazy('accounts:password_reset')
				context = {'form':form, 'url':url}
				return render(request, 'accounts/login.html', context)					
		#check password
		password = memb.password
		check = check_password(password1, password)
		
		if check == False or memb.is_active == False:
			url = reverse_lazy('accounts:password_reset')
			context = {'form':form, 'url':url}
			return render(request, 'accounts/login.html', context)
		else:
			login(request, memb)
			return render(request, 'home/index.html', {})						


	

				

			
			


	
	
		
	

