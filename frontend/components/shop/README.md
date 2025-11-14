# Shop Components

This directory contains all e-commerce shop-related components for the Airzone application.

## Components

### ProductCard
**File:** `ProductCard.tsx`

Displays a single product with image, name, description, price, and stock information.

**Features:**
- Product image display with fallback
- NFT requirement indicator with lock overlay
- Stock availability display
- Add to cart button with state management
- Responsive design

**Props:**
- `product`: Product object
- `onAddToCart`: Callback when adding to cart
- `showNFTRequirement`: Show NFT requirement badge (default: true)
- `hasRequiredNFT`: Whether user has required NFT (default: true)

### ProductList
**File:** `ProductList.tsx`

Displays a grid of products with loading and empty states.

**Features:**
- Responsive grid layout (1-4 columns based on screen size)
- Loading state with spinner
- Empty state with message
- NFT requirement checking for each product

**Props:**
- `products`: Array of products
- `nfts`: User's NFT collection (optional)
- `onAddToCart`: Callback when adding to cart
- `loading`: Loading state (default: false)
- `emptyMessage`: Custom empty state message

### ShoppingCart
**File:** `ShoppingCart.tsx`

Displays cart items with quantity controls and order summary.

**Features:**
- Cart item list with images and details
- Quantity increment/decrement controls
- Remove item functionality
- Order summary with total calculation
- Empty cart state
- Checkout button

**Props:**
- `items`: Array of cart items
- `onCheckout`: Callback for checkout
- `onRemoveItem`: Callback for removing items
- `onUpdateQuantity`: Callback for quantity updates
- `isCheckoutDisabled`: Disable checkout button (default: false)

### CheckoutForm
**File:** `CheckoutForm.tsx`

Stripe payment form for processing orders.

**Features:**
- Stripe Elements integration
- Payment processing with loading state
- Error handling and display
- Secure payment indicator
- Amount display

**Props:**
- `amount`: Total amount to charge
- `orderId`: Order ID for payment
- `onSuccess`: Callback on successful payment
- `onError`: Callback on payment error

## Pages

### Shop Page
**File:** `frontend/app/shop/page.tsx`

Main shop page displaying all active products.

**Features:**
- Product list with NFT filtering
- Cart item count badge
- Login prompt for unauthenticated users
- Error handling with retry
- View cart button

### Product Detail Page
**File:** `frontend/app/shop/[id]/page.tsx`

Detailed product view with purchase options.

**Features:**
- Large product image
- Full product description
- Quantity selector
- Stock availability
- NFT requirement display with verification status
- Add to cart with quantity
- Back to shop navigation

### Checkout Page
**File:** `frontend/app/checkout/page.tsx`

Complete checkout flow with cart review and payment.

**Features:**
- Two-step checkout process (Cart → Payment)
- Shopping cart review with edit capabilities
- NFT requirement validation
- Stripe payment integration
- Order creation
- Success state with redirect
- Help sidebar with shipping/security info

## Integration

### State Management
All components integrate with Zustand stores:
- `useCartStore`: Cart state and operations
- `useAuthStore`: User authentication
- `useNFTStore`: NFT ownership verification

### API Integration
Components use API functions from `lib/api/`:
- `products.ts`: Product fetching
- `orders.ts`: Order creation
- `payments.ts`: Payment intent creation

### Stripe Integration
Checkout uses `@stripe/react-stripe-js` for payment processing:
- Elements wrapper for payment form
- PaymentElement for card input
- Payment confirmation handling

## NFT Gating

Products can require NFT ownership for purchase:
1. Product has `required_nft_id` field
2. System checks if user has any completed NFT
3. Locked products show lock overlay
4. Checkout validates NFT requirements before order creation

## Styling

All components use:
- Tailwind CSS for styling
- Responsive design (mobile-first)
- Consistent color scheme (blue primary, gray neutrals)
- Accessible UI patterns

## Usage Example

```tsx
import { ProductList } from '@/components/shop/ProductList';
import { useCartStore } from '@/stores/cart-store';
import { useNFTStore } from '@/stores/nft-store';

function ShopPage() {
  const { addItem } = useCartStore();
  const { nfts } = useNFTStore();
  
  return (
    <ProductList
      products={products}
      nfts={nfts}
      onAddToCart={(product) => addItem(product, 1)}
    />
  );
}
```

## Requirements Covered

This implementation satisfies the following requirements:
- **4.1**: Product display and listing
- **4.2**: Product details and information
- **5.1**: Shopping cart functionality
- **5.2**: NFT-gated product access
- **5.5**: Stripe payment integration
- **5.6**: Order creation and payment processing
