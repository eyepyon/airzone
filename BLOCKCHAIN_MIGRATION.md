# ブロックチェーン移行完了

## 概要

AirzoneのブロックチェーンをSuiからXRPL (XRP Ledger)に移行しました。

## 移行理由

- **ネイティブNFTサポート**: XRPLはNFT機能が標準で組み込まれている
- **高速トランザクション**: 3-5秒で確定
- **低コスト**: トランザクション手数料は約0.00001 XRP
- **環境に優しい**: Proof of Workを使用しない
- **成熟したエコシステム**: 2012年から稼働している実績

## 変更内容

### 削除されたもの

- `backend/clients/sui_client.py` - Suiクライアント
- `contracts/` ディレクトリ全体 - Sui Moveスマートコントラクト
- `scripts/deploy_contract.sh` - Suiコントラクトデプロイスクリプト
- `scripts/verify_contract.py` - Sui検証スクリプト
- `backend/verify_sui_client.py` - Sui検証スクリプト

### 追加・更新されたもの

- `backend/clients/xrpl_client.py` - 新しいXRPLクライアント
- `backend/services/nft_service.py` - XRPLに対応
- `backend/services/wallet_service.py` - XRPLに対応
- `backend/routes/nft.py` - XRPLクライアントを使用
- `backend/config.py` - XRPL設定に変更
- `backend/.env` - XRPL設定に変更
- `backend/requirements.txt` - `xrpl-py`ライブラリに変更
- `scripts/generate_sponsor_wallet.py` - XRPL用に更新
- `backend/verify_xrpl_client.py` - XRPL検証スクリプト
- `docs/xrpl-integration.md` - XRPL統合ガイド

## セットアップ手順

### 1. 依存関係のインストール

```bash
cd backend
pip install -r requirements.txt
```

### 2. スポンサーウォレットの生成

```bash
python scripts/generate_sponsor_wallet.py
```

### 3. 環境変数の設定

`backend/.env`に以下を追加:

```env
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 4. テストネットフォーセットから資金を取得

https://xrpl.org/xrp-testnet-faucet.html

### 5. 動作確認

```bash
python backend/verify_xrpl_client.py
```

## API変更

### 環境変数

**旧 (Sui):**
```env
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=suiprivkey1...
SUI_PACKAGE_ID=0x...
```

**新 (XRPL):**
```env
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### NFT発行レスポンス

**旧 (Sui):**
```json
{
  "nft_object_id": "0x...",
  "transaction_digest": "..."
}
```

**新 (XRPL):**
```json
{
  "nft_token_id": "000...",
  "transaction_hash": "..."
}
```

## データベース

既存のデータベーススキーマは変更不要です。`wallets`テーブルと`nft_mints`テーブルはそのまま使用できます。

## 参考資料

- [XRPL統合ガイド](docs/xrpl-integration.md)
- [XRPL公式ドキュメント](https://xrpl.org/)
- [xrpl-py ライブラリ](https://xrpl-py.readthedocs.io/)
