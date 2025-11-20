# API接続問題の最終修正まとめ

## 問題

フロントエンドからバックエンドAPIへのリクエストが404エラーを返す。

## 原因

1. フロントエンドが相対パス（`/api/v1/...`）を使用していた
2. Next.jsのrewritesが設定されていたが、本番環境では機能しない
3. 環境変数`NEXT_PUBLIC_API_URL`が一部のページでのみ使用されていた

## 最終的な解決方法

### 1. 環境変数の統一使用

すべてのAPIリクエストで`NEXT_PUBLIC_API_URL`を使用するように修正：

**修正したファイル:**
- `frontend/app/staking/page.tsx`
- `frontend/app/referral/page.tsx`

**修正内容:**
```typescript
const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
const response = await fetch(`${apiUrl}/api/v1/endpoint`, {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
```

### 2. 環境変数の設定

**本番環境** (`frontend/.env`):
```env
# 空文字列 = 相対パス使用（Nginxでプロキシ）
NEXT_PUBLIC_API_URL=
```

**開発環境** (`frontend/.env.local`):
```env
# ローカルバックエンドを直接指定
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### 3. Next.js設定

**ファイル**: `frontend/next.config.mjs`

開発環境用のrewritesを追加（本番環境ではNginxを使用）：

```javascript
async rewrites() {
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
  return [
    {
      source: '/api/:path*',
      destination: `${backendUrl}/api/:path*`,
    },
  ];
}
```

## 本番環境の設定

### Nginx設定（推奨）

```nginx
# /etc/nginx/sites-available/airzone

server {
    listen 80;
    server_name airz.one;

    # APIリクエストをバックエンドにプロキシ
    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers (if needed)
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type, Authorization";
    }

    # フロントエンド（Next.js）
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 環境変数の設定

本番環境では、`NEXT_PUBLIC_API_URL`を空文字列に設定：

```bash
# frontend/.env
NEXT_PUBLIC_API_URL=
```

これにより：
- フロントエンドは相対パス `/api/v1/...` を使用
- Nginxが `/api/` を `http://localhost:5000/api/` にプロキシ
- 同一オリジンとなり、CORSの問題も回避

## 開発環境の設定

### 1. .env.localファイルを作成

```bash
cd frontend
cp .env.local.example .env.local
```

### 2. バックエンドを起動

```bash
cd backend
python app.py
```

バックエンドは `http://localhost:5000` で起動します。

### 3. フロントエンドを起動

```bash
cd frontend
npm run dev
```

フロントエンドは `http://localhost:3000` で起動します。

## 動作確認

### 1. バックエンドの確認

```bash
# ヘルスチェック
curl http://localhost:5000/health

# 紹介API
curl -X GET http://localhost:5000/api/v1/referral/stats \
  -H "Authorization: Bearer YOUR_TOKEN"

# エスクローAPI
curl -X GET http://localhost:5000/api/v1/escrow/campaigns \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. フロントエンドの確認

1. ブラウザで https://airz.one/staking にアクセス
2. F12キーを押して開発者ツールを開く
3. Networkタブで以下を確認：
   - `/api/v1/escrow/campaigns` のリクエスト
   - ステータスコード（200 OKであること）
   - レスポンスがJSONであること
4. Consoleタブでエラーがないことを確認

## トラブルシューティング

### 404エラーが続く場合

1. **バックエンドが起動しているか確認**
   ```bash
   ps aux | grep python
   netstat -an | grep 5000
   ```

2. **環境変数を確認**
   ```bash
   # 本番環境
   cat frontend/.env
   # NEXT_PUBLIC_API_URL= （空文字列）

   # 開発環境
   cat frontend/.env.local
   # NEXT_PUBLIC_API_URL=http://localhost:5000
   ```

3. **Nginxの設定を確認**
   ```bash
   nginx -t
   systemctl status nginx
   ```

4. **フロントエンドを再ビルド**
   ```bash
   cd frontend
   npm run build
   ```

### CORSエラーが発生する場合

バックエンドのCORS設定を確認：

```python
# backend/app.py
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://airz.one"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## 完了

この修正により：
- ✅ 開発環境でAPIリクエストが正常に動作
- ✅ 本番環境でNginxを通じてAPIリクエストが正常に動作
- ✅ CORSの問題を回避
- ✅ すべてのページで統一されたAPI接続方法

## 関連ドキュメント

- `admin/FIX_REFERRAL_404_ERROR.md` - 紹介ページの404エラー修正
- `admin/FIX_STAKING_PAGE_DISPLAY.md` - ステーキングページの表示問題
- `admin/DEBUG_ESCROW_CAMPAIGNS.md` - エスクローキャンペーンのデバッグ
