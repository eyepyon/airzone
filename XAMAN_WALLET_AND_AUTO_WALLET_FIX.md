# Xaman Wallet & 自動ウォレット修正

## 修正内容

### 1. 自動ウォレット生成の修正

#### 問題
- ユーザー登録時にウォレットが自動生成されない
- `xrpl-py`パッケージがインストールされていなかった

#### 解決方法

**バックエンドパッケージのインストール**:
```bash
pip install xrpl-py==4.3.1
```

**requirements.txtの更新**:
```
xrpl-py==4.3.1
```

**動作確認**:
```python
from clients.xrpl_client import XRPLClient
client = XRPLClient('testnet')
address, seed = client.generate_wallet()
print(f'Address: {address}')
```

### 2. Xaman Wallet連携の最新化

#### 問題
- 古い仕様の手動入力方式のみ
- 実際のXaman APIと連携していない

#### 解決方法

**新しいXaman SDK実装** (`frontend/lib/xaman-wallet-sdk.ts`):

```typescript
import { xamanWalletSDK } from '@/lib/xaman-wallet-sdk';

// 接続
const state = await xamanWalletSDK.connect();
// → QRコード表示 → Xamanアプリで署名 → 自動接続

// 状態確認
const isConnected = xamanWalletSDK.isConnected();
const address = xamanWalletSDK.getAddress();

// 切断
await xamanWalletSDK.disconnect();
```

**Xaman APIクライアント** (`backend/clients/xaman_client.py`):

```python
from clients.xaman_client import XamanClient

client = XamanClient(api_key, api_secret)

# サインインペイロード作成
payload = client.create_signin_payload()
# → QRコード、ディープリンク、WebSocket URL

# 支払いペイロード作成
payload = client.create_payment_payload(
    destination='rN7n7otQDd6FczFgLdSqtcsAUxDkw6fzRH',
    amount_drops='1000000',
    memo='order_123'
)

# ステータス確認
status = client.get_payload_status(uuid)
```

## 実装の特徴

### 自動ウォレット生成

**フロー**:
```
ユーザー登録
  ↓
AuthService.authenticate_google()
  ↓
XRPLClient.generate_wallet()
  ├─ アドレス生成
  └─ シード生成
  ↓
シード暗号化（Fernet）
  ↓
データベースに保存
  ↓
認証レスポンスに含める
```

**セキュリティ**:
- シードはFernet対称暗号化
- 環境変数で暗号化キーを管理
- データベースには暗号化されたシードのみ保存

### Xaman Wallet連携

**フロー**:
```
1. ユーザーが「Xaman Walletを接続」をクリック
   ↓
2. バックエンドでXamanペイロード作成
   ├─ API Key/Secret使用
   └─ サインインペイロード
   ↓
3. QRコードとディープリンクを表示
   ↓
4. ユーザーがXamanアプリでスキャン/開く
   ↓
5. Xamanアプリで署名
   ↓
6. WebSocketでリアルタイム通知
   ↓
7. ウォレットアドレスを取得
   ↓
8. バックエンドに登録
   ↓
9. 接続完了！
```

**WebSocket通信**:
```typescript
const ws = new WebSocket(payload.refs.websocket_status);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.signed === true) {
    // 署名完了
    const address = data.response.account;
    const txid = data.response.txid;
  } else if (data.signed === false) {
    // 署名拒否
  }
};
```

## 設定方法

### 1. Xaman API設定

**Xaman Developer Consoleでアプリを作成**:
1. https://apps.xumm.dev/ にアクセス
2. 新しいアプリを作成
3. API KeyとAPI Secretを取得

**環境変数に設定**:
```env
# backend/.env
XAMAN_API_KEY=your_api_key_here
XAMAN_API_SECRET=your_api_secret_here
```

**config.pyに追加**:
```python
class Config:
    XAMAN_API_KEY = os.getenv('XAMAN_API_KEY')
    XAMAN_API_SECRET = os.getenv('XAMAN_API_SECRET')
```

### 2. フォールバックモード

Xaman API設定がない場合、自動的に簡易版（手動入力）にフォールバックします：

```python
if xaman_api_key and xaman_api_secret:
    # 実際のXaman APIを使用
    xaman_client = XamanClient(xaman_api_key, xaman_api_secret)
    payload = xaman_client.create_signin_payload()
else:
    # フォールバック: 簡易版
    logger.warning("Xaman API credentials not configured, using fallback")
    # 手動入力方式
```

## 使用方法

### ユーザー側

#### 自動ウォレット（デフォルト）

```
1. Google OAuth でログイン
   ↓
2. 自動的にXRPLウォレットが生成される
   ↓
3. ダッシュボードでアドレスを確認
   ↓
4. NFTは自動的にこのウォレットに送信される
```

#### Xaman Wallet接続（オプション）

```
1. ダッシュボードで「Xaman Walletを接続」をクリック
   ↓
2. QRコードが表示される
   ↓
3. Xamanアプリでスキャン
   ↓
4. 署名を承認
   ↓
5. 接続完了！
   ↓
6. 以降、NFTはXaman Walletに送信される
```

### 開発者側

#### 自動ウォレットの使用

```python
from services.wallet_service import WalletService

# ウォレット作成（自動）
wallet = wallet_service.ensure_user_has_wallet(user_id)

# ウォレット情報取得
wallet = wallet_service.get_user_wallet(user_id)
print(f"Address: {wallet['address']}")

# 残高確認
balance = wallet_service.get_wallet_balance(user_id)
print(f"Balance: {balance / 1_000_000} XRP")
```

#### Xaman Walletの使用

```typescript
import { xamanWalletSDK } from '@/lib/xaman-wallet-sdk';

// 接続
const handleConnect = async () => {
  try {
    const state = await xamanWalletSDK.connect();
    console.log('Connected:', state.address);
  } catch (error) {
    console.error('Connection failed:', error);
  }
};

// トランザクション署名
const handleSign = async () => {
  const txid = await xamanWalletSDK.signTransaction({
    TransactionType: 'Payment',
    Destination: 'rN7n7otQDd6FczFgLdSqtcsAUxDkw6fzRH',
    Amount: '1000000',
  });
  console.log('Transaction ID:', txid);
};
```

## トラブルシューティング

### 自動ウォレットが生成されない

**原因**: xrpl-pyがインストールされていない

**解決方法**:
```bash
cd backend
pip install xrpl-py==4.3.1
```

### Xaman接続が失敗する

**原因1**: API設定が不正

**解決方法**:
```bash
# .envを確認
XAMAN_API_KEY=your_key
XAMAN_API_SECRET=your_secret
```

**原因2**: WebSocket接続エラー

**解決方法**:
- ファイアウォール設定を確認
- ブラウザのコンソールでエラーを確認
- Xaman APIのステータスを確認

### QRコードが表示されない

**原因**: バックエンドエラー

**解決方法**:
```bash
# バックエンドログを確認
tail -f backend/logs/app.log

# エラーメッセージを確認
```

## まとめ

この修正により：

1. ✅ ユーザー登録時に自動的にXRPLウォレットが生成される
2. ✅ Xaman Wallet連携が最新の仕様に対応
3. ✅ QRコードスキャンで簡単に接続
4. ✅ WebSocketでリアルタイム通知
5. ✅ フォールバックモードで開発も容易
6. ✅ セキュアなシード管理

ユーザーは自動生成ウォレットまたはXaman Walletを選択でき、どちらも完全に機能します！
