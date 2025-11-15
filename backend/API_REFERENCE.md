# Airzone API リファレンス

## 概要

Airzone バックエンド API の完全なリファレンスドキュメントです。すべてのエンドポイント、リクエスト/レスポンス形式、エラーコードについて説明します。

## ベース URL

```
開発環境: http://localhost:5000
本番環境: https://api.airz.one
```

## 認証

ほとんどのエンドポイントは JWT（JSON Web Token）認証が必要です。

### 認証ヘッダー

```
Authorization: Bearer <access_token>
```

### トークンの取得

Google OAuth 認証を使用してアクセストークンを取得します。詳細は [認証エンドポイント](#認証-auth) を参照してください。

## 共通レスポンス形式

### 成功レスポンス

```json
{
  "status": "success",
  "data": {
    // レスポンスデータ
  }
}
```

### エラーレスポンス

```json
{
  "status": "error",
  "error": "エラーメッセージ",
  "code": 400
}
```

## HTTP ステータスコード

| コード | 説明 |
|--------|------|
| 200 | OK - リクエスト成功 |
| 201 | Created - リソース作成成功 |
| 202 | Accepted - 非同期処理受付 |
| 400 | Bad Request - リクエストが不正 |
| 401 | Unauthorized - 認証が必要 |
| 403 | Forbidden - アクセス権限なし |
| 404 | Not Found - リソースが見つからない |
| 409 | Conflict - リソースの競合 |
| 500 | Internal Server Error - サーバーエラー |

---


## 認証 (Auth)

### POST /auth/google

Google OAuth ID トークンを使用してユーザー認証を行います。

**認証:** 不要

**リクエストボディ:**
```json
{
  "id_token": "string"  // Google OAuth ID トークン
}
```

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "ユーザー名",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

**エラー:**
- `400` - id_token が不正または欠落
- `401` - Google 認証失敗
- `500` - サーバーエラー

**要件:** 1.1, 1.4, 1.5, 8.2

---

### POST /auth/refresh

リフレッシュトークンを使用して新しいアクセストークンを取得します。

**認証:** 不要

**リクエストボディ:**
```json
{
  "refresh_token": "string"  // JWT リフレッシュトークン
}
```

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

**エラー:**
- `400` - refresh_token が欠落
- `401` - トークンが無効または期限切れ
- `500` - サーバーエラー

**要件:** 1.5, 8.2

---

### GET /auth/me

現在認証されているユーザーの情報を取得します。

**認証:** 必要

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "ユーザー名",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

**エラー:**
- `401` - 認証トークンが無効
- `404` - ユーザーが見つからない
- `500` - サーバーエラー

**要件:** 6.1, 8.2

---

## NFT (NFT)

### GET /nfts

認証されたユーザーのすべての NFT を取得します。

**認証:** 必要

**クエリパラメータ:**
- `status` (optional): ステータスでフィルタ (`pending`, `minting`, `completed`, `failed`)
- `limit` (optional): 返却する最大 NFT 数

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "nfts": [
      {
        "id": "uuid",
        "user_id": "uuid",
        "wallet_address": "0x...",
        "nft_object_id": "0x...",
        "transaction_digest": "0x...",
        "status": "completed",
        "metadata": {
          "name": "Welcome NFT",
          "description": "説明",
          "image_url": "https://..."
        },
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "count": 1
  }
}
```

**エラー:**
- `400` - 無効なクエリパラメータ
- `401` - 認証トークンが無効
- `500` - サーバーエラー

**要件:** 3.4, 8.2

---

### POST /nfts/mint

認証されたユーザーの NFT 発行をリクエストします。

**認証:** 必要

**リクエストボディ:**
```json
{
  "name": "NFT 名",
  "description": "NFT の説明",
  "image_url": "https://example.com/image.png",
  "metadata": {}  // オプション: 追加メタデータ
}
```

**レスポンス (202):**
```json
{
  "status": "success",
  "data": {
    "task_id": "uuid",
    "message": "NFT minting task queued successfully"
  }
}
```

**エラー:**
- `400` - 必須フィールドが欠落または無効
- `401` - 認証トークンが無効
- `500` - サーバーエラー

**要件:** 3.1, 8.2

**注意:** このエンドポイントは非同期処理です。タスクの状態は `/nfts/status/{task_id}` で確認できます。

---

### GET /nfts/{nft_id}

特定の NFT の詳細を取得します。

**認証:** 必要

**パスパラメータ:**
- `nft_id`: NFT レコード ID (UUID)

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "nft": {
      "id": "uuid",
      "user_id": "uuid",
      "wallet_address": "0x...",
      "nft_object_id": "0x...",
      "transaction_digest": "0x...",
      "status": "completed",
      "metadata": {},
      "error_message": null,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

**エラー:**
- `401` - 認証トークンが無効
- `403` - アクセス権限なし（他のユーザーの NFT）
- `404` - NFT が見つからない
- `500` - サーバーエラー

**要件:** 3.4, 8.2

---

### GET /nfts/status/{task_id}

NFT 発行タスクのステータスを取得します。

**認証:** 必要

**パスパラメータ:**
- `task_id`: `/nfts/mint` から返されたタスク ID

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "task": {
      "id": "uuid",
      "task_type": "mint_nft",
      "status": "completed",
      "payload": {
        "user_id": "uuid",
        "nft_name": "Welcome NFT"
      },
      "result": {
        "nft_object_id": "0x...",
        "transaction_digest": "0x..."
      },
      "error_message": null,
      "retry_count": 0,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

**エラー:**
- `401` - 認証トークンが無効
- `403` - アクセス権限なし
- `404` - タスクが見つからない
- `500` - サーバーエラー

**要件:** 3.1, 8.2

---

## 商品 (Products)

### GET /products

すべての商品を取得します（公開エンドポイント）。

**認証:** オプション

**クエリパラメータ:**
- `only_active` (optional): アクティブな商品のみ (default: true)
- `limit` (optional): 返却する最大商品数
- `offset` (optional): スキップする商品数
- `search` (optional): 名前/説明の検索キーワード
- `min_stock` (optional): 最小在庫数
- `required_nft_id` (optional): NFT 要件でフィルタ

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "products": [
      {
        "id": "uuid",
        "name": "オリジナルTシャツ",
        "description": "商品説明",
        "price": 3500,
        "stock_quantity": 100,
        "image_url": "https://...",
        "required_nft_id": null,
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "count": 1
  }
}
```

**エラー:**
- `400` - 無効なクエリパラメータ
- `500` - サーバーエラー

**要件:** 4.1, 8.2

---

### GET /products/{product_id}

特定の商品の詳細を取得します（公開エンドポイント）。

**認証:** オプション

**パスパラメータ:**
- `product_id`: 商品 ID (UUID)

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "product": {
      "id": "uuid",
      "name": "オリジナルTシャツ",
      "description": "商品説明",
      "price": 3500,
      "stock_quantity": 100,
      "image_url": "https://...",
      "required_nft_id": null,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

**エラー:**
- `404` - 商品が見つからない
- `500` - サーバーエラー

**要件:** 4.2, 8.2

---

### POST /products

新しい商品を作成します（管理者のみ）。

**認証:** 必要

**リクエストボディ:**
```json
{
  "name": "商品名",
  "price": 3500,
  "description": "商品説明",
  "stock_quantity": 100,
  "image_url": "https://...",
  "required_nft_id": "uuid",  // オプション
  "is_active": true
}
```

**レスポンス (201):**
```json
{
  "status": "success",
  "data": {
    "product": {
      "id": "uuid",
      "name": "商品名",
      "description": "商品説明",
      "price": 3500,
      "stock_quantity": 100,
      "image_url": "https://...",
      "required_nft_id": null,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

**エラー:**
- `400` - 必須フィールドが欠落または無効
- `401` - 認証トークンが無効
- `500` - サーバーエラー

**要件:** 4.2, 8.2

---

### PUT /products/{product_id}

商品を更新します（管理者のみ）。

**認証:** 必要

**パスパラメータ:**
- `product_id`: 商品 ID (UUID)

**リクエストボディ:**
```json
{
  "name": "更新された商品名",
  "price": 4000,
  "description": "更新された説明",
  "stock_quantity": 50,
  "image_url": "https://...",
  "required_nft_id": "uuid",
  "is_active": false
}
```

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "product": {
      "id": "uuid",
      "name": "更新された商品名",
      "price": 4000,
      // ... その他のフィールド
    }
  }
}
```

**エラー:**
- `400` - 無効なフィールド値
- `401` - 認証トークンが無効
- `404` - 商品が見つからない
- `500` - サーバーエラー

**要件:** 4.4, 8.2

---

### DELETE /products/{product_id}

商品を削除（非アクティブ化）します（管理者のみ）。

**認証:** 必要

**パスパラメータ:**
- `product_id`: 商品 ID (UUID)

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "message": "Product deleted successfully"
  }
}
```

**エラー:**
- `401` - 認証トークンが無効
- `404` - 商品が見つからない
- `500` - サーバーエラー

**要件:** 4.5, 8.2

---

## 注文 (Orders)

### POST /orders

新しい注文を作成します。

**認証:** 必要

**リクエストボディ:**
```json
{
  "items": [
    {
      "product_id": "uuid",
      "quantity": 2
    }
  ]
}
```

**レスポンス (201):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "status": "pending",
    "total_amount": 7000,
    "items": [
      {
        "id": "uuid",
        "product_id": "uuid",
        "product_name": "オリジナルTシャツ",
        "quantity": 2,
        "unit_price": 3500,
        "subtotal": 7000
      }
    ],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**エラー:**
- `400` - 必須フィールドが欠落または無効
- `401` - 認証トークンが無効
- `403` - NFT 要件が満たされていない
- `409` - 在庫不足
- `500` - サーバーエラー

**要件:** 5.1, 5.2, 5.3, 8.2

---

### GET /orders

ユーザーの注文履歴を取得します。

**認証:** 必要

**クエリパラメータ:**
- `status` (optional): ステータスでフィルタ (`pending`, `processing`, `completed`, `failed`, `cancelled`)
- `limit` (optional): 返却する最大注文数 (default: 50, max: 100)

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "orders": [
      {
        "id": "uuid",
        "user_id": "uuid",
        "status": "completed",
        "total_amount": 7000,
        "items": [...],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "count": 1
  }
}
```

**エラー:**
- `400` - 無効なクエリパラメータ
- `401` - 認証トークンが無効
- `500` - サーバーエラー

**要件:** 5.4, 8.2

---

### GET /orders/{order_id}

特定の注文の詳細を取得します。

**認証:** 必要

**パスパラメータ:**
- `order_id`: 注文 ID (UUID)

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "status": "completed",
    "total_amount": 7000,
    "items": [
      {
        "id": "uuid",
        "product_id": "uuid",
        "product_name": "オリジナルTシャツ",
        "quantity": 2,
        "unit_price": 3500,
        "subtotal": 7000
      }
    ],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**エラー:**
- `400` - 無効な注文 ID 形式
- `401` - 認証トークンが無効
- `403` - アクセス権限なし（他のユーザーの注文）
- `404` - 注文が見つからない
- `500` - サーバーエラー

**要件:** 5.4, 8.2

---

## 決済 (Payments)

### POST /payments/intent

注文の Stripe Payment Intent を作成します。

**認証:** 必要

**リクエストボディ:**
```json
{
  "order_id": "uuid",
  "customer_email": "user@example.com"  // オプション
}
```

**レスポンス (201):**
```json
{
  "status": "success",
  "data": {
    "payment_id": "uuid",
    "client_secret": "pi_xxx_secret_xxx",
    "amount": 7000,
    "currency": "jpy",
    "status": "pending"
  }
}
```

**エラー:**
- `400` - 必須フィールドが欠落または無効な注文
- `401` - 認証トークンが無効
- `403` - アクセス権限なし（他のユーザーの注文）
- `404` - 注文が見つからない
- `500` - サーバーエラー

**要件:** 5.5, 8.2

**注意:** `client_secret` をフロントエンドの Stripe.js に渡して決済を完了します。

---

### POST /payments/webhook

Stripe Webhook イベントを処理します。

**認証:** 不要（Stripe 署名検証）

**ヘッダー:**
- `Stripe-Signature`: Webhook 署名

**リクエストボディ:** Stripe イベントペイロード（生データ）

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "event_type": "payment_intent.succeeded",
    "event_id": "evt_xxx"
  }
}
```

**エラー:**
- `400` - 無効なペイロードまたは署名
- `500` - サーバーエラー

**要件:** 5.5, 5.6, 8.2

**注意:** このエンドポイントは Stripe から呼び出されます。Stripe ダッシュボードで Webhook URL を設定してください。

---

### GET /payments/{payment_id}

決済の詳細を取得します。

**認証:** 必要

**パスパラメータ:**
- `payment_id`: 決済 ID (UUID)

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "order_id": "uuid",
    "stripe_payment_intent_id": "pi_xxx",
    "amount": 7000,
    "currency": "jpy",
    "status": "succeeded",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**エラー:**
- `400` - 無効な決済 ID 形式
- `401` - 認証トークンが無効
- `403` - アクセス権限なし
- `404` - 決済が見つからない
- `500` - サーバーエラー

**要件:** 8.2

---

## WiFi (WiFi)

### POST /wifi/connect

新しい WiFi 接続セッションを作成します。

**認証:** 不要（キャプティブポータルフロー用）

**リクエストボディ:**
```json
{
  "mac_address": "AA:BB:CC:DD:EE:FF",  // オプション
  "ip_address": "192.168.1.100",       // オプション
  "user_id": "uuid"                     // オプション
}
```

**レスポンス (201):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "ip_address": "192.168.1.100",
    "connected_at": "2024-01-01T00:00:00Z",
    "disconnected_at": null,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**エラー:**
- `400` - 無効なフィールド形式
- `500` - サーバーエラー

**要件:** 2.1, 2.2, 8.2

**注意:** このエンドポイントはユーザー認証前にキャプティブポータルから呼び出されます。

---

### GET /wifi/sessions

ユーザーの WiFi セッション履歴を取得します。

**認証:** 必要

**クエリパラメータ:**
- `limit` (optional): 返却する最大セッション数 (default: 50, max: 100)

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "sessions": [
      {
        "id": "uuid",
        "user_id": "uuid",
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "ip_address": "192.168.1.100",
        "connected_at": "2024-01-01T00:00:00Z",
        "disconnected_at": "2024-01-01T01:00:00Z",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T01:00:00Z"
      }
    ],
    "count": 1
  }
}
```

**エラー:**
- `400` - 無効なクエリパラメータ
- `401` - 認証トークンが無効
- `500` - サーバーエラー

**要件:** 2.4, 8.2

---

### POST /wifi/sessions/{session_id}/disconnect

WiFi セッションを切断済みとしてマークします。

**認証:** 必要

**パスパラメータ:**
- `session_id`: WiFi セッション ID (UUID)

**レスポンス (200):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "ip_address": "192.168.1.100",
    "connected_at": "2024-01-01T00:00:00Z",
    "disconnected_at": "2024-01-01T01:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T01:00:00Z"
  }
}
```

**エラー:**
- `400` - 無効なセッション ID 形式
- `401` - 認証トークンが無効
- `403` - アクセス権限なし
- `404` - セッションが見つからない
- `500` - サーバーエラー

**要件:** 2.3, 8.2

---

## エラーコード詳細

### 認証エラー (401)

```json
{
  "status": "error",
  "error": "Invalid or expired token",
  "code": 401
}
```

**原因:**
- アクセストークンが無効
- トークンの有効期限切れ
- トークンが提供されていない

**対処法:**
- `/auth/refresh` でトークンを更新
- 再度ログインして新しいトークンを取得

---

### バリデーションエラー (400)

```json
{
  "status": "error",
  "error": "Validation error message",
  "code": 400,
  "field": "field_name"  // オプション
}
```

**原因:**
- 必須フィールドが欠落
- フィールド値が無効な形式
- ビジネスルール違反

**対処法:**
- リクエストボディを確認
- フィールド形式を修正
- エラーメッセージの指示に従う

---

### リソース未検出 (404)

```json
{
  "status": "error",
  "error": "Resource not found",
  "code": 404
}
```

**原因:**
- 指定された ID のリソースが存在しない
- リソースが削除済み

**対処法:**
- ID を確認
- リソースの存在を確認

---

### アクセス拒否 (403)

```json
{
  "status": "error",
  "error": "Access denied",
  "code": 403
}
```

**原因:**
- 他のユーザーのリソースへのアクセス
- NFT 要件が満たされていない
- 権限不足

**対処法:**
- 自分のリソースのみアクセス
- 必要な NFT を取得
- 適切な権限を取得

---

### リソース競合 (409)

```json
{
  "status": "error",
  "error": "Insufficient stock",
  "code": 409
}
```

**原因:**
- 在庫不足
- リソースの状態が不適切

**対処法:**
- 在庫を確認
- 後で再試行

---

## レート制限

現在、レート制限は実装されていませんが、将来的に追加される可能性があります。

推奨される使用パターン:
- バースト的なリクエストを避ける
- 適切なキャッシュを使用
- 必要な場合のみ API を呼び出す

---

## ベストプラクティス

### 1. トークン管理

```javascript
// アクセストークンをローカルストレージに保存
localStorage.setItem('access_token', token);

// リクエストヘッダーに含める
headers: {
  'Authorization': `Bearer ${localStorage.getItem('access_token')}`
}

// トークン期限切れ時は自動更新
if (response.status === 401) {
  await refreshToken();
  // リクエストを再試行
}
```

### 2. エラーハンドリング

```javascript
try {
  const response = await fetch('/api/v1/products');
  const data = await response.json();
  
  if (data.status === 'error') {
    // エラーメッセージを表示
    showError(data.error);
  } else {
    // 成功時の処理
    handleSuccess(data.data);
  }
} catch (error) {
  // ネットワークエラーなど
  showError('Network error occurred');
}
```

### 3. 非同期処理

```javascript
// NFT 発行リクエスト
const mintResponse = await fetch('/api/v1/nfts/mint', {
  method: 'POST',
  body: JSON.stringify({ name, description, image_url })
});
const { task_id } = await mintResponse.json();

// ポーリングでステータス確認
const checkStatus = async () => {
  const statusResponse = await fetch(`/api/v1/nfts/status/${task_id}`);
  const { task } = await statusResponse.json();
  
  if (task.status === 'completed') {
    // 完了
    showSuccess('NFT minted successfully!');
  } else if (task.status === 'failed') {
    // 失敗
    showError(task.error_message);
  } else {
    // まだ処理中、再度確認
    setTimeout(checkStatus, 2000);
  }
};

checkStatus();
```

---

## サポート

API に関する質問や問題がある場合:

1. このドキュメントを確認
2. エラーメッセージを確認
3. ログを確認
4. 開発チームに連絡

---

**最終更新:** 2024-11-15  
**API バージョン:** v1  
**ドキュメントバージョン:** 1.0
