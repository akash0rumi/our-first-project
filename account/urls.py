from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('user_login/', views.user_login, name = 'user_login'),
    path('logout/', views.user_logout, name = 'user_logout'),
    path('user_profile/', views.user_profile, name = 'user_profile'),
]
