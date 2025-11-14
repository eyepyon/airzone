// Type definitions for the Airzone application

export interface User {
  id: string;
  email: string;
  name: string;
  google_id: string;
  created_at: string;
  updated_at: string;
}

export interface Wallet {
  id: string;
  user_id: string;
  address: string;
  created_at: string;
  updated_at: string;
}

export interface NFT {
  id: string;
  user_id: string;
  wallet_address: string;
  nft_object_id: string | null;
  transaction_digest: string | null;
  status: 'pending' | 'minting' | 'completed' | 'failed';
  metadata: Record<string, any>;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: string;
  name: string;
  description: string | null;
  price: number;
  stock_quantity: number;
  image_url: string | null;
  required_nft_id: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: string;
  user_id: string;
  total_amount: number;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled';
  created_at: string;
  updated_at: string;
  items?: OrderItem[];
}

export interface OrderItem {
  id: string;
  order_id: string;
  product_id: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
  created_at: string;
}

export interface Payment {
  id: string;
  order_id: string;
  stripe_payment_intent_id: string;
  amount: number;
  currency: string;
  status: 'pending' | 'processing' | 'succeeded' | 'failed' | 'cancelled';
  created_at: string;
  updated_at: string;
}

export interface WiFiSession {
  id: string;
  user_id: string | null;
  mac_address: string | null;
  ip_address: string | null;
  connected_at: string;
  disconnected_at: string | null;
  created_at: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

// API Response types
export interface APIResponse<T> {
  status: 'success' | 'error';
  data?: T;
  error?: string;
  code?: number;
  details?: any;
}

export interface AuthResponse {
  user: User;
  wallet: Wallet;
  access_token: string;
  refresh_token: string;
}

export interface TaskStatus {
  id: string;
  task_type: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  payload: Record<string, any>;
  result: Record<string, any> | null;
  error_message: string | null;
  retry_count: number;
  max_retries: number;
  created_at: string;
  updated_at: string;
}
