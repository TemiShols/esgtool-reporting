from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register'),
    path('category/', views.select_category, name='category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #   path('redirect-login/', views.login_user_redirect, name='login_redirect'),
]