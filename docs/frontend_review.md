# フロントエンドコードレビュー報告書

## 概要
`/frontend/` ディレクトリ内のNext.jsアプリケーションのコードレビューを行いました。
全体的な構成は標準的ですが、**ビジネスロジックに関わる重大な問題**と、セキュリティおよび保守性に関する改善点が見つかりました。

## 致命的な問題 (Critical Issues)

### 1. XRP/JPYレートのハードコード
`lib/xrpl-payment.ts` および `components/shop/XRPLPaymentForm.tsx` において、XRPの換算レートが **1 XRP = 150 JPY** に固定されています。

**該当箇所:**
- `lib/xrpl-payment.ts`: L110
- `components/shop/XRPLPaymentForm.tsx`: L29

```typescript
// lib/xrpl-payment.ts
export async function getXRPJPYRate(): Promise<number> {
  // TODO: 実際の為替レートAPIから取得
  // 例: CoinGecko API, Binance API など
  return 150; // 1 XRP = 150 JPY（仮）
}
```

**リスク:**
実際の市場価格と乖離した場合、ユーザーが過剰に支払う、または支払額が不足する（安く買えてしまう）という深刻な金銭的損害が発生します。

**修正案:**
CoinGeckoやBinanceなどの外部API、またはバックエンド経由でリアルタイムのレートを取得する実装に置き換える必要があります。

## 改善が必要な点 (Improvements)

### 1. APIクライアントの利用不徹底
`lib/api-client.ts` という共通のAPIクライアントが用意されていますが、いくつかの重要なコンポーネントで `fetch` を直接使用しています。

**該当箇所:**
- `app/checkout/page.tsx`: L81 (NFT要件チェック)
- `components/shop/XRPLPaymentForm.tsx`: L63 (ステータス確認), L105 (決済実行)

**リスク:**
`api-client.ts` に実装されている「トークンの自動リフレッシュ」や「統一されたエラーハンドリング」が機能しません。トークンの有効期限が切れた際、これらの処理で予期せぬエラーが発生する可能性があります。

**推奨:**
すべてのAPI通信を `lib/api/` 以下のモジュールに集約し、`apiClient` を経由するようにリファクタリングすることを強く推奨します。

### 2. トークンのlocalStorage保存
認証トークン（Access Token, Refresh Token）を `localStorage` に保存しています。

**該当箇所:**
- `lib/api-client.ts`: L130, L145

**リスク:**
XSS（クロスサイトスクリプティング）脆弱性があった場合、攻撃者にトークンを奪取されるリスクがあります。

**推奨:**
Next.jsのMiddlewareとCookie（httpOnly, secure）を使用したセッション管理への移行を検討してください。あるいは、Refresh TokenだけでもCookieで管理することを推奨します。

### 3. 環境変数のフォールバック
`process.env.NEXT_PUBLIC_API_URL` が未設定の場合、空文字やローカルホストにフォールバックする実装になっていますが、本番環境で環境変数が設定されていない場合に意図しない動作をする可能性があります。

## 良い点 (Good Points)

1.  **コンポーネント設計**: UIコンポーネントが細かく分割されており、再利用性が考慮されています。
2.  **状態管理**: Zustandを使用したストア管理（`auth-store`, `cart-store`）が導入されており、状態管理がシンプルに保たれています。
3.  **型定義**: TypeScriptの型定義が適切に行われており、開発時の安全性確保されています。

## 結論
**XRPレートのハードコード**はサービスイン前に必ず修正すべき致命的な問題です。
また、APIクライアントの利用を統一することで、アプリケーションの安定性と保守性が大きく向上します。
