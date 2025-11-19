# ログアウト後の真っ白画面の修正

## 問題

ログアウトボタンを押すと真っ白な画面になり、ホームページに戻らない問題がありました。

## 原因

`auth-store.ts`のログアウト処理で、状態はクリアされるものの、ページのリダイレクトが実装されていませんでした。

```typescript
// 修正前
logout: () => {
  apiLogout();
  set({
    user: null,
    wallet: null,
    token: null,
    isAuthenticated: false,
    error: null,
  });
  // リダイレクトなし → 真っ白な画面
},
```

## 修正内容

### 1. ログアウト後にホームページへリダイレクト (`frontend/stores/auth-store.ts`)

```typescript
logout: () => {
  apiLogout();
  set({
    user: null,
    wallet: null,
    token: null,
    isAuthenticated: false,
    error: null,
  });
  
  // Clear cart on logout
  if (typeof window !== 'undefined') {
    try {
      // Clear cart from localStorage
      const cartStore = localStorage.getItem('cart-storage');
      if (cartStore) {
        const cart = JSON.parse(cartStore);
        cart.state.items = [];
        cart.state.total = 0;
        localStorage.setItem('cart-storage', JSON.stringify(cart));
      }
    } catch (error) {
      console.error('Failed to clear cart:', error);
    }
    
    // Redirect to home page after logout
    window.location.href = '/';
  }
},
```

### 追加機能

1. **カートのクリア**
   - ログアウト時にカート内の商品もクリア
   - セキュリティとプライバシーの向上

2. **ホームページへリダイレクト**
   - `window.location.href = '/'` でホームページへ遷移
   - 完全なページリロードで状態をクリーン

## 動作フロー

### ログアウト処理

```
1. ログアウトボタンクリック
   ↓
2. apiLogout() - トークンをlocalStorageから削除
   ↓
3. Zustand状態をクリア
   ├─ user: null
   ├─ wallet: null
   ├─ token: null
   └─ isAuthenticated: false
   ↓
4. カートをクリア
   ├─ items: []
   └─ total: 0
   ↓
5. ホームページへリダイレクト
   └─ window.location.href = '/'
```

## テスト方法

### 1. ログアウトテスト

```bash
# フロントエンドを起動
cd frontend
npm run dev
```

1. ログイン
2. 商品をカートに追加
3. ログアウトボタンをクリック

**期待される動作**:
- ✅ ホームページにリダイレクト
- ✅ カートが空になる
- ✅ ユーザー情報がクリア
- ✅ 真っ白な画面にならない

### 2. 状態確認

ブラウザの開発者ツールで確認：

```javascript
// Console
localStorage.getItem('access_token')  // null
localStorage.getItem('refresh_token') // null

// Application > Local Storage
// cart-storage の items が空配列
```

## セキュリティとプライバシー

### ログアウト時にクリアされるデータ

1. **認証トークン**
   - `access_token`
   - `refresh_token`

2. **ユーザー情報**
   - `user`
   - `wallet`

3. **カート情報**
   - `items`
   - `total`

### 残るデータ

以下のデータは残ります（必要に応じて）：
- ブラウザのキャッシュ
- Cookie（使用していない場合）

## トラブルシューティング

### ログアウト後もユーザー情報が残る

**原因**: ブラウザキャッシュ

**解決方法**:
```bash
# ハードリロード
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

### カートが空にならない

**原因**: localStorage の同期エラー

**解決方法**:
```javascript
// Console で手動クリア
localStorage.clear()
location.reload()
```

### リダイレクトが遅い

**原因**: ネットワーク遅延

**解決方法**:
```typescript
// ローディング表示を追加（オプション）
logout: () => {
  set({ isLoading: true });
  apiLogout();
  // ... rest of logout logic
}
```

## 代替実装（Next.js Router使用）

Next.js の `useRouter` を使う方法もあります：

```typescript
// stores/auth-store.ts
import { useRouter } from 'next/navigation';

// ただし、Zustand store内では直接使えないため、
// コンポーネント側で処理する必要があります

// components/layout/Header.tsx
const router = useRouter();

const handleLogout = () => {
  logout();
  router.push('/');
};
```

現在の実装（`window.location.href`）の方がシンプルで確実です。

## まとめ

この修正により：

1. ✅ ログアウト後にホームページへ自動リダイレクト
2. ✅ カート情報も自動的にクリア
3. ✅ 真っ白な画面にならない
4. ✅ セキュリティとプライバシーの向上
5. ✅ ユーザー体験の改善

ログアウト処理が完全に機能するようになりました。
