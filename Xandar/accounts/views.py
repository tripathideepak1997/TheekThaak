from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your views here.
def login_page(request):
    return render(request, 'accounts/login.html')




































































































































































































































































































def check_email(request):
	if request.method == 'POST':
		mail = request.POST.get('email')
		user_email = User.objects.filter(email=mail)

		if user_email:
			request.session['user_email'] = mail
			return redirect('password_reset')
		else:
			return redirect('loginapp')
	else: 
		return render(request, 'accounts/check_mail.html')

def reset_password(request):
	if request.method == 'POST':
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		u = User.objects.get(username__exact='ttn')
		# change :  currently changes for username ttn only. have to make dynamic for authenticated user.

		if password1==password2:
			if u.check_password(request.POST['old_password']):
				u.set_password(password1)
				u.save()
				return redirect('password_reset_complete')
			# change : else : else if old password is wrong
		# change : else : else if new passwords dont match
	else:
		return render(request, 'accounts/reset_password.html')

