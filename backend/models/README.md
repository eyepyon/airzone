# Database Models

This directory contains all SQLAlchemy database models for the Airzone application.

## Models Overview

### Base Model (`base.py`)
- `BaseModel`: Abstract base class providing common fields (id, created_at, updated_at)
- `to_dict()`: Method to convert model instances to dictionaries
- `generate_uuid()`: Utility function for UUID generation

### User Management
- **User** (`user.py`): User accounts with Google OAuth authentication
- **Wallet** (`wallet.py`): Sui blockchain wallets associated with users

### NFT System
- **NFTMint** (`nft_mint.py`): NFT minting operations and status tracking

### E-Commerce
- **Product** (`product.py`): Products available for purchase
- **Order** (`order.py`): Customer orders
- **OrderItem** (`order.py`): Individual items within orders
- **Payment** (`payment.py`): Payment transactions via Stripe

### Infrastructure
- **WiFiSession** (`wifi_session.py`): WiFi captive portal connection sessions
- **TaskQueue** (`task_queue.py`): Background task management

## Model Relationships

```
User
├── wallets (1:N)
├── nft_mints (1:N)
├── orders (1:N)
└── wifi_sessions (1:N)

Order
├── order_items (1:N)
└── payments (1:N)

OrderItem
└── product (N:1)
```

## Database Initialization

To create all tables:
```bash
python init_db.py --env development
```

To drop and recreate tables:
```bash
python init_db.py --env development --drop
```

## Migrations

Alembic is configured for database migrations. See `alembic/README` for usage instructions.

## Field Conventions

- All tables use UUID (string) primary keys
- All tables have `created_at` and `updated_at` timestamps
- Foreign keys follow the pattern `{table}_id`
- Enum fields are used for status tracking
- Sensitive data (private keys) are excluded from `to_dict()` output
