# XRPL フロントエンド修正

## 問題

```
Module not found: Can't resolve 'xrpl'
```

フロントエンドで`xrpl`パッケージをインポートしようとしていましたが、これはNode.js環境向けのライブラリであり、ブラウザ環境では動作しません。

## 原因

`frontend/lib/xrpl-payment.ts`で直接`xrpl`パッケージを使用していました：

```typescript
// 問題のあるコード
import { Client, Wallet, xrpToDrops, dropsToXrp } from 'xrpl';
```

## 解決方法

フロントエンドでは`xrpl`パッケージを直接使用せず、バックエンドAPIを経由してXRPL操作を行うように変更しました。

### 修正前

```typescript
// フロントエンドで直接XRPLクライアントを使用
const client = await getClient();
const response = await client.request({
  command: 'account_info',
  account: address,
  ledger_index: 'validated',
});
```

### 修正後

```typescript
// バックエンドAPI経由で取得
const response = await fetch(`${API_URL}/api/v1/wallet/balance?address=${address}`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
  },
});
```

## 変更内容

### 1. インポートの削除

```typescript
// 削除
import { Client, Wallet, xrpToDrops, dropsToXrp } from 'xrpl';

// 追加
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.airz.one';
```

### 2. 関数の書き換え

#### getWalletBalance()

```typescript
// 修正前: 直接XRPLネットワークに接続
export async function getWalletBalance(address: string): Promise<number> {
  const client = await getClient();
  const response = await client.request({
    command: 'account_info',
    account: address,
    ledger_index: 'validated',
  });
  const balanceDrops = response.result.account_data.Balance;
  return parseFloat(dropsToXrp(String(balanceDrops)));
}

// 修正後: バックエンドAPI経由
export async function getWalletBalance(address: string): Promise<number> {
  const response = await fetch(`${API_URL}/api/v1/wallet/balance?address=${address}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
  const data = await response.json();
  return data.data.balance_xrp || 0;
}
```

#### sendXRPPayment()

```typescript
// 修正前: 直接トランザクション送信
export async function sendXRPPayment(
  fromWalletSeed: string,
  toAddress: string,
  amountXRP: number,
  memo?: string
): Promise<{...}> {
  const client = await getClient();
  const wallet = Wallet.fromSeed(fromWalletSeed);
  // ... トランザクション作成・署名・送信
}

// 修正後: バックエンドAPI経由
export async function sendXRPPayment(
  orderId: string,
  amountXRP: number
): Promise<{...}> {
  const response = await fetch(`${API_URL}/api/v1/payments/xrpl/execute`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    },
    body: JSON.stringify({ order_id: orderId }),
  });
  const data = await response.json();
  return {
    hash: data.data.transaction_hash,
    validated: true,
    ledgerIndex: 0,
  };
}
```

#### getTransactionDetails()

```typescript
// 修正前: 直接XRPLネットワークに問い合わせ
export async function getTransactionDetails(txHash: string): Promise<any> {
  const client = await getClient();
  const response = await client.request({
    command: 'tx',
    transaction: txHash,
  });
  return response.result;
}

// 修正後: バックエンドAPI経由
export async function getTransactionDetails(txHash: string): Promise<any> {
  const response = await fetch(`${API_URL}/api/v1/payments/xrpl/verify/${txHash}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
  const data = await response.json();
  return data.data;
}
```

## アーキテクチャ

### 修正前（問題あり）

```
フロントエンド
  ↓ xrpl.js（ブラウザで動作しない）
XRPLネットワーク
```

### 修正後（正しい）

```
フロントエンド
  ↓ REST API
バックエンド
  ↓ xrpl.py（Python）
XRPLネットワーク
```

## メリット

### 1. セキュリティ

- **秘密鍵がフロントエンドに露出しない**
- バックエンドで安全に管理

### 2. 互換性

- **ブラウザ環境で動作**
- Node.js専用ライブラリの問題を回避

### 3. パフォーマンス

- **バックエンドでキャッシュ可能**
- 複数のリクエストを最適化

### 4. メンテナンス性

- **ビジネスロジックがバックエンドに集約**
- フロントエンドはUIに専念

## バックエンドAPI

必要なエンドポイント（既に実装済み）：

1. **GET /api/v1/wallet/balance**
   - ウォレット残高を取得

2. **POST /api/v1/payments/xrpl/execute**
   - XRP決済を実行

3. **GET /api/v1/payments/xrpl/verify/{tx_hash}**
   - トランザクション詳細を取得

## テスト方法

### 1. ビルドエラーの確認

```bash
cd frontend
npm run build
```

**期待される結果**: エラーなくビルド成功

### 2. 開発サーバー起動

```bash
npm run dev
```

**期待される結果**: `Module not found: Can't resolve 'xrpl'` エラーが出ない

### 3. 機能テスト

1. ログイン
2. ダッシュボードでウォレット残高を確認
3. 商品を購入してXRP決済を実行

**期待される結果**: すべて正常に動作

## トラブルシューティング

### キャッシュエラー

```bash
# Next.jsキャッシュをクリア
rm -rf .next
npm run dev
```

### node_modulesの再インストール

```bash
rm -rf node_modules package-lock.json
npm install
```

### TypeScriptエラー

```bash
# 型チェック
npm run type-check
```

## まとめ

この修正により：

1. ✅ フロントエンドで`xrpl`パッケージを使用しない
2. ✅ すべてのXRPL操作はバックエンド経由
3. ✅ ブラウザ環境で正常に動作
4. ✅ セキュリティが向上
5. ✅ メンテナンス性が向上

フロントエンドとバックエンドの責任が明確に分離され、より堅牢なアーキテクチャになりました。
