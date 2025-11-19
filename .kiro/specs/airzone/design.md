# Design Document

## Overview

Airzone（https://airz.one/）は、OpenNDS キャプティブポータルと XRPL ブロックチェーンを統合した、WiFi 接続トリガー型の NFT 配布・EC ショッププラットフォームです。

### 主要機能
- Google OAuth による認証と自動ウォレット生成
- OpenNDS キャプティブポータル統合
- XRPL ブロックチェーン上での NFT 自動発行
- NFT ゲート付き EC ショップ
- Stripe 決済統合
- 非同期タスク処理

### 技術スタック概要
- **Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Backend**: Flask 3.0 + Python 3.11+ + SQLAlchemy
- **Database**: MySQL 8.0
- **Task Queue**: Python threading / asyncio
- **Blockchain**: XRPL
- **Payment**: Stripe
- **Infrastructure**: Apache 2.4 (直接デプロイ)

## Architecture

### システムアーキテクチャ図

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Device                              │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │   Browser    │◄────────┤ WiFi Client  │                      │
│  └──────┬───────┘         └──────────────┘                      │
└─────────┼───────────────────────────────────────────────────────┘
          │
          │ HTTPS (TLS 1.3)
          │
┌─────────▼───────────────────────────────────────────────────────┐
│                    Apache 2.4 (Web Server)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  mod_proxy (Reverse Proxy) + mod_wsgi + Let's Encrypt   │   │
│  └──────┬───────────────────────────────┬───────────────────┘   │
└─────────┼───────────────────────────────┼───────────────────────┘
          │                               │
          │                               │
┌─────────▼───────────────┐   ┌───────▼──────────────────────────┐
│   Next.js 14 Frontend   │   │      Flask 3.0 Backend           │
│  ┌──────────────────┐   │   │  ┌────────────────────────────┐  │
│  │  App Router      │   │   │  │  Blueprint Routes          │  │
│  │  - SSR/SSG       │   │   │  │  - /api/v1/auth            │  │
│  │  - Client Comp.  │   │   │  │  - /api/v1/nfts            │  │
│  └──────────────────┘   │   │  │  - /api/v1/products        │  │
│  ┌──────────────────┐   │   │  │  - /api/v1/orders          │  │
│  │  State (Zustand) │   │   │  │  - /api/v1/payments        │  │
│  └──────────────────┘   │   │  └────────────────────────────┘  │
│  ┌──────────────────┐   │   │  ┌────────────────────────────┐  │
│  │  @mysten/dapp-kit│   │   │  │  Service Layer             │  │
│  │  @stripe/react   │   │   │  │  - AuthService             │  │
│  └──────────────────┘   │   │  │  - NFTService              │  │
└─────────────────────────┘   │  │  - OrderService            │  │
                              │  │  - PaymentService          │  │
                              │  └────────────────────────────┘  │
                              │  ┌────────────────────────────┐  │
                              │  │  Repository Layer          │  │
                              │  │  - UserRepository          │  │
                              │  │  - NFTRepository           │  │
                              │  │  - ProductRepository       │  │
                              │  │  - OrderRepository         │  │
                              │  └────────┬───────────────────┘  │
                              └───────────┼──────────────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
          ┌─────────▼─────────┐  ┌────────▼────────────────────────┐
          │   MySQL 8.0       │  │  Background Task Manager        │
          │  ┌─────────────┐  │  │  (Python threading/asyncio)     │
          │  │ users       │  │  │  ┌───────────────────────────┐  │
          │  │ wallets     │  │  │  │ NFT Mint Tasks            │  │
          │  │ nft_mints   │  │  │  │ - ThreadPoolExecutor      │  │
          │  │ products    │  │  │  │ - Task Status in DB       │  │
          │  │ orders      │  │  │  └───────────────────────────┘  │
          │  │ payments    │  │  └─────────────────┬───────────────┘
          │  │ task_queue  │  │                    │
          │  └─────────────┘  │                    │
          └───────────────────┘                    │
                                                                │
                              ┌─────────────────────────────────▼────────┐
                              │         Sui Blockchain Network            │
                              │  ┌────────────────────────────────────┐  │
                              │  │  Move Smart Contract               │  │
                              │  │  - NFT Minting Module              │  │
                              │  │  - Sponsored Transaction           │  │
                              │  └────────────────────────────────────┘  │
                              └──────────────────────────────────────────┘
                              
                              ┌──────────────────────────────────────────┐
                              │         Stripe Payment API               │
                              │  - Payment Intent                        │
                              │  - Webhook Handler                       │
                              └──────────────────────────────────────────┘
```

### レイヤー構造

#### 1. Presentation Layer (Frontend)
- Next.js 14 App Router によるサーバーサイドレンダリング
- Zustand によるクライアント状態管理
- Tailwind CSS によるレスポンシブ UI

#### 2. API Layer (Backend)
- Flask Blueprint による RESTful API
- JWT 認証ミドルウェア
- レート制限とセキュリティミドルウェア

#### 3. Business Logic Layer
- Service クラスによるビジネスロジックのカプセル化
- トランザクション管理
- エラーハンドリング

#### 4. Data Access Layer
- Repository パターンによる抽象化
- SQLAlchemy ORM
- データベース接続プーリング

#### 5. Infrastructure Layer
- Python threading/asyncio による非同期タスク処理
- データベースベースのタスクキュー管理
- 外部 API 統合（Sui, Stripe, Google OAuth）

## Components and Interfaces

### Frontend Components

#### 1. Authentication Components

**LoginButton.tsx**
```typescript
interface LoginButtonProps {
  onSuccess: (token: string) => void;
}
```
- Google OAuth フローを開始
- JWT トークンを受信して保存

**WalletDisplay.tsx**
```typescript
interface WalletDisplayProps {
  address: string;
  nfts: NFT[];
}
```
- ユーザーのウォレットアドレスを表示
- 保有 NFT リストを表示

#### 2. Captive Portal Components

**CaptivePortalPage.tsx**
- WiFi 接続時の認証ページ
- Google ログインボタン
- 利用規約同意チェックボックス

**WelcomeScreen.tsx**
- 認証成功後の画面
- NFT 配布状況の表示
- EC ショップへの誘導

#### 3. NFT Components

**NFTCard.tsx**
```typescript
interface NFTCardProps {
  nft: {
    id: string;
    name: string;
    description: string;
    image_url: string;
    metadata: object;
  };
}
```
- NFT の詳細情報を表示
- 画像とメタデータの表示

**NFTGallery.tsx**
- ユーザーの NFT コレクションをグリッド表示
- フィルタリングとソート機能

#### 4. E-Commerce Components

**ProductList.tsx**
```typescript
interface ProductListProps {
  products: Product[];
  requiredNFT?: string;
}
```
- 商品一覧の表示
- NFT 保有状態による表示制御

**ProductCard.tsx**
```typescript
interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: string) => void;
}
```
- 商品の詳細情報
- カートへの追加ボタン

**ShoppingCart.tsx**
```typescript
interface ShoppingCartProps {
  items: CartItem[];
  onCheckout: () => void;
}
```
- カート内商品の表示
- 合計金額の計算
- チェックアウトボタン

**CheckoutForm.tsx**
```typescript
interface CheckoutFormProps {
  amount: number;
  onSuccess: (orderId: string) => void;
}
```
- Stripe Elements による決済フォーム
- NFT 保有確認
- 注文確定処理

#### 5. State Management (Zustand)

**authStore.ts**
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  login: (token: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}
```

**cartStore.ts**
```typescript
interface CartState {
  items: CartItem[];
  addItem: (product: Product, quantity: number) => void;
  removeItem: (productId: string) => void;
  clearCart: () => void;
  total: number;
}
```

**nftStore.ts**
```typescript
interface NFTState {
  nfts: NFT[];
  loading: boolean;
  fetchNFTs: (walletAddress: string) => Promise<void>;
  refreshNFTs: () => Promise<void>;
}
```

### Backend Components

#### 1. API Blueprints

**auth_blueprint.py**
- `POST /api/v1/auth/google` - Google OAuth 認証
- `POST /api/v1/auth/refresh` - トークンリフレッシュ
- `GET /api/v1/auth/me` - 現在のユーザー情報取得

**nft_blueprint.py**
- `GET /api/v1/nfts` - ユーザーの NFT 一覧取得
- `POST /api/v1/nfts/mint` - NFT 発行リクエスト
- `GET /api/v1/nfts/{id}` - NFT 詳細取得
- `GET /api/v1/nfts/status/{task_id}` - NFT 発行状態確認

**product_blueprint.py**
- `GET /api/v1/products` - 商品一覧取得
- `GET /api/v1/products/{id}` - 商品詳細取得
- `POST /api/v1/products` - 商品作成（管理者のみ）
- `PUT /api/v1/products/{id}` - 商品更新（管理者のみ）
- `DELETE /api/v1/products/{id}` - 商品削除（管理者のみ）

**order_blueprint.py**
- `POST /api/v1/orders` - 注文作成
- `GET /api/v1/orders` - ユーザーの注文履歴取得
- `GET /api/v1/orders/{id}` - 注文詳細取得

**payment_blueprint.py**
- `POST /api/v1/payments/intent` - Stripe Payment Intent 作成
- `POST /api/v1/payments/webhook` - Stripe Webhook ハンドラー
- `GET /api/v1/payments/{id}` - 決済情報取得

**wifi_blueprint.py**
- `POST /api/v1/wifi/connect` - WiFi 接続セッション作成
- `GET /api/v1/wifi/sessions` - WiFi セッション履歴取得

#### 2. Service Layer

**AuthService**
```python
class AuthService:
    def __init__(self, user_repo: UserRepository, wallet_repo: WalletRepository):
        pass
    
    def authenticate_google(self, id_token: str) -> Tuple[User, str]:
        """Google OAuth トークンを検証してユーザーを認証"""
        pass
    
    def create_jwt_token(self, user_id: str) -> str:
        """JWT アクセストークンを生成"""
        pass
    
    def verify_jwt_token(self, token: str) -> dict:
        """JWT トークンを検証"""
        pass
```

**NFTService**
```python
class NFTService:
    def __init__(self, nft_repo: NFTRepository, task_manager: TaskManager):
        pass
    
    async def mint_nft(self, user_id: str, wallet_address: str) -> str:
        """NFT 発行タスクをキューに追加"""
        pass
    
    def get_user_nfts(self, wallet_address: str) -> List[NFT]:
        """ユーザーの NFT を取得"""
        pass
    
    def verify_nft_ownership(self, wallet_address: str, nft_id: str) -> bool:
        """NFT 保有を確認"""
        pass
```

**OrderService**
```python
class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        pass
    
    def create_order(self, user_id: str, items: List[dict]) -> Order:
        """注文を作成"""
        pass
    
    def validate_nft_requirements(self, user_id: str, product_ids: List[str]) -> bool:
        """商品購入に必要な NFT を確認"""
        pass
    
    def update_order_status(self, order_id: str, status: str) -> Order:
        """注文ステータスを更新"""
        pass
```

**PaymentService**
```python
class PaymentService:
    def __init__(self, payment_repo: PaymentRepository, stripe_client):
        pass
    
    def create_payment_intent(self, order_id: str, amount: int) -> dict:
        """Stripe Payment Intent を作成"""
        pass
    
    def handle_webhook(self, payload: dict, signature: str) -> None:
        """Stripe Webhook を処理"""
        pass
    
    def process_successful_payment(self, payment_intent_id: str) -> None:
        """決済成功時の処理"""
        pass
```

**WalletService**
```python
class WalletService:
    def __init__(self, wallet_repo: WalletRepository, sui_client):
        pass
    
    def create_wallet(self, user_id: str) -> Wallet:
        """新しい XRPL ウォレットを生成"""
        pass
    
    def get_wallet_balance(self, address: str) -> int:
        """ウォレット残高を取得"""
        pass
```

#### 3. Repository Layer

**UserRepository**
```python
class UserRepository:
    def create(self, email: str, google_id: str, name: str) -> User:
        pass
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    def find_by_google_id(self, google_id: str) -> Optional[User]:
        pass
    
    def update(self, user_id: str, **kwargs) -> User:
        pass
```

**NFTRepository**
```python
class NFTRepository:
    def create(self, user_id: str, wallet_address: str, nft_data: dict) -> NFTMint:
        pass
    
    def find_by_wallet(self, wallet_address: str) -> List[NFTMint]:
        pass
    
    def find_by_id(self, nft_id: str) -> Optional[NFTMint]:
        pass
    
    def update_status(self, nft_id: str, status: str) -> NFTMint:
        pass
```

**ProductRepository**
```python
class ProductRepository:
    def create(self, name: str, price: int, **kwargs) -> Product:
        pass
    
    def find_all(self, filters: dict = None) -> List[Product]:
        pass
    
    def find_by_id(self, product_id: str) -> Optional[Product]:
        pass
    
    def update(self, product_id: str, **kwargs) -> Product:
        pass
    
    def delete(self, product_id: str) -> bool:
        pass
```

**OrderRepository**
```python
class OrderRepository:
    def create(self, user_id: str, total_amount: int) -> Order:
        pass
    
    def find_by_user(self, user_id: str) -> List[Order]:
        pass
    
    def find_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    def update_status(self, order_id: str, status: str) -> Order:
        pass
```

#### 4. Background Task Manager

**TaskManager**
```python
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any
import uuid

class TaskManager:
    def __init__(self, max_workers: int = 5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_repo = TaskRepository()
    
    def submit_task(self, func: Callable, *args, **kwargs) -> str:
        """タスクをキューに追加"""
        task_id = str(uuid.uuid4())
        self.task_repo.create(task_id, 'pending')
        
        future = self.executor.submit(self._execute_task, task_id, func, *args, **kwargs)
        return task_id
    
    def _execute_task(self, task_id: str, func: Callable, *args, **kwargs) -> Any:
        """タスクを実行"""
        try:
            self.task_repo.update_status(task_id, 'running')
            result = func(*args, **kwargs)
            self.task_repo.update_status(task_id, 'completed', result=result)
            return result
        except Exception as e:
            self.task_repo.update_status(task_id, 'failed', error=str(e))
            raise
    
    def get_task_status(self, task_id: str) -> dict:
        """タスクの状態を取得"""
        return self.task_repo.find_by_id(task_id)
```

## Data Models

### Database Schema

#### users テーブル
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_google_id (google_id),
    INDEX idx_email (email)
);
```

#### wallets テーブル
```sql
CREATE TABLE wallets (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    address VARCHAR(255) UNIQUE NOT NULL,
    private_key_encrypted TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_address (address)
);
```

#### nft_mints テーブル
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
    INDEX idx_wallet_address (wallet_address),
    INDEX idx_status (status)
);
```

#### products テーブル
```sql
CREATE TABLE products (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INT NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    image_url VARCHAR(500),
    required_nft_id VARCHAR(36),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_is_active (is_active),
    INDEX idx_required_nft (required_nft_id)
);
```

#### orders テーブル
```sql
CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    total_amount INT NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);
```

#### order_items テーブル
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
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_order_id (order_id)
);
```

#### payments テーブル
```sql
CREATE TABLE payments (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    stripe_payment_intent_id VARCHAR(255) UNIQUE NOT NULL,
    amount INT NOT NULL,
    currency VARCHAR(3) DEFAULT 'jpy',
    status ENUM('pending', 'processing', 'succeeded', 'failed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id),
    INDEX idx_stripe_payment_intent_id (stripe_payment_intent_id)
);
```

#### wifi_sessions テーブル
```sql
CREATE TABLE wifi_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    mac_address VARCHAR(17),
    ip_address VARCHAR(45),
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    disconnected_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_mac_address (mac_address)
);
```

#### task_queue テーブル
```sql
CREATE TABLE task_queue (
    id VARCHAR(36) PRIMARY KEY,
    task_type VARCHAR(50) NOT NULL,
    status ENUM('pending', 'running', 'completed', 'failed') DEFAULT 'pending',
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

### SQLAlchemy Models

**models/user.py**
```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    google_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    wallets = relationship('Wallet', back_populates='user', cascade='all, delete-orphan')
    nft_mints = relationship('NFTMint', back_populates='user', cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')
    wifi_sessions = relationship('WiFiSession', back_populates='user')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

## Error Handling

### エラー分類

#### 1. クライアントエラー (4xx)
- `400 Bad Request`: 不正なリクエストパラメータ
- `401 Unauthorized`: 認証失敗
- `403 Forbidden`: 権限不足
- `404 Not Found`: リソースが見つからない
- `409 Conflict`: リソースの競合（在庫不足など）
- `429 Too Many Requests`: レート制限超過

#### 2. サーバーエラー (5xx)
- `500 Internal Server Error`: 予期しないサーバーエラー
- `502 Bad Gateway`: 外部 API エラー
- `503 Service Unavailable`: サービス一時停止

### エラーレスポンス形式

```json
{
  "status": "error",
  "error": "エラーメッセージ",
  "code": 400,
  "details": {
    "field": "email",
    "message": "無効なメールアドレス形式です"
  }
}
```

### エラーハンドリング戦略

#### Backend (Flask)
```python
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, ValidationError):
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 400
        }), 400
    
    if isinstance(e, AuthenticationError):
        return jsonify({
            'status': 'error',
            'error': 'Authentication failed',
            'code': 401
        }), 401
    
    # Log unexpected errors
    app.logger.error(f'Unexpected error: {str(e)}', exc_info=True)
    
    return jsonify({
        'status': 'error',
        'error': 'Internal server error',
        'code': 500
    }), 500
```

#### Frontend (Next.js)
```typescript
// lib/api-client.ts
export class APIError extends Error {
  constructor(
    public status: number,
    public code: number,
    message: string,
    public details?: any
  ) {
    super(message);
  }
}

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new APIError(
        response.status,
        data.code,
        data.error,
        data.details
      );
    }
    
    return data.data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError(0, 0, 'Network error');
  }
}
```

### リトライ戦略

#### NFT 発行タスク
```python
def mint_nft_with_retry(wallet_address: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            result = sui_client.mint_nft(wallet_address)
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

## Testing Strategy

### Backend Testing

#### 1. Unit Tests (pytest)
```python
# tests/test_auth_service.py
def test_authenticate_google_new_user(mock_google_client, auth_service):
    """新規ユーザーの Google 認証をテスト"""
    id_token = "mock_token"
    user, jwt_token = auth_service.authenticate_google(id_token)
    
    assert user.email == "test@example.com"
    assert jwt_token is not None

# tests/test_nft_service.py
def test_mint_nft_creates_task(nft_service, mock_task_manager):
    """NFT 発行タスクが作成されることをテスト"""
    task_id = nft_service.mint_nft("user_id", "wallet_address")
    
    assert task_id is not None
    mock_task_manager.submit_task.assert_called_once()
```

#### 2. Integration Tests
```python
# tests/integration/test_order_flow.py
def test_complete_order_flow(client, db_session):
    """注文から決済までの完全なフローをテスト"""
    # 1. ユーザー作成
    # 2. 商品作成
    # 3. 注文作成
    # 4. 決済処理
    # 5. 注文ステータス確認
```

#### 3. API Tests
```python
# tests/api/test_products_api.py
def test_get_products(client, auth_headers):
    """商品一覧 API をテスト"""
    response = client.get('/api/v1/products', headers=auth_headers)
    
    assert response.status_code == 200
    assert 'data' in response.json
```

### Frontend Testing

#### 1. Component Tests (Jest + React Testing Library)
```typescript
// __tests__/components/ProductCard.test.tsx
describe('ProductCard', () => {
  it('商品情報を正しく表示する', () => {
    const product = {
      id: '1',
      name: 'Test Product',
      price: 1000,
    };
    
    render(<ProductCard product={product} onAddToCart={jest.fn()} />);
    
    expect(screen.getByText('Test Product')).toBeInTheDocument();
    expect(screen.getByText('¥1,000')).toBeInTheDocument();
  });
});
```

#### 2. Integration Tests
```typescript
// __tests__/flows/checkout.test.tsx
describe('Checkout Flow', () => {
  it('チェックアウトプロセスが正常に完了する', async () => {
    // 1. カートに商品追加
    // 2. チェックアウトページに遷移
    // 3. 決済情報入力
    // 4. 注文確定
  });
});
```

### Test Coverage Goals
- Backend: 最低 80% のコードカバレッジ
- Frontend: 主要コンポーネントとフローのカバレッジ
- E2E: 重要なユーザーフローのカバレッジ

### Mocking Strategy
- 外部 API (Sui, Stripe, Google OAuth) はモック化
- データベースはテスト用の in-memory DB または専用テスト DB を使用
- 非同期タスクはモック化してテストを高速化
