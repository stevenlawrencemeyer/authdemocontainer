import random
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils import six
from django.utils.encoding import force_bytes, force_text
from django.utils.http import (urlsafe_base64_encode, 
    urlsafe_base64_decode)

# So what is a Django token?
# It is a way of identifying yourself
# See also:
# https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()

def sendmail_utility(mail_subject, domplus, msg1, msg2, to_email, user, 
    account_activation_token, request):
		
		# See the output in console log
		# Interesting
		# DO NOT DO THIS IN A LIVE IMPLEMENTATION!
		 
		print('in sendmail_utility_utility *************************')
		print()
		print('account activation token')
		print(account_activation_token)
		print()
		print(dir(account_activation_token))
		print()
		print('account_activation_token.secret')
		print(account_activation_token.secret)
		print()
		
		#send email with token
		#we want a URI string that looks like this:
		# https://(site url)/accounts/activate/user id/token/
		#get current site provides the site url
		current_site = get_current_site(request)
		dom = current_site.domain
		#dom is a string with the site url
		#we add accounts and activate
		dom+= domplus
		#we encode the user id as bytes
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		print('uid= ' + str(uid))
		print(type(uid))
		#uid_str is the string version of uid
		uid_str = str(uid)
		#massage uid_str to remove some unwanted characters
		uid_str = uid_str.replace("b'", "").replace("'","")
		#get the token
		token = account_activation_token.make_token(user)
		#act_link is the actual activation link
		act_link = dom + '/' + uid_str + '/' + str(token)
		#Let's print it to the console
		print(act_link)
	
		z = msg1 + ' ' + user.display_username + ' ' + msg2 + ' '
		message = " {0} \n {1}".format(z, act_link)
		
		#We got the wannabe member's email address from the form's
		#cleaned_data
		#to_email = form.cleaned_data.get('email')
		email = EmailMessage(mail_subject, message, to=[to_email])
		email.send()

def generate_random_str():
	base_str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY\
	    Z0123456789$%^&*()_-+={[}]:;<>~|'
	str_len = 32
	n = len(base_str)
	z = ''
	for i in range(str_len):
		k = random.randint(0, n-1)
		z+= base_str[k]
	return z
