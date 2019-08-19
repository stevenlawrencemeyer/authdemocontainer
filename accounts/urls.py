from django.contrib.auth.decorators import (login_required, 
    permission_required)
    
from django.urls import path
from django.urls import reverse_lazy

from .views import (IndexView,
    ConfirmRegistrationView, 
    MemberLoginView, 
    RegisterView,
    MemberPasswordChangeView,
    MemberPasswordResetView, 
    MemberPasswordResetConfirm,
    MemberPasswordResetDone, 
    MemberUpdateView,
    ActivateView, 
    ProfileUpdateView,
    ProfileDetailView, 
    validate_user, UnauthAccessView,
    MemberDetailView, EmailChangeView)
    
from django.contrib.auth.views import LogoutView
    
# The app_name also denotes the namespace for the app
app_name = 'accounts'


urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    
    path('register/', RegisterView.as_view(), name='register'),
    
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), 
       name='activate'),
       
    #There are various ways of restricting access to logged in
    #members. Setting login_required in urls is the one
    #I prefer when using class based views 
    path('profile-update/<int:pk>/', 
        login_required(ProfileUpdateView.as_view()), 
        name='profile_update'),

    path('unauthorised-access', UnauthAccessView.as_view(), 
        name='unauthorised_access'),

    path('profile/<int:pk>/', ProfileDetailView.as_view(), 
        name='profile_detail'),

    path('login/', MemberLoginView.as_view(), name='login'),
  
    path('logout/', 
        LogoutView.as_view(next_page=reverse_lazy('home:index')),
        name='logout'),
        
    path('password-change/',
        MemberPasswordChangeView.as_view(), name='password_change'),
        
    path('password-reset/',
		MemberPasswordResetView.as_view(), 
        name='password_reset'),
        
    path('reset/<uidb64>/<token>/',
        MemberPasswordResetConfirm.as_view(), 
        name='password_reset_confirm'),
        
    path('password-reset-done', MemberPasswordResetDone.as_view(),
        name='password_reset_done'),
        
    path('validate-user', validate_user, name='validate_user'),

    path('member-detail/<int:pk>/', 
        login_required(MemberDetailView.as_view()),
        name='member_detail'),

    path('member-update/<int:pk>/',
        login_required(MemberUpdateView.as_view()),
        name='member_update'),
        
    path('confirm-registration',
        ConfirmRegistrationView.as_view(),
        name = 'confirm_registration'),
        
    path('email-change/<int:pk>/',
        login_required(EmailChangeView.as_view()),
        name='email_change'),

]

