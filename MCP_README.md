# Supabase MCP (Model Context Protocol) について

## MCPとは？

Supabase MCP（Model Context Protocol）は、AI アシスタント（Claude、Cursor、VS Code Copilotなど）がSupabaseプロジェクトと直接やり取りできるようにするプロトコルです。

## 重要な違い

このプロジェクトでは2つの異なる接続方法があります：

### 1. 通常のSupabase Python Client接続（現在実装済み）
- `mcp_config.py` - 通常のPython Supabaseクライアント
- Djangoアプリケーションからの接続用
- データベース移行、CRUD操作などに使用

### 2. Supabase MCP（AI アシスタント用）
- AIツール（Claude、Cursor等）から直接Supabaseにアクセス
- セキュリティトークンを使用した読み取り専用アクセス
- プロンプトインジェクションのリスクがあるため本番環境では非推奨

## MCP設定方法（AI アシスタント用）

### 1. Personal Access Tokenの作成
1. Supabaseダッシュボードにログイン
2. アカウント設定 > Access Tokens
3. 新しいトークンを作成（読み取り専用権限推奨）

### 2. VS Code / Cursor での設定
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["@supabase/mcp@latest"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "your-access-token"
      }
    }
  }
}
```

### 3. Claude Desktop での設定
```json
{
  "supabase": {
    "command": "npx",
    "args": ["@supabase/mcp@latest"],
    "env": {
      "SUPABASE_ACCESS_TOKEN": "your-access-token"
    }
  }
}
```

## セキュリティ上の注意事項

⚠️ **重要な警告**:
- MCPは開発環境でのみ使用してください
- 本番環境のデータベースには接続しないでください
- 読み取り専用モードを使用してください
- プロジェクト単位でアクセスを制限してください

## 現在のプロジェクトでの使用方法

このDjangoプロジェクトでは、通常のSupabase Python Clientを使用してデータベース移行を行います：

```bash
# 環境設定
cp .env.example .env
# .envファイルを編集してSupabaseの認証情報を入力

# データベース移行
python manage.py migrate

# SQLiteからSupabaseへのデータ移行
python manage.py migrate_to_supabase
```

MCPは主にAIアシスタントがコード生成や分析を行う際に、Supabaseのスキーマ情報を直接参照するために使用されます。