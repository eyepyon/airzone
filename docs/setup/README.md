# セットアップドキュメント

このディレクトリには、Airzoneプロジェクトのセットアップに関するドキュメントが含まれています。

## クイックスタート

- [GETTING_STARTED.md](./GETTING_STARTED.md) - 英語版スタートガイド
- [GETTING_STARTED_JP.md](./GETTING_STARTED_JP.md) - 日本語版スタートガイド

## データベースセットアップ

### 推奨ドキュメント

- [DATABASE_QUICK_START.md](./DATABASE_QUICK_START.md) - **最も簡単な方法**
- [DATABASE_SETUP_SIMPLE.md](./DATABASE_SETUP_SIMPLE.md) - シンプルなセットアップ手順

### 詳細ドキュメント

- [DATABASE_SETUP.md](./DATABASE_SETUP.md) - 完全なセットアップ手順
- [DATABASE_SETUP_CHECKLIST.md](./DATABASE_SETUP_CHECKLIST.md) - セットアップチェックリスト
- [DATABASE_SETUP_COMPLETE.md](./DATABASE_SETUP_COMPLETE.md) - 完了確認手順
- [DATABASE_SETUP_NO_ROOT.md](./DATABASE_SETUP_NO_ROOT.md) - root権限なしでのセットアップ

## 管理画面セットアップ

- [INSTALL.md](./INSTALL.md) - Laravel管理画面のインストール手順

## AI開発ツール

- [AI_TOOLS_SETUP.md](./AI_TOOLS_SETUP.md) - AI開発ツールのセットアップ

## セットアップの順序

1. **データベース**: `DATABASE_QUICK_START.md` を参照
2. **バックエンド**: `GETTING_STARTED.md` の Backend Setup セクション
3. **フロントエンド**: `GETTING_STARTED.md` の Frontend Setup セクション
4. **管理画面**: `INSTALL.md` を参照

## トラブルシューティング

セットアップ中に問題が発生した場合は、[../troubleshooting/](../troubleshooting/) ディレクトリのドキュメントを参照してください。

## 注意事項

- セットアップ前に必要な環境（Node.js, Python, MySQL, PHP）がインストールされていることを確認してください
- 本番環境では、セキュリティ設定を適切に行ってください
- データベースのパスワードは必ず変更してください
