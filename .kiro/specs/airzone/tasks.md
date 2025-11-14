# Implementation Plan

## Progress Summary

### Backend (Flask)
- ✅ Core Infrastructure: Models, Repositories, Services, Clients, Task Manager
- ✅ Middleware: JWT Authentication, Security, Error Handling
- ✅ All Blueprints: Auth (8.2), NFT (8.3), Product (8.4), Order (8.5), Payment (8.6), WiFi (8.7)
- ✅ Error Handlers and Logging

### Frontend (Next.js)
- ✅ Core Setup: Project structure, API client, State management (Zustand)
- ✅ UI Components: Layout, Button, Card, Loading, Toast
- ✅ Authentication: LoginButton, AuthProvider, Login page
- ✅ Pages: Dashboard, Login, Captive Portal, NFT Gallery, Shop, Checkout, Orders
- ✅ NFT Components: NFTCard, NFTGallery
- ✅ Shop Components: ProductCard, ProductList, ShoppingCart, CheckoutForm

### Blockchain
- ⏳ Sui Move smart contracts not yet implemented

### Infrastructure
- ⏳ Database setup, Apache configuration, systemd services pending

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





  






  - [x] 2.4 Payment、WiFiSession、TaskQueue モデルの実装

















    - Payment モデルを作成（backend/models/payment.py）
    - WiFiSession モデルを作成（backend/models/wifi_session.py）
    - TaskQueue モデルを作成（backend/models/task_queue.py）
    - _Requirements: 2.2, 2.3, 5.5, 10.4_



- [x] 3. Repository レイヤーの実装



-

  - [x] 3.1 BaseRepository の作成





    - 共通 CRUD 操作を持つ基底クラスを実装（backend/repositories/base.py）
    - パラメータ化クエリの使用





    - _Requirements: 6.4, 8.4, 9.2_
  
  - [x] 3.2 User と Wallet の Repository 実装






    - UserRepository を作成（backend/repositories/user_repository.py）




    - WalletRepository を作成（backend/repositories/wallet_repository.py）
    - find_by_google_id, find_by_email などのカスタムクエリ
    - _Requirements: 1.2, 1.3_


  
  - [x] 3.3 NFT と Product の Repository 実装















    - NFTRepository を作成（backend/repositories/nft_repository.py）
    - ProductRepository を作成（backend/repositories/product_repository.py）







    - find_by_wallet, find_by_status などのフィルタリング





    - _Requirements: 3.4, 4.2, 4.3_
  



-

  - [x] 3.4 Order、Payment、Task の Repository 実装













    - OrderRepository を作成（backend/repositories/order_repository.py）




    - PaymentRepository を作成（backend/repositories/payment_repository.py）


    - TaskRepository を作成（backend/repositories/task_repository.py）
    - ステータス更新メソッド
    - _Requirements: 5.3, 5.4, 5.5, 5.6, 10.4_




- [x] 4. 外部 API クライアントの実装






  - [x] 4.1 Google OAuth クライアントの実装



    - GoogleAuthClient を作成（backend/clients/google_auth.py）
    - google-auth ライブラリを使用した ID トークン検証
    - ユーザー情報の取得
    - _Requirements: 1.1_
  
  - [x] 4.2 Sui ブロックチェーンクライアントの実装








    - SuiClient を作成（backend/clients/sui_client.py）
    - pysui を使用したウォレット生成
    - NFT 発行トランザクションの作成と送信
    - スポンサードトランザクションの実装
    - _Requirements: 1.3, 3.2, 3.3_
  
  - [x] 4.3 Stripe クライアントの実装








    - StripeClient を作成（backend/clients/stripe_client.py）
    - Payment Intent の作成
    - Webhook 署名検証
    - _Requirements: 5.5_



- [x] 5. バックグラウンドタスクマネージャーの実装





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

- [x] 6. Service レイヤーの実装




  - [x] 6.1 AuthService の実装







    - AuthService を作成（backend/services/auth_service.py）
    - Google OAuth 認証フロー
    - JWT トークンの生成と検証
    - リフレッシュトークンの処理
    - _Requirements: 1.1, 1.4, 1.5, 6.1_

  
  - [x] 6.2 WalletService の実装







    - WalletService を作成（backend/services/wallet_service.py）
    - Sui ウォレットの生成
    - 秘密鍵の暗号化と保存
    - _Requirements: 1.3, 6.2_

  
-

  - [x] 6.3 NFTService の実装






    - NFTService を作成（backend/services/nft_service.py）
    - NFT 発行タスクのキューイング
    - NFT 保有確認
    - ユーザーの NFT 一覧取得
    - _Requirements: 3.1, 3.2, 3.4, 3.5_
  
  - [x] 6.4 ProductService の実装


    - ProductService を作成（backend/services/product_service.py）
    - 商品の CRUD 操作
    - 在庫管理
    - NFT 要件の検証



    - _Requirements: 4.2, 4.3, 4.4, 4.5_
  
  - [x] 6.5 OrderService の実装


    - OrderService を作成（backend/services/order_service.py）
    - 注文の作成と検証
    - NFT 保有要件のチェック
    - 在庫の確認と予約
    - 注文ステータスの更新
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.6, 5.7_
  
  - [x] 6.6 PaymentService の実装


    - PaymentService を作成（backend/services/payment_service.py）
    - Stripe Payment Intent の作成
    - Webhook イベントの処理
    - 決済成功時の注文完了処理
    - 決済失敗時の在庫復元
    - _Requirements: 5.5, 5.6, 5.7_

- [x] 7. エラーハンドリングとセキュリティの実装







  - [x] 7.1 カスタム例外とエラーハンドラーの実装


    - カスタム例外クラスを作成（backend/exceptions.py）
    - グローバルエラーハンドラーを実装
    - 構造化ロギングの設定
    - _Requirements: 6.4, 6.5, 6.6, 8.7_
  
  - [x] 7.2 セキュリティミドルウェアの実装



    - 入力バリデーションとサニタイゼーション
    - CSRF 保護の実装
    - XSS 対策の実装
    - _Requirements: 6.4, 6.5, 6.6_

- [x] 8. API Blueprint とルートの実装




  - [x] 8.1 JWT 認証ミドルウェアの実装
    - JWT トークン検証ミドルウェアを作成（backend/middleware/auth.py）
    - jwt_required デコレータの実装
    - get_current_user ヘルパー関数の実装
    - _Requirements: 6.1, 6.7_
  -

  - [x] 8.2 auth_blueprint の実装
    - auth_blueprint を作成（backend/routes/auth.py）
    - POST /api/v1/auth/google - Google OAuth 認証
    - POST /api/v1/auth/refresh - トークンリフレッシュ
    - GET /api/v1/auth/me - 現在のユーザー情報
    - app.py に Blueprint を登録
    - _Requirements: 1.1, 1.4, 1.5, 8.2, 8.6, 8.7_

  - [x] 8.3 nft_blueprint の実装
    - nft_blueprint を作成（backend/routes/nft.py）
    - GET /api/v1/nfts - ユーザーの NFT 一覧
    - POST /api/v1/nfts/mint - NFT 発行リクエスト
    - GET /api/v1/nfts/{id} - NFT 詳細
    - GET /api/v1/nfts/status/{task_id} - 発行状態確認
    - app.py に Blueprint を登録
    - _Requirements: 3.1, 3.4, 8.2, 8.6, 8.7_

  - [x] 8.4 product_blueprint の実装
    - product_blueprint を作成（backend/routes/product.py）
    - GET /api/v1/products - 商品一覧
    - GET /api/v1/products/{id} - 商品詳細
    - POST /api/v1/products - 商品作成（管理者）
    - PUT /api/v1/products/{id} - 商品更新（管理者）
    - DELETE /api/v1/products/{id} - 商品削除（管理者）
    - app.py に Blueprint を登録
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 8.2, 8.6, 8.7_
  
  - [x] 8.5 order_blueprint の実装





    - order_blueprint を作成（backend/routes/order.py）
    - POST /api/v1/orders - 注文作成
    - GET /api/v1/orders - ユーザーの注文履歴取得
    - GET /api/v1/orders/{id} - 注文詳細取得
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 8.2, 8.6, 8.7_
  
  - [x] 8.6 payment_blueprint の実装





    - payment_blueprint を作成（backend/routes/payment.py）
    - POST /api/v1/payments/intent - Stripe Payment Intent 作成
    - POST /api/v1/payments/webhook - Stripe Webhook ハンドラー
    - GET /api/v1/payments/{id} - 決済情報取得
    - _Requirements: 5.5, 5.6, 8.2, 8.6, 8.7_
  
  - [x] 8.7 wifi_blueprint の実装




    - WiFiSessionRepository を作成（backend/repositories/wifi_session_repository.py）
    - wifi_blueprint を作成（backend/routes/wifi.py）
    - POST /api/v1/wifi/connect - WiFi 接続セッション作成
    - GET /api/v1/wifi/sessions - WiFi セッション履歴取得
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 8.2, 8.6, 8.7_

- [x] 9. バックエンド統合
  - [x] 9.1 Flask アプリケーションへの Blueprint 登録
    - すべての Blueprint を app.py に登録（auth, nft, product, order, payment, wifi）
    - エンドポイントの動作確認
    - _Requirements: 8.1, 8.2, 9.1_
  
  - [ ]* 9.2 バックエンドテストの作成
    - pytest 設定ファイルの作成
    - Service レイヤーのユニットテスト
    - API エンドポイントの統合テスト
    - _Requirements: 12.1, 12.3, 12.4_

## Frontend Implementation
-

- [x] 10. Next.js プロジェクトのセットアップ



  - [x] 10.1 Next.js プロジェクトの初期化







    - Next.js 14 App Router プロジェクトを作成（frontend/）
    - TypeScript、Tailwind CSS の設定
    - ESLint、Prettier の設定
    - _Requirements: 7.1, 7.2, 12.5_
  
  - [x] 10.2 プロジェクト構造とパッケージのセットアップ







    - 環境変数の設定（.env.local.example）
    - プロジェクト構造の作成（app/, components/, lib/, types/, stores/）
    - 必要なパッケージのインストール（zustand, @mysten/dapp-kit, @stripe/react-stripe-js）
    - _Requirements: 7.1, 7.2, 7.3_

- [x] 11. 型定義と API クライアントの実装





  - [x] 11.1 TypeScript 型定義の作成







    - User, NFT, Product, Order, Payment などの型を定義（frontend/types/index.ts）
    - API レスポンス型の定義
    - _Requirements: 7.3_
  -

  - [x] 11.2 API クライアントの実装






    - API クライアントを作成（frontend/lib/api-client.ts）
    - fetch ラッパー関数とエラーハンドリング
    - JWT トークン管理（localStorage）
    - _Requirements: 7.3, 8.6, 8.7_
  
-

  - [x] 11.3 API サービス関数の実装





    - 認証 API 関数（frontend/lib/api/auth.ts）
    - NFT API 関数（frontend/lib/api/nfts.ts）
    - 商品 API 関数（frontend/lib/api/products.ts）
    - 注文・決済 API 関数（frontend/lib/api/orders.ts, payments.ts）
    - _Requirements: 7.3, 8.2_
-

- [x] 12. 状態管理の実装





  - [x] 12.1 Zustand ストアの作成














    - authStore を作成（frontend/stores/auth-store.ts）
    - cartStore を作成（frontend/stores/cart-store.ts）
    - nftStore を作成（frontend/stores/nft-store.ts）
    - _Requirements: 7.3_
-

- [x] 13. 共通 UI コンポーネントの実装




  - [x] 13.1 レイアウトコンポーネントの作成





    - Header コンポーネント（frontend/components/layout/Header.tsx）
    - Footer コンポーネント（frontend/components/layout/Footer.tsx）
    - Layout コンポーネント（frontend/components/layout/Layout.tsx）
    - _Requirements: 7.1, 7.2_
  
  - [x] 13.2 UI ユーティリティコンポーネントの作成







    - Button コンポーネント（frontend/components/ui/Button.tsx）
    - Card コンポーネント（frontend/components/ui/Card.tsx）
    - Loading コンポーネント（frontend/components/ui/Loading.tsx）
    - Toast 通知コンポーネント（frontend/components/ui/Toast.tsx）
    - _Requirements: 7.1, 7.2, 7.4_
-

- [x] 14. 認証コンポーネントの実装
  - [x] 14.1 認証関連コンポーネントの作成
    - LoginButton コンポーネント（frontend/components/auth/LoginButton.tsx）
    - AuthProvider コンポーネント（frontend/components/auth/AuthProvider.tsx）
    - Google OAuth フローの実装
    - JWT トークンの保存とリフレッシュロジック
    - Login ページの作成（frontend/app/login/page.tsx）
    - _Requirements: 1.1, 1.4, 1.5, 6.1, 7.1_
-

- [x] 15. キャプティブポータルページの実装
  - [x] 15.1 キャプティブポータル UI の作成
    - キャプティブポータルページ（frontend/app/captive/page.tsx）
    - WelcomeScreen コンポーネント（frontend/components/captive/WelcomeScreen.tsx）
    - WiFi 接続時の認証フロー
    - 利用規約同意 UI
    - NFT 配布状況の表示
    - 自動 NFT 発行リクエストとステータスポーリング
    - _Requirements: 2.1, 2.5, 3.1_

- [x] 16. NFT 関連コンポーネントの実装
  - [x] 16.1 NFT 表示コンポーネントの作成
    - NFTCard コンポーネント（frontend/components/nft/NFTCard.tsx）
    - NFTGallery コンポーネント（frontend/components/nft/NFTGallery.tsx）
    - NFT 一覧ページ（frontend/app/nfts/page.tsx）
    - NFT 詳細ページ（frontend/app/nfts/[id]/page.tsx）
    - NFT 発行状態の表示
    - _Requirements: 1.3, 3.4_

- [x] 17. EC ショップコンポーネントの実装
  - [x] 17.1 商品表示コンポーネントの作成
    - ProductCard コンポーネント（frontend/components/shop/ProductCard.tsx）
    - ProductList コンポーネント（frontend/components/shop/ProductList.tsx）
    - ショップページ（frontend/app/shop/page.tsx）
    - 商品詳細ページ（frontend/app/shop/[id]/page.tsx）
    - NFT 保有状態による表示制御
    - _Requirements: 4.1, 4.2, 5.2_
  
  - [x] 17.2 カートとチェックアウトの実装
    - ShoppingCart コンポーネント（frontend/components/shop/ShoppingCart.tsx）
    - CheckoutForm コンポーネント（frontend/components/shop/CheckoutForm.tsx）
    - チェックアウトページ（frontend/app/checkout/page.tsx）
    - カートページ（frontend/app/cart/page.tsx）
    - Stripe Elements の統合
    - 決済処理フロー
    - _Requirements: 5.1, 5.2, 5.5, 5.6_

- [x] 18. ページとルーティングの実装
  - [x] 18.1 主要ページの作成
    - ダッシュボードページ（frontend/app/dashboard/page.tsx）
    - ログインページ（frontend/app/login/page.tsx）
    - キャプティブポータルページ（frontend/app/captive/page.tsx）
    - ホームページの更新（frontend/app/page.tsx）
    - 注文履歴ページ（frontend/app/orders/page.tsx）
    - 注文詳細ページ（frontend/app/orders/[id]/page.tsx）
    - _Requirements: 7.1, 7.6_
  
  - [x] 18.2 レスポンシブデザインとエラーハンドリング
    - レスポンシブデザインの実装（モバイル、タブレット、デスクトップ）
    - エラーバウンダリの実装（frontend/app/error.tsx）
    - 404 ページの実装（frontend/app/not-found.tsx）
    - _Requirements: 7.1, 7.2, 7.4_

- [ ]* 19. フロントエンドテストの実装
  - Jest + React Testing Library の設定
  - 主要コンポーネントのテスト
  - ユーザーフローの統合テスト
  - _Requirements: 12.2_

## Blockchain Integration

- [x] 20. Sui Move スマートコントラクトの実装








  - [x] 20.1 Move プロジェクトのセットアップ





    - contracts/ ディレクトリを作成
    - Move プロジェクトの初期化（sui move new）
    - Move.toml の設定（依存関係、アドレス設定）





    - _Requirements: 3.2_
  
  - [x] 20.2 NFT モジュールの作成





    - NFT 構造体の定義（contracts/sources/airzone_nft.move）
    - mint 関数の実装（NFT 発行ロジック）


    - transfer 関数の実装（NFT 転送ロジック）








    - メタデータ管理機能（名前、説明、画像URL）
    - _Requirements: 3.2, 3.3_
  

  - [ ] 20.3 スポンサードトランザクションの実装



    - ガス代スポンサー機能の実装
    - スポンサーウォレットの設定と管理

    - backend/clients/sui_client.py でのスポンサードトランザクション統合
    - _Requirements: 3.3_
  

  - [ ] 20.4 スマートコントラクトのデプロイ
    - Sui Testnet へのデプロイ
    - デプロイスクリプトの作成（scripts/deploy_contract.sh）
    - コントラクトアドレスを backend/.env に設定
    - デプロイ後の動作確認
    - _Requirements: 3.2_

## Infrastructure and Deployment

- [ ] 21. データベースセットアップ

  - [ ] 21.1 データベース初期化

    - MySQL 8.0 データベースの作成（CREATE DATABASE airzone）
    - データベースユーザーの作成と権限設定
    - Alembic マイグレーションファイルの作成（backend/alembic/versions/）
    - Alembic マイグレーションの実行（alembic upgrade head）
    - 初期データの投入スクリプト作成（scripts/seed_data.py）
    - テスト用商品データの投入
    - _Requirements: 9.1_


- [ ] 22. デプロイメント設定管理
    - 本番環境用の backend/.env ファイル設定
    - 本番環境用の frontend/.env.local ファイル設定
    - シークレットキーの生成（JWT_SECRET_KEY, STRIPE_SECRET_KEY など）
    - ウォレット秘密鍵の暗号化設定
    - _Requirements: 6.2, 6.3_
  
  - [ ] 22.2 Apache Web サーバー設定
    - Apache 設定ファイルの作成（/etc/apache2/sites-available/airzone.conf）
    - mod_wsgi 設定（Flask アプリケーション用）
    - mod_proxy 設定（Next.js アプリケーション用リバースプロキシ）
    - SSL/TLS 設定（Let's Encrypt certbot）
    - HSTS ヘッダーの設定
    - _Requirements: 11.1, 11.3, 11.4, 11.5, 11.6, 6.3, 6.8_
  
  - [ ] 22.3 systemd サービスの設定
    - Flask アプリケーション用 systemd サービスファイル作成（/etc/systemd/system/airzone-backend.service）
    - Next.js アプリケーション用 systemd サービスファイル作成（/etc/systemd/system/airzone-frontend.service）
    - サービスの有効化と自動起動設定（systemctl enable）
    - サービスの起動と動作確認
    - _Requirements: 11.1_
    - _Requirements: 11.1_

- [ ]* 23. モニタリングとロギング
  - アプリケーションログの設定（ログローテーション）
  - エラートラッキングツールの統合（Sentry など）
  - パフォーマンスモニタリングの設定
  - ログ集約とアラート設定
  - _Requirements: 12.6, 12.7_

## Final Integration and Testing

- [ ] 24. OpenNDS キャプティブポータル統合
  - [ ] 24.1 OpenNDS 設定
    - OpenNDS のインストールと設定ファイル作成（/etc/opennds/opennds.conf）
    - キャプティブポータル URL の設定（https://airz.one/captive）
    - 認証成功後のリダイレクト設定
    - WiFi セッション情報の backend への送信設定
    - _Requirements: 2.1, 2.2_
  
  - [ ] 24.2 WiFi → 認証 → NFT 発行フローのテスト
    - OpenNDS との統合テスト
    - WiFi 接続時のキャプティブポータル表示確認
    - Google 認証フローの動作確認
    - NFT 自動発行の動作確認
    - 完全なフローの動作確認
    - _Requirements: 2.1, 2.2, 2.5, 3.1_

- [ ] 25. エンドツーエンド統合テスト
  - [ ] 25.1 主要ユーザーフローのテスト
    - WiFi 接続から NFT 受け取りまでのフロー
    - NFT 保有確認から商品購入までのフロー
    - 決済完了から注文確認までのフロー
    - エラーケースのテスト（決済失敗、在庫切れなど）
    - _Requirements: 2.1, 3.1, 5.2, 5.5, 5.6, 5.7_
  
  - [ ]* 25.2 パフォーマンス最適化
    - データベースクエリの最適化（インデックス追加）
    - フロントエンドバンドルサイズの最適化
    - 画像最適化（Next.js Image コンポーネント）
    - API レスポンスタイムの測定と改善
    - _Requirements: 7.4_
  
  - [ ]* 25.3 セキュリティ監査
    - セキュリティベストプラクティスの確認
    - 脆弱性スキャン（OWASP ZAP など）
    - SQL インジェクション対策の確認
    - XSS 対策の確認
    - CSRF 対策の確認
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

- [ ]* 26. ドキュメント作成
  - API ドキュメント（OpenAPI/Swagger 形式）
  - デプロイメントガイド（README_DEPLOYMENT.md）
  - 運用マニュアル（README_OPERATIONS.md）
  - トラブルシューティングガイド
  - _Requirements: 8.2_
