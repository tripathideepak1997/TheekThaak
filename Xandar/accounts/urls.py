from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='loginapp'),
    path('reset_password/', views.reset_password, name="reset_password"),
]