# Xaman Wallet 自動接続実装

## 概要

ウォレットに接続すると、アドレスが自動的に取得される実装が完了しました。
手動でアドレスを入力する必要はありません。

## 実装方法

### 1. ブラウザ拡張機能経由（自動）

Xaman Browser Extensionがインストールされている場合、自動的に検出して接続します。

```typescript
// Xaman拡張機能を検出
if (window.xaman) {
  // アカウント接続をリクエスト
  const accounts = await window.xaman.request({
    method: 'xrpl_requestAccounts',
  });
  
  // アドレスを自動取得
  const address = accounts[0];
}
```

### 2. WalletConnect経由（QRコード）

モバイルアプリの場合、QRコードをスキャンして接続します。

```typescript
// WalletConnectセッションを作成
const { uri, qrCode } = await createWalletConnectSession();

// QRコードを表示
showQRCode(qrCode);

// ユーザーがXamanアプリでスキャン
// → アドレスが自動的に取得される
```

## 使用方法

### ユーザー側

#### ステップ1: 接続ボタンをクリック

```
ダッシュボード → 「Xaman Walletに接続」ボタンをクリック
```

#### ステップ2: 自動接続

**パターンA: ブラウザ拡張機能がある場合**
```
1. 「Xaman Walletに接続」をクリック
   ↓
2. Xaman拡張機能が自動的に起動
   ↓
3. 「接続を許可」をクリック
   ↓
4. アドレスが自動的に取得される
   ↓
5. 接続完了！
```

**パターンB: モバイルアプリの場合**
```
1. 「Xaman Walletに接続」をクリック
   ↓
2. QRコードが表示される
   ↓
3. Xamanアプリを開く
   ↓
4. QRコードをスキャン
   ↓
5. 「接続を許可」をタップ
   ↓
6. アドレスが自動的に取得される
   ↓
7. 接続完了！
```

### 開発者側

#### コンポーネントの使用

```typescript
import XamanWalletConnectAuto from '@/components/wallet/XamanWalletConnectAuto';

<XamanWalletConnectAuto
  onConnect={(address) => {
    console.log('Connected:', address);
  }}
  onDisconnect={() => {
    console.log('Disconnected');
  }}
/>
```

#### プログラムから接続

```typescript
import { xamanConnector } from '@/lib/xaman-wallet-connector';

// 接続
const connection = await xamanConnector.connect();
console.log('Address:', connection.address);
console.log('Network:', connection.network);

// 状態確認
const isConnected = xamanConnector.isConnected();
const address = xamanConnector.getAddress();

// 切断
await xamanConnector.disconnect();
```

## 技術詳細

### アーキテクチャ

```
フロントエンド
  ↓
XamanWalletConnector
  ├─ Xaman Browser Extension
  │   └─ window.xaman.request()
  │       └─ アドレス自動取得
  │
  └─ WalletConnect
      ├─ QRコード表示
      ├─ Xamanアプリでスキャン
      └─ アドレス自動取得
  ↓
バックエンドに登録
  ↓
データベースに保存
```

### Xaman Browser Extension API

```typescript
// 拡張機能が利用可能か確認
const hasExtension = typeof window.xaman !== 'undefined';

// アカウント接続をリクエスト
const accounts = await window.xaman.request({
  method: 'xrpl_requestAccounts',
});

// ネットワーク情報を取得
const network = await window.xaman.request({
  method: 'xrpl_getNetwork',
});

// トランザクションに署名
const result = await window.xaman.request({
  method: 'xrpl_signTransaction',
  params: {
    transaction: {
      TransactionType: 'Payment',
      Destination: 'rN7n7otQDd6FczFgLdSqtcsAUxDkw6fzRH',
      Amount: '1000000',
    },
  },
});
```

### WalletConnect フロー

```
1. バックエンドでセッション作成
   POST /api/v1/wallet/walletconnect/session
   → { uri, qrCode }

2. QRコードを表示
   <img src={qrCode} />

3. ユーザーがXamanアプリでスキャン

4. ポーリングで接続を確認
   GET /api/v1/wallet/walletconnect/status
   → { connected: true, address: 'rXXX...' }

5. アドレスを取得
   connection.address
```

## セキュリティ

### 安全な接続

1. **ユーザーの明示的な許可**
   - 拡張機能: 「接続を許可」ボタン
   - モバイル: Xamanアプリで承認

2. **秘密鍵は共有されない**
   - アドレスと公開鍵のみ取得
   - 秘密鍵はユーザーのウォレットに保管

3. **トランザクション署名**
   - 各トランザクションごとにユーザーが承認
   - 自動署名なし

### データ保護

```typescript
// LocalStorageに保存（アドレスのみ）
localStorage.setItem('xaman_wallet_connection', JSON.stringify({
  address: 'rN7n7otQDd6FczFgLdSqtcsAUxDkw6fzRH',
  network: 'testnet',
}));

// 秘密鍵は保存されない
```

## トラブルシューティング

### 拡張機能が検出されない

**原因**: Xaman Browser Extensionがインストールされていない

**解決方法**:
1. Chrome Web Store で "Xaman" を検索
2. 拡張機能をインストール
3. ページをリロード

### QRコードが表示されない

**原因**: バックエンドエラー

**解決方法**:
```bash
# バックエンドログを確認
tail -f backend/logs/app.log

# エンドポイントをテスト
curl -X POST http://localhost:5000/api/v1/wallet/walletconnect/session \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 接続がタイムアウトする

**原因**: ネットワーク接続の問題

**解決方法**:
1. インターネット接続を確認
2. Xamanアプリが最新版か確認
3. QRコードを再生成

### アドレスが取得できない

**原因**: 権限が許可されていない

**解決方法**:
1. Xaman拡張機能の設定を確認
2. サイトへのアクセス許可を確認
3. 拡張機能を再インストール

## 比較: 手動入力 vs 自動接続

### 手動入力方式（旧）

```
❌ ユーザーがアドレスをコピー
❌ プロンプトに手動で入力
❌ 入力ミスの可能性
❌ 手間がかかる
```

### 自動接続方式（新）

```
✅ ボタンをクリックするだけ
✅ アドレスが自動的に取得
✅ 入力ミスなし
✅ 簡単で高速
```

## まとめ

この実装により：

1. ✅ **アドレスの手動入力が不要**
   - ウォレットに接続するだけ
   - アドレスは自動的に取得

2. ✅ **2つの接続方法をサポート**
   - ブラウザ拡張機能（デスクトップ）
   - WalletConnect（モバイル）

3. ✅ **ユーザー体験の向上**
   - MetaMaskやWalletConnectと同じUX
   - 簡単で直感的

4. ✅ **セキュア**
   - 秘密鍵は共有されない
   - ユーザーの明示的な許可が必要

5. ✅ **エラーハンドリング完備**
   - 明確なエラーメッセージ
   - トラブルシューティングガイド

ウォレット接続が簡単になり、ユーザー体験が大幅に向上しました！
