# Airzone システムアーキテクチャ

## 概要

Airzone は、WiFi 接続をトリガーとした NFT 配布と EC ショップを統合したプラットフォームです。このドキュメントでは、システム全体のアーキテクチャ、コンポーネント間の関係、データフロー、技術スタックについて説明します。

## システム構成図

```
┌─────────────────────────────────────────────────────────────────┐
│                         ユーザー                                  │
│                    (WiFi 接続デバイス)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ WiFi 接続
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OpenNDS                                     │
│                 (キャプティブポータル)                            │
│                                                                   │
│  - WiFi 認証ゲートウェイ                                          │
│  - ユーザーをキャプティブポータルページにリダイレクト              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP リダイレクト
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Apache Web Server                             │
│                   (リバースプロキシ)                              │
│                                                                   │
│  - SSL/TLS 終端                                                  │
│  - リクエストルーティング                                         │
│  - セキュリティヘッダー                                           │
└──────────┬──────────────────────────────┬───────────────────────┘
           │                              │
           │ /api/v1/*                    │ /*
           ▼                              ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   Backend (Flask)        │    │   Frontend (Next.js)     │
│   Port: 5000             │    │   Port: 3000             │
│                          │    │                          │
│  ┌────────────────────┐  │    │  ┌────────────────────┐  │
│  │   API Routes       │  │    │  │   Pages            │  │
│  │  - Auth            │  │    │  │  - Home            │  │
│  │  - NFT             │  │    │  │  - Captive Portal  │  │
│  │  - Products        │  │    │  │  - Shop            │  │
│  │  - Orders          │  │    │  │  - Dashboard       │  │
│  │  - Payments        │  │    │  │  - Checkout        │  │
│  │  - WiFi            │  │    │  │  - Orders          │  │
│  └────────┬───────────┘  │    │  └────────────────────┘  │
│           │              │    │                          │
│  ┌────────▼───────────┐  │    │  ┌────────────────────┐  │
│  │   Services         │  │    │  │   Components       │  │
│  │  - AuthService     │  │    │  │  - Auth            │  │
│  │  - NFTService      │  │    │  │  - NFT             │  │
│  │  - ProductService  │  │    │  │  - Shop            │  │
│  │  - OrderService    │  │    │  │  - Layout          │  │
│  │  - PaymentService  │  │    │  │  - UI              │  │
│  │  - WalletService   │  │    │  └────────────────────┘  │
│  └────────┬───────────┘  │    │                          │
│           │              │    │  ┌────────────────────┐  │
│  ┌────────▼───────────┐  │    │  │   State (Zustand)  │  │
│  │   Repositories     │  │    │  │  - Auth Store      │  │
│  │  - UserRepo        │  │    │  │  - Cart Store      │  │
│  │  - NFTRepo         │  │    │  │  - NFT Store       │  │
│  │  - ProductRepo     │  │    │  └────────────────────┘  │
│  │  - OrderRepo       │  │    │                          │
│  │  - PaymentRepo     │  │    │  ┌────────────────────┐  │
│  │  - WalletRepo      │  │    │  │   API Client       │  │
│  │  - WiFiSessionRepo │  │    │  │  - HTTP Client     │  │
│  └────────┬───────────┘  │    │  │  - Error Handling  │  │
│           │              │    │  └────────────────────┘  │
│  ┌────────▼───────────┐  │    └──────────────────────────┘
│  │   Models (ORM)     │  │
│  │  - User            │  │
│  │  - Wallet          │  │
│  │  - NFTMint         │  │
│  │  - Product         │  │
│  │  - Order           │  │
│  │  - Payment         │  │
│  │  - WiFiSession     │  │
│  │  - TaskQueue       │  │
│  └────────┬───────────┘  │
│           │              │
│  ┌────────▼───────────┐  │
│  │   Clients          │  │
│  │  - XRPLClient      │  │
│  │  - StripeClient    │  │
│  │  - GoogleAuthClient│  │
│  └────────┬───────────┘  │
│           │              │
│  ┌────────▼───────────┐  │
│  │   Task Manager     │  │
│  │  - NFT Minting     │  │
│  │  - Background Jobs │  │
│  └────────────────────┘  │
└──────────┬───────────────┘
           │
           │ Database Queries
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MySQL Database                              │
│                        Port: 3306                                │
│                                                                   │
│  Tables:                                                          │
│  - users                - products                                │
│  - wallets              - orders                                  │
│  - nft_mints            - order_items                             │
│  - wifi_sessions        - payments                                │
│  - task_queue                                                     │
└─────────────────────────────────────────────────────────────────┘

External Services:
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  XRPL Blockchain │  │  Stripe API      │  │  Google OAuth    │
│  (Testnet)       │  │  (Payments)      │  │  (Auth)          │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

## 技術スタック

### フロントエンド
- **フレームワーク:** Next.js 14 (App Router)
- **言語:** TypeScript
- **スタイリング:** Tailwind CSS
- **状態管理:** Zustand
- **ブロックチェーン:** XRPL
- **決済:** @stripe/react-stripe-js
- **HTTP クライアント:** Fetch API

### バックエンド
- **フレームワーク:** Flask 3.0
- **言語:** Python 3.11+
- **ORM:** SQLAlchemy 2.0
- **マイグレーション:** Alembic
- **認証:** JWT (PyJWT)
- **タスクキュー:** カスタム実装（TaskManager）

### データベース
- **RDBMS:** MySQL 8.0
- **接続プール:** SQLAlchemy Engine

### ブロックチェーン
- **プラットフォーム:** XRPL (XRP Ledger)
- **SDK:** xrpl-py (Python XRPL SDK)
- **ネットワーク:** Testnet / Mainnet

### 外部サービス
- **認証:** Google OAuth 2.0
- **決済:** Stripe
- **WiFi:** OpenNDS (オプション)

### インフラ
- **Web サーバー:** Apache 2.4
- **プロセス管理:** systemd
- **SSL/TLS:** Let's Encrypt

---

## コンポーネント詳細

### 1. フロントエンド (Next.js)

#### 責務
- ユーザーインターフェースの提供
- クライアントサイドの状態管理
- バックエンド API との通信
- Stripe 決済フローの処理
- XRPL ウォレット接続（将来的）

#### 主要ディレクトリ構造
```
frontend/
├── app/                    # Next.js App Router ページ
│   ├── page.tsx           # ホームページ
│   ├── login/             # ログインページ
│   ├── captive/           # キャプティブポータル
│   ├── dashboard/         # ダッシュボード
│   ├── shop/              # ショップ
│   ├── checkout/          # チェックアウト
│   ├── orders/            # 注文履歴
│   └── nfts/              # NFT ギャラリー
├── components/            # React コンポーネント
│   ├── auth/             # 認証関連
│   ├── nft/              # NFT 表示
│   ├── shop/             # EC ショップ
│   ├── layout/           # レイアウト
│   └── ui/               # 再利用可能 UI
├── lib/                  # ユーティリティ
│   ├── api/              # API サービス
│   └── api-client.ts     # HTTP クライアント
├── stores/               # Zustand ストア
│   ├── auth-store.ts     # 認証状態
│   ├── cart-store.ts     # カート状態
│   └── nft-store.ts      # NFT 状態
└── types/                # TypeScript 型定義
```

#### データフロー
1. ユーザーアクション → コンポーネント
2. コンポーネント → API Client
3. API Client → Backend API
4. レスポンス → Zustand Store
5. Store → コンポーネント再レンダリング

---

### 2. バックエンド (Flask)

#### 責務
- RESTful API の提供
- ビジネスロジックの実装
- データベース操作
- 外部サービスとの統合
- 認証・認可
- バックグラウンドタスク処理

#### レイヤーアーキテクチャ

```
┌─────────────────────────────────────┐
│         Routes (API Layer)          │  ← HTTP リクエスト処理
│  - リクエスト検証                    │
│  - レスポンス整形                    │
│  - エラーハンドリング                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Services (Business Logic)      │  ← ビジネスロジック
│  - ドメインロジック                  │
│  - トランザクション管理              │
│  - 外部サービス呼び出し              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Repositories (Data Access)       │  ← データアクセス
│  - CRUD 操作                        │
│  - クエリ構築                        │
│  - データマッピング                  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       Models (ORM Entities)         │  ← データモデル
│  - テーブル定義                      │
│  - リレーションシップ                │
│  - バリデーション                    │
└─────────────────────────────────────┘
```

#### 主要ディレクトリ構造
```
backend/
├── routes/               # API エンドポイント
│   ├── auth.py          # 認証
│   ├── nft.py           # NFT
│   ├── product.py       # 商品
│   ├── order.py         # 注文
│   ├── payment.py       # 決済
│   └── wifi.py          # WiFi
├── services/            # ビジネスロジック
│   ├── auth_service.py
│   ├── nft_service.py
│   ├── product_service.py
│   ├── order_service.py
│   ├── payment_service.py
│   └── wallet_service.py
├── repositories/        # データアクセス
│   ├── user_repository.py
│   ├── nft_repository.py
│   ├── product_repository.py
│   ├── order_repository.py
│   ├── payment_repository.py
│   ├── wallet_repository.py
│   └── wifi_session_repository.py
├── models/              # ORM モデル
│   ├── user.py
│   ├── wallet.py
│   ├── nft_mint.py
│   ├── product.py
│   ├── order.py
│   ├── payment.py
│   ├── wifi_session.py
│   └── task_queue.py
├── clients/             # 外部サービスクライアント
│   ├── xrpl_client.py
│   ├── stripe_client.py
│   └── google_auth.py
├── middleware/          # ミドルウェア
│   ├── auth.py          # JWT 認証
│   ├── security.py      # セキュリティ
│   └── rate_limit.py    # レート制限
├── tasks/               # バックグラウンドタスク
│   ├── task_manager.py
│   └── nft_tasks.py
├── alembic/             # データベースマイグレーション
│   └── versions/
├── app.py               # アプリケーションエントリーポイント
├── config.py            # 設定管理
└── exceptions.py        # カスタム例外
```

---

### 3. データベース (MySQL)

#### スキーマ設計

**users テーブル**
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    google_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_google_id (google_id)
);
```

**wallets テーブル**
```sql
CREATE TABLE wallets (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    address VARCHAR(255) UNIQUE NOT NULL,
    encrypted_private_key TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_address (address)
);
```

**nft_mints テーブル**
```sql
CREATE TABLE nft_mints (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    wallet_address VARCHAR(255) NOT NULL,
    nft_object_id VARCHAR(255),
    transaction_digest VARCHAR(255),
    status ENUM('pending', 'minting', 'completed', 'failed') DEFAULT 'pending',
    metadata JSON,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_nft_object_id (nft_object_id)
);
```

**products テーブル**
```sql
CREATE TABLE products (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INT NOT NULL,
    stock_quantity INT DEFAULT 0,
    image_url VARCHAR(500),
    required_nft_id VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_is_active (is_active),
    INDEX idx_required_nft_id (required_nft_id)
);
```

**orders テーブル**
```sql
CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    total_amount INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);
```

**order_items テーブル**
```sql
CREATE TABLE order_items (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    quantity INT NOT NULL,
    unit_price INT NOT NULL,
    subtotal INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
);
```

**payments テーブル**
```sql
CREATE TABLE payments (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    stripe_payment_intent_id VARCHAR(255) UNIQUE,
    amount INT NOT NULL,
    currency VARCHAR(3) DEFAULT 'jpy',
    status ENUM('pending', 'processing', 'succeeded', 'failed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id),
    INDEX idx_stripe_payment_intent_id (stripe_payment_intent_id),
    INDEX idx_status (status)
);
```

**wifi_sessions テーブル**
```sql
CREATE TABLE wifi_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    mac_address VARCHAR(17),
    ip_address VARCHAR(45),
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    disconnected_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_mac_address (mac_address)
);
```

**task_queue テーブル**
```sql
CREATE TABLE task_queue (
    id VARCHAR(36) PRIMARY KEY,
    task_type VARCHAR(50) NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    payload JSON,
    result JSON,
    error_message TEXT,
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_task_type (task_type)
);
```

---

### 4. ブロックチェーン (Sui)

#### スマートコントラクト

**airzone_nft.move**
```move
module airzone::nft {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use std::string::{Self, String};

    struct AirzoneNFT has key, store {
        id: UID,
        name: String,
        description: String,
        image_url: String,
    }

    public entry fun mint(
        name: vector<u8>,
        description: vector<u8>,
        image_url: vector<u8>,
        recipient: address,
        ctx: &mut TxContext
    ) {
        let nft = AirzoneNFT {
            id: object::new(ctx),
            name: string::utf8(name),
            description: string::utf8(description),
            image_url: string::utf8(image_url),
        };
        transfer::public_transfer(nft, recipient);
    }
}
```

#### スポンサードトランザクション

1. **スポンサーウォレット:** システムが管理するウォレット
2. **ガス代支払い:** スポンサーがすべてのトランザクションのガス代を支払う
3. **ユーザー体験:** ユーザーは XRPL トークンを持たずに NFT を受け取れる

**フロー:**
```
1. ユーザーが NFT 発行をリクエスト
2. Backend がスポンサーウォレットでトランザクションに署名
3. XRPL ネットワークにトランザクション送信
4. スポンサーがガス代を支払う
5. NFT がユーザーのウォレットに転送される
```

---

## データフロー

### 1. ユーザー登録・認証フロー

```
┌──────────┐
│ ユーザー │
└────┬─────┘
     │ 1. Google ログインボタンクリック
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 2. Google OAuth フロー開始
     ▼
┌──────────────┐
│ Google OAuth │
└────┬─────────┘
     │ 3. ID トークン返却
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 4. POST /api/v1/auth/google (id_token)
     ▼
┌──────────────┐
│  Backend     │
│  AuthService │
└────┬─────────┘
     │ 5. ID トークン検証
     ▼
┌──────────────┐
│ Google API   │
└────┬─────────┘
     │ 6. ユーザー情報返却
     ▼
┌──────────────┐
│  Backend     │
│  UserRepo    │
└────┬─────────┘
     │ 7. ユーザー作成/取得
     ▼
┌──────────────┐
│  MySQL       │
└────┬─────────┘
     │ 8. ユーザーレコード
     ▼
┌──────────────┐
│  Backend     │
│  WalletService│
└────┬─────────┘
     │ 9. ウォレット自動生成（初回のみ）
     ▼
┌──────────────┐
│  Backend     │
│  AuthService │
└────┬─────────┘
     │ 10. JWT トークン生成
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 11. トークン保存
     │ 12. ダッシュボードへリダイレクト
     ▼
┌──────────────┐
│ ユーザー     │
│ (認証済み)   │
└──────────────┘
```

---

### 2. NFT 発行フロー

```
┌──────────┐
│ ユーザー │
└────┬─────┘
     │ 1. NFT 発行リクエスト
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 2. POST /api/v1/nfts/mint
     │    (name, description, image_url)
     ▼
┌──────────────┐
│  Backend     │
│  NFTService  │
└────┬─────────┘
     │ 3. ユーザーのウォレット取得
     ▼
┌──────────────┐
│  WalletRepo  │
└────┬─────────┘
     │ 4. ウォレットアドレス
     ▼
┌──────────────┐
│  NFTService  │
└────┬─────────┘
     │ 5. NFT レコード作成 (status: pending)
     ▼
┌──────────────┐
│  NFTRepo     │
└────┬─────────┘
     │ 6. NFT レコード保存
     ▼
┌──────────────┐
│  MySQL       │
└────┬─────────┘
     │ 7. NFT ID
     ▼
┌──────────────┐
│  NFTService  │
└────┬─────────┘
     │ 8. バックグラウンドタスク作成
     ▼
┌──────────────┐
│ TaskManager  │
└────┬─────────┘
     │ 9. タスクキューに追加
     ▼
┌──────────────┐
│  MySQL       │
│  task_queue  │
└────┬─────────┘
     │ 10. Task ID 返却
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 11. ポーリング開始
     │     GET /api/v1/nfts/status/{task_id}
     ▼

[バックグラウンド処理]

┌──────────────┐
│ TaskManager  │
│ (Worker)     │
└────┬─────────┘
     │ 12. タスク取得・実行
     ▼
┌──────────────┐
│  NFTService  │
└────┬─────────┘
     │ 13. NFT ステータス更新 (minting)
     ▼
┌──────────────┐
│  SuiClient   │
└────┬─────────┘
     │ 14. スポンサーウォレットで署名
     │ 15. mint トランザクション作成
     ▼
┌──────────────┐
│ XRPL Network  │
└────┬─────────┘
     │ 16. トランザクション実行
     │ 17. NFT オブジェクト作成
     │ 18. ユーザーウォレットに転送
     ▼
┌──────────────┐
│  SuiClient   │
└────┬─────────┘
     │ 19. トランザクション結果
     ▼
┌──────────────┐
│  NFTService  │
└────┬─────────┘
     │ 20. NFT ステータス更新 (completed)
     │     nft_object_id, transaction_digest 保存
     ▼
┌──────────────┐
│  MySQL       │
└────┬─────────┘
     │ 21. 更新完了
     ▼
┌──────────────┐
│  Frontend    │
│  (ポーリング)│
└────┬─────────┘
     │ 22. ステータス確認
     │ 23. completed 検出
     │ 24. 成功メッセージ表示
     ▼
┌──────────────┐
│ ユーザー     │
│ (NFT 受領)   │
└──────────────┘
```

---

### 3. 商品購入フロー

```
┌──────────┐
│ ユーザー │
└────┬─────┘
     │ 1. 商品をカートに追加
     ▼
┌──────────────┐
│  Frontend    │
│  CartStore   │
└────┬─────────┘
     │ 2. カート状態更新
     │ 3. チェックアウトページへ
     ▼
┌──────────────┐
│  Frontend    │
│  Checkout    │
└────┬─────────┘
     │ 4. POST /api/v1/orders
     │    (items: [{product_id, quantity}])
     ▼
┌──────────────┐
│  Backend     │
│  OrderService│
└────┬─────────┘
     │ 5. 商品情報取得
     ▼
┌──────────────┐
│ ProductRepo  │
└────┬─────────┘
     │ 6. 商品データ
     ▼
┌──────────────┐
│  OrderService│
└────┬─────────┘
     │ 7. NFT 要件チェック
     ▼
┌──────────────┐
│  NFTRepo     │
└────┬─────────┘
     │ 8. ユーザーの NFT 確認
     ▼
┌──────────────┐
│  OrderService│
└────┬─────────┘
     │ 9. 在庫チェック
     │ 10. 合計金額計算
     ▼
┌──────────────┐
│  OrderRepo   │
└────┬─────────┘
     │ 11. 注文作成 (status: pending)
     │ 12. 注文アイテム作成
     ▼
┌──────────────┐
│  MySQL       │
└────┬─────────┘
     │ 13. 注文 ID
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 14. POST /api/v1/payments/intent
     │     (order_id)
     ▼
┌──────────────┐
│  Backend     │
│PaymentService│
└────┬─────────┘
     │ 15. Stripe Payment Intent 作成
     ▼
┌──────────────┐
│ StripeClient │
└────┬─────────┘
     │ 16. Payment Intent API 呼び出し
     ▼
┌──────────────┐
│  Stripe API  │
└────┬─────────┘
     │ 17. client_secret 返却
     ▼
┌──────────────┐
│PaymentService│
└────┬─────────┘
     │ 18. Payment レコード作成
     ▼
┌──────────────┐
│  MySQL       │
└────┬─────────┘
     │ 19. Payment ID
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 20. Stripe Elements 表示
     │ 21. ユーザーがカード情報入力
     ▼
┌──────────────┐
│ ユーザー     │
└────┬─────────┘
     │ 22. 支払い確定
     ▼
┌──────────────┐
│  Frontend    │
│  Stripe.js   │
└────┬─────────┘
     │ 23. confirmPayment()
     ▼
┌──────────────┐
│  Stripe API  │
└────┬─────────┘
     │ 24. 決済処理
     │ 25. Webhook 送信
     ▼
┌──────────────┐
│  Backend     │
│  /payments/  │
│  webhook     │
└────┬─────────┘
     │ 26. Webhook 署名検証
     ▼
┌──────────────┐
│PaymentService│
└────┬─────────┘
     │ 27. Payment ステータス更新 (succeeded)
     │ 28. Order ステータス更新 (completed)
     │ 29. 在庫減少
     ▼
┌──────────────┐
│  MySQL       │
└────┬─────────┘
     │ 30. 更新完了
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 31. 成功ページ表示
     │ 32. 注文確認メール送信（将来実装）
     ▼
┌──────────────┐
│ ユーザー     │
│ (購入完了)   │
└──────────────┘
```

---

### 4. WiFi 接続フロー（OpenNDS 統合）

```
┌──────────┐
│ ユーザー │
└────┬─────┘
     │ 1. WiFi ネットワークに接続
     ▼
┌──────────────┐
│   OpenNDS    │
└────┬─────────┘
     │ 2. キャプティブポータル検出
     │ 3. リダイレクト
     │    https://airz.one/captive?mac=XX:XX:XX:XX:XX:XX&ip=192.168.1.100
     ▼
┌──────────────┐
│  Frontend    │
│  /captive    │
└────┬─────────┘
     │ 4. POST /api/v1/wifi/connect
     │    (mac_address, ip_address)
     ▼
┌──────────────┐
│  Backend     │
└────┬─────────┘
     │ 5. WiFi セッション作成
     ▼
┌──────────────┐
│  MySQL       │
│wifi_sessions │
└────┬─────────┘
     │ 6. Session ID
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 7. ログインページ表示
     │ 8. 利用規約・NFT 特典説明
     ▼
┌──────────────┐
│ ユーザー     │
└────┬─────────┘
     │ 9. Google ログイン
     ▼
[認証フロー実行]
     ▼
┌──────────────┐
│  Backend     │
└────┬─────────┘
     │ 10. WiFi セッション更新 (user_id 設定)
     ▼
┌──────────────┐
│  MySQL       │
└────┬─────────┘
     │ 11. 更新完了
     ▼
┌──────────────┐
│  Backend     │
│  NFTService  │
└────┬─────────┘
     │ 12. 自動 NFT 発行トリガー
     ▼
[NFT 発行フロー実行]
     ▼
┌──────────────┐
│  Frontend    │
└────┬─────────┘
     │ 13. ダッシュボードへリダイレクト
     │ 14. NFT 発行中メッセージ表示
     ▼
┌──────────────┐
│ ユーザー     │
│ (WiFi 利用可)│
│ (NFT 発行中) │
└──────────────┘
```

---

## セキュリティアーキテクチャ

### 1. 認証・認可

#### JWT トークン
- **アクセストークン:** 有効期限 1 時間
- **リフレッシュトークン:** 有効期限 30 日
- **署名アルゴリズム:** HS256
- **ペイロード:** user_id, email, exp, iat

#### Google OAuth 2.0
- **フロー:** Authorization Code Flow
- **スコープ:** email, profile
- **ID トークン検証:** Google API で検証

### 2. データ保護

#### 暗号化
- **ウォレット秘密鍵:** AES-256-GCM で暗号化
- **暗号化キー:** 環境変数で管理
- **SSL/TLS:** Let's Encrypt 証明書

#### 入力検証
- **サニタイゼーション:** すべてのユーザー入力
- **バリデーション:** 型、形式、範囲チェック
- **SQL インジェクション対策:** SQLAlchemy ORM 使用

### 3. API セキュリティ

#### CORS
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://airz.one"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

#### セキュリティヘッダー
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

#### レート制限
- **実装:** Flask-Limiter（将来実装）
- **制限:** IP ベース、エンドポイント別

### 4. ブロックチェーンセキュリティ

#### スポンサーウォレット
- **秘密鍵管理:** 環境変数、暗号化保存
- **アクセス制御:** バックエンドのみアクセス可能
- **残高監視:** 自動アラート（将来実装）

#### トランザクション検証
- **署名検証:** XRPL SDK で自動検証
- **手数料制限:** 約 0.00001 XRP（固定）
- **エラーハンドリング:** リトライロジック

---

## スケーラビリティ

### 現在のアーキテクチャ

#### 単一サーバー構成
```
┌─────────────────────────────────┐
│         Single Server           │
│                                 │
│  ┌──────────┐  ┌──────────┐   │
│  │ Apache   │  │  MySQL   │   │
│  │          │  │          │   │
│  │ Backend  │  │          │   │
│  │ Frontend │  │          │   │
│  └──────────┘  └──────────┘   │
└─────────────────────────────────┘
```

**制限:**
- 同時接続数: ~1000
- リクエスト/秒: ~100
- データベース接続: ~100

### 将来のスケーリング戦略

#### 水平スケーリング
```
┌─────────────────────────────────────────────────┐
│              Load Balancer                      │
└──────┬──────────────┬──────────────┬───────────┘
       │              │              │
┌──────▼──────┐ ┌────▼──────┐ ┌────▼──────┐
│  Backend 1  │ │ Backend 2 │ │ Backend 3 │
└──────┬──────┘ └────┬──────┘ └────┬──────┘
       │              │              │
       └──────────────┴──────────────┘
                      │
              ┌───────▼────────┐
              │  MySQL Cluster │
              │  (Master-Slave)│
              └────────────────┘
```

#### キャッシング
- **Redis:** セッション、API レスポンス
- **CDN:** 静的アセット、画像
- **ブラウザキャッシュ:** Next.js 最適化

#### データベース最適化
- **読み取りレプリカ:** 読み取り負荷分散
- **接続プール:** 効率的な接続管理
- **インデックス:** クエリ最適化
- **パーティショニング:** 大規模データ対応

#### バックグラウンドジョブ
- **Celery:** 分散タスクキュー（将来実装）
- **Redis:** メッセージブローカー
- **ワーカープロセス:** 複数ワーカー

---

## 監視・ロギング

### ログ管理

#### ログレベル
- **DEBUG:** 開発環境のみ
- **INFO:** 通常の操作ログ
- **WARNING:** 警告（リトライ可能なエラー）
- **ERROR:** エラー（要対応）
- **CRITICAL:** 重大なエラー（即座に対応）

#### ログ出力先
```python
# 開発環境
- コンソール出力
- ファイル: logs/app.log

# 本番環境
- ファイル: /var/log/airzone/app.log
- ローテーション: 日次、7日保持
- 集約: Elasticsearch + Kibana（将来実装）
```

#### ログ形式
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "INFO",
  "logger": "airzone.services.nft_service",
  "message": "NFT minted successfully",
  "user_id": "uuid",
  "nft_id": "uuid",
  "transaction_digest": "0x..."
}
```

### メトリクス監視

#### システムメトリクス
- CPU 使用率
- メモリ使用率
- ディスク使用率
- ネットワーク I/O

#### アプリケーションメトリクス
- リクエスト数/秒
- レスポンスタイム
- エラー率
- アクティブユーザー数

#### ビジネスメトリクス
- NFT 発行数
- 注文数
- 決済成功率
- WiFi 接続数

#### 監視ツール（将来実装）
- **Prometheus:** メトリクス収集
- **Grafana:** ダッシュボード
- **Sentry:** エラートラッキング
- **Uptime Robot:** 死活監視

---

## デプロイメント

### 開発環境

```bash
# Backend
cd backend
python app.py

# Frontend
cd frontend
npm run dev

# Database
mysql -u root -p
```

### 本番環境

#### systemd サービス
```ini
# /etc/systemd/system/airzone-backend.service
[Unit]
Description=Airzone Backend API
After=network.target mysql.service

[Service]
Type=simple
User=airzone
WorkingDirectory=/var/www/airzone/backend
Environment="PATH=/var/www/airzone/backend/venv/bin"
ExecStart=/var/www/airzone/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/airzone-frontend.service
[Unit]
Description=Airzone Frontend
After=network.target

[Service]
Type=simple
User=airzone
WorkingDirectory=/var/www/airzone/frontend
ExecStart=/usr/bin/npm start
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Apache 設定
```apache
<VirtualHost *:443>
    ServerName airz.one
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/airz.one/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/airz.one/privkey.pem
    
    # Security Headers
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "DENY"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Strict-Transport-Security "max-age=31536000"
    
    # Backend API Proxy
    ProxyPass /api/v1 http://localhost:5000/api/v1
    ProxyPassReverse /api/v1 http://localhost:5000/api/v1
    
    # Frontend Proxy
    ProxyPass / http://localhost:3000/
    ProxyPassReverse / http://localhost:3000/
    
    # WebSocket Support (for Next.js HMR in dev)
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/?(.*) "ws://localhost:3000/$1" [P,L]
</VirtualHost>
```

### CI/CD パイプライン（将来実装）

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend && pytest
          cd frontend && npm test
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        run: |
          ssh user@server 'cd /var/www/airzone && git pull'
          ssh user@server 'systemctl restart airzone-backend'
          ssh user@server 'systemctl restart airzone-frontend'
```

---

## パフォーマンス最適化

### フロントエンド

#### Next.js 最適化
- **静的生成 (SSG):** 商品ページ
- **サーバーサイドレンダリング (SSR):** ダッシュボード
- **画像最適化:** next/image コンポーネント
- **コード分割:** 動的インポート
- **プリフェッチ:** Link コンポーネント

#### バンドルサイズ削減
```javascript
// 動的インポート
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Loading />,
  ssr: false
});

// Tree shaking
import { specific } from 'library';  // ✓
// import * as all from 'library';    // ✗
```

### バックエンド

#### データベースクエリ最適化
```python
# N+1 問題回避
orders = session.query(Order)\
    .options(joinedload(Order.items))\
    .filter(Order.user_id == user_id)\
    .all()

# インデックス活用
# CREATE INDEX idx_user_id ON orders(user_id);
```

#### 接続プール
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

#### キャッシング戦略
```python
# 商品リストキャッシュ（将来実装）
@cache.memoize(timeout=300)
def get_products():
    return product_service.get_all_products()
```

---

## トラブルシューティング

### 一般的な問題

#### 1. データベース接続エラー
**症状:** `Can't connect to MySQL server`

**原因:**
- MySQL サービスが停止
- 接続情報が不正
- ファイアウォールでブロック

**対処法:**
```bash
# MySQL 起動確認
systemctl status mysql

# 接続テスト
mysql -u airzone_user -p airzone

# ログ確認
tail -f /var/log/mysql/error.log
```

#### 2. NFT 発行失敗
**症状:** NFT ステータスが `failed`

**原因:**
- スポンサーウォレット残高不足
- XRPL ネットワーク障害
- トランザクションタイムアウト

**対処法:**
```bash
# スポンサー残高確認
python backend/verify_sponsored_transactions.py

# エラーログ確認
grep "NFT minting failed" /var/log/airzone/app.log

# 手動リトライ
# タスクキューから再実行
```

#### 3. 決済処理エラー
**症状:** 決済が `pending` のまま

**原因:**
- Stripe Webhook 未受信
- Webhook 署名検証失敗
- ネットワークエラー

**対処法:**
```bash
# Webhook ログ確認
grep "webhook" /var/log/airzone/app.log

# Stripe ダッシュボードで確認
# https://dashboard.stripe.com/webhooks

# 手動で決済ステータス更新
```

---

## まとめ

Airzone は、モダンな Web 技術とブロックチェーン技術を組み合わせた、スケーラブルで安全なプラットフォームです。

### 主要な設計原則

1. **レイヤー分離:** Routes → Services → Repositories → Models
2. **疎結合:** コンポーネント間の依存を最小化
3. **セキュリティファースト:** 認証、暗号化、入力検証
4. **スケーラビリティ:** 水平スケーリング可能な設計
5. **保守性:** 明確なコード構造、ドキュメント

### 技術的ハイライト

- **スポンサードトランザクション:** ユーザーは手数料不要で NFT を受け取れる
- **自動ウォレット生成:** ユーザー登録時に XRPL ウォレットを自動作成
- **Xaman Wallet対応:** ユーザーが自分のウォレットを接続可能
- **NFT ゲート EC:** NFT 保有者限定商品の販売
- **非同期処理:** バックグラウンドタスクで NFT 発行
- **セキュアな決済:** Stripe 統合で安全な決済処理

---

**最終更新:** 2024-11-15  
**バージョン:** 1.0  
**作成者:** Airzone Development Team
