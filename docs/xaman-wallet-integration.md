# Xaman Wallet 統合ガイド

## 概要

Xaman Wallet（旧Xumm）は、XRPLの主要なモバイル・デスクトップウォレットです。ユーザーは自分のXaman Walletを接続して、NFTを受け取ることができます。

## Xaman Walletとは

- **公式サイト**: https://xaman.app/
- **旧名**: Xumm
- **対応プラットフォーム**: iOS、Android、デスクトップ
- **機能**: XRP送受信、NFT管理、トランザクション署名

## 統合方法

### 1. フロントエンド統合

#### Xaman Wallet接続ボタン

```tsx
import XamanWalletButton from '@/components/wallet/XamanWalletButton';

export default function Dashboard() {
  return (
    <div>
      <h1>ダッシュボード</h1>
      <XamanWalletButton />
    </div>
  );
}
```

#### ウォレット状態の管理

```typescript
import { xamanWallet } from '@/lib/xaman-wallet';

// ウォレットに接続
const state = await xamanWallet.connect();
console.log('Connected:', state.address);

// ウォレットから切断
xamanWallet.disconnect();

// 現在の状態を取得
const currentState = xamanWallet.getState();
```

### 2. バックエンドAPI

#### ウォレット接続

```bash
POST /api/v1/wallet/connect
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "address": "rXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "wallet_type": "xaman"
}
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "wallet": {
      "address": "rXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "wallet_type": "xaman",
      "connected": true
    }
  }
}
```

#### ウォレット切断

```bash
POST /api/v1/wallet/disconnect
Authorization: Bearer <access_token>
```

#### 残高確認

```bash
GET /api/v1/wallet/balance
Authorization: Bearer <access_token>
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "balance_drops": 1000000,
    "balance_xrp": 1.0,
    "address": "rXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  }
}
```

## ユーザーフロー

### 1. 自動ウォレット vs Xaman Wallet

#### 自動ウォレット（デフォルト）
- ユーザー登録時に自動生成
- バックエンドで秘密鍵を管理
- ユーザーは何もする必要なし
- NFTは自動的にこのウォレットに発行

#### Xaman Wallet（オプション）
- ユーザーが自分のXaman Walletを接続
- 秘密鍵はユーザーが管理
- より高いセキュリティ
- NFTはユーザーのXaman Walletに発行

### 2. ウォレット接続フロー

```
1. ユーザーが「Xaman Walletを接続」ボタンをクリック
   ↓
2. Xaman APIでQRコードまたはディープリンクを生成
   ↓
3. ユーザーがXamanアプリで承認
   ↓
4. ウォレットアドレスがフロントエンドに返される
   ↓
5. バックエンドAPIにウォレットアドレスを送信
   ↓
6. データベースのウォレット情報を更新
   ↓
7. 以降のNFT発行はこのアドレスに送信
```

## Xaman SDK統合（実装例）

### NPMパッケージのインストール

```bash
npm install xumm-sdk
```

### SDK初期化

```typescript
import { Xumm } from 'xumm-sdk';

const xumm = new Xumm(
  process.env.NEXT_PUBLIC_XAMAN_API_KEY!,
  process.env.NEXT_PUBLIC_XAMAN_API_SECRET!
);
```

### ペイロード作成とサインイン

```typescript
async function connectXamanWallet() {
  // サインインペイロードを作成
  const payload = await xumm.payload.create({
    txjson: {
      TransactionType: 'SignIn'
    }
  });

  // QRコードまたはディープリンクを表示
  console.log('QR Code:', payload.refs.qr_png);
  console.log('Deep Link:', payload.next.always);

  // ユーザーの承認を待つ
  const result = await xumm.payload.subscribe(payload.uuid);

  if (result.signed) {
    // ウォレットアドレスを取得
    const address = result.account;
    console.log('Connected wallet:', address);
    return address;
  } else {
    throw new Error('User rejected the sign-in request');
  }
}
```

### トランザクション署名

```typescript
async function signTransaction(transaction: any) {
  // トランザクションペイロードを作成
  const payload = await xumm.payload.create({
    txjson: transaction
  });

  // ユーザーの署名を待つ
  const result = await xumm.payload.subscribe(payload.uuid);

  if (result.signed) {
    return result.txid;
  } else {
    throw new Error('User rejected the transaction');
  }
}
```

## セキュリティ考慮事項

### 1. ウォレットアドレスの検証

```python
def validate_xrpl_address(address: str) -> bool:
    """XRPLアドレスの形式を検証"""
    if not address.startswith('r'):
        return False
    if len(address) < 25 or len(address) > 35:
        return False
    # Base58チェックサムの検証（オプション）
    return True
```

### 2. トランザクション検証

- ユーザーがXamanアプリで内容を確認
- トランザクションの詳細を明確に表示
- 不正なトランザクションを防ぐ

### 3. APIキーの管理

```env
# .env.local
NEXT_PUBLIC_XAMAN_API_KEY=your-api-key
NEXT_PUBLIC_XAMAN_API_SECRET=your-api-secret
```

**重要**: APIシークレットはサーバーサイドでのみ使用

## NFT発行フロー

### Xaman Wallet接続時

```python
# backend/services/nft_service.py

def mint_nft_to_xaman_wallet(user_id: str, nft_metadata: dict):
    """Xaman Walletユーザー向けNFT発行"""
    
    # ユーザーのウォレットを取得
    wallet = wallet_repo.find_by_user_id(user_id)
    
    # XRPLクライアントでNFTを発行
    result = xrpl_client.mint_nft(
        recipient_address=wallet.address,  # Xaman Walletのアドレス
        nft_uri=nft_metadata['uri'],
        transfer_fee=0,
        flags=8  # tfTransferable
    )
    
    return result
```

## トラブルシューティング

### ウォレット接続エラー

```typescript
try {
  await xamanWallet.connect();
} catch (error) {
  if (error.message.includes('timeout')) {
    // タイムアウト: ユーザーが承認しなかった
    alert('接続がタイムアウトしました。もう一度お試しください。');
  } else if (error.message.includes('rejected')) {
    // ユーザーが拒否
    alert('接続がキャンセルされました。');
  } else {
    // その他のエラー
    console.error('Connection error:', error);
    alert('ウォレット接続に失敗しました。');
  }
}
```

### NFT受信の確認

```typescript
// XRPLエクスプローラーでNFTを確認
const explorerUrl = `https://testnet.xrpl.org/accounts/${address}/nfts`;
window.open(explorerUrl, '_blank');
```

## 関連ドキュメント

### ユーザー向け
- [ウォレット管理ガイド](WALLET_GUIDE_JP.md) - ユーザー向け使い方ガイド

### 開発者向け
- [XRPL統合ガイド](xrpl-integration.md) - XRPL基礎
- [セットアップガイド](SETUP_GUIDE_JP.md) - 開発環境構築
- [API リファレンス](../backend/API_REFERENCE.md) - API詳細

## 参考リンク

- [Xaman公式サイト](https://xaman.app/)
- [Xaman SDK ドキュメント](https://xumm.readme.io/)
- [XRPL NFT ドキュメント](https://xrpl.org/nft-conceptual-overview.html)
- [XRPLエクスプローラー（Testnet）](https://testnet.xrpl.org/)

## 今後の拡張

- [ ] Xaman Walletでのトランザクション署名
- [ ] NFT転送機能
- [ ] マルチシグネチャ対応
- [ ] ハードウェアウォレット統合
