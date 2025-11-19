// Purchase restriction utilities

import type { Product, PurchaseRestriction, NFT } from '@/types';
import Cookies from 'js-cookie';

/**
 * Check if user can purchase a product based on restrictions
 */
export function canPurchaseProduct(
  product: Product,
  userNFTs: NFT[],
  isAuthenticated: boolean
): {
  canPurchase: boolean;
  reason?: string;
} {
  if (!product.is_active) {
    return { canPurchase: false, reason: '商品は現在販売されていません' };
  }

  if (product.stock_quantity <= 0) {
    return { canPurchase: false, reason: '在庫切れです' };
  }

  if (!isAuthenticated) {
    return { canPurchase: false, reason: 'ログインが必要です' };
  }

  // If purchase_restriction is not set, default to public
  const restriction = product.purchase_restriction || 'public';

  switch (restriction) {
    case 'onsite_only':
      return checkOnsiteAccess();

    case 'onsite_and_referral':
      return checkOnsiteOrReferralAccess();

    case 'nft_holders':
      return checkNFTAccess(product, userNFTs);

    case 'public':
      return { canPurchase: true };

    default:
      return { canPurchase: false, reason: '不明な購入制限です' };
  }
}

/**
 * Check if user has onsite access (OpenNDS cookie)
 */
function checkOnsiteAccess(): { canPurchase: boolean; reason?: string } {
  const onsiteCookie = Cookies.get('airzone_onsite');
  
  if (onsiteCookie) {
    return { canPurchase: true };
  }

  return {
    canPurchase: false,
    reason: '現地参加者のみ購入可能です。WiFiに接続してください。',
  };
}

/**
 * Check if user has onsite or referral access
 */
function checkOnsiteOrReferralAccess(): {
  canPurchase: boolean;
  reason?: string;
} {
  const onsiteCookie = Cookies.get('airzone_onsite');
  const referralCookie = Cookies.get('airzone_referral');

  if (onsiteCookie || referralCookie) {
    return { canPurchase: true };
  }

  return {
    canPurchase: false,
    reason: '現地参加者または紹介リンクからのアクセスが必要です',
  };
}

/**
 * Check if user has required NFT
 */
function checkNFTAccess(
  product: Product,
  userNFTs: NFT[]
): { canPurchase: boolean; reason?: string } {
  if (!product.required_nft_id) {
    return { canPurchase: true };
  }

  const hasRequiredNFT = userNFTs.some(
    (nft) =>
      nft.status === 'completed' &&
      (nft.id === product.required_nft_id || nft.nft_object_id === product.required_nft_id)
  );

  if (hasRequiredNFT) {
    return { canPurchase: true };
  }

  return {
    canPurchase: false,
    reason: '指定のNFTを保有している必要があります',
  };
}

/**
 * Get restriction badge info for display
 */
export function getRestrictionBadge(restriction: PurchaseRestriction): {
  label: string;
  color: string;
  icon: string;
} {
  switch (restriction) {
    case 'onsite_only':
      return {
        label: '現地限定',
        color: 'bg-purple-100 text-purple-800 border-purple-200',
        icon: '📍',
      };

    case 'onsite_and_referral':
      return {
        label: '現地・紹介限定',
        color: 'bg-blue-100 text-blue-800 border-blue-200',
        icon: '🎫',
      };

    case 'nft_holders':
      return {
        label: 'NFT保有者限定',
        color: 'bg-yellow-100 text-yellow-800 border-yellow-200',
        icon: '🎨',
      };

    case 'public':
      return {
        label: '誰でも購入可',
        color: 'bg-green-100 text-green-800 border-green-200',
        icon: '🌐',
      };

    default:
      return {
        label: '制限あり',
        color: 'bg-gray-100 text-gray-800 border-gray-200',
        icon: '🔒',
      };
  }
}

/**
 * Get product type badge info
 */
export function getProductTypeBadge(productType: Product['product_type']): {
  label: string;
  color: string;
  icon: string;
} {
  switch (productType) {
    case 'nft':
      return {
        label: 'NFT',
        color: 'bg-indigo-100 text-indigo-800',
        icon: '🎨',
      };

    case 'goods':
      return {
        label: 'グッズ',
        color: 'bg-pink-100 text-pink-800',
        icon: '🛍️',
      };

    case 'event_ticket':
      return {
        label: '公演チケット',
        color: 'bg-orange-100 text-orange-800',
        icon: '🎟️',
      };

    default:
      return {
        label: '商品',
        color: 'bg-gray-100 text-gray-800',
        icon: '📦',
      };
  }
}

/**
 * Get delivery method label
 */
export function getDeliveryMethodLabel(method: Product['delivery_method']): string {
  switch (method) {
    case 'pickup':
      return '現地受け取り';
    case 'shipping':
      return '配送';
    case 'digital':
      return 'デジタル配信';
    default:
      return '未設定';
  }
}
