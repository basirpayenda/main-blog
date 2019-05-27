from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_update, name='profile_update'),

]
