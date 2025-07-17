# Supabaseストレージ設定手順

## 1. Supabaseダッシュボードでの設定

### A. ストレージバケットの作成
1. **Storage** → **Buckets** → **Create bucket**
2. バケット名: `portfolio-images`
3. **Public bucket** にチェック（画像を公開アクセス可能にする）
4. **Create bucket** をクリック

### B. S3 Access Keysの取得
1. **Settings** → **Storage** → **S3 Access Keys**
2. 以下の情報を取得:
   - **Access Key ID**
   - **Secret Access Key**
   - **Region** (通常は `ap-northeast-1`)
   - **Endpoint URL**: `https://[YOUR-PROJECT-ID].supabase.co/storage/v1/s3`

### C. Service Role Keyの取得
1. **Settings** → **API**
2. **service_role** key をコピー

## 2. 必要な環境変数

以下を `.env` ファイルに追加してください：

```env
# Supabaseストレージ設定
SUPABASE_STORAGE_BUCKET_NAME=portfolio-images
SUPABASE_STORAGE_ACCESS_KEY_ID=your-access-key-id
SUPABASE_STORAGE_SECRET_ACCESS_KEY=your-secret-access-key
SUPABASE_STORAGE_REGION=ap-northeast-1
SUPABASE_STORAGE_ENDPOINT=https://[YOUR-PROJECT-ID].supabase.co/storage/v1/s3
```

## 3. 注意事項

- **Public bucket** を作成することで、画像に直接アクセスできます
- **RLS (Row Level Security)** を設定して、適切なアクセス制御を行うことを推奨
- 画像のURLは以下の形式になります：
  `https://[YOUR-PROJECT-ID].supabase.co/storage/v1/object/public/portfolio-images/ファイル名`