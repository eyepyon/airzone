# Backend Scripts

このディレクトリには、バックエンドのセットアップとメンテナンス用スクリプトが含まれています。

## スクリプトの種類

### データベースセットアップ

- `init_db.py` - データベースの初期化
- `setup_db_simple.py` - シンプルなデータベースセットアップ
- `run_migration.py` - データベースマイグレーションの実行

### ウォレット管理

- `fund_sponsor_wallet.py` - スポンサーウォレットへの資金供給

## 使用方法

### データベースの初期化

```bash
cd backend
python scripts/init_db.py
```

このスクリプトは以下を実行します：
- データベースの作成
- テーブルの作成
- 初期データの投入

### データベースマイグレーション

```bash
cd backend
python scripts/run_migration.py
```

既存のデータベースに新しいカラムやテーブルを追加します。

### スポンサーウォレットへの資金供給

```bash
cd backend
python scripts/fund_sponsor_wallet.py
```

XRPLテストネットでスポンサーウォレットに資金を供給します。

## 環境変数

スクリプトの実行には以下の環境変数が必要です：

```bash
# データベース
DATABASE_URL=mysql+pymysql://user:password@localhost/airzone

# XRPL
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## 実行順序

初回セットアップ時は以下の順序で実行してください：

1. **データベース初期化**
   ```bash
   python scripts/init_db.py
   ```

2. **マイグレーション実行**（必要に応じて）
   ```bash
   python scripts/run_migration.py
   ```

3. **スポンサーウォレット資金供給**（テストネットの場合）
   ```bash
   python scripts/fund_sponsor_wallet.py
   ```

## 注意事項

### 本番環境での実行

- 本番環境でスクリプトを実行する前に、必ずバックアップを取ってください
- `init_db.py` は既存のデータを削除する可能性があります
- マイグレーションは本番環境で慎重に実行してください

### テスト環境での実行

- テスト環境では自由にスクリプトを実行できます
- データベースをリセットする場合は `init_db.py` を使用
- XRPLテストネットは無料で使用できます

## トラブルシューティング

### データベース接続エラー

`.env` ファイルの `DATABASE_URL` を確認してください：

```bash
DATABASE_URL=mysql+pymysql://root:password@localhost/airzone
```

### XRPL接続エラー

`.env` ファイルの XRPL 設定を確認してください：

```bash
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### マイグレーションエラー

マイグレーションが失敗した場合：

1. データベースのバックアップを確認
2. エラーメッセージを確認
3. 必要に応じて手動でSQLを実行

## スクリプトの追加

新しいスクリプトを追加する場合：

1. `scripts/` ディレクトリに新しいファイルを作成
2. 適切な命名規則に従う（例：`setup_*.py`, `migrate_*.py`）
3. 実行可能にする：`chmod +x scripts/your_script.py`
4. このREADMEを更新
5. 必要に応じてドキュメントを追加

## 関連ドキュメント

- [データベースセットアップガイド](../../docs/setup/DATABASE_SETUP.md)
- [XRPL統合ガイド](../../XRPL_BLOCKCHAIN_IMPLEMENTATION.md)
- [デプロイメントガイド](../../DEPLOYMENT_INDEX.md)
