# Requirements Document

## Introduction

Airzone は、OpenNDS キャプティブポータルを使用した WiFi 接続トリガー型の NFT 配布・EC ショップ統合プラットフォームです。ユーザーが店舗や施設の WiFi に接続すると、Sui ブロックチェーン上の NFT が自動的に配布され、その NFT を使用して EC ショップで商品を購入できるシステムを提供します。

## Glossary

- **Airzone System**: WiFi 接続トリガー型の NFT 配布・EC ショップ統合プラットフォーム全体（ドメイン: https://airz.one/）
- **OpenNDS**: オープンソースのキャプティブポータルソフトウェア
- **Captive Portal**: WiFi 接続時にユーザーを認証ページにリダイレクトする仕組み
- **NFT (Non-Fungible Token)**: Sui ブロックチェーン上で発行される代替不可能なデジタル資産
- **Sui Blockchain**: Move 言語で記述されたスマートコントラクトを実行するブロックチェーンプラットフォーム
- **Wallet**: ユーザーの Sui ブロックチェーンアドレスを管理するデジタルウォレット
- **EC Shop**: NFT を使用して商品を購入できる電子商取引ショップ
- **Sponsor Wallet**: NFT 発行時のガス代を負担するシステム側のウォレット
- **JWT (JSON Web Token)**: ユーザー認証に使用されるトークン
- **Redis**: キャッシュおよびタスクキュー用のインメモリデータストア
- **Celery**: 非同期タスク処理用の分散タスクキュー

## Requirements

### Requirement 1: ユーザー認証とウォレット管理

**User Story:** ユーザーとして、Google アカウントでログインし、自動的に Sui ウォレットを作成してもらいたい。これにより、ブロックチェーンの知識がなくても NFT を受け取れるようになる。

#### Acceptance Criteria

1. WHEN ユーザーが Google OAuth 認証を完了する, THE Airzone System SHALL JWT アクセストークンを発行する
2. WHEN 新規ユーザーが初回ログインする, THE Airzone System SHALL users テーブルに新しいユーザーレコードを作成する
3. WHEN 新規ユーザーが作成される, THE Airzone System SHALL Sui ブロックチェーン上に新しいウォレットアドレスを生成し wallets テーブルに保存する
4. THE Airzone System SHALL JWT アクセストークンの有効期限を 1 時間に設定する
5. THE Airzone System SHALL JWT リフレッシュトークンの有効期限を 30 日間に設定する

### Requirement 2: WiFi 接続とキャプティブポータル

**User Story:** 店舗オーナーとして、顧客が WiFi に接続したときに自動的にキャプティブポータルを表示し、認証後に NFT を配布したい。これにより、顧客エンゲージメントを向上させることができる。

#### Acceptance Criteria

1. WHEN ユーザーが WiFi ネットワークに接続する, THE Airzone System SHALL OpenNDS を通じてキャプティブポータルページにリダイレクトする
2. WHEN ユーザーがキャプティブポータルで認証を完了する, THE Airzone System SHALL wifi_sessions テーブルに新しいセッションレコードを作成する
3. WHEN WiFi セッションが作成される, THE Airzone System SHALL セッション開始時刻を created_at フィールドに記録する
4. THE Airzone System SHALL 各 WiFi セッションに一意の UUID を割り当てる
5. WHEN ユーザーが認証を完了する, THE Airzone System SHALL インターネットアクセスを許可する

### Requirement 3: NFT 自動配布

**User Story:** ユーザーとして、WiFi 認証後に自動的に NFT を受け取りたい。これにより、店舗での特典や割引を利用できるようになる。

#### Acceptance Criteria

1. WHEN ユーザーが WiFi 認証を完了する, THE Airzone System SHALL Celery タスクキューに NFT 発行タスクを追加する
2. WHEN NFT 発行タスクが実行される, THE Airzone System SHALL Sui ブロックチェーン上で Move スマートコントラクトを呼び出す
3. WHEN NFT が発行される, THE Airzone System SHALL Sponsor Wallet を使用してガス代を支払う
4. WHEN NFT 発行が成功する, THE Airzone System SHALL nft_mints テーブルに発行記録を保存する
5. WHEN NFT 発行が失敗する, THE Airzone System SHALL エラーログを記録し、リトライ処理を 3 回まで実行する

### Requirement 4: EC ショップと商品管理

**User Story:** 店舗オーナーとして、NFT 保有者向けの商品を登録し、価格や在庫を管理したい。これにより、NFT を活用した販売促進ができる。

#### Acceptance Criteria

1. THE Airzone System SHALL products テーブルに商品情報を保存する
2. THE Airzone System SHALL 各商品に名前、説明、価格、在庫数、画像 URL を含める
3. WHEN 管理者が商品を作成する, THE Airzone System SHALL 商品レコードに UUID を割り当てる
4. THE Airzone System SHALL 商品の作成日時と更新日時を記録する
5. WHEN 商品情報が更新される, THE Airzone System SHALL updated_at フィールドを現在時刻に更新する

### Requirement 5: 注文処理と決済

**User Story:** ユーザーとして、保有している NFT を使用して商品を購入し、Stripe で安全に決済したい。これにより、スムーズなショッピング体験を得られる。

#### Acceptance Criteria

1. WHEN ユーザーが商品をカートに追加する, THE Airzone System SHALL セッションストレージにカート情報を保存する
2. WHEN ユーザーがチェックアウトを開始する, THE Airzone System SHALL ユーザーが必要な NFT を保有していることを検証する
3. WHEN NFT 検証が成功する, THE Airzone System SHALL orders テーブルに新しい注文レコードを作成する
4. WHEN 注文が作成される, THE Airzone System SHALL order_items テーブルに各商品の詳細を保存する
5. WHEN ユーザーが決済を完了する, THE Airzone System SHALL Stripe Payment Intent を作成し、payments テーブルに決済記録を保存する
6. WHEN 決済が成功する, THE Airzone System SHALL 注文ステータスを "completed" に更新する
7. WHEN 決済が失敗する, THE Airzone System SHALL 注文ステータスを "failed" に更新し、在庫を復元する

### Requirement 6: セキュリティとデータ保護

**User Story:** システム管理者として、ユーザーデータとトランザクションを安全に保護したい。これにより、ユーザーの信頼を獲得し、法規制に準拠できる。

#### Acceptance Criteria

1. THE Airzone System SHALL すべての API エンドポイントで JWT Bearer Token 認証を要求する
2. THE Airzone System SHALL ユーザーパスワードを bcrypt アルゴリズムでハッシュ化する
3. THE Airzone System SHALL すべての HTTP 通信に TLS 1.3 を使用する
4. THE Airzone System SHALL SQL インジェクション攻撃を防ぐためにパラメータ化クエリを使用する
5. THE Airzone System SHALL XSS 攻撃を防ぐためにすべてのユーザー入力をサニタイズする
6. THE Airzone System SHALL CSRF 攻撃を防ぐためにトークン検証を実装する
7. THE Airzone System SHALL API レート制限を実装し、DDoS 攻撃を軽減する
8. THE Airzone System SHALL HSTS (HTTP Strict Transport Security) を有効化する

### Requirement 7: フロントエンド UI とユーザー体験

**User Story:** ユーザーとして、直感的で使いやすいインターフェースで NFT を確認し、商品を購入したい。これにより、ストレスなくサービスを利用できる。

#### Acceptance Criteria

1. THE Airzone System SHALL Next.js 14 App Router を使用してサーバーサイドレンダリングを実装する
2. THE Airzone System SHALL Tailwind CSS を使用してレスポンシブデザインを提供する
3. THE Airzone System SHALL Zustand を使用してグローバル状態管理を実装する
4. WHEN ユーザーがページを読み込む, THE Airzone System SHALL 200 ミリ秒以内に初期コンテンツを表示する
5. THE Airzone System SHALL @mysten/dapp-kit を使用して Sui ウォレット接続機能を提供する
6. THE Airzone System SHALL @stripe/react-stripe-js を使用して安全な決済フォームを表示する

### Requirement 8: バックエンド API とデータ処理

**User Story:** 開発者として、明確に定義された RESTful API を使用してフロントエンドとバックエンドを統合したい。これにより、保守性と拡張性が向上する。

#### Acceptance Criteria

1. THE Airzone System SHALL Flask 3.0 を使用して RESTful API を実装する
2. THE Airzone System SHALL すべての API エンドポイントを /api/v1/ ベースパスの下に配置する
3. THE Airzone System SHALL Blueprint パターンを使用してルートを整理する
4. THE Airzone System SHALL Repository パターンを使用してデータベースアクセスを抽象化する
5. THE Airzone System SHALL Service レイヤーを使用してビジネスロジックを実装する
6. WHEN API が成功レスポンスを返す, THE Airzone System SHALL {"status": "success", "data": {}} 形式を使用する
7. WHEN API がエラーレスポンスを返す, THE Airzone System SHALL {"status": "error", "error": "message", "code": number} 形式を使用する

### Requirement 9: データベース設計と整合性

**User Story:** システム管理者として、データの整合性を保ち、効率的にクエリできるデータベース構造を維持したい。これにより、システムの信頼性とパフォーマンスが向上する。

#### Acceptance Criteria

1. THE Airzone System SHALL MySQL 8.0 を使用してデータを永続化する
2. THE Airzone System SHALL SQLAlchemy ORM を使用してデータベース操作を実行する
3. THE Airzone System SHALL すべてのテーブル名を複数形の snake_case で命名する
4. THE Airzone System SHALL すべてのテーブルに UUID 型の id 主キーを含める
5. THE Airzone System SHALL すべてのテーブルに created_at および updated_at タイムスタンプフィールドを含める
6. THE Airzone System SHALL 外部キーを "{table}_id" 形式で命名する
7. THE Airzone System SHALL 外部キー制約を使用して参照整合性を保証する

### Requirement 10: 非同期処理とバックグラウンドタスク

**User Story:** システム管理者として、NFT 発行などの時間のかかる処理を非同期で実行したい。これにより、ユーザーの待ち時間を短縮し、システムのスループットを向上させる。

#### Acceptance Criteria

1. THE Airzone System SHALL Celery を使用してバックグラウンドタスクを処理する
2. THE Airzone System SHALL Redis をタスクキューのブローカーとして使用する
3. WHEN NFT 発行リクエストを受信する, THE Airzone System SHALL タスクを Celery キューに追加し、即座にレスポンスを返す
4. THE Airzone System SHALL タスクの実行状態を Redis に保存する
5. WHEN タスクが失敗する, THE Airzone System SHALL 指数バックオフを使用して最大 3 回リトライする

### Requirement 11: インフラストラクチャとデプロイメント

**User Story:** DevOps エンジニアとして、コンテナ化されたアプリケーションを簡単にデプロイし、スケールしたい。これにより、運用コストを削減し、可用性を向上させる。

#### Acceptance Criteria

1. THE Airzone System SHALL Docker を使用してアプリケーションをコンテナ化する
2. THE Airzone System SHALL Docker Compose を使用してマルチコンテナ環境を定義する
3. THE Airzone System SHALL Apache 2.4 を Web サーバーとして使用する
4. THE Airzone System SHALL mod_wsgi を使用して Flask アプリケーションを提供する
5. THE Airzone System SHALL mod_proxy を使用してリバースプロキシを設定する
6. THE Airzone System SHALL Let's Encrypt を使用して SSL/TLS 証明書を自動更新する
7. THE Airzone System SHALL Redis をキャッシュレイヤーとして使用する

### Requirement 12: テストとコード品質

**User Story:** 開発者として、高品質なコードを維持し、リグレッションを防ぎたい。これにより、バグを早期に発見し、安心してリファクタリングできる。

#### Acceptance Criteria

1. THE Airzone System SHALL pytest を使用してバックエンドのユニットテストを実行する
2. THE Airzone System SHALL Jest および React Testing Library を使用してフロントエンドのテストを実行する
3. THE Airzone System SHALL 最低 80% のコードカバレッジを維持する
4. THE Airzone System SHALL 外部 API 呼び出しをモック化してテストする
5. THE Airzone System SHALL ESLint および Prettier を使用してコードスタイルを統一する
6. THE Airzone System SHALL PEP 8 スタイルガイドに従って Python コードを記述する
7. THE Airzone System SHALL すべての Python 関数に型ヒントを含める
8. THE Airzone System SHALL すべての Python 関数に Google Style の docstring を含める
