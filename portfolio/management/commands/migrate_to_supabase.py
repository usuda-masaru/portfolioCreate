"""
SQLiteからSupabaseへのデータ移行コマンド
"""

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection
import json
import os
from mcp_config import supabase_client

class Command(BaseCommand):
    help = 'SQLiteからSupabaseへデータを移行'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='実際の移行を実行せず、プレビューのみ表示',
        )
        parser.add_argument(
            '--models',
            type=str,
            help='移行対象のモデル名（カンマ区切り）',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        models_filter = options['models'].split(',') if options['models'] else None
        
        self.stdout.write(self.style.SUCCESS('Supabaseへの移行を開始します...'))
        
        # 接続テスト
        if not supabase_client.test_connection():
            self.stdout.write(self.style.ERROR('Supabaseへの接続に失敗しました。'))
            return
        
        # ポートフォリオアプリのモデルを取得
        app_label = 'portfolio'
        models = apps.get_app_config(app_label).get_models()
        
        for model in models:
            model_name = model.__name__
            
            # フィルタリング
            if models_filter and model_name not in models_filter:
                continue
            
            self.stdout.write(f'\\n{model_name}を処理中...')
            
            # データを取得
            data = list(model.objects.all().values())
            
            if not data:
                self.stdout.write(f'  {model_name}: データなし')
                continue
            
            self.stdout.write(f'  {model_name}: {len(data)}件のデータ')
            
            if dry_run:
                self.stdout.write(f'  [DRY RUN] {model_name}のデータ例:')
                if data:
                    self.stdout.write(f'  {json.dumps(data[0], indent=2, default=str)}')
            else:
                # データを変換（必要に応じて）
                converted_data = self._convert_data(data, model)
                
                # Supabaseに移行
                table_name = model._meta.db_table
                result = supabase_client.migrate_data(converted_data, table_name)
                
                if result:
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ {model_name}: 移行完了')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ {model_name}: 移行失敗')
                    )
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\\nDRY RUN完了。実際の移行は実行されませんでした。'))
        else:
            self.stdout.write(self.style.SUCCESS('\\nSupabaseへの移行が完了しました。'))

    def _convert_data(self, data, model):
        """データ変換（必要に応じて）"""
        converted = []
        
        for item in data:
            # 日時フィールドの変換
            for field in model._meta.fields:
                if field.name in item and hasattr(field, 'auto_now_add'):
                    if item[field.name]:
                        # 文字列として保存
                        item[field.name] = str(item[field.name])
            
            converted.append(item)
        
        return converted