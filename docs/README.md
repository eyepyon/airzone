# Airzone ドキュメント

**日本語索引**: [INDEX_JP.md](INDEX_JP.md)

## 目次

### 🚀 セットアップ

- [完全セットアップガイド](SETUP_GUIDE_JP.md) - 詳細なインストール手順
- [クイックスタート](../GETTING_STARTED_JP.md) - 素早く始める

### 🔗 ブロックチェーン

- [XRPL統合ガイド](xrpl-integration.md) - XRPL基礎と統合方法
- [Xaman Wallet統合ガイド](xaman-wallet-integration.md) - 開発者向け詳細
- [ウォレット管理ガイド](WALLET_GUIDE_JP.md) - ユーザー向け使い方
- [ブロックチェーン移行](../BLOCKCHAIN_MIGRATION.md) - SuiからXRPLへの移行

### 📊 機能

- [効果測定ダッシュボード](analytics-dashboard.md) - DAU/MAU/DL数の計測

### 🛠️ 管理

- [管理パネルガイド](../admin/README.md) - 管理画面の使い方
- [管理パネルインストール](../admin/INSTALL.md) - 管理画面のセットアップ

### 📚 API

- [API リファレンス](../backend/API_REFERENCE.md) - エンドポイント詳細

## ドキュメント構成

```
docs/
├── README.md                      # このファイル
├── SETUP_GUIDE_JP.md             # 完全セットアップガイド
├── xrpl-integration.md           # XRPL統合ガイド
├── xaman-wallet-integration.md   # Xaman Wallet統合（開発者向け）
├── WALLET_GUIDE_JP.md            # ウォレット管理（ユーザー向け）
└── analytics-dashboard.md        # 効果測定ダッシュボード
```

## 対象読者別ガイド

### 👤 エンドユーザー

1. [ウォレット管理ガイド](WALLET_GUIDE_JP.md) - ウォレットの使い方
2. [Xaman Walletアプリ](https://xaman.app/) - ウォレットアプリのダウンロード

### 👨‍💻 開発者

1. [完全セットアップガイド](SETUP_GUIDE_JP.md) - 開発環境構築
2. [XRPL統合ガイド](xrpl-integration.md) - ブロックチェーン統合
3. [Xaman Wallet統合ガイド](xaman-wallet-integration.md) - ウォレット統合
4. [API リファレンス](../backend/API_REFERENCE.md) - API仕様

### 👨‍💼 管理者

1. [管理パネルガイド](../admin/README.md) - 管理画面の使い方
2. [効果測定ダッシュボード](analytics-dashboard.md) - 指標の見方
3. [運用ガイド](../OPERATIONS.md) - 本番環境の運用

### 🚀 デプロイ担当者

1. [デプロイチェックリスト](../DEPLOYMENT_CHECKLIST.md) - デプロイ前の確認
2. [デプロイ設定](../DEPLOYMENT_CONFIGURATION.md) - 設定方法
3. [運用ガイド](../OPERATIONS.md) - 運用手順

## クイックリンク

### 外部リソース

- [XRPL公式ドキュメント](https://xrpl.org/)
- [Xaman公式サイト](https://xaman.app/)
- [Xaman SDK](https://xumm.readme.io/)
- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Next.js公式ドキュメント](https://nextjs.org/docs)
- [Laravel公式ドキュメント](https://laravel.com/docs/10.x)

### ツール

- [XRPLテストネットフォーセット](https://xrpl.org/xrp-testnet-faucet.html)
- [XRPLエクスプローラー（Testnet）](https://testnet.xrpl.org/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Stripe Dashboard](https://dashboard.stripe.com/)

## サポート

問題が発生した場合：

1. 該当するドキュメントのトラブルシューティングセクションを確認
2. ログファイルを確認:
   - バックエンド: `backend/logs/app.log`
   - 管理パネル: `admin/storage/logs/laravel.log`
3. GitHubのIssuesで報告

## 貢献

ドキュメントの改善提案は歓迎します。Pull Requestをお送りください。
