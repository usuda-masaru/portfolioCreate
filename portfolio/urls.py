from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Authentication
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.custom_signup, name='signup'),
    
    # Management
    path('manage/', views.manage_menu, name='manage_menu'),
    
    # Public Portfolio
    path('<uuid:profile_id>/', views.portfolio_detail, name='detail'),
    path('<uuid:profile_id>/update-github/', views.update_github_profile, name='update_github'),
]