from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Skill, Experience, Project, GitHubProfile, SkillCategory


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
            'placeholder': 'ユーザー名'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
            'placeholder': 'パスワード'
        })
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'title', 'bio', 'email', 'location', 'website', 'twitter', 'qiita', 'avatar']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'お名前'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '職種・肩書き'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '自己紹介',
                'rows': 5
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'メールアドレス'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '居住地'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'ウェブサイト'
            }),
            'qiita': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'Qiita URL'
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'Twitter URL'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'accept': 'image/*'
            })
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'name', 'experience_years', 'description']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'スキル名'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '経験年数',
                'min': 0
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '詳細説明',
                'rows': 3
            })
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'start_date', 'end_date', 'is_current', 'description', 'role', 'team_size', 'technologies', 'processes', 'achievements']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '案件名'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'type': 'date'
            }),
            'is_current': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-blue-600 bg-gray-800 border-gray-600 rounded focus:ring-blue-500 focus:ring-2'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '案件内容',
                'rows': 4
            }),
            'role': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '役割'
            }),
            'team_size': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'チーム規模',
                'min': 1
            }),
            'technologies': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '使用技術',
                'rows': 3
            }),
            'processes': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '担当工程'
            }),
            'achievements': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '成果・実績',
                'rows': 3
            })
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'project_type', 'description', 'image', 'url', 'github_url', 'technologies', 'created_date', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'プロジェクト名'
            }),
            'project_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '説明',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'accept': 'image/*'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'プロジェクトURL'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'GitHub URL'
            }),
            'technologies': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': '使用技術',
                'rows': 3
            }),
            'created_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'type': 'date'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-blue-600 bg-gray-800 border-gray-600 rounded focus:ring-blue-500 focus:ring-2'
            })
        }


class GitHubProfileForm(forms.ModelForm):
    class Meta:
        model = GitHubProfile
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'GitHub ユーザー名'
            })
        }