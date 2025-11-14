// Shopping cart store using Zustand

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Product, CartItem } from '../types';

interface CartState {
  items: CartItem[];
  total: number;

  // Actions
  addItem: (product: Product, quantity?: number) => void;
  removeItem: (productId: string) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  clearCart: () => void;
  getItemCount: () => number;
}

const calculateTotal = (items: CartItem[]): number => {
  return items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);
};

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      total: 0,

      addItem: (product: Product, quantity: number = 1) => {
        const items = get().items;
        const existingItemIndex = items.findIndex(
          (item) => item.product.id === product.id
        );

        let newItems: CartItem[];
        if (existingItemIndex >= 0) {
          // Update quantity if item already exists
          newItems = items.map((item, index) =>
            index === existingItemIndex
              ? { ...item, quantity: item.quantity + quantity }
              : item
          );
        } else {
          // Add new item
          newItems = [...items, { product, quantity }];
        }

        set({
          items: newItems,
          total: calculateTotal(newItems),
        });
      },

      removeItem: (productId: string) => {
        const newItems = get().items.filter(
          (item) => item.product.id !== productId
        );
        set({
          items: newItems,
          total: calculateTotal(newItems),
        });
      },

      updateQuantity: (productId: string, quantity: number) => {
        if (quantity <= 0) {
          get().removeItem(productId);
          return;
        }

        const newItems = get().items.map((item) =>
          item.product.id === productId ? { ...item, quantity } : item
        );
        set({
          items: newItems,
          total: calculateTotal(newItems),
        });
      },

      clearCart: () => {
        set({ items: [], total: 0 });
      },

      getItemCount: () => {
        return get().items.reduce((count, item) => count + item.quantity, 0);
      },
    }),
    {
      name: 'cart-storage', // localStorage key
    }
  )
);
