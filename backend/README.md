# Airzone Backend

Flask-based backend API for the Airzone NFT distribution and e-commerce platform.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python app.py
```

## Project Structure

```
backend/
├── app.py                 # Flask application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── exceptions.py          # Custom exception classes
├── models/                # SQLAlchemy models
├── repositories/          # Data access layer
├── services/              # Business logic layer
├── routes/                # API blueprints
├── clients/               # External API clients
├── middleware/            # Custom middleware
└── tasks/                 # Background tasks
```

## API Endpoints

- `/health` - Health check
- `/api/v1` - API version info
- `/api/v1/auth` - Authentication endpoints
- `/api/v1/nfts` - NFT management
- `/api/v1/products` - Product catalog
- `/api/v1/orders` - Order management
- `/api/v1/payments` - Payment processing
- `/api/v1/wifi` - WiFi session management

## Configuration

See `.env.example` for all available configuration options.

Key configurations:
- Database connection (MySQL)
- JWT authentication
- Google OAuth
- Stripe payments
- Sui blockchain
- CORS settings
