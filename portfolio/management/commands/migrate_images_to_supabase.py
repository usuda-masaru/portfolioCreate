"""
ローカル画像をSupabaseストレージに移行するコマンド
"""

from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
from portfolio.models import Profile, Project
import os

class Command(BaseCommand):
    help = 'ローカル画像をSupabaseストレージに移行'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='実際の移行を実行せず、プレビューのみ表示',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if not settings.USE_SUPABASE_STORAGE:
            self.stdout.write(
                self.style.ERROR('Supabaseストレージが設定されていません。.envファイルを確認してください。')
            )
            return
        
        self.stdout.write(self.style.SUCCESS('Supabaseストレージへの画像移行を開始します...'))
        
        # プロファイル画像の移行
        self.migrate_profile_images(dry_run)
        
        # プロジェクト画像の移行
        self.migrate_project_images(dry_run)
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\\nDRY RUN完了。実際の移行は実行されませんでした。'))
        else:
            self.stdout.write(self.style.SUCCESS('\\nSupabaseストレージへの画像移行が完了しました。'))

    def migrate_profile_images(self, dry_run):
        self.stdout.write('\\n=== プロファイル画像の移行 ===')
        
        profiles = Profile.objects.filter(avatar__isnull=False).exclude(avatar='')
        local_media_root = settings.BASE_DIR / 'media'
        
        for profile in profiles:
            # ローカルファイルパスを構築
            local_path = local_media_root / profile.avatar.name
            
            if local_path.exists():
                self.stdout.write(f'プロファイル: {profile.name}')
                self.stdout.write(f'  元のパス: {local_path}')
                
                if dry_run:
                    self.stdout.write(f'  [DRY RUN] Supabaseにアップロード予定: {profile.avatar.name}')
                else:
                    # 画像をSupabaseストレージにアップロード
                    with open(local_path, 'rb') as f:
                        filename = profile.avatar.name.split('/')[-1]
                        new_name = f'avatars/{filename}'
                        saved_path = default_storage.save(new_name, f)
                        
                        # データベースのパスを更新
                        profile.avatar.name = saved_path
                        profile.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ アップロード完了: {saved_path}')
                        )
                        self.stdout.write(f'  URL: {profile.avatar.url}')
            else:
                self.stdout.write(f'プロファイル: {profile.name}')
                self.stdout.write(f'  ✗ ローカルファイルが存在しません: {local_path}')

    def migrate_project_images(self, dry_run):
        self.stdout.write('\\n=== プロジェクト画像の移行 ===')
        
        projects = Project.objects.filter(image__isnull=False).exclude(image='')
        local_media_root = settings.BASE_DIR / 'media'
        
        for project in projects:
            # ローカルファイルパスを構築
            local_path = local_media_root / project.image.name
            
            if local_path.exists():
                self.stdout.write(f'プロジェクト: {project.title}')
                self.stdout.write(f'  元のパス: {local_path}')
                
                if dry_run:
                    self.stdout.write(f'  [DRY RUN] Supabaseにアップロード予定: {project.image.name}')
                else:
                    # 画像をSupabaseストレージにアップロード
                    with open(local_path, 'rb') as f:
                        filename = project.image.name.split('/')[-1]
                        new_name = f'projects/{filename}'
                        saved_path = default_storage.save(new_name, f)
                        
                        # データベースのパスを更新
                        project.image.name = saved_path
                        project.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ アップロード完了: {saved_path}')
                        )
                        self.stdout.write(f'  URL: {project.image.url}')
            else:
                self.stdout.write(f'プロジェクト: {project.title}')
                self.stdout.write(f'  ✗ ローカルファイルが存在しません: {local_path}')