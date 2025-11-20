# トラブルシューティングドキュメント

このディレクトリには、開発中に発生した問題とその修正方法をまとめたドキュメントが含まれています。

## API接続問題

- [FINAL_API_FIX_SUMMARY.md](./FINAL_API_FIX_SUMMARY.md) - API接続問題の総合的な修正まとめ

## 管理画面の問題

- [FIX_404_ADMIN.md](./FIX_404_ADMIN.md) - Laravel管理画面の404エラー修正
- [FIX_IMPORTANCE_500_ERROR.md](./FIX_IMPORTANCE_500_ERROR.md) - 重要ユーザー管理の500エラー修正
- [FIX_VIP_BATCH_TRANSFER_404.md](./FIX_VIP_BATCH_TRANSFER_404.md) - VIP機能と一括送金の404エラー修正

## エスクローキャンペーン

- [FIX_ESCROW_500_ERROR.md](./FIX_ESCROW_500_ERROR.md) - エスクロー管理画面の500エラー修正
- [FIX_STAKING_PAGE_DISPLAY.md](./FIX_STAKING_PAGE_DISPLAY.md) - ステーキングページの表示問題修正
- [DEBUG_ESCROW_CAMPAIGNS.md](./DEBUG_ESCROW_CAMPAIGNS.md) - エスクローキャンペーンのデバッグ手順

## 紹介機能

- [FIX_REFERRALS_500_ERROR.md](./FIX_REFERRALS_500_ERROR.md) - 紹介機能の500エラー修正
- [FIX_REFERRAL_JSON_ERROR.md](./FIX_REFERRAL_JSON_ERROR.md) - 紹介ページのJSONパースエラー修正
- [FIX_REFERRAL_404_ERROR.md](./FIX_REFERRAL_404_ERROR.md) - 紹介ページの404エラー修正
- [FIX_REFERRAL_BLANK_PAGE.md](./FIX_REFERRAL_BLANK_PAGE.md) - 紹介ページの真っ白問題修正

## 商品管理

- [FIX_PRODUCT_DISPLAY.md](./FIX_PRODUCT_DISPLAY.md) - 商品詳細ページの表示問題修正

## 使用方法

各ドキュメントには以下の情報が含まれています：

1. **問題の説明** - 何が起きたか
2. **原因** - なぜ起きたか
3. **修正方法** - どう修正したか
4. **動作確認** - 修正後の確認方法
5. **トラブルシューティング** - さらに問題が発生した場合の対処法

## 注意事項

- これらのドキュメントは開発中に発生した問題の記録です
- 本番環境に適用する前に、必ずテスト環境で確認してください
- データベースマイグレーションは必ずバックアップを取ってから実行してください
