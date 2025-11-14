# Service Layer Implementation

This directory contains the business logic layer for the Airzone application. Each service encapsulates specific domain logic and coordinates between repositories, external clients, and other services.

## Implemented Services

### 1. AuthService (`auth_service.py`)
**Requirements: 1.1, 1.4, 1.5, 6.1**

Handles user authentication and JWT token management:
- Google OAuth authentication flow
- JWT access token generation (1 hour expiration)
- JWT refresh token generation (30 days expiration)
- Token verification and validation
- User session management

**Key Methods:**
- `authenticate_google(id_token)` - Authenticate with Google OAuth
- `create_access_token(user_id)` - Generate JWT access token
- `create_refresh_token(user_id)` - Generate JWT refresh token
- `verify_access_token(token)` - Verify and decode access token
- `refresh_access_token(refresh_token)` - Refresh expired access token
- `get_current_user(access_token)` - Get user info from token

### 2. WalletService (`wallet_service.py`)
**Requirements: 1.3, 6.2**

Manages Sui blockchain wallets:
- Automatic wallet generation for new users
- Private key encryption using Fernet symmetric encryption
- Secure private key storage and retrieval
- Wallet balance queries

**Key Methods:**
- `create_wallet(user_id)` - Generate new Sui wallet
- `get_user_wallet(user_id)` - Retrieve user's wallet
- `get_wallet_balance(user_id)` - Get SUI token balance
- `get_decrypted_private_key(user_id)` - Decrypt private key for transactions
- `ensure_user_has_wallet(user_id)` - Create wallet if doesn't exist

### 3. NFTService (`nft_service.py`)
**Requirements: 3.1, 3.2, 3.4, 3.5**

Handles NFT minting and ownership:
- Asynchronous NFT minting via task queue
- NFT ownership verification
- User NFT collection management
- Minting status tracking

**Key Methods:**
- `mint_nft(user_id, nft_name, nft_description, nft_image_url, metadata)` - Queue NFT mint
- `get_user_nfts(user_id, status, limit)` - Get user's NFT collection
- `get_mint_status(nft_id)` - Check minting progress
- `verify_nft_ownership(user_id, nft_object_id)` - Verify NFT ownership
- `has_completed_nft(user_id)` - Check if user has any completed NFT

### 4. ProductService (`product_service.py`)
**Requirements: 4.2, 4.3, 4.4, 4.5**

Manages e-commerce products:
- Product CRUD operations
- Stock management and reservation
- NFT requirement verification
- Product search and filtering

**Key Methods:**
- `create_product(name, price, ...)` - Create new product
- `get_product(product_id)` - Get product details
- `get_all_products(only_active, limit, offset)` - List products
- `update_product(product_id, **kwargs)` - Update product
- `delete_product(product_id)` - Deactivate product
- `check_stock_availability(product_id, quantity)` - Check stock
- `reserve_stock(product_id, quantity)` - Reserve stock for order
- `restore_stock(product_id, quantity)` - Restore stock on cancellation
- `verify_nft_requirement(user_id, product_id)` - Verify NFT ownership

### 5. OrderService (`order_service.py`)
**Requirements: 5.1, 5.2, 5.3, 5.4, 5.6, 5.7**

Manages order processing:
- Order creation with validation
- NFT requirement checking
- Stock reservation and restoration
- Order status management
- Order cancellation handling

**Key Methods:**
- `create_order(user_id, items)` - Create new order with validation
- `get_order(order_id)` - Get order with items
- `get_user_orders(user_id, status, limit)` - Get user's order history
- `update_order_status(order_id, status)` - Update order status
- `complete_order(order_id)` - Mark order as completed
- `fail_order(order_id)` - Fail order and restore stock
- `cancel_order(order_id)` - Cancel order and restore stock

### 6. PaymentService (`payment_service.py`)
**Requirements: 5.5, 5.6, 5.7**

Handles payment processing:
- Stripe Payment Intent creation
- Webhook signature verification
- Payment event processing
- Order completion on successful payment
- Stock restoration on payment failure

**Key Methods:**
- `create_payment_intent(order_id, customer_email)` - Create Stripe payment
- `handle_webhook(payload, signature_header)` - Process Stripe webhooks
- `get_payment(payment_id)` - Get payment details
- `get_order_payments(order_id)` - Get all payments for order
- `cancel_payment(payment_id)` - Cancel payment and restore stock

## Dependencies

All services depend on:
- SQLAlchemy Session for database operations
- Repository layer for data access
- External clients (Google, Sui, Stripe) for third-party integrations
- Task Manager for asynchronous operations

## Usage Example

```python
from sqlalchemy.orm import Session
from services.auth_service import AuthService
from services.wallet_service import WalletService
from clients.google_auth import GoogleAuthClient
from clients.sui_client import SuiClient

# Initialize services
db_session = Session()
google_client = GoogleAuthClient(client_id="...")
sui_client = SuiClient(network="testnet", sponsor_private_key="...")

auth_service = AuthService(
    db_session=db_session,
    google_client=google_client,
    jwt_secret="secret",
    jwt_access_expires=3600,
    jwt_refresh_expires=2592000
)

wallet_service = WalletService(
    db_session=db_session,
    sui_client=sui_client,
    encryption_key="encryption_key"
)

# Authenticate user
user_dict, access_token, refresh_token = auth_service.authenticate_google(id_token)

# Create wallet for user
wallet = wallet_service.create_wallet(user_dict['id'])
```

## Error Handling

All services implement consistent error handling:
- `ValueError` for validation errors and business logic violations
- `Exception` for unexpected errors
- Automatic database rollback on errors
- Comprehensive logging for debugging

## Testing

Services should be tested with:
- Unit tests for individual methods
- Integration tests for service interactions
- Mock external dependencies (Stripe, Sui, Google)
- Test database for data operations
