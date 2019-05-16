from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
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






