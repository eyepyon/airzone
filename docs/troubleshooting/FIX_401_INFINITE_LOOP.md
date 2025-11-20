# 401エラー無限ループの修正

## 問題

`/api/v1/orders` などのAPIエンドポイントで401エラーが発生すると、トークンリフレッシュを試みて再度リクエストを送信し、それがまた401を返すという無限ループが発生していました。

## 原因

`frontend/lib/api-client.ts` の `apiRequest` 関数で、401エラーが発生すると以下の処理が実行されていました：

1. トークンをリフレッシュ
2. 新しいトークンで再度リクエスト
3. それも401を返す
4. 再度トークンをリフレッシュ（無限ループ）

リトライ時に `skipRefresh` フラグがなかったため、無限にリトライが発生していました。

## 修正内容

### 1. `api-client.ts` の修正

#### skipRefreshフラグの追加

```typescript
interface RequestOptions extends RequestInit {
  token?: string;
  skipRefresh?: boolean;  // 追加
}
```

#### 401エラー処理の改善

```typescript
if (response.status === 401 && authToken && !options.skipRefresh) {
  // Try to refresh token
  const refreshed = await refreshAccessToken();
  if (refreshed) {
    // Retry the request with new token (only once)
    return apiRequest<T>(endpoint, { 
      ...options, 
      token: getAuthToken()!, 
      skipRefresh: true  // 2回目のリトライを防ぐ
    });
  } else {
    // Refresh failed, clear tokens and redirect to login
    removeAuthToken();
    removeRefreshToken();
    if (typeof window !== 'undefined') {
      window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
    }
  }
}
```

#### エラーメッセージの改善

```typescript
export class APIError extends Error {
  constructor(
    public status: number,
    public code: number,
    message: string,
    public details?: unknown
  ) {
    super(`[${status}] ${message}`);  // ステータスコードを含める
    this.name = 'APIError';
  }
}
```

### 2. ページレベルでの401エラー処理

#### `app/orders/page.tsx`

```typescript
catch (err) {
  console.error('Failed to fetch orders:', err);
  
  // 401エラーの場合はログインページにリダイレクト
  if (err instanceof Error && err.message.includes('401')) {
    router.push('/login?redirect=/orders');
    return;
  }
  
  const errorMessage = err instanceof Error ? err.message : '注文の取得に失敗しました';
  setError(errorMessage);
  setOrders([]);
}
```

#### `app/orders/[id]/page.tsx`

```typescript
catch (err) {
  console.error('Failed to fetch order:', err);
  
  // 401エラーの場合はログインページにリダイレクト
  if (err instanceof Error && err.message.includes('401')) {
    router.push(`/login?redirect=/orders/${params.id}`);
    return;
  }
  
  setError(err instanceof Error ? err.message : '注文の取得に失敗しました');
}
```

## 修正後の動作

### 正常なフロー

1. APIリクエスト送信
2. 401エラー受信
3. トークンリフレッシュ試行
4. 成功した場合：新しいトークンで1回だけリトライ
5. 失敗した場合：ログインページにリダイレクト

### 無限ループの防止

- `skipRefresh: true` フラグにより、リトライは1回のみ
- リフレッシュ失敗時は即座にログインページへリダイレクト
- ページレベルでも401エラーを検出してリダイレクト

## テスト方法

### 1. トークン期限切れのシミュレーション

```javascript
// ブラウザのコンソールで実行
localStorage.setItem('access_token', 'invalid_token');
```

### 2. 注文ページにアクセス

```
http://localhost:3000/orders
```

### 3. 期待される動作

- 401エラーが発生
- トークンリフレッシュを試行
- リフレッシュ失敗
- ログインページにリダイレクト（`/login?redirect=/orders`）
- **無限ループは発生しない**

### 4. ネットワークタブで確認

- `/api/v1/orders` へのリクエストは最大2回（初回 + リトライ1回）
- それ以上のリクエストは発生しない

## 影響範囲

この修正により、以下のすべてのAPIリクエストで無限ループが防止されます：

- ✅ 注文一覧取得 (`/api/v1/orders`)
- ✅ 注文詳細取得 (`/api/v1/orders/{id}`)
- ✅ 商品一覧取得 (`/api/v1/products`)
- ✅ NFT一覧取得 (`/api/v1/nfts`)
- ✅ ウォレット操作 (`/api/v1/wallet/*`)
- ✅ その他すべてのAPIエンドポイント

## 関連ファイル

- `frontend/lib/api-client.ts` - APIクライアント（コア修正）
- `frontend/app/orders/page.tsx` - 注文一覧ページ
- `frontend/app/orders/[id]/page.tsx` - 注文詳細ページ

## 注意事項

### 本番環境での重要な原則

1. **無限ループ禁止** - リトライは必ず回数制限を設ける
2. **適切なエラーハンドリング** - 401エラーは即座にログインページへ
3. **ユーザー体験** - エラー時は明確なメッセージとリダイレクト

### 今後の開発

新しいAPIリクエストを実装する際は：

1. `apiRequest` 関数を使用する（自動的に401処理が適用される）
2. ページレベルでも401エラーをキャッチしてリダイレクト
3. エラーメッセージをユーザーに表示

## 修正日時

2024年11月20日

## 関連ドキュメント

- [APIドメイン問題の修正](./FIX_API_DOMAIN_ISSUE.md)
- [API接続問題の修正手順](./FIX_REFERRAL_404_ERROR.md)
- [アーキテクチャ概要](../../ARCHITECTURE.md)
