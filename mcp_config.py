"""
Supabase接続設定ファイル
注意: Supabase MCP (Model Context Protocol) は、
AIアシスタントがSupabaseと直接やり取りするためのプロトコルです。
このファイルは通常のSupabase Python クライアントの接続設定です。
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    """Supabase クライアント"""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_PROJECT_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY')
        self.client: Client = create_client(self.url, self.key) if self.url and self.key else None
    
    def get_client(self) -> Client:
        """Supabaseクライアントを取得"""
        return self.client
    
    def test_connection(self) -> bool:
        """接続テスト"""
        if not self.client:
            print("Supabase設定が不完全です。.envファイルを確認してください。")
            return False
        try:
            # プロジェクトのヘルスチェック
            response = self.client.rpc('ping').execute()
            return True
        except Exception as e:
            print(f"接続エラー: {e}")
            # 基本的なテーブル確認を試行
            try:
                response = self.client.table('portfolio_profile').select('id').limit(1).execute()
                return True
            except:
                return False
    
    def migrate_data(self, source_data: list, table_name: str):
        """データ移行"""
        if not self.client:
            print("Supabase接続が確立されていません")
            return None
        try:
            # バッチでデータを挿入
            if source_data:
                response = self.client.table(table_name).insert(source_data).execute()
                print(f"{table_name}へのデータ移行完了: {len(source_data)}件")
                return response
        except Exception as e:
            print(f"データ移行エラー: {e}")
            return None

# Supabaseクライアントインスタンスの作成
supabase_client = SupabaseClient()