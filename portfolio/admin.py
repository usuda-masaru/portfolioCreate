from django.contrib import admin
from .models import Profile, SkillCategory, Skill, Experience, Project, GitHubProfile


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 1


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1


class GitHubProfileInline(admin.StackedInline):
    model = GitHubProfile
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'created_at']
    search_fields = ['name', 'title', 'email']
    inlines = [SkillInline, ExperienceInline, ProjectInline, GitHubProfileInline]
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_order']
    ordering = ['display_order']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'experience_years', 'profile']
    list_filter = ['category']
    search_fields = ['name', 'profile__name']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_current', 'profile']
    list_filter = ['is_current', 'start_date']
    search_fields = ['title', 'profile__name']
    date_hierarchy = 'start_date'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type', 'created_date', 'is_featured', 'display_order', 'profile']
    list_filter = ['project_type', 'is_featured', 'created_date']
    search_fields = ['title', 'description', 'profile__name']
    date_hierarchy = 'created_date'


@admin.register(GitHubProfile)
class GitHubProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'repositories_count', 'followers_count', 'following_count', 'last_updated']
    search_fields = ['username', 'profile__name']
    readonly_fields = ['last_updated']
