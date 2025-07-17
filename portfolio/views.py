from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.forms import modelformset_factory
from .models import Profile, SkillCategory, Skill, Experience, Project, GitHubProfile
from .forms import (ProfileForm, SkillForm, ExperienceForm, ProjectForm, 
                   GitHubProfileForm, CustomAuthenticationForm)
import requests
from django.conf import settings
import json
import time


def fetch_user_language_stats(username):
    """GitHubユーザーの言語統計を取得"""
    try:
        # ユーザーのリポジトリを取得
        repos_url = f"https://api.github.com/users/{username}/repos"
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Portfolio-Django-App'
        }
        repos_response = requests.get(repos_url, params={'per_page': 100}, headers=headers)
        
        if repos_response.status_code != 200:
            return {}
        
        repos = repos_response.json()
        language_totals = {}
        
        # 各リポジトリの言語情報を取得
        for repo in repos:
            if repo.get('fork'):  # フォークは除外
                continue
                
            languages_url = f"https://api.github.com/repos/{username}/{repo['name']}/languages"
            
            # API制限を考慮して少し待機
            time.sleep(0.1)
            
            try:
                lang_response = requests.get(languages_url, headers=headers)
                if lang_response.status_code == 200:
                    languages = lang_response.json()
                    
                    # 言語ごとのバイト数を累積
                    for language, bytes_count in languages.items():
                        if language in language_totals:
                            language_totals[language] += bytes_count
                        else:
                            language_totals[language] = bytes_count
            except requests.RequestException:
                continue
        
        # パーセンテージを計算
        total_bytes = sum(language_totals.values())
        if total_bytes == 0:
            return {}
        
        language_percentages = {}
        for language, bytes_count in language_totals.items():
            percentage = (bytes_count / total_bytes) * 100
            language_percentages[language] = {
                'bytes': bytes_count,
                'percentage': round(percentage, 2)
            }
        
        # 使用量の多い順にソート
        sorted_languages = dict(sorted(language_percentages.items(), 
                                     key=lambda x: x[1]['percentage'], 
                                     reverse=True))
        
        # 上位10言語のみ返す
        return dict(list(sorted_languages.items())[:10])
        
    except requests.RequestException:
        return {}


def portfolio_detail(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    skills_by_category = {}
    
    categories = SkillCategory.objects.all()
    for category in categories:
        skills = Skill.objects.filter(profile=profile, category=category)
        if skills.exists():
            skills_by_category[category] = skills
    
    experiences = Experience.objects.filter(profile=profile)
    projects = Project.objects.filter(profile=profile)
    github_profile = None
    
    try:
        github_profile = GitHubProfile.objects.get(profile=profile)
    except GitHubProfile.DoesNotExist:
        pass
    
    
    context = {
        'profile': profile,
        'skills_by_category': skills_by_category,
        'experiences': experiences,
        'projects': projects,
        'github_profile': github_profile,
        'skills_count': sum(len(skills) for skills in skills_by_category.values()),
        'experiences_count': experiences.count(),
        'projects_count': projects.count(),
    }
    
    return render(request, 'portfolio/detail.html', context)


def update_github_profile(request, profile_id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, id=profile_id)
        
        try:
            github_profile = GitHubProfile.objects.get(profile=profile)
            username = github_profile.username
            
            # GitHub API call with rate limit handling
            api_url = f"https://api.github.com/users/{username}"
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Portfolio-Django-App'
            }
            response = requests.get(api_url, headers=headers)
            
            if response.status_code == 403:
                # レート制限チェック
                if 'rate limit exceeded' in response.text.lower():
                    return JsonResponse({'success': False, 'message': 'GitHub APIのレート制限に達しました。しばらく待ってから再試行してください。'})
                else:
                    return JsonResponse({'success': False, 'message': 'GitHub APIへのアクセスが拒否されました。'})
            elif response.status_code == 200:
                data = response.json()
                github_profile.repositories_count = data.get('public_repos', 0)
                github_profile.followers_count = data.get('followers', 0)
                github_profile.following_count = data.get('following', 0)
                github_profile.gists_count = data.get('public_gists', 0)
                github_profile.github_bio = data.get('bio') or ''
                github_profile.github_location = data.get('location') or ''
                github_profile.github_blog = data.get('blog') or ''
                # アカウント作成日の処理
                created_at_str = data.get('created_at')
                if created_at_str:
                    from datetime import datetime
                    github_profile.created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                
                # 言語統計を取得
                try:
                    language_stats = fetch_user_language_stats(username)
                    github_profile.language_stats = language_stats
                except Exception as e:
                    print(f"Language stats error: {e}")
                    github_profile.language_stats = {}
                
                github_profile.save()
                
                return JsonResponse({'success': True, 'message': 'GitHub情報を更新しました'})
            else:
                return JsonResponse({'success': False, 'message': 'GitHub情報の取得に失敗しました'})
                
        except GitHubProfile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'GitHubプロフィールが設定されていません'})
    
    return JsonResponse({'success': False, 'message': '無効なリクエストです'})


def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('portfolio:dashboard')
            else:
                messages.error(request, 'ユーザー名またはパスワードが間違っています。')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'portfolio/login.html', {'form': form})


@login_required
def custom_logout(request):
    logout(request)
    return redirect('portfolio:login')


def custom_signup(request):
    """Portfolio用のカスタムサインアップビュー"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # プロフィールを自動作成
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'アカウントが正常に作成されました。ログインしてください。')
            return redirect('portfolio:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'portfolio/signup.html', {'form': form})


@login_required
def dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'profile': profile,
        'skills_count': Skill.objects.filter(profile=profile).count() if profile else 0,
        'experiences_count': Experience.objects.filter(profile=profile).count() if profile else 0,
        'projects_count': Project.objects.filter(profile=profile).count() if profile else 0,
    }
    
    return render(request, 'portfolio/dashboard.html', context)


@login_required
def profile_edit(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'プロフィールが保存されました。')
            return redirect('portfolio:dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'portfolio/profile_edit.html', {'form': form, 'profile': profile})


@login_required
def skills_manage(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, '先にプロフィールを作成してください。')
        return redirect('portfolio:profile_edit')
    
    skills = Skill.objects.filter(profile=profile)
    
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        
        if edit_id:
            # 編集モード
            try:
                skill = Skill.objects.get(id=edit_id, profile=profile)
                form = SkillForm(request.POST, instance=skill)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'スキルが更新されました。')
                    return redirect('portfolio:skills_manage')
            except Skill.DoesNotExist:
                messages.error(request, 'スキルが見つかりません。')
        else:
            # 新規追加モード
            form = SkillForm(request.POST)
            if form.is_valid():
                skill = form.save(commit=False)
                skill.profile = profile
                skill.save()
                messages.success(request, 'スキルが追加されました。')
                return redirect('portfolio:skills_manage')
    else:
        form = SkillForm()
    
    return render(request, 'portfolio/skills_manage.html', {
        'form': form, 
        'skills': skills, 
        'profile': profile
    })


@login_required
def skill_delete(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, profile__user=request.user)
    skill.delete()
    messages.success(request, 'スキルが削除されました。')
    return redirect('portfolio:skills_manage')


@login_required
def experiences_manage(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, '先にプロフィールを作成してください。')
        return redirect('portfolio:profile_edit')
    
    experiences = Experience.objects.filter(profile=profile)
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = profile
            experience.save()
            messages.success(request, '経歴が追加されました。')
            return redirect('portfolio:experiences_manage')
    else:
        form = ExperienceForm()
    
    return render(request, 'portfolio/experiences_manage.html', {
        'form': form, 
        'experiences': experiences, 
        'profile': profile
    })


@login_required
def experience_delete(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id, profile__user=request.user)
    experience.delete()
    messages.success(request, '経歴が削除されました。')
    return redirect('portfolio:experiences_manage')


@login_required
def projects_manage(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, '先にプロフィールを作成してください。')
        return redirect('portfolio:profile_edit')
    
    projects = Project.objects.filter(profile=profile)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = profile
            project.save()
            messages.success(request, 'プロジェクトが追加されました。')
            return redirect('portfolio:projects_manage')
    else:
        form = ProjectForm()
    
    return render(request, 'portfolio/projects_manage.html', {
        'form': form, 
        'projects': projects, 
        'profile': profile
    })


@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id, profile__user=request.user)
    project.delete()
    messages.success(request, 'プロジェクトが削除されました。')
    return redirect('portfolio:projects_manage')


@login_required
def github_manage(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, '先にプロフィールを作成してください。')
        return redirect('portfolio:profile_edit')
    
    try:
        github_profile = GitHubProfile.objects.get(profile=profile)
    except GitHubProfile.DoesNotExist:
        github_profile = None
    
    if request.method == 'POST':
        form = GitHubProfileForm(request.POST, instance=github_profile)
        if form.is_valid():
            github_profile = form.save(commit=False)
            github_profile.profile = profile
            
            # GitHub APIから情報を取得
            username = github_profile.username
            api_url = f"https://api.github.com/users/{username}"
            try:
                headers = {
                    'Accept': 'application/vnd.github.v3+json',
                    'User-Agent': 'Portfolio-Django-App'
                }
                response = requests.get(api_url, headers=headers)
                if response.status_code == 403:
                    if 'rate limit exceeded' in response.text.lower():
                        messages.warning(request, 'GitHub APIのレート制限に達しました。しばらく待ってから再試行してください。')
                    else:
                        messages.warning(request, 'GitHub APIへのアクセスが拒否されました。')
                elif response.status_code == 200:
                    data = response.json()
                    github_profile.repositories_count = data.get('public_repos', 0)
                    github_profile.followers_count = data.get('followers', 0)
                    github_profile.following_count = data.get('following', 0)
                    github_profile.gists_count = data.get('public_gists', 0)
                    github_profile.github_bio = data.get('bio') or ''
                    github_profile.github_location = data.get('location') or ''
                    github_profile.github_blog = data.get('blog') or ''
                    # アカウント作成日の処理
                    created_at_str = data.get('created_at')
                    if created_at_str:
                        from datetime import datetime
                        github_profile.created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                    
                    # 言語統計を取得
                    try:
                        language_stats = fetch_user_language_stats(username)
                        github_profile.language_stats = language_stats
                    except Exception as e:
                        print(f"Language stats error: {e}")
                        github_profile.language_stats = {}
                    
                    github_profile.save()
                    messages.success(request, 'GitHubプロフィールが保存されました。')
                else:
                    messages.warning(request, 'GitHubユーザーが見つかりませんでした。')
            except requests.RequestException:
                messages.warning(request, 'GitHub APIにアクセスできませんでした。')
            
            return redirect('portfolio:github_manage')
    else:
        form = GitHubProfileForm(instance=github_profile)
    
    return render(request, 'portfolio/github_manage.html', {
        'form': form, 
        'github_profile': github_profile, 
        'profile': profile
    })
