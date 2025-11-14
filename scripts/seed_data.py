"""
Seed data script for populating the database with initial test data.
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models import Product
from config import config

# Load environment variables
load_dotenv()


def get_db_session():
    """Create and return a database session."""
    env = os.getenv('FLASK_ENV', 'development')
    db_url = config[env].SQLALCHEMY_DATABASE_URI
    
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()


def seed_products(session):
    """
    Seed the database with test product data.
    
    Args:
        session: SQLAlchemy session
    """
    print("Seeding products...")
    
    # Check if products already exist
    existing_count = session.query(Product).count()
    if existing_count > 0:
        print(f"⚠ Database already contains {existing_count} products. Skipping seed.")
        return
    
    # Test products
    products = [
        {
            'name': 'オリジナルTシャツ',
            'description': 'Airzone限定デザインのオリジナルTシャツ。高品質なコットン100%素材を使用。',
            'price': 3500,  # 3,500円
            'stock_quantity': 50,
            'image_url': 'https://example.com/images/tshirt.jpg',
            'required_nft_id': None,  # No NFT required
            'is_active': True
        },
        {
            'name': 'プレミアムコーヒー豆セット',
            'description': '厳選されたスペシャルティコーヒー豆3種類のセット。NFT保有者限定商品。',
            'price': 5000,  # 5,000円
            'stock_quantity': 30,
            'image_url': 'https://example.com/images/coffee.jpg',
            'required_nft_id': 'nft_required',  # Requires NFT
            'is_active': True
        },
        {
            'name': 'ステッカーセット',
            'description': 'Airzoneロゴ入りステッカー5枚セット。防水加工済み。',
            'price': 800,  # 800円
            'stock_quantity': 100,
            'image_url': 'https://example.com/images/stickers.jpg',
            'required_nft_id': None,
            'is_active': True
        },
        {
            'name': 'VIP会員限定トートバッグ',
            'description': 'NFT保有者のみ購入可能な限定トートバッグ。大容量で普段使いに最適。',
            'price': 4200,  # 4,200円
            'stock_quantity': 20,
            'image_url': 'https://example.com/images/tote.jpg',
            'required_nft_id': 'nft_required',
            'is_active': True
        },
        {
            'name': 'オリジナルマグカップ',
            'description': 'Airzoneロゴ入りセラミックマグカップ。電子レンジ・食洗機対応。',
            'price': 2000,  # 2,000円
            'stock_quantity': 75,
            'image_url': 'https://example.com/images/mug.jpg',
            'required_nft_id': None,
            'is_active': True
        },
        {
            'name': 'プレミアムメンバーシップ（1年間）',
            'description': 'NFT保有者限定の年間プレミアムメンバーシップ。特別イベントへの招待や限定商品の先行購入権を含む。',
            'price': 15000,  # 15,000円
            'stock_quantity': 10,
            'image_url': 'https://example.com/images/membership.jpg',
            'required_nft_id': 'nft_required',
            'is_active': True
        },
        {
            'name': 'ワイヤレスイヤホン',
            'description': '高音質Bluetooth 5.0対応ワイヤレスイヤホン。ノイズキャンセリング機能付き。',
            'price': 8900,  # 8,900円
            'stock_quantity': 25,
            'image_url': 'https://example.com/images/earphones.jpg',
            'required_nft_id': None,
            'is_active': True
        },
        {
            'name': 'エコバッグ',
            'description': '環境に優しいリサイクル素材を使用したエコバッグ。コンパクトに折りたためます。',
            'price': 1500,  # 1,500円
            'stock_quantity': 60,
            'image_url': 'https://example.com/images/ecobag.jpg',
            'required_nft_id': None,
            'is_active': True
        },
    ]
    
    # Add products to session
    for product_data in products:
        product = Product(**product_data)
        session.add(product)
        print(f"  + {product_data['name']} - ¥{product_data['price']:,}")
    
    # Commit changes
    session.commit()
    print(f"✓ Successfully seeded {len(products)} products")


def main():
    """Main function to run all seed operations."""
    print("=" * 60)
    print("Airzone Database Seeding")
    print("=" * 60)
    print()
    
    try:
        # Create database session
        session = get_db_session()
        
        # Seed data
        seed_products(session)
        
        print("\n✓ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error during database seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if 'session' in locals():
            session.close()


if __name__ == '__main__':
    main()
