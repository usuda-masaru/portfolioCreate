# Supabase セットアップ手順

## 1. Supabaseプロジェクトの作成

1. **Supabase公式サイト**にアクセス: https://supabase.com
2. **"Start your project"**をクリック
3. **"New project"**を選択
4. 以下の情報を入力：
   - Project name: `portfolio-django`
   - Database Password: 強固なパスワードを設定
   - Region: Asia Northeast (Tokyo)
5. **"Create new project"**をクリック

## 2. データベース情報の取得

プロジェクトが作成されたら、以下の情報を取得してください：

### Settings > Database から：
- **Host**: `[YOUR_PROJECT_REF].supabase.co`
- **Database name**: `postgres`
- **Port**: `5432`
- **User**: `postgres`
- **Password**: プロジェクト作成時に設定したパスワード

### Settings > API から：
- **Project URL**: `https://[YOUR_PROJECT_REF].supabase.co`
- **anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **service_role key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## 3. .envファイルの更新

`.env`ファイルを以下の実際の値で更新してください：

```env
# Supabase データベース設定
SUPABASE_DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@[YOUR_PROJECT_REF].supabase.co:5432/postgres
SUPABASE_SECRET_KEY=[YOUR_SERVICE_ROLE_KEY]
SUPABASE_PROJECT_URL=https://[YOUR_PROJECT_REF].supabase.co
SUPABASE_ANON_KEY=[YOUR_ANON_KEY]

# Django設定
SECRET_KEY=django-insecure--(fgtx4!ac=p)41t0jhfkahcve!fd2@f2po2odx#a$9hdda1z#
DEBUG=True
```

## 4. 移行手順

### 4.1 データベース接続テスト
```bash
python manage.py shell
```

```python
from mcp_config import mcp_client
print("接続テスト:", mcp_client.test_connection())
```

### 4.2 マイグレーションの実行
```bash
# 新しいデータベースでマイグレーション
python manage.py migrate

# 初期データの設定
python manage.py setup_initial_data
```

### 4.3 データの移行（プレビュー）
```bash
# ドライランで確認
python manage.py migrate_to_supabase --dry-run

# 実際の移行
python manage.py migrate_to_supabase
```

## 5. 確認事項

### 5.1 管理者アカウントの作成
```bash
python manage.py createsuperuser
```

### 5.2 サーバーの起動確認
```bash
python manage.py runserver
```

### 5.3 Supabaseダッシュボードでのデータ確認
- Table Editor でデータが正しく移行されているか確認
- Authentication設定の確認

## 6. トラブルシューティング

### 接続エラーの場合：
- DATABASE_URLの形式を確認
- ファイアウォール設定の確認
- Supabaseプロジェクトの状態確認

### データ移行エラーの場合：
- 元のSQLiteデータベースの確認
- モデルの互換性確認
- データ型の変換確認

## 7. 本番環境への移行

### 7.1 環境変数の設定
- `DEBUG=False`に設定
- `ALLOWED_HOSTS`の設定
- `SECRET_KEY`の変更

### 7.2 セキュリティの強化
- Row Level Security (RLS)の設定
- APIキーの管理
- CORS設定の調整