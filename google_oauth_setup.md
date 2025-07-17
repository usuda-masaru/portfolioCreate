# Google OAuth設定手順

## 1. Google Cloud Consoleでの設定

### A. Google Cloud Consoleにアクセス
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを選択または新しく作成

### B. OAuth 2.0認証情報の作成
1. **APIs & Services** → **Credentials** にアクセス
2. **+ CREATE CREDENTIALS** → **OAuth client ID** を選択
3. **Application type**: Web application
4. **Name**: Portfolio Django App
5. **Authorized redirect URIs**に以下を追加:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `http://127.0.0.1:8000/accounts/google/login/callback/`

### C. 認証情報を取得
作成後、以下の情報をコピー:
- **Client ID**: `123456789-abcdef.apps.googleusercontent.com`
- **Client Secret**: `GOCSPX-abcdefghijklmnop`

## 2. .envファイルの更新

`.env`ファイルに以下を追加:

```env
# Google OAuth設定
GOOGLE_OAUTH_CLIENT_ID=123456789-abcdef.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=GOCSPX-abcdefghijklmnop
```

## 3. 管理画面での設定

1. http://localhost:8000/admin/ にアクセス
2. **Social applications** → **Add social application**
3. 以下を設定:
   - **Provider**: Google
   - **Name**: Google
   - **Client id**: 上記で取得したClient ID
   - **Secret key**: 上記で取得したClient Secret
   - **Sites**: example.com を選択

## 4. テスト用URL

- **ログイン**: http://localhost:8000/accounts/login/
- **サインアップ**: http://localhost:8000/accounts/signup/
- **ログアウト**: http://localhost:8000/accounts/logout/

## 5. 注意事項

- **本番環境**では、Authorized redirect URIsに本番URLを追加してください
- **OAuth consent screen**の設定も必要です（Google Cloud Console）
- **プライバシーポリシー**と**利用規約**のURLが必要になる場合があります