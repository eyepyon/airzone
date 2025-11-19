// Type definitions for the Airzone application

// ============================================================================
// Core Domain Types
// ============================================================================

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

export type ProductType = 'nft' | 'goods' | 'event_ticket';
export type DeliveryMethod = 'pickup' | 'shipping' | 'digital';
export type PurchaseRestriction = 'onsite_only' | 'onsite_and_referral' | 'nft_holders' | 'public';

export interface Product {
  id: string;
  name: string;
  description: string | null;
  price: number;
  stock_quantity: number;
  image_url: string | null;
  product_type?: ProductType; // Optional for backward compatibility
  delivery_method?: DeliveryMethod | null; // Optional for backward compatibility
  purchase_restriction?: PurchaseRestriction; // Optional for backward compatibility
  required_nft_id?: string | null;
  is_active: boolean;
  event_date?: string | null; // For event tickets
  venue?: string | null; // For event tickets
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
  payment?: Payment;
}

export interface ShippingAddress {
  recipient_name: string;
  postal_code: string;
  prefecture: string;
  city: string;
  address_line1: string;
  address_line2?: string;
  phone_number: string;
  delivery_time_preference?: string;
}

export interface OrderItem {
  id: string;
  order_id: string;
  product_id: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
  delivery_method: DeliveryMethod | null;
  shipping_address: ShippingAddress | null;
  pickup_qr_code: string | null;
  created_at: string;
  product?: Product;
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

export interface TaskQueue {
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

// ============================================================================
// Client-Side Types
// ============================================================================

export interface CartItem {
  product: Product;
  quantity: number;
}

// ============================================================================
// API Response Types
// ============================================================================

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

export interface RefreshTokenResponse {
  access_token: string;
}

export interface MintNFTResponse {
  task_id: string;
  status: string;
}

export interface NFTStatusResponse {
  task: TaskQueue;
  nft?: NFT;
}

export interface PaymentIntentResponse {
  client_secret: string;
  payment_intent_id: string;
}

export interface ProductListResponse {
  products: Product[];
  total: number;
}

export interface OrderListResponse {
  orders: Order[];
  total: number;
}

export interface NFTListResponse {
  nfts: NFT[];
  total: number;
}

export interface WiFiSessionResponse {
  session: WiFiSession;
}

export interface WiFiSessionListResponse {
  sessions: WiFiSession[];
  total: number;
}

// ============================================================================
// API Request Types
// ============================================================================

export interface GoogleAuthRequest {
  id_token: string;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface MintNFTRequest {
  wallet_address: string;
}

export interface CreateProductRequest {
  name: string;
  description?: string;
  price: number;
  stock_quantity: number;
  image_url?: string;
  required_nft_id?: string;
  is_active?: boolean;
}

export interface UpdateProductRequest {
  name?: string;
  description?: string;
  price?: number;
  stock_quantity?: number;
  image_url?: string;
  required_nft_id?: string;
  is_active?: boolean;
}

export interface CreateOrderRequest {
  items: {
    product_id: string;
    quantity: number;
    delivery_method?: DeliveryMethod;
    shipping_address?: ShippingAddress;
  }[];
}

export interface CreatePaymentIntentRequest {
  order_id: string;
}

export interface CreateWiFiSessionRequest {
  mac_address?: string;
  ip_address?: string;
}

// ============================================================================
// Utility Types
// ============================================================================

export type NFTStatus = NFT['status'];
export type OrderStatus = Order['status'];
export type PaymentStatus = Payment['status'];
export type TaskStatus = TaskQueue['status'];

export interface PaginationParams {
  page?: number;
  limit?: number;
}

export interface FilterParams {
  status?: string;
  is_active?: boolean;
  required_nft_id?: string;
}

export interface SortParams {
  sort_by?: string;
  order?: 'asc' | 'desc';
}

export interface QueryParams extends PaginationParams, FilterParams, SortParams {}

// ============================================================================
// Error Types
// ============================================================================

export class APIError extends Error {
  constructor(
    public status: number,
    public code: number,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// ============================================================================
// Component Props Types
// ============================================================================

export interface NFTCardProps {
  nft: NFT;
  onClick?: (nft: NFT) => void;
}

export interface ProductCardProps {
  product: Product;
  onAddToCart?: (product: Product) => void;
  showNFTRequirement?: boolean;
}

export interface OrderCardProps {
  order: Order;
  onClick?: (order: Order) => void;
}

export interface WalletDisplayProps {
  address: string;
  nfts: NFT[];
}

export interface LoginButtonProps {
  onSuccess?: (token: string) => void;
  onError?: (error: Error) => void;
}

export interface CheckoutFormProps {
  amount: number;
  orderId: string;
  onSuccess?: (orderId: string) => void;
  onError?: (error: Error) => void;
}

export interface ShoppingCartProps {
  items: CartItem[];
  onCheckout?: () => void;
  onRemoveItem?: (productId: string) => void;
  onUpdateQuantity?: (productId: string, quantity: number) => void;
}
