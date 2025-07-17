"""
ユーザー登録時の自動処理
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """新規ユーザー登録時にプロファイルを自動作成"""
    if created:
        # Google OAuth経由の場合、追加情報を取得
        social_account = None
        try:
            social_account = SocialAccount.objects.get(user=instance, provider='google')
        except SocialAccount.DoesNotExist:
            pass
        
        # プロファイルの作成
        profile_data = {
            'name': instance.get_full_name() or instance.username or 'ユーザー',
            'email': instance.email,
            'title': 'エンジニア',  # デフォルト値
            'bio': 'よろしくお願いします。',  # デフォルト値
        }
        
        # Google OAuth経由の場合、追加情報を設定
        if social_account and social_account.extra_data:
            extra_data = social_account.extra_data
            profile_data['name'] = extra_data.get('name', profile_data['name'])
            if 'picture' in extra_data:
                # Google のプロフィール画像をアバターとして使用する場合
                # 実装は省略（必要に応じて追加）
                pass
        
        Profile.objects.create(
            user=instance,
            **profile_data
        )