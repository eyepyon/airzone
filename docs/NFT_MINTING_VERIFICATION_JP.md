# NFT発行の検証ガイド

## NFT発行フロー

### 1. 発行プロセス

```
ユーザー登録
    ↓
自動ウォレット作成
    ↓
WiFi接続 / NFT発行リクエスト
    ↓
NFT発行タスク作成（PENDING）
    ↓
XRPLブロックチェーンでNFT発行（MINTING）
    ↓
トランザクション完了（COMPLETED）
    ↓
NFTがウォレットに付与
```

### 2. 実装の確認

#### ✅ 実装済み機能

1. **自動ウォレット生成**
   - ユーザー登録時に自動作成
   - XRPLアドレス（rから始まる）
   - 秘密鍵は暗号化して保存

2. **NFT発行サービス**
   - `NFTService.mint_nft()` - NFT発行リクエスト
   - `NFTService._execute_nft_mint()` - 実際の発行処理
   - タスクマネージャーで非同期処理

3. **XRPLクライアント**
   - `XRPLClient.mint_nft()` - ブロックチェーンへのNFT発行
   - NFTokenMintトランザクション使用
   - トランザクションハッシュを記録

4. **データベース記録**
   - `nft_mints` テーブルにステータス記録
   - PENDING → MINTING → COMPLETED
   - NFT Token IDとトランザクションハッシュを保存

## 検証方法

### 方法1: フロントエンドから確認

#### ステップ1: ログイン
```
1. https://airz.one にアクセス
2. Googleアカウントでログイン
3. ダッシュボードに移動
```

#### ステップ2: ウォレット確認
```
ダッシュボード → 💼 XRPL Wallet
- ウォレットアドレスが表示される
- "Active" バッジが表示される
- アドレスをコピー
```

#### ステップ3: NFT発行
```
方法A: WiFi接続
- 対象WiFiに接続
- 自動的にNFT発行

方法B: 手動リクエスト
- /nfts ページにアクセス
- "Mint NFT" ボタンをクリック
```

#### ステップ4: NFT確認
```
/nfts ページで確認
- 発行中: "Minting..." ステータス
- 完了: NFT画像とメタデータ表示
- NFT Token IDが表示される
```

### 方法2: XRPLエクスプローラーで確認

#### ステップ1: ウォレットアドレスをコピー
```
ダッシュボード → ウォレットアドレスをコピー
例: rN7n7otQDd6FczFgLdlqtyMVrn3HMzve5w
```

#### ステップ2: エクスプローラーで確認
```
Testnet: https://testnet.xrpl.org/accounts/{address}
Mainnet: https://livenet.xrpl.org/accounts/{address}
```

#### ステップ3: NFTタブを確認
```
1. アカウントページの "NFTs" タブをクリック
2. 発行されたNFTのリストが表示される
3. NFT Token IDをクリックして詳細確認
```

### 方法3: APIで直接確認

#### NFT一覧取得
```bash
curl -X GET "https://api.airz.one/api/v1/nfts" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**レスポンス例**:
```json
{
  "status": "success",
  "data": {
    "nfts": [
      {
        "id": "nft_123",
        "user_id": "user_456",
        "wallet_address": "rN7n7otQDd6FczFgLdlqtyMVrn3HMzve5w",
        "nft_object_id": "00080000...",
        "status": "completed",
        "transaction_digest": "ABC123...",
        "nft_metadata": {
          "name": "Airzone NFT",
          "description": "Welcome NFT",
          "image_url": "https://..."
        },
        "created_at": "2025-11-18T10:00:00Z"
      }
    ]
  }
}
```

### 方法4: データベースで直接確認

```sql
-- NFT発行記録を確認
SELECT 
    id,
    user_id,
    wallet_address,
    status,
    nft_object_id,
    transaction_digest,
    created_at
FROM nft_mints
WHERE user_id = 'YOUR_USER_ID'
ORDER BY created_at DESC;

-- ウォレット情報を確認
SELECT 
    id,
    user_id,
    address,
    created_at
FROM wallets
WHERE user_id = 'YOUR_USER_ID';
```

## トラブルシューティング

### 問題1: NFTが表示されない

#### 原因と解決策

**原因A: 発行処理中**
```
ステータス: PENDING または MINTING
解決策: 数分待ってページを再読み込み
```

**原因B: スポンサーウォレットの残高不足**
```
確認方法:
curl -X GET "https://api.airz.one/api/v1/admin/xrpl/sponsor-health" \
  -H "Authorization: Bearer ADMIN_TOKEN"

解決策:
1. スポンサーウォレットにXRPを送金
2. Testnetの場合: https://xrpl.org/xrp-testnet-faucet.html
```

**原因C: ネットワークエラー**
```
確認方法:
- バックエンドログを確認: backend/logs/app.log
- エラーメッセージを確認

解決策:
- XRPLネットワークの状態を確認
- 再度NFT発行をリクエスト
```

### 問題2: ウォレットが作成されない

#### 確認事項

```sql
-- ユーザーが存在するか確認
SELECT * FROM users WHERE id = 'YOUR_USER_ID';

-- ウォレットが存在するか確認
SELECT * FROM wallets WHERE user_id = 'YOUR_USER_ID';
```

#### 解決策

```
1. ログアウト
2. ログイン（ウォレットが自動作成される）
3. ダッシュボードで確認
```

### 問題3: NFT発行が失敗する

#### ログ確認

```bash
# バックエンドログ
tail -f /var/www/airzone/backend/logs/app.log | grep NFT

# エラーを検索
grep "ERROR" /var/www/airzone/backend/logs/app.log | grep nft
```

#### よくあるエラー

**エラー1: "Sponsor wallet not configured"**
```
原因: スポンサーウォレットが設定されていない
解決策: .envファイルでXRPL_SPONSOR_SEEDを設定
```

**エラー2: "Insufficient balance"**
```
原因: スポンサーウォレットの残高不足
解決策: スポンサーウォレットにXRPを送金
```

**エラー3: "Invalid wallet address"**
```
原因: ウォレットアドレスが無効
解決策: ウォレットを再作成
```

## NFT発行の確認チェックリスト

### ✅ 事前確認

- [ ] ユーザーが登録されている
- [ ] ウォレットが作成されている
- [ ] スポンサーウォレットに十分なXRPがある
- [ ] XRPLネットワークが正常に動作している

### ✅ 発行後確認

- [ ] `/nfts` ページでNFTが表示される
- [ ] NFTのステータスが "completed"
- [ ] NFT Token IDが記録されている
- [ ] トランザクションハッシュが記録されている
- [ ] XRPLエクスプローラーでNFTが確認できる

### ✅ データ整合性確認

- [ ] データベースに記録がある
- [ ] ウォレットアドレスが一致している
- [ ] ブロックチェーン上のNFTと一致している

## 実際の動作確認手順

### 完全なテストフロー

```bash
# 1. 新規ユーザーを作成
# ブラウザでGoogleログイン

# 2. ウォレット確認
# ダッシュボードでウォレットアドレスを確認
WALLET_ADDRESS="rN7n7otQDd6FczFgLdlqtyMVrn3HMzve5w"

# 3. NFT発行リクエスト
curl -X POST "https://api.airz.one/api/v1/nfts/mint" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nft_name": "Test NFT",
    "nft_description": "Test Description",
    "nft_image_url": "https://example.com/image.png"
  }'

# 4. ステータス確認（数秒待つ）
curl -X GET "https://api.airz.one/api/v1/nfts" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 5. XRPLエクスプローラーで確認
# https://testnet.xrpl.org/accounts/$WALLET_ADDRESS
```

## まとめ

### NFTは正しくウォレットに付与されます

✅ **実装済み**:
1. 自動ウォレット生成
2. NFT発行サービス
3. XRPLブロックチェーン統合
4. トランザクション記録
5. エラーハンドリング

✅ **確認方法**:
1. フロントエンド（/nfts）
2. XRPLエクスプローラー
3. API
4. データベース

✅ **安全性**:
- ブロックチェーン上で永続化
- トランザクションハッシュで検証可能
- 秘密鍵は暗号化して保存

NFTは確実にユーザーのウォレットに付与され、XRPLブロックチェーン上で管理されています。
