# 紹介ページ404エラー修正

## 問題

紹介ページで「統計の取得に失敗しました (404)」というエラーが表示される。

## 原因

1. フロントエンドが相対パス `/api/v1/referral/stats` を使用している
2. Next.jsのrewritesが設定されていなかった
3. 環境変数`NEXT_PUBLIC_API_URL`が正しく使用されていなかった

## 修正内容

### 1. Next.js設定の更新

**ファイル**: `frontend/next.config.mjs`

APIリクエストをバックエンドにプロキシする設定を追加：

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

### 2. フロントエンドコードの更新

**ファイル**: `frontend/app/referral/page.tsx`

環境変数を使用してAPIエンドポイントを構築：

```typescript
const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
const statsResponse = await fetch(`${apiUrl}/api/v1/referral/stats`, {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
```

### 3. 環境変数の確認

**ファイル**: `frontend/.env`

```env
# 開発環境
NEXT_PUBLIC_API_URL=http://localhost:5000

# 本番環境
NEXT_PUBLIC_API_URL=https://api.airz.one
```

## 適用手順

### 1. フロントエンドの再ビルド

```bash
cd frontend
npm run build
```

### 2. バックエンドが起動していることを確認

```bash
# バックエンドのステータスを確認
curl http://localhost:5000/health

# または
curl https://api.airz.one/health
```

### 3. バックエンドが起動していない場合

```bash
cd backend
python app.py
```

## 動作確認

### 1. APIエンドポイントの直接テスト

```bash
# ログイン後、トークンを取得
TOKEN="YOUR_ACCESS_TOKEN"

# 開発環境
curl -X GET http://localhost:5000/api/v1/referral/stats \
  -H "Authorization: Bearer $TOKEN"

# 本番環境
curl -X GET https://api.airz.one/api/v1/referral/stats \
  -H "Authorization: Bearer $TOKEN"
```

期待されるレスポンス：
```json
{
  "status": "success",
  "data": {
    "total_referrals": 0,
    "completed_referrals": 0,
    "pending_referrals": 0,
    "total_coins_earned": 0,
    "current_coins": 0
  }
}
```

### 2. フロントエンドでの確認

1. https://airz.one/referral にアクセス
2. F12キーを押して開発者ツールを開く
3. Networkタブで以下を確認：
   - `/api/v1/referral/stats` のリクエスト
   - ステータスコード（200 OKであること）
   - レスポンスの内容
4. Consoleタブで以下を確認：
   - `Stats API response:` のログ
   - エラーメッセージがないこと

## トラブルシューティング

### 404エラーが続く場合

1. **バックエンドが起動しているか確認**
   ```bash
   # プロセスを確認
   ps aux | grep python
   
   # ポートを確認
   netstat -an | grep 5000
   ```

2. **バックエンドのログを確認**
   ```bash
   tail -f backend/logs/app.log
   ```

3. **ルートが登録されているか確認**
   ```bash
   # backend/app.pyを確認
   grep "register_blueprint.*referral" backend/app.py
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

### 環境変数が読み込まれない場合

```bash
# .envファイルを確認
cat frontend/.env

# Next.jsを再起動
cd frontend
npm run dev
```

## 本番環境の設定

### Nginx設定（推奨）

```nginx
# /etc/nginx/sites-available/airzone

# APIリクエストをバックエンドにプロキシ
location /api/ {
    proxy_pass http://localhost:5000/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# フロントエンド
location / {
    proxy_pass http://localhost:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### 環境変数の設定

本番環境では、`NEXT_PUBLIC_API_URL`を空文字列に設定して、相対パスを使用：

```env
# frontend/.env.production
NEXT_PUBLIC_API_URL=
```

これにより、`/api/v1/...`という相対パスがそのまま使用され、Nginxがバックエンドにプロキシします。

## 完了

修正後、紹介ページが正常に動作し、統計情報が表示されるようになります。

ただし、データベースマイグレーション（`referral_code`、`referred_by`、`coins`カラムの追加）も必要です。詳細は `admin/FIX_REFERRAL_JSON_ERROR.md` を参照してください。
