from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.





























































































#----------------------------------------Amulya-----------------------------
def login_page(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            User.objects.get(username=username)
            user_authenticated = authenticate(request, username=username, password=password)
            if user_authenticated is not None:
                login(request, user_authenticated)
                return HttpResponse('all set')
            else:
                context = {'message': 'Incorrect Password'}
        except User.DoesNotExist:
                context = {'message': 'No such user exist'}
        return render(request, 'accounts/login.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('accounts:loginapp')


















































































#--------------------------------User Aman------------------------------



































































































#-------------------------------_User Deepak-------------------------
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
