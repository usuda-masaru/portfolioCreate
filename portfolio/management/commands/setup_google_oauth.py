"""
Google OAuth設定を管理画面に自動で追加するコマンド
"""

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
import os

class Command(BaseCommand):
    help = 'Google OAuth設定を管理画面に追加'

    def handle(self, *args, **options):
        # 環境変数からGoogle OAuth認証情報を取得
        client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR('GOOGLE_OAUTH_CLIENT_IDとGOOGLE_OAUTH_CLIENT_SECRETを.envファイルに設定してください。')
            )
            return
        
        # Siteオブジェクトを取得または作成
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={'domain': 'localhost:8000', 'name': 'Portfolio Site'}
        )
        
        if created:
            self.stdout.write(f'サイト作成: {site.domain}')
        
        # SocialAppを作成または更新
        social_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            # 既存の場合は更新
            social_app.client_id = client_id
            social_app.secret = client_secret
            social_app.save()
            self.stdout.write('Google OAuth設定を更新しました')
        else:
            self.stdout.write('Google OAuth設定を作成しました')
        
        # サイトとの関連付け
        social_app.sites.add(site)
        
        self.stdout.write(
            self.style.SUCCESS(f'Google OAuth設定が完了しました。')
        )
        self.stdout.write(f'Client ID: {client_id}')
        self.stdout.write(f'Site: {site.domain}')
        self.stdout.write('\\n以下のURLでテストできます:')
        self.stdout.write('- ログイン: http://localhost:8000/accounts/login/')
        self.stdout.write('- サインアップ: http://localhost:8000/accounts/signup/')