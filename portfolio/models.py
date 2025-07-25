from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="名前")
    title = models.CharField(max_length=200, verbose_name="職種・肩書き")
    bio = models.TextField(verbose_name="自己紹介")
    email = models.EmailField(verbose_name="メールアドレス")
    location = models.CharField(max_length=100, blank=True, verbose_name="居住地")
    website = models.URLField(blank=True, verbose_name="ウェブサイト")
    twitter = models.URLField(blank=True, verbose_name="Twitter")
    qiita = models.URLField(blank=True, verbose_name="Qiita")
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name="プロフィール画像")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "プロフィール"
        verbose_name_plural = "プロフィール"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('portfolio:detail', kwargs={'profile_id': self.id})


class SkillCategory(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'フロントエンド'),
        ('backend', 'バックエンド'),
        ('infrastructure', 'インフラ'),
        ('database', 'データベース'),
        ('framework', 'フレームワーク'),
        ('cloud', 'クラウド'),
        ('tools', 'ツール'),
        ('other', 'その他'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True, verbose_name="カテゴリ名")
    display_order = models.IntegerField(default=0, verbose_name="表示順")
    
    class Meta:
        verbose_name = "スキルカテゴリ"
        verbose_name_plural = "スキルカテゴリ"
        ordering = ['display_order']
    
    def __str__(self):
        return self.get_name_display()


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="スキル名")
    experience_years = models.IntegerField(verbose_name="経験年数")
    description = models.TextField(blank=True, verbose_name="詳細説明")
    
    class Meta:
        verbose_name = "スキル"
        verbose_name_plural = "スキル"
        ordering = ['category', '-experience_years']
    
    def __str__(self):
        return f"{self.name} ({self.experience_years}年)"


class Experience(models.Model):
    PROCESS_CHOICES = [
        ('requirement', '要件定義'),
        ('design', '設計'),
        ('development', '開発'),
        ('testing', 'テスト'),
        ('deployment', 'デプロイ'),
        ('maintenance', '保守・運用'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=200, verbose_name="案件名")
    start_date = models.DateField(verbose_name="開始日")
    end_date = models.DateField(null=True, blank=True, verbose_name="終了日")
    is_current = models.BooleanField(default=False, verbose_name="現在も継続中")
    description = models.TextField(verbose_name="案件内容")
    role = models.CharField(max_length=100, verbose_name="役割")
    team_size = models.IntegerField(verbose_name="チーム規模")
    technologies = models.TextField(verbose_name="使用技術")
    processes = models.CharField(max_length=200, verbose_name="担当工程")
    achievements = models.TextField(blank=True, verbose_name="成果・実績")
    
    class Meta:
        verbose_name = "経歴"
        verbose_name_plural = "経歴"
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title


class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('web', 'Webアプリケーション'),
        ('mobile', 'モバイルアプリ'),
        ('desktop', 'デスクトップアプリ'),
        ('api', 'API'),
        ('landing', 'ランディングページ'),
        ('other', 'その他'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200, verbose_name="プロジェクト名")
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, verbose_name="種類")
    description = models.TextField(verbose_name="説明")
    image = models.ImageField(upload_to='projects/', verbose_name="プロジェクト画像")
    url = models.URLField(blank=True, verbose_name="URL")
    github_url = models.URLField(blank=True, verbose_name="GitHub URL")
    technologies = models.TextField(verbose_name="使用技術")
    created_date = models.DateField(verbose_name="作成日")
    display_order = models.IntegerField(default=0, verbose_name="表示順")
    is_featured = models.BooleanField(default=False, verbose_name="注目作品")
    
    class Meta:
        verbose_name = "プロジェクト"
        verbose_name_plural = "プロジェクト"
        ordering = ['-is_featured', 'display_order', '-created_date']
    
    def __str__(self):
        return self.title


class GitHubProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='github_profile')
    username = models.CharField(max_length=100, verbose_name="GitHub ユーザー名")
    repositories_count = models.IntegerField(default=0, verbose_name="リポジトリ数")
    followers_count = models.IntegerField(default=0, verbose_name="フォロワー数")
    following_count = models.IntegerField(default=0, verbose_name="フォロー数")
    gists_count = models.IntegerField(default=0, verbose_name="Gist数")
    created_at = models.DateTimeField(null=True, blank=True, verbose_name="アカウント作成日")
    github_bio = models.TextField(blank=True, default='', verbose_name="GitHub Bio")
    github_location = models.CharField(max_length=100, blank=True, default='', verbose_name="GitHub 居住地")
    github_blog = models.URLField(blank=True, default='', verbose_name="GitHub Blog URL")
    language_stats = models.JSONField(default=dict, blank=True, verbose_name="言語統計")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="最終更新")
    
    class Meta:
        verbose_name = "GitHubプロフィール"
        verbose_name_plural = "GitHubプロフィール"
    
    def __str__(self):
        return f"{self.username} のGitHubプロフィール"
