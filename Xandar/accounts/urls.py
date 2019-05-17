from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_page, name='loginapp'),
    path('logout/', views.logout_user, name='logoutapp'),
    path('reset_password/', views.reset_password, name="reset_password"),
]