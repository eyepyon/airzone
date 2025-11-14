import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import config

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize CORS
CORS(app, 
     origins=app.config['CORS_ORIGINS'],
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Initialize JWT
jwt = JWTManager(app)

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
        db.close()


# JWT Error Handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired JWT tokens"""
    return jsonify({
        'status': 'error',
        'error': 'Token has expired',
        'code': 401
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid JWT tokens"""
    return jsonify({
        'status': 'error',
        'error': 'Invalid token',
        'code': 401
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing JWT tokens"""
    return jsonify({
        'status': 'error',
        'error': 'Authorization token is missing',
        'code': 401
    }), 401


# Global Error Handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors"""
    return jsonify({
        'status': 'error',
        'error': 'Bad request',
        'code': 400
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 Unauthorized errors"""
    return jsonify({
        'status': 'error',
        'error': 'Unauthorized',
        'code': 401
    }), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors"""
    return jsonify({
        'status': 'error',
        'error': 'Forbidden',
        'code': 403
    }), 403


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return jsonify({
        'status': 'error',
        'error': 'Resource not found',
        'code': 404
    }), 404


@app.errorhandler(409)
def conflict(error):
    """Handle 409 Conflict errors"""
    return jsonify({
        'status': 'error',
        'error': 'Resource conflict',
        'code': 409
    }), 409


@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Handle 429 Too Many Requests errors"""
    return jsonify({
        'status': 'error',
        'error': 'Rate limit exceeded',
        'code': 429
    }), 429


@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 Internal Server Error"""
    app.logger.error(f'Internal server error: {str(error)}', exc_info=True)
    return jsonify({
        'status': 'error',
        'error': 'Internal server error',
        'code': 500
    }), 500


@app.errorhandler(502)
def bad_gateway(error):
    """Handle 502 Bad Gateway errors"""
    return jsonify({
        'status': 'error',
        'error': 'Bad gateway - external service error',
        'code': 502
    }), 502


@app.errorhandler(503)
def service_unavailable(error):
    """Handle 503 Service Unavailable errors"""
    return jsonify({
        'status': 'error',
        'error': 'Service temporarily unavailable',
        'code': 503
    }), 503


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


# Blueprint registration will be added here as they are implemented
# Example:
# from routes.auth import auth_blueprint
# app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
