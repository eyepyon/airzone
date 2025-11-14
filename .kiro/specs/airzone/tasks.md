# Implementation Plan

## Backend Implementation

- [ ] 1. プロジェクト構造とコア設定のセットアップ
  - Flask アプリケーションの基本構造を作成（app.py, config.py, requirements.txt）
  - 環境変数管理の設定（.env.example, config.py）
  - MySQL データベース接続設定（SQLAlchemy）
  - CORS、JWT、セキュリティミドルウェアの設定
  - _Requirements: 6.1, 6.3, 8.1, 8.2_

- [ ] 2. データベースモデルとマイグレーションの実装
  - [ ] 2.1 SQLAlchemy Base モデルとユーティリティの作成
    - Base クラス、to_dict() メソッド、UUID 生成ユーティリティを実装
    - _Requirements: 9.1, 9.2, 9.4_
  
  - [ ] 2.2 User および Wallet モデルの実装
    - users テーブルと wallets テーブルのモデルを作成
    - リレーションシップの定義
    - _Requirements: 1.2, 1.3, 9.5, 9.6_
  
  - [ ] 2.3 NFT、Product、Order 関連モデルの実装
    - nft_mints, products, orders, order_items テーブルのモデルを作成
    - 外部キー制約とインデックスの設定
    - _Requirements: 3.4, 4.1, 5.3, 5.4, 9.7_
  
  - [ ] 2.4 Payment、WiFiSession、TaskQueue モデルの実装
    - payments, wifi_sessions, task_queue テーブルのモデルを作成
    - _Requirements: 2.2, 2.3, 5.5, 10.4_
  
  - [ ] 2.5 データベースマイグレーションスクリプトの作成
    - Alembic を使用したマイグレーション設定
    - 初期マイグレーションファイルの生成
    - _Requirements: 9.1_

- [ ] 3. Repository レイヤーの実装
  - [ ] 3.1 BaseRepository の作成
    - 共通 CRUD 操作を持つ基底クラスを実装
    - パラメータ化クエリの使用
    - _Requirements: 6.4, 8.4, 9.2_
  
  - [ ] 3.2 UserRepository と WalletRepository の実装
    - ユーザーとウォレットの CRUD 操作を実装
    - find_by_google_id, find_by_email などのカスタムクエリ
    - _Requirements: 1.2, 1.3_
  
  - [ ] 3.3 NFTRepository と ProductRepository の実装
    - NFT と商品の CRUD 操作を実装
    - find_by_wallet, find_by_status などのフィルタリング
    - _Requirements: 3.4, 4.2, 4.3_
  
  - [ ] 3.4 OrderRepository と PaymentRepository の実装
    - 注文と決済の CRUD 操作を実装
    - ステータス更新メソッド
    - _Requirements: 5.3, 5.4, 5.5, 5.6_

- [ ] 4. バックグラウンドタスクマネージャーの実装
  - [ ] 4.1 TaskManager クラスの実装
    - ThreadPoolExecutor を使用した非同期タスク実行
    - タスクステータス管理（pending, running, completed, failed）
    - _Requirements: 10.1, 10.2, 10.3_
  
  - [ ] 4.2 TaskRepository の実装
    - task_queue テーブルへの CRUD 操作
    - タスクステータスの更新とクエリ
    - _Requirements: 10.4_
  
  - [ ] 4.3 リトライロジックの実装
    - 指数バックオフを使用したリトライメカニズム
    - 最大リトライ回数の設定
    - _Requirements: 3.5, 10.5_

- [ ] 5. 外部 API クライアントの実装
  - [ ] 5.1 Google OAuth クライアントの実装
    - google-auth ライブラリを使用した ID トークン検証
    - ユーザー情報の取得
    - _Requirements: 1.1_
  
  - [ ] 5.2 Sui ブロックチェーンクライアントの実装
    - pysui を使用したウォレット生成
    - NFT 発行トランザクションの作成と送信
    - スポンサードトランザクションの実装
    - _Requirements: 1.3, 3.2, 3.3_
  
  - [ ] 5.3 Stripe クライアントの実装
    - Payment Intent の作成
    - Webhook 署名検証
    - _Requirements: 5.5_

- [ ] 6. Service レイヤーの実装
  - [ ] 6.1 AuthService の実装
    - Google OAuth 認証フロー
    - JWT トークンの生成と検証
    - リフレッシュトークンの処理
    - _Requirements: 1.1, 1.4, 1.5, 6.1_
  
  - [ ] 6.2 WalletService の実装
    - Sui ウォレットの生成
    - 秘密鍵の暗号化と保存
    - ウォレット残高の取得
    - _Requirements: 1.3_
  
  - [ ] 6.3 NFTService の実装
    - NFT 発行タスクのキューイング
    - NFT 保有確認
    - ユーザーの NFT 一覧取得
    - _Requirements: 3.1, 3.2, 3.4, 3.5_
  
  - [ ] 6.4 ProductService の実装
    - 商品の CRUD 操作
    - 在庫管理
    - NFT 要件の検証
    - _Requirements: 4.2, 4.3, 4.4, 4.5_
  
  - [ ] 6.5 OrderService の実装
    - 注文の作成と検証
    - NFT 保有要件のチェック
    - 在庫の確認と予約
    - 注文ステータスの更新
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.6, 5.7_
  
  - [ ] 6.6 PaymentService の実装
    - Stripe Payment Intent の作成
    - Webhook イベントの処理
    - 決済成功時の注文完了処理
    - 決済失敗時の在庫復元
    - _Requirements: 5.5, 5.6, 5.7_

- [ ] 7. API Blueprint とルートの実装
  - [ ] 7.1 認証ミドルウェアの実装
    - JWT トークン検証ミドルウェア
    - レート制限ミドルウェア
    - _Requirements: 6.1, 6.7_
  
  - [ ] 7.2 auth_blueprint の実装
    - POST /api/v1/auth/google - Google OAuth 認証
    - POST /api/v1/auth/refresh - トークンリフレッシュ
    - GET /api/v1/auth/me - 現在のユーザー情報
    - _Requirements: 1.1, 1.4, 1.5, 8.2, 8.6, 8.7_
  
  - [ ] 7.3 nft_blueprint の実装
    - GET /api/v1/nfts - ユーザーの NFT 一覧
    - POST /api/v1/nfts/mint - NFT 発行リクエスト
    - GET /api/v1/nfts/{id} - NFT 詳細
    - GET /api/v1/nfts/status/{task_id} - 発行状態確認
    - _Requirements: 3.1, 3.4, 8.2, 8.6, 8.7_
  
  - [ ] 7.4 product_blueprint の実装
    - GET /api/v1/products - 商品一覧
    - GET /api/v1/products/{id} - 商品詳細
    - POST /api/v1/products - 商品作成（管理者）
    - PUT /api/v1/products/{id} - 商品更新（管理者）
    - DELETE /api/v1/products/{id} - 商品削除（管理者）
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 8.2, 8.6, 8.7_
  
  - [ ] 7.5 order_blueprint の実装
    - POST /api/v1/orders - 注文作成
    - GET /api/v1/orders - 注文履歴
    - GET /api/v1/orders/{id} - 注文詳細
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 8.2, 8.6, 8.7_
  
  - [ ] 7.6 payment_blueprint の実装
    - POST /api/v1/payments/intent - Payment Intent 作成
    - POST /api/v1/payments/webhook - Stripe Webhook
    - GET /api/v1/payments/{id} - 決済情報
    - _Requirements: 5.5, 5.6, 8.2, 8.6, 8.7_
  
  - [ ] 7.7 wifi_blueprint の実装
    - POST /api/v1/wifi/connect - WiFi セッション作成
    - GET /api/v1/wifi/sessions - セッション履歴
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 8.2, 8.6, 8.7_

- [ ] 8. エラーハンドリングとロギングの実装
  - カスタム例外クラスの作成
  - グローバルエラーハンドラーの実装
  - 構造化ロギングの設定
  - _Requirements: 6.4, 6.5, 6.6, 8.7_

- [ ] 9. セキュリティ機能の実装
  - [ ] 9.1 入力バリデーションとサニタイゼーション
    - XSS 対策の実装
    - SQL インジェクション対策（パラメータ化クエリ）
    - _Requirements: 6.4, 6.5_
  
  - [ ] 9.2 CSRF 保護の実装
    - CSRF トークンの生成と検証
    - _Requirements: 6.6_
  
  - [ ] 9.3 パスワードハッシュ化（将来の拡張用）
    - bcrypt を使用したハッシュ化
    - _Requirements: 6.2_

- [ ] 10. バックエンドテストの実装
  - [ ] 10.1 ユニットテストの作成
    - Service レイヤーのテスト
    - Repository レイヤーのテスト
    - _Requirements: 12.1, 12.3, 12.4_
  
  - [ ] 10.2 API 統合テストの作成
    - 各エンドポイントのテスト
    - 認証フローのテスト
    - _Requirements: 12.1, 12.3_

## Frontend Implementation

- [ ] 11. Next.js プロジェクトのセットアップ
  - Next.js 14 App Router プロジェクトの初期化
  - TypeScript、Tailwind CSS、ESLint、Prettier の設定
  - 環境変数の設定（.env.local.example）
  - _Requirements: 7.1, 7.2, 12.5_

- [ ] 12. 状態管理とユーティリティの実装
  - [ ] 12.1 Zustand ストアの作成
    - authStore（ユーザー認証状態）
    - cartStore（ショッピングカート）
    - nftStore（NFT 一覧）
    - _Requirements: 7.3_
  
  - [ ] 12.2 API クライアントの実装
    - fetch ラッパー関数
    - エラーハンドリング
    - JWT トークン管理
    - _Requirements: 7.3, 8.6, 8.7_
  
  - [ ] 12.3 型定義の作成
    - User, NFT, Product, Order などの TypeScript 型
    - API レスポンス型
    - _Requirements: 7.3_

- [ ] 13. 認証コンポーネントの実装
  - [ ] 13.1 LoginButton コンポーネント
    - Google OAuth フローの実装
    - JWT トークンの保存
    - _Requirements: 1.1, 7.1_
  
  - [ ] 13.2 AuthProvider コンポーネント
    - 認証状態の管理
    - トークンリフレッシュ
    - _Requirements: 1.4, 1.5_
  
  - [ ] 13.3 ProtectedRoute コンポーネント
    - 認証が必要なページの保護
    - リダイレクト処理
    - _Requirements: 6.1_

- [ ] 14. キャプティブポータルページの実装
  - [ ] 14.1 CaptivePortalPage の作成
    - WiFi 接続時の認証ページ
    - Google ログインボタン
    - 利用規約同意 UI
    - _Requirements: 2.1, 2.5_
  
  - [ ] 14.2 WelcomeScreen の作成
    - 認証成功後の画面
    - NFT 配布状況の表示
    - EC ショップへの誘導
    - _Requirements: 3.1_

- [ ] 15. NFT 関連コンポーネントの実装
  - [ ] 15.1 WalletDisplay コンポーネント
    - ウォレットアドレスの表示
    - 保有 NFT 数の表示
    - _Requirements: 1.3_
  
  - [ ] 15.2 NFTCard コンポーネント
    - NFT の詳細情報表示
    - 画像とメタデータの表示
    - _Requirements: 3.4_
  
  - [ ] 15.3 NFTGallery コンポーネント
    - NFT コレクションのグリッド表示
    - フィルタリングとソート
    - _Requirements: 3.4_

- [ ] 16. EC ショップコンポーネントの実装
  - [ ] 16.1 ProductList コンポーネント
    - 商品一覧の表示
    - NFT 保有状態による表示制御
    - _Requirements: 4.1, 4.2, 5.2_
  
  - [ ] 16.2 ProductCard コンポーネント
    - 商品詳細情報の表示
    - カートへの追加ボタン
    - _Requirements: 4.1, 4.2_
  
  - [ ] 16.3 ShoppingCart コンポーネント
    - カート内商品の表示
    - 数量変更と削除
    - 合計金額の計算
    - _Requirements: 5.1_
  
  - [ ] 16.4 CheckoutForm コンポーネント
    - Stripe Elements の統合
    - NFT 保有確認 UI
    - 注文確定処理
    - _Requirements: 5.2, 5.5, 5.6_

- [ ] 17. ページとルーティングの実装
  - [ ] 17.1 ホームページ（app/page.tsx）
    - ランディングページ
    - サービス説明
    - _Requirements: 7.1_
  
  - [ ] 17.2 ダッシュボードページ（app/dashboard/page.tsx）
    - ユーザー情報の表示
    - NFT ギャラリー
    - 注文履歴
    - _Requirements: 7.1_
  
  - [ ] 17.3 ショップページ（app/shop/page.tsx）
    - 商品一覧
    - カート機能
    - _Requirements: 7.1_
  
  - [ ] 17.4 チェックアウトページ（app/checkout/page.tsx）
    - 注文確認
    - 決済フォーム
    - _Requirements: 7.1, 7.6_

- [ ] 18. UI/UX の最適化
  - [ ] 18.1 レスポンシブデザインの実装
    - モバイル、タブレット、デスクトップ対応
    - _Requirements: 7.2_
  
  - [ ] 18.2 ローディング状態の実装
    - スケルトンスクリーン
    - ローディングスピナー
    - _Requirements: 7.4_
  
  - [ ] 18.3 エラー表示の実装
    - トースト通知
    - エラーバウンダリ
    - _Requirements: 7.1_

- [ ] 19. フロントエンドテストの実装
  - [ ] 19.1 コンポーネントテストの作成
    - Jest + React Testing Library
    - 主要コンポーネントのテスト
    - _Requirements: 12.2_
  
  - [ ] 19.2 統合テストの作成
    - ユーザーフローのテスト
    - _Requirements: 12.2_

## Infrastructure and Deployment

- [ ] 20. Apache 設定とデプロイメント準備
  - [ ] 20.1 Apache 設定ファイルの作成
    - mod_wsgi 設定
    - mod_proxy 設定（Next.js 用）
    - SSL/TLS 設定
    - _Requirements: 11.3, 11.4, 11.5, 6.3, 6.8_
  
  - [ ] 20.2 Let's Encrypt SSL 証明書の設定
    - certbot の設定
    - 自動更新の設定
    - _Requirements: 11.6_
  
  - [ ] 20.3 systemd サービスファイルの作成
    - Flask アプリケーション用
    - Next.js アプリケーション用
    - バックグラウンドタスクワーカー用
    - _Requirements: 11.1_

- [ ] 21. 環境変数とシークレット管理
  - 本番環境用の環境変数設定
  - シークレットの安全な管理
  - _Requirements: 6.2, 6.3_

- [ ] 22. データベースセットアップ
  - MySQL データベースの作成
  - マイグレーションの実行
  - 初期データの投入
  - _Requirements: 9.1_

- [ ] 23. モニタリングとロギング
  - アプリケーションログの設定
  - エラートラッキング
  - パフォーマンスモニタリング
  - _Requirements: 12.6, 12.7_

## Blockchain Integration

- [ ] 24. Sui Move スマートコントラクトの実装
  - [ ] 24.1 NFT モジュールの作成
    - NFT 構造体の定義
    - mint 関数の実装
    - transfer 関数の実装
    - _Requirements: 3.2, 3.3_
  
  - [ ] 24.2 スポンサードトランザクションの実装
    - ガス代スポンサー機能
    - _Requirements: 3.3_
  
  - [ ] 24.3 スマートコントラクトのデプロイ
    - Testnet へのデプロイ
    - Mainnet へのデプロイ
    - _Requirements: 3.2_

- [ ] 25. ブロックチェーン統合テスト
  - NFT 発行フローのエンドツーエンドテスト
  - トランザクション確認
  - _Requirements: 3.2, 3.3, 3.4_

## Final Integration and Testing

- [ ] 26. エンドツーエンド統合
  - [ ] 26.1 WiFi → 認証 → NFT 発行フローの統合
    - OpenNDS との統合
    - 完全なフローのテスト
    - _Requirements: 2.1, 2.2, 2.5, 3.1_
  
  - [ ] 26.2 NFT → 商品購入 → 決済フローの統合
    - NFT 保有確認から決済完了までのテスト
    - _Requirements: 5.2, 5.5, 5.6, 5.7_

- [ ] 27. パフォーマンス最適化
  - データベースクエリの最適化
  - フロントエンドバンドルサイズの最適化
  - 画像最適化
  - _Requirements: 7.4_

- [ ] 28. セキュリティ監査
  - セキュリティベストプラクティスの確認
  - 脆弱性スキャン
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

- [ ] 29. ドキュメント作成
  - API ドキュメント
  - デプロイメントガイド
  - 運用マニュアル
  - _Requirements: 8.2_
