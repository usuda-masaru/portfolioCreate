from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Authentication
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.custom_signup, name='signup'),
    
    # Management Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage/', views.manage_menu, name='manage_menu'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('skills/', views.skills_manage, name='skills_manage'),
    path('skills/delete/<int:skill_id>/', views.skill_delete, name='skill_delete'),
    path('experiences/', views.experiences_manage, name='experiences_manage'),
    path('experiences/delete/<int:experience_id>/', views.experience_delete, name='experience_delete'),
    path('projects/', views.projects_manage, name='projects_manage'),
    path('projects/delete/<int:project_id>/', views.project_delete, name='project_delete'),
    path('github/', views.github_manage, name='github_manage'),
    
    # Public Portfolio
    path('<uuid:profile_id>/', views.portfolio_detail, name='detail'),
    path('<uuid:profile_id>/update-github/', views.update_github_profile, name='update_github'),
]