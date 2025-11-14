# Implementation Plan

## Backend Implementation

- [x] 1. プロジェクト構造とコア設定のセットアップ




  - Flask アプリケーションの基本構造を作成（backend/app.py, backend/config.py, backend/requirements.txt）
  - 環境変数管理の設定（.env.example）
  - MySQL データベース接続設定（SQLAlchemy）
  - CORS、JWT、セキュリティミドルウェアの設定
  - _Requirements: 6.1, 6.3, 8.1, 8.2, 9.1, 9.2_

- [x] 2. データベースモデルの実装









  - [x] 2.1 Base モデルとユーティリティの作成


    - SQLAlchemy Base クラスを作成（backend/models/base.py）

    - to_dict() メソッド、UUID 生成ユーティリティを実装

    - _Requirements: 9.1, 9.2, 9.4_
  
  - [x] 2.2 User および Wallet モデルの実装


    - User モデルを作成（backend/models/user.py）
    - Wallet モデルを作成（backend/models/wallet.py）
    - リレーションシップの定義
    - _Requirements: 1.2, 1.3, 9.5, 9.6, 9.7_
  
  - [x] 2.3 NFT、Product、Order モデルの実装


    - NFTMint モデルを作成（backend/models/nft_mint.py）


    - Product モデルを作成（backend/models/product.py）
    - Order および OrderItem モデルを作成（backend/models/order.py）
    - 外部キー制約とインデックスの設定
    - _Requirements: 3.4, 4.1, 5.3, 5.4, 9.7_





  






  - [-] 2.4 Payment、WiFiSession、TaskQueue モデルの実装












    - Payment モデルを作成（backend/models/payment.py）
    - WiFiSession モデルを作成（backend/models/wifi_session.py）
    - TaskQueue モデルを作成（backend/models/task_queue.py）
    - _Requirements: 2.2, 2.3, 5.5, 10.4_



- [ ] 3. Repository レイヤーの実装
  - [ ] 3.1 BaseRepository の作成
    - 共通 CRUD 操作を持つ基底クラスを実装（backend/repositories/base.py）
    - パラメータ化クエリの使用





    - _Requirements: 6.4, 8.4, 9.2_
  
  - [-] 3.2 User と Wallet の Repository 実装





    - UserRepository を作成（backend/repositories/user_repository.py）
    - WalletRepository を作成（backend/repositories/wallet_repository.py）
    - find_by_google_id, find_by_email などのカスタムクエリ
    - _Requirements: 1.2, 1.3_


  
  - [ ] 3.3 NFT と Product の Repository 実装

    - NFTRepository を作成（backend/repositories/nft_repository.py）
    - ProductRepository を作成（backend/repositories/product_repository.py）
    - find_by_wallet, find_by_status などのフィルタリング
    - _Requirements: 3.4, 4.2, 4.3_
  
  - [ ] 3.4 Order、Payment、Task の Repository 実装

    - OrderRepository を作成（backend/repositories/order_repository.py）




    - PaymentRepository を作成（backend/repositories/payment_repository.py）
    - TaskRepository を作成（backend/repositories/task_repository.py）
    - ステータス更新メソッド
    - _Requirements: 5.3, 5.4, 5.5, 5.6, 10.4_




- [ ] 4. 外部 API クライアントの実装


  - [x] 4.1 Google OAuth クライアントの実装



    - GoogleAuthClient を作成（backend/clients/google_auth.py）
    - google-auth ライブラリを使用した ID トークン検証
    - ユーザー情報の取得
    - _Requirements: 1.1_
  
  - [ ] 4.2 Sui ブロックチェーンクライアントの実装

    - SuiClient を作成（backend/clients/sui_client.py）
    - pysui を使用したウォレット生成
    - NFT 発行トランザクションの作成と送信
    - スポンサードトランザクションの実装
    - _Requirements: 1.3, 3.2, 3.3_
  
  - [ ] 4.3 Stripe クライアントの実装

    - StripeClient を作成（backend/clients/stripe_client.py）
    - Payment Intent の作成
    - Webhook 署名検証
    - _Requirements: 5.5_

- [ ] 5. バックグラウンドタスクマネージャーの実装



  - [x] 5.1 TaskManager クラスの実装


    - TaskManager を作成（backend/tasks/task_manager.py）
    - ThreadPoolExecutor を使用した非同期タスク実行
    - タスクステータス管理（pending, running, completed, failed）
    - _Requirements: 10.1, 10.2, 10.3, 10.4_
  
  - [x] 5.2 NFT 発行タスクの実装


    - NFT 発行タスク関数を作成（backend/tasks/nft_tasks.py）
    - 指数バックオフを使用したリトライメカニズム



    - 最大リトライ回数の設定
    - _Requirements: 3.1, 3.2, 3.5, 10.5_

- [ ] 6. Service レイヤーの実装
  - [ ] 6.1 AuthService の実装

    - AuthService を作成（backend/services/auth_service.py）
    - Google OAuth 認証フロー
    - JWT トークンの生成と検証
    - リフレッシュトークンの処理
    - _Requirements: 1.1, 1.4, 1.5, 6.1_

  
  - [ ] 6.2 WalletService の実装
    - WalletService を作成（backend/services/wallet_service.py）
    - Sui ウォレットの生成
    - 秘密鍵の暗号化と保存
    - _Requirements: 1.3, 6.2_

  

  - [ ] 6.3 NFTService の実装
    - NFTService を作成（backend/services/nft_service.py）
    - NFT 発行タスクのキューイング
    - NFT 保有確認
    - ユーザーの NFT 一覧取得
    - _Requirements: 3.1, 3.2, 3.4, 3.5_
  
  - [ ] 6.4 ProductService の実装
    - ProductService を作成（backend/services/product_service.py）
    - 商品の CRUD 操作
    - 在庫管理
    - NFT 要件の検証



    - _Requirements: 4.2, 4.3, 4.4, 4.5_
  
  - [ ] 6.5 OrderService の実装
    - OrderService を作成（backend/services/order_service.py）
    - 注文の作成と検証
    - NFT 保有要件のチェック
    - 在庫の確認と予約
    - 注文ステータスの更新
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.6, 5.7_
  
  - [ ] 6.6 PaymentService の実装
    - PaymentService を作成（backend/services/payment_service.py）
    - Stripe Payment Intent の作成
    - Webhook イベントの処理
    - 決済成功時の注文完了処理
    - 決済失敗時の在庫復元
    - _Requirements: 5.5, 5.6, 5.7_

- [ ] 7. エラーハンドリングとセキュリティの実装


  - [ ] 7.1 カスタム例外とエラーハンドラーの実装
    - カスタム例外クラスを作成（backend/exceptions.py）
    - グローバルエラーハンドラーを実装
    - 構造化ロギングの設定
    - _Requirements: 6.4, 6.5, 6.6, 8.7_
  
  - [ ] 7.2 セキュリティミドルウェアの実装

    - 入力バリデーションとサニタイゼーション
    - CSRF 保護の実装
    - XSS 対策の実装
    - _Requirements: 6.4, 6.5, 6.6_

- [ ] 8. API Blueprint とルートの実装


  - [ ] 8.1 認証ミドルウェアの実装
    - JWT トークン検証ミドルウェアを作成（backend/middleware/auth.py）
    - レート制限ミドルウェアを作成（backend/middleware/rate_limit.py）
    - _Requirements: 6.1, 6.7_
  
  - [ ] 8.2 auth_blueprint の実装

    - auth_blueprint を作成（backend/routes/auth.py）
    - POST /api/v1/auth/google - Google OAuth 認証
    - POST /api/v1/auth/refresh - トークンリフレッシュ
    - GET /api/v1/auth/me - 現在のユーザー情報
    - _Requirements: 1.1, 1.4, 1.5, 8.2, 8.6, 8.7_
  
  - [ ] 8.3 nft_blueprint の実装

    - nft_blueprint を作成（backend/routes/nft.py）
    - GET /api/v1/nfts - ユーザーの NFT 一覧
    - POST /api/v1/nfts/mint - NFT 発行リクエスト
    - GET /api/v1/nfts/{id} - NFT 詳細
    - GET /api/v1/nfts/status/{task_id} - 発行状態確認
    - _Requirements: 3.1, 3.4, 8.2, 8.6, 8.7_
  
  - [ ] 8.4 product_blueprint の実装

    - product_blueprint を作成（backend/routes/product.py）
    - GET /api/v1/products - 商品一覧
    - GET /api/v1/products/{id} - 商品詳細
    - POST /api/v1/products - 商品作成（管理者）
    - PUT /api/v1/products/{id} - 商品更新（管理者）
    - DELETE /api/v1/products/{id} - 商品削除（管理者）
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 8.2, 8.6, 8.7_
  
  - [ ] 8.5 order と payment の blueprint 実装

    - order_blueprint を作成（backend/routes/order.py）
    - payment_blueprint を作成（backend/routes/payment.py）
    - wifi_blueprint を作成（backend/routes/wifi.py）
    - 各エンドポイントの実装
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 8.2, 8.6, 8.7_

- [ ] 9. バックエンド統合とテスト
  - [ ] 9.1 Flask アプリケーションの統合
    - すべての Blueprint を app.py に登録
    - データベース初期化スクリプトの作成
    - 環境変数の設定確認
    - _Requirements: 8.1, 8.2, 9.1_
  
  - [ ]* 9.2 バックエンドテストの作成
    - pytest 設定ファイルの作成
    - Service レイヤーのユニットテスト
    - API エンドポイントの統合テスト
    - _Requirements: 12.1, 12.3, 12.4_

## Frontend Implementation

- [ ] 10. Next.js プロジェクトのセットアップ
  - Next.js 14 App Router プロジェクトの初期化（frontend/）
  - TypeScript、Tailwind CSS、ESLint、Prettier の設定
  - 環境変数の設定（.env.local.example）
  - プロジェクト構造の作成（app/, components/, lib/, types/）
  - _Requirements: 7.1, 7.2, 12.5_

- [ ] 11. 型定義と API クライアントの実装
  - [ ] 11.1 TypeScript 型定義の作成
    - User, NFT, Product, Order などの型を定義（frontend/types/）
    - API レスポンス型の定義
    - _Requirements: 7.3_
  
  - [ ] 11.2 API クライアントの実装
    - API クライアントを作成（frontend/lib/api-client.ts）
    - fetch ラッパー関数
    - エラーハンドリング
    - JWT トークン管理
    - _Requirements: 7.3, 8.6, 8.7_

- [ ] 12. 状態管理の実装
  - [ ] 12.1 Zustand ストアの作成
    - authStore を作成（frontend/stores/auth-store.ts）
    - cartStore を作成（frontend/stores/cart-store.ts）
    - nftStore を作成（frontend/stores/nft-store.ts）
    - _Requirements: 7.3_

- [ ] 13. 認証コンポーネントの実装
  - [ ] 13.1 認証関連コンポーネントの作成
    - LoginButton コンポーネント（frontend/components/auth/LoginButton.tsx）
    - AuthProvider コンポーネント（frontend/components/auth/AuthProvider.tsx）
    - ProtectedRoute コンポーネント（frontend/components/auth/ProtectedRoute.tsx）
    - Google OAuth フローの実装
    - JWT トークンの保存とリフレッシュ
    - _Requirements: 1.1, 1.4, 1.5, 6.1, 7.1_

- [ ] 14. キャプティブポータルページの実装
  - [ ] 14.1 キャプティブポータル UI の作成
    - CaptivePortalPage を作成（frontend/app/captive/page.tsx）
    - WelcomeScreen コンポーネント（frontend/components/captive/WelcomeScreen.tsx）
    - WiFi 接続時の認証ページ
    - 利用規約同意 UI
    - NFT 配布状況の表示
    - _Requirements: 2.1, 2.5, 3.1_

- [ ] 15. NFT 関連コンポーネントの実装
  - [ ] 15.1 NFT 表示コンポーネントの作成
    - WalletDisplay コンポーネント（frontend/components/nft/WalletDisplay.tsx）
    - NFTCard コンポーネント（frontend/components/nft/NFTCard.tsx）
    - NFTGallery コンポーネント（frontend/components/nft/NFTGallery.tsx）
    - ウォレットアドレスと NFT の表示
    - _Requirements: 1.3, 3.4_

- [ ] 16. EC ショップコンポーネントの実装
  - [ ] 16.1 商品表示コンポーネントの作成
    - ProductList コンポーネント（frontend/components/shop/ProductList.tsx）
    - ProductCard コンポーネント（frontend/components/shop/ProductCard.tsx）
    - 商品一覧の表示
    - NFT 保有状態による表示制御
    - _Requirements: 4.1, 4.2, 5.2_
  
  - [ ] 16.2 カートとチェックアウトの実装
    - ShoppingCart コンポーネント（frontend/components/shop/ShoppingCart.tsx）
    - CheckoutForm コンポーネント（frontend/components/shop/CheckoutForm.tsx）
    - Stripe Elements の統合
    - カート機能と決済処理
    - _Requirements: 5.1, 5.2, 5.5, 5.6_

- [ ] 17. ページとルーティングの実装
  - [ ] 17.1 主要ページの作成
    - ホームページ（frontend/app/page.tsx）
    - ダッシュボードページ（frontend/app/dashboard/page.tsx）
    - ショップページ（frontend/app/shop/page.tsx）
    - チェックアウトページ（frontend/app/checkout/page.tsx）
    - _Requirements: 7.1, 7.6_
  
  - [ ] 17.2 UI/UX の最適化
    - レスポンシブデザインの実装
    - ローディング状態の実装（スケルトンスクリーン、スピナー）
    - エラー表示の実装（トースト通知、エラーバウンダリ）
    - _Requirements: 7.1, 7.2, 7.4_

- [ ]* 18. フロントエンドテストの実装
  - Jest + React Testing Library の設定
  - 主要コンポーネントのテスト
  - ユーザーフローの統合テスト
  - _Requirements: 12.2_

## Blockchain Integration

- [ ] 19. Sui Move スマートコントラクトの実装
  - [ ] 19.1 NFT モジュールの作成
    - NFT 構造体の定義（contracts/sources/nft.move）
    - mint 関数の実装
    - transfer 関数の実装
    - _Requirements: 3.2, 3.3_
  
  - [ ] 19.2 スポンサードトランザクションの実装
    - ガス代スポンサー機能の実装
    - _Requirements: 3.3_
  
  - [ ] 19.3 スマートコントラクトのデプロイ
    - Testnet へのデプロイ
    - デプロイスクリプトの作成
    - _Requirements: 3.2_

## Infrastructure and Deployment

- [ ] 20. デプロイメント設定
  - [ ] 20.1 環境変数とシークレット管理
    - 本番環境用の環境変数設定
    - シークレットの安全な管理
    - _Requirements: 6.2, 6.3_
  
  - [ ] 20.2 データベースセットアップ
    - MySQL データベースの作成
    - マイグレーションスクリプトの実行
    - 初期データの投入
    - _Requirements: 9.1_
  
  - [ ] 20.3 Apache 設定
    - Apache 設定ファイルの作成
    - mod_wsgi 設定（Flask 用）
    - mod_proxy 設定（Next.js 用）
    - SSL/TLS 設定（Let's Encrypt）
    - systemd サービスファイルの作成
    - _Requirements: 11.1, 11.3, 11.4, 11.5, 11.6, 6.3, 6.8_

- [ ]* 21. モニタリングとロギング
  - アプリケーションログの設定
  - エラートラッキング
  - パフォーマンスモニタリング
  - _Requirements: 12.6, 12.7_

## Final Integration

- [ ] 22. エンドツーエンド統合とテスト
  - [ ] 22.1 WiFi → 認証 → NFT 発行フローの統合
    - OpenNDS との統合設定
    - 完全なフローのテスト
    - _Requirements: 2.1, 2.2, 2.5, 3.1_
  
  - [ ] 22.2 NFT → 商品購入 → 決済フローの統合
    - NFT 保有確認から決済完了までのテスト
    - _Requirements: 5.2, 5.5, 5.6, 5.7_
  
  - [ ]* 22.3 パフォーマンス最適化
    - データベースクエリの最適化
    - フロントエンドバンドルサイズの最適化
    - 画像最適化
    - _Requirements: 7.4_
  
  - [ ]* 22.4 セキュリティ監査
    - セキュリティベストプラクティスの確認
    - 脆弱性スキャン
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

- [ ]* 23. ドキュメント作成
  - API ドキュメント
  - デプロイメントガイド
  - 運用マニュアル
  - _Requirements: 8.2_
  - 運用マニュアル
  - _Requirements: 8.2_
