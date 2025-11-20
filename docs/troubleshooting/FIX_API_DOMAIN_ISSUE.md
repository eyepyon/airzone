# API ドメイン問題の修正

## 問題

フロントエンドから `/api/v1/...` を直接呼び出していたため、間違ったドメイン（`https://airz.one`）にリクエストが送信されていました。

正しいAPIドメインは `https://api.airz.one` です。

## 原因

多くのコンポーネントとライブラリで、環境変数 `NEXT_PUBLIC_API_URL` を使用せずに直接 `/api/v1/...` を呼び出していました。

## 修正内容

以下のファイルで環境変数を使用するように修正しました：

### コアライブラリ
- `frontend/lib/xaman-wallet.ts` - Xaman Wallet統合
- `frontend/lib/xaman-wallet-sdk.ts` - Xaman Wallet SDK
- `frontend/lib/xaman-wallet-connector.ts` - Xaman Wallet Connector

### コンポーネント
- `frontend/components/referral/ReferralCard.tsx` - 紹介カード
- `frontend/components/shop/XRPLPaymentForm.tsx` - XRPL決済フォーム
- `frontend/components/wallet/XamanWalletConnect.tsx` - Xaman Wallet接続
- `frontend/components/wallet/XamanWalletConnectFull.tsx` - Xaman Wallet接続（完全版）
- `frontend/components/wallet/XamanWalletConnectSimple.tsx` - Xaman Wallet接続（簡易版）
- `frontend/components/wallet/XamanWalletConnectWorking.tsx` - Xaman Wallet接続（動作版）

### ページ
- `frontend/app/checkout/page.tsx` - チェックアウトページ
- `frontend/app/referral/page.tsx` - 紹介ページ（既に修正済み）
- `frontend/app/staking/page.tsx` - ステーキングページ（既に修正済み）

## 修正パターン

### 修正前
```typescript
const response = await fetch('/api/v1/wallet/connect', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
```

### 修正後
```typescript
const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
const response = await fetch(`${apiUrl}/api/v1/wallet/connect`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
```

## 環境変数設定

`frontend/.env` で以下のように設定されています：

```env
NEXT_PUBLIC_API_URL=https://api.airz.one
```

## 確認方法

1. フロントエンドをビルド：
```bash
cd frontend
npm run build
```

2. ブラウザの開発者ツールでネットワークタブを確認
   - すべてのAPIリクエストが `https://api.airz.one/api/v1/...` に送信されることを確認

## 影響範囲

- ✅ ウォレット接続機能
- ✅ XRPL決済機能
- ✅ 紹介システム
- ✅ ステーキング機能
- ✅ チェックアウト機能
- ✅ NFT確認機能

## 注意事項

### 本番環境での重要な原則

1. **ダミーデータ禁止** - 実装できない機能を動いているように見せかけない
2. **XRPLブロックチェーン必須** - ブロックチェーン関連の機能は必ずXRPLへの実際の問い合わせを行う
3. **データベースでの誤魔化し禁止** - ブロックチェーンデータをデータベースだけで管理しない

### 今後の開発

新しいAPIエンドポイントを呼び出す際は、必ず以下のパターンを使用してください：

```typescript
const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
const response = await fetch(`${apiUrl}/api/v1/your-endpoint`, {
  // ...
});
```

## テスト

修正後、以下の機能をテストしてください：

1. ログイン・ログアウト
2. Xaman Wallet接続
3. XRPL決済
4. 紹介コード取得
5. ステーキング情報取得
6. NFT保有確認

すべてのAPIリクエストが正しいドメイン（`https://api.airz.one`）に送信されることを確認してください。

## 修正日時

2024年11月20日

## 関連ドキュメント

- [API接続問題の修正手順](./FIX_REFERRAL_404_ERROR.md)
- [環境変数設定](../../frontend/.env)
- [アーキテクチャ概要](../../ARCHITECTURE.md)
