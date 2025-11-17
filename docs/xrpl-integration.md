# XRPL統合ガイド

## 概要

AirzoneはXRPL (XRP Ledger) ブロックチェーンを使用してNFTの発行と管理を行います。

## XRPLの特徴

- **高速トランザクション**: 3-5秒で確定
- **低コスト**: トランザクション手数料は約0.00001 XRP
- **ネイティブNFTサポート**: NFT機能が標準で組み込まれている
- **環境に優しい**: Proof of Workを使用しない

## セットアップ

### 1. スポンサーウォレットの生成

```bash
python scripts/generate_sponsor_wallet.py
```

ネットワークを選択:
- **Testnet**: 開発・テスト用（推奨）
- **Devnet**: 開発用
- **Mainnet**: 本番環境用

### 2. ウォレットへの資金供給

#### Testnet/Devnet
テストネットフォーセットから無料でXRPを取得:
- https://xrpl.org/xrp-testnet-faucet.html

#### Mainnet
実際のXRPを送金してください。推奨: 最低100 XRP

### 3. 環境変数の設定

`backend/.env`に以下を追加:

```env
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## NFT発行

### APIエンドポイント

```
POST /api/v1/nfts/mint
```

リクエスト:
```json
{
  "nft_name": "Airzone NFT #1",
  "nft_description": "Special WiFi access NFT",
  "nft_image_url": "https://example.com/nft/image.png"
}
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "task_id": "uuid",
    "status": "pending"
  }
}
```

### NFTメタデータ

XRPLのNFTは`URI`フィールドを使用してメタデータを保存します。
URIは以下を指すことができます:

- IPFS URL: `ipfs://QmXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
- HTTP URL: `https://example.com/metadata.json`

メタデータJSON形式:
```json
{
  "name": "Airzone NFT #1",
  "description": "Special WiFi access NFT",
  "image": "https://example.com/nft/image.png",
  "attributes": [
    {
      "trait_type": "Access Level",
      "value": "Premium"
    }
  ]
}
```

## NFT機能

### 転送可能フラグ

NFT発行時に以下のフラグを設定できます:

- `tfTransferable` (8): NFTを転送可能にする
- `tfBurnable` (1): NFTをバーン（破棄）可能にする
- `tfOnlyXRP` (2): XRPでのみ取引可能
- `tfTrustLine` (4): トラストライン必須

デフォルト: `tfTransferable` (8)

### 転送手数料

NFTの二次販売時に発行者が受け取る手数料を設定できます:
- 範囲: 0-50000 (0-50%)
- 例: 1000 = 10%

## ウォレット管理

### 自動ウォレット生成

新規ユーザー登録時に自動的にXRPLウォレットが生成されます:

```python
from services.wallet_service import WalletService

wallet = wallet_service.create_wallet(user_id)
# Returns: {'address': 'rXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', ...}
```

### ウォレットシードの暗号化

ウォレットシード（秘密鍵）は以下の方法で保護されます:

1. Fernet対称暗号化を使用
2. 暗号化キーは環境変数で管理
3. データベースには暗号化されたシードのみ保存

## トラブルシューティング

### スポンサーウォレットの残高不足

```python
from clients.xrpl_client import XRPLClient

client = XRPLClient(network='testnet', sponsor_seed='sXXXXXXXXXX')
health = client.check_sponsor_health()

if not health['healthy']:
    print(health['warnings'])
    print(health['recommendations'])
```

### NFT発行の失敗

一般的な原因:
1. スポンサーウォレットの残高不足
2. 無効なURI形式
3. ネットワーク接続の問題

ログを確認:
```bash
tail -f backend/logs/app.log
```

## Xaman Wallet統合

ユーザーは自分のXaman Wallet（旧Xumm）を接続してNFTを受け取ることができます。

### ドキュメント

- **ユーザー向け**: [ウォレット管理ガイド](WALLET_GUIDE_JP.md)
- **開発者向け**: [Xaman Wallet統合ガイド](xaman-wallet-integration.md)

### 自動ウォレット vs Xaman Wallet

| 機能 | 自動ウォレット | Xaman Wallet |
|------|--------------|--------------|
| 生成 | 自動 | ユーザーが接続 |
| 秘密鍵管理 | バックエンド | ユーザー |
| セキュリティ | 標準 | 高 |
| 使いやすさ | 簡単 | 要アプリ |

## 関連ドキュメント

- [ウォレット管理ガイド](WALLET_GUIDE_JP.md) - ユーザー向け
- [Xaman Wallet統合ガイド](xaman-wallet-integration.md) - 開発者向け
- [セットアップガイド](SETUP_GUIDE_JP.md) - 初期設定

## 参考リンク

- [XRPL公式ドキュメント](https://xrpl.org/)
- [NFT機能ガイド](https://xrpl.org/nft-conceptual-overview.html)
- [xrpl-py ライブラリ](https://xrpl-py.readthedocs.io/)
- [テストネットフォーセット](https://xrpl.org/xrp-testnet-faucet.html)
- [Xaman Wallet](https://xaman.app/)
- [Xaman SDK](https://xumm.readme.io/)
