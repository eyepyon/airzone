import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import config
from logging_config import setup_logging
from error_handlers import register_error_handlers
from middleware.security import setup_security_headers
from middleware.rate_limit import setup_rate_limiting

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Setup structured logging
setup_logging(app)

# Initialize CORS
CORS(app, 
     origins=app.config['CORS_ORIGINS'],
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization', 'X-CSRF-Token'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Initialize JWT
jwt = JWTManager(app)

# Setup security headers
setup_security_headers(app)

# Setup rate limiting
if app.config.get('RATELIMIT_ENABLED', True):
    setup_rate_limiting(app)

# Register error handlers
register_error_handlers(app)

# Initialize Database
engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    pool_size=app.config['SQLALCHEMY_POOL_SIZE'],
    pool_recycle=app.config['SQLALCHEMY_POOL_RECYCLE'],
    pool_pre_ping=app.config['SQLALCHEMY_POOL_PRE_PING'],
    echo=app.config['SQLALCHEMY_ECHO']
)

# Create session factory
SessionLocal = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))


# Request logging middleware
@app.before_request
def log_request():
    """Log incoming requests"""
    from flask import request
    app.logger.info(
        f"Incoming request: {request.method} {request.path}",
        extra={
            'request_method': request.method,
            'request_path': request.path,
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
    )


@app.after_request
def log_response(response):
    """Log outgoing responses"""
    from flask import request
    app.logger.info(
        f"Response: {response.status_code}",
        extra={
            'request_method': request.method,
            'request_path': request.path,
            'status_code': response.status_code
        }
    )
    return response


# Database session management
@app.before_request
def create_session():
    """Create database session before each request"""
    from flask import g
    g.db = SessionLocal()


@app.teardown_request
def remove_session(exception=None):
    """Remove database session after each request"""
    from flask import g
    db = g.pop('db', None)
    if db is not None:
        if exception:
            db.rollback()
            app.logger.error(
                "Database session rolled back due to exception",
                extra={'exception': str(exception)}
            )
        db.close()


# JWT Error Handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired JWT tokens"""
    app.logger.warning(
        "Expired JWT token",
        extra={
            'jwt_payload': jwt_payload,
            'request_path': None  # Will be added by request context if available
        }
    )
    return jsonify({
        'status': 'error',
        'error': 'Token has expired',
        'code': 401
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid JWT tokens"""
    app.logger.warning(
        f"Invalid JWT token: {error}",
        extra={'error': str(error)}
    )
    return jsonify({
        'status': 'error',
        'error': 'Invalid token',
        'code': 401
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing JWT tokens"""
    app.logger.info(
        f"Missing JWT token: {error}",
        extra={'error': str(error)}
    )
    return jsonify({
        'status': 'error',
        'error': 'Authorization token is missing',
        'code': 401
    }), 401


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'data': {
            'service': 'airzone-api',
            'version': '1.0.0',
            'environment': env
        }
    }), 200


# API version endpoint
@app.route('/api/v1', methods=['GET'])
def api_version():
    """API version endpoint"""
    return jsonify({
        'status': 'success',
        'data': {
            'version': 'v1',
            'endpoints': {
                'auth': '/api/v1/auth',
                'nfts': '/api/v1/nfts',
                'products': '/api/v1/products',
                'orders': '/api/v1/orders',
                'payments': '/api/v1/payments',
                'wifi': '/api/v1/wifi'
            }
        }
    }), 200


# Blueprint registration
# All blueprints are now implemented

# Register auth blueprint
from routes.auth import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

# Register NFT blueprint
from routes.nft import nft_blueprint
app.register_blueprint(nft_blueprint, url_prefix='/api/v1/nfts')

# Register product blueprint
from routes.product import product_blueprint
app.register_blueprint(product_blueprint, url_prefix='/api/v1/products')

# Register order blueprint
from routes.order import order_blueprint
app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders')

# Register payment blueprint
from routes.payment import payment_blueprint
app.register_blueprint(payment_blueprint, url_prefix='/api/v1/payments')

# Register wifi blueprint
from routes.wifi import wifi_blueprint
app.register_blueprint(wifi_blueprint, url_prefix='/api/v1/wifi')

# Register download blueprint
from routes.download import download_blueprint
app.register_blueprint(download_blueprint, url_prefix='/api/v1/downloads')

# Register wallet blueprint
from routes.wallet import wallet_blueprint
app.register_blueprint(wallet_blueprint, url_prefix='/api/v1/wallet')

# Register referral blueprint
from routes.referral import referral_blueprint
app.register_blueprint(referral_blueprint, url_prefix='/api/v1/referral')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
