# ブロックチェーン移行完了

## 概要

AirzoneのブロックチェーンをXRPL (XRP Ledger)に移行しました。

## 移行理由

- **ネイティブNFTサポート**: XRPLはNFT機能が標準で組み込まれている
- **高速トランザクション**: 3-5秒で確定
- **低コスト**: トランザクション手数料は約0.00001 XRP
- **環境に優しい**: Proof of Workを使用しない
- **成熟したエコシステム**: 2012年から稼働している実績

## 変更内容

### 削除されたもの

- 旧ブロックチェーンクライアント
- スマートコントラクトディレクトリ
- 旧デプロイスクリプト

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

**XRPL:**
```env
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### NFT発行レスポンス

**XRPL:**
```json
{
  "nft_token_id": "000...",
  "transaction_hash": "..."
}
```

## データベース

既存のデータベーススキーマは変更不要です。`wallets`テーブルと`nft_mints`テーブルはそのまま使用できます。

## 関連ドキュメント

### ブロックチェーン
- [XRPL統合ガイド](docs/xrpl-integration.md)
- [Xaman Wallet統合](docs/xaman-wallet-integration.md)
- [ウォレット管理ガイド](docs/WALLET_GUIDE_JP.md)

### セットアップ
- [完全セットアップガイド](docs/SETUP_GUIDE_JP.md)
- [クイックスタート](GETTING_STARTED_JP.md)

### 参考リンク
- [XRPL公式ドキュメント](https://xrpl.org/)
- [xrpl-py ライブラリ](https://xrpl-py.readthedocs.io/)
- [Xaman Wallet](https://xaman.app/)
