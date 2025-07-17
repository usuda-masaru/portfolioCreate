from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio.models import Profile, SkillCategory, Skill, Experience, Project, GitHubProfile
from datetime import date


class Command(BaseCommand):
    help = 'Setup initial data for portfolio'

    def handle(self, *args, **options):
        # Create skill categories
        categories = [
            ('frontend', 'フロントエンド', 1),
            ('backend', 'バックエンド', 2),
            ('infrastructure', 'インフラ', 3),
            ('database', 'データベース', 4),
            ('framework', 'フレームワーク', 5),
            ('cloud', 'クラウド', 6),
            ('tools', 'ツール', 7),
            ('other', 'その他', 8),
        ]
        
        for name, display_name, order in categories:
            category, created = SkillCategory.objects.get_or_create(
                name=name,
                defaults={'display_order': order}
            )
            if created:
                self.stdout.write(f'Created category: {display_name}')
        
        # Create sample user and profile
        user, created = User.objects.get_or_create(
            username='sample_engineer',
            defaults={
                'email': 'sample@example.com',
                'first_name': 'Sample',
                'last_name': 'Engineer'
            }
        )
        
        if created:
            self.stdout.write('Created sample user')
        
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'name': 'サンプル エンジニア',
                'title': 'フルスタックエンジニア',
                'bio': '10年以上のWeb開発経験を持つフルスタックエンジニアです。フロントエンドからバックエンド、インフラまで幅広く対応可能です。',
                'email': 'sample@example.com',
                'location': '東京都',
                'website': 'https://example.com',
                'twitter': 'https://twitter.com/sample',
                'qiita': 'https://qiita.com/sample',
            }
        )
        
        if created:
            self.stdout.write('Created sample profile')
            
            # Add skills
            skills_data = [
                ('JavaScript', 'frontend', 5, 4),
                ('TypeScript', 'frontend', 3, 3),
                ('React', 'framework', 4, 4),
                ('Vue.js', 'framework', 2, 2),
                ('Python', 'backend', 6, 4),
                ('Django', 'framework', 4, 3),
                ('FastAPI', 'framework', 2, 3),
                ('PostgreSQL', 'database', 5, 3),
                ('MySQL', 'database', 3, 3),
                ('Docker', 'infrastructure', 3, 3),
                ('AWS', 'cloud', 4, 3),
                ('Git', 'tools', 8, 4),
            ]
            
            for skill_name, category_name, years, proficiency in skills_data:
                category = SkillCategory.objects.get(name=category_name)
                Skill.objects.create(
                    profile=profile,
                    category=category,
                    name=skill_name,
                    experience_years=years,
                    proficiency=proficiency
                )
            
            self.stdout.write('Created sample skills')
            
            # Add experiences
            experiences_data = [
                {
                    'title': 'ECサイト開発プロジェクト',
                    'company': 'テックカンパニー株式会社',
                    'start_date': date(2022, 4, 1),
                    'end_date': date(2024, 3, 31),
                    'is_current': False,
                    'description': '大規模ECサイトの開発・運用プロジェクトに参加。React+TypeScript、Django REST Framework、PostgreSQLを使用。',
                    'role': 'テックリード',
                    'team_size': 8,
                    'technologies': 'React, TypeScript, Django, PostgreSQL, Docker, AWS',
                    'processes': '要件定義, 設計, 開発, テスト, デプロイ',
                    'achievements': 'サイト速度30%向上、売上20%増加に貢献'
                },
                {
                    'title': '社内システム開発',
                    'company': 'イノベーション株式会社',
                    'start_date': date(2020, 1, 1),
                    'end_date': date(2022, 3, 31),
                    'is_current': False,
                    'description': '社内業務効率化のためのWebアプリケーション開発。Vue.js、FastAPI、MySQLを使用。',
                    'role': 'フルスタックエンジニア',
                    'team_size': 4,
                    'technologies': 'Vue.js, FastAPI, MySQL, Docker',
                    'processes': '要件定義, 設計, 開発, テスト',
                    'achievements': '業務効率50%向上、残業時間削減'
                }
            ]
            
            for exp_data in experiences_data:
                Experience.objects.create(profile=profile, **exp_data)
            
            self.stdout.write('Created sample experiences')
            
            # Add projects
            projects_data = [
                {
                    'title': 'タスク管理アプリ',
                    'project_type': 'web',
                    'description': 'チーム向けのタスク管理Webアプリケーション。リアルタイム通知機能付き。',
                    'url': 'https://example.com/taskapp',
                    'github_url': 'https://github.com/sample/taskapp',
                    'technologies': 'React, TypeScript, Django, PostgreSQL, WebSocket',
                    'created_date': date(2023, 6, 1),
                    'is_featured': True,
                    'display_order': 1
                },
                {
                    'title': 'ポートフォリオサイト',
                    'project_type': 'landing',
                    'description': '個人ポートフォリオサイト。レスポンシブデザイン対応。',
                    'url': 'https://example.com/portfolio',
                    'github_url': 'https://github.com/sample/portfolio',
                    'technologies': 'Next.js, TailwindCSS, TypeScript',
                    'created_date': date(2023, 3, 1),
                    'is_featured': False,
                    'display_order': 2
                }
            ]
            
            for proj_data in projects_data:
                Project.objects.create(profile=profile, **proj_data)
            
            self.stdout.write('Created sample projects')
            
            # Add GitHub profile
            GitHubProfile.objects.create(
                profile=profile,
                username='sampleuser',
                repositories_count=25,
                followers_count=50,
                following_count=30
            )
            
            self.stdout.write('Created sample GitHub profile')
        
        self.stdout.write(self.style.SUCCESS('Initial data setup completed!'))
        self.stdout.write(f'Profile URL: /portfolio/{profile.id}/')