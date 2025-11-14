# Design Document

## Overview

Airzone（https://airz.one/）は、OpenNDS キャプティブポータルと Sui ブロックチェーンを統合した、WiFi 接続トリガー型の NFT 配布・EC ショッププラットフォームです。

### 主要機能
- Google OAuth による認証と自動ウォレット生成
- OpenNDS キャプティブポータル統合
- Sui ブロックチェーン上での NFT 自動発行
- NFT ゲート付き EC ショップ
- Stripe 決済統合
- 非同期タスク処理

### 技術スタック概要
- **Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Backend**: Flask 3.0 + Python 3.11+ + SQLAlchemy
- **Database**: MySQL 8.0
- **Cache/Queue**: Redis + Celery
- **Blockchain**: Sui (Move)
- **Payment**: Stripe
- **Infrastructure**: Docker + Apache 2.4

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
          ┌─────────▼─────────┐  ┌────────▼────────┐  ┌────────▼────────┐
          │   MySQL 8.0       │  │  Redis Cache    │  │  Celery Worker  │
          │  ┌─────────────┐  │  │  - Sessions     │  │  ┌───────────┐  │
          │  │ users       │  │  │  - Task Queue   │  │  │ NFT Mint  │  │
          │  │ wallets     │  │  │  - Rate Limit   │  │  │ Tasks     │  │
          │  │ nft_mints   │  │  └─────────────────┘  │  └───────────┘  │
          │  │ products    │  │                       └────────┬────────┘
          │  │ orders      │  │                                │
          │  │ payments    │  │                                │
          │  └─────────────┘  │                                │
          └───────────────────┘                                │
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
- Redis キャッシュ
- Celery 非同期タスク
- 外部 API 統合（Sui, Stripe, Google OAuth）

## Components and Interfaces

### Frontend Components

#### 1. Authentication Components
