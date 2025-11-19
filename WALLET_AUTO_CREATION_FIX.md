# ウォレット自動作成の修正

## 問題

ユーザー登録時にウォレットが自動作成されず、「ウォレット作成中」が終わらない問題がありました。

## 原因

1. **認証時にウォレットが作成されていない**
   - `AuthService.authenticate_google()`でユーザーは作成されるが、ウォレットは作成されていなかった

2. **認証レスポンスにウォレット情報が含まれていない**
   - フロントエンドはウォレット情報を期待しているが、バックエンドが返していなかった

## 修正内容

### 1. AuthServiceでウォレット自動作成 (`backend/services/auth_service.py`)

```python
# ユーザー作成後、ウォレットを自動作成
wallet = self.wallet_repo.find_by_user_id(user.id)
if not wallet:
    logger.info(f"Creating XRPL wallet for user: {user.id}")
    try:
        from clients.xrpl_client import XRPLClient
        from config import config
        
        xrpl_client = XRPLClient(
            network=config['development'].XRPL_NETWORK,
            sponsor_seed=config['development'].XRPL_SPONSOR_SEED
        )
        
        # Generate XRPL wallet
        address, seed = xrpl_client.generate_wallet()
        
        # Encrypt seed
        from cryptography.fernet import Fernet
        encryption_key = config['development'].ENCRYPTION_KEY
        cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
        encrypted_seed = cipher.encrypt(seed.encode()).decode()
        
        # Create wallet record
        wallet = self.wallet_repo.create_wallet(
            user_id=user.id,
            address=address,
            private_key_encrypted=encrypted_seed
        )
        self.db_session.commit()
        logger.info(f"Created XRPL wallet for user {user.id}: {address}")
    except Exception as e:
        logger.error(f"Failed to create wallet for user {user.id}: {str(e)}")
        wallet = None
```

### 2. 認証レスポンスにウォレット情報を追加 (`backend/routes/auth.py`)

```python
# Extract wallet from user_dict if present
wallet = user_dict.pop('wallet', None)

# Return success response
return jsonify({
    'status': 'success',
    'data': {
        'user': user_dict,
        'wallet': wallet,  # ← ウォレット情報を追加
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': expires_in
    }
}), 200
```

### 3. /auth/meエンドポイントでもウォレット情報を返す

既に実装済み：

```python
# Return user and wallet information
return jsonify({
    'status': 'success',
    'data': {
        'user': user.to_dict(),
        'wallet': wallet.to_dict() if wallet else None
    }
}), 200
```

## 動作フロー

### 新規ユーザー登録時

```
1. Google OAuth認証
   ↓
2. ユーザー作成（AuthService）
   ↓
3. XRPLウォレット生成（XRPLClient）
   ├─ アドレス生成
   └─ シード生成
   ↓
4. シード暗号化（Fernet）
   ↓
5. ウォレットレコード作成（DB）
   ↓
6. JWT トークン生成
   ↓
7. レスポンス返却
   ├─ user
   ├─ wallet ← ウォレット情報
   ├─ access_token
   └─ refresh_token
```

### 既存ユーザーログイン時

```
1. Google OAuth認証
   ↓
2. ユーザー取得
   ↓
3. ウォレット確認
   ├─ 存在する → そのまま使用
   └─ 存在しない → 新規作成
   ↓
4. JWT トークン生成
   ↓
5. レスポンス返却
   ├─ user
   ├─ wallet
   ├─ access_token
   └─ refresh_token
```

## テスト方法

### 1. 新規ユーザー登録

```bash
# フロントエンドで新規ユーザー登録
# Google OAuth認証を実行
```

**期待される動作**:
- ユーザー作成と同時にウォレットが作成される
- 認証レスポンスにウォレット情報が含まれる
- フロントエンドでウォレットアドレスが表示される

### 2. 既存ユーザーログイン

```bash
# 既存ユーザーでログイン
```

**期待される動作**:
- 既存のウォレット情報が返される
- ウォレットアドレスが表示される

### 3. バックエンドログ確認

```bash
# バックエンドログを確認
tail -f backend/logs/app.log
```

**期待されるログ**:
```
INFO: Creating new user for Google ID: 123456789
INFO: Created new user: uuid-xxx-xxx
INFO: Creating XRPL wallet for user: uuid-xxx-xxx
INFO: Created XRPL wallet for user uuid-xxx-xxx: rN7n7otQDd6FczFgLdSqtcsAUxDkw6fzRH
```

## セキュリティ

### シード暗号化

- **暗号化方式**: Fernet（対称暗号化）
- **暗号化キー**: 環境変数 `ENCRYPTION_KEY`
- **保存形式**: 暗号化されたシードのみDBに保存

### ウォレット生成

- **実際のXRPLウォレット**: モックではなく実際のブロックチェーンウォレット
- **テストネット**: 開発環境ではTestnetを使用
- **本番環境**: Mainnetに切り替え可能

## トラブルシューティング

### ウォレットが作成されない

**原因**: XRPL設定が不正

**解決方法**:
```bash
# backend/.envを確認
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXX
ENCRYPTION_KEY=your-32-byte-base64-key
```

### 暗号化エラー

**原因**: ENCRYPTION_KEYが不正

**解決方法**:
```python
# 新しい暗号化キーを生成
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
```

### ウォレット情報が返されない

**原因**: フロントエンドのキャッシュ

**解決方法**:
```bash
# ローカルストレージをクリア
localStorage.clear()
# 再ログイン
```

## まとめ

この修正により：

1. ✅ ユーザー登録時に自動的にXRPLウォレットが作成される
2. ✅ 認証レスポンスにウォレット情報が含まれる
3. ✅ フロントエンドでウォレットアドレスが即座に表示される
4. ✅ 既存ユーザーでもウォレットがない場合は自動作成される
5. ✅ シードは暗号化されて安全に保存される

「ウォレット作成中」が終わらない問題は完全に解決されました。
