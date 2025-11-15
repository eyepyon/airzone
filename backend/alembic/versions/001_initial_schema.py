"""initial_schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables for the Airzone application."""
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('google_id', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_google_id', 'users', ['google_id'])
    op.create_index('idx_email', 'users', ['email'])
    
    # Create wallets table
    op.create_table(
        'wallets',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('address', sa.String(255), nullable=False, unique=True),
        sa.Column('private_key_encrypted', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_user_id', 'wallets', ['user_id'])
    op.create_index('idx_address', 'wallets', ['address'])
    
    # Create nft_mints table
    op.create_table(
        'nft_mints',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('wallet_address', sa.String(255), nullable=False),
        sa.Column('nft_object_id', sa.String(255), nullable=True),
        sa.Column('transaction_digest', sa.String(255), nullable=True),
        sa.Column('status', sa.Enum('pending', 'minting', 'completed', 'failed', name='nftmintstatus'), nullable=False),
        sa.Column('nft_metadata', sa.JSON(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_nft_user_id', 'nft_mints', ['user_id'])
    op.create_index('idx_wallet_address', 'nft_mints', ['wallet_address'])
    op.create_index('idx_status', 'nft_mints', ['status'])
    
    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('stock_quantity', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('image_url', sa.String(500), nullable=True),
        sa.Column('required_nft_id', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_is_active', 'products', ['is_active'])
    op.create_index('idx_required_nft', 'products', ['required_nft_id'])
    
    # Create orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('total_amount', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'processing', 'completed', 'failed', 'cancelled', name='orderstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_order_user_id', 'orders', ['user_id'])
    op.create_index('idx_order_status', 'orders', ['status'])
    
    # Create order_items table
    op.create_table(
        'order_items',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('order_id', sa.String(36), nullable=False),
        sa.Column('product_id', sa.String(36), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Integer(), nullable=False),
        sa.Column('subtotal', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_order_id', 'order_items', ['order_id'])
    
    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('order_id', sa.String(36), nullable=False),
        sa.Column('stripe_payment_intent_id', sa.String(255), nullable=False, unique=True),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False, server_default='jpy'),
        sa.Column('status', sa.Enum('pending', 'processing', 'succeeded', 'failed', 'cancelled', name='paymentstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_payment_order_id', 'payments', ['order_id'])
    op.create_index('idx_stripe_payment_intent_id', 'payments', ['stripe_payment_intent_id'])
    
    # Create wifi_sessions table
    op.create_table(
        'wifi_sessions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=True),
        sa.Column('mac_address', sa.String(17), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('connected_at', sa.DateTime(), nullable=False),
        sa.Column('disconnected_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_wifi_user_id', 'wifi_sessions', ['user_id'])
    op.create_index('idx_mac_address', 'wifi_sessions', ['mac_address'])
    
    # Create task_queue table
    op.create_table(
        'task_queue',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('task_type', sa.String(50), nullable=False),
        sa.Column('status', sa.Enum('pending', 'running', 'completed', 'failed', name='taskstatus'), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('result', sa.JSON(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('max_retries', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_task_status', 'task_queue', ['status'])
    op.create_index('idx_task_type', 'task_queue', ['task_type'])


def downgrade() -> None:
    """Drop all tables."""
    
    # Drop tables in reverse order to respect foreign key constraints
    op.drop_table('task_queue')
    op.drop_table('wifi_sessions')
    op.drop_table('payments')
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_table('nft_mints')
    op.drop_table('wallets')
    op.drop_table('users')
