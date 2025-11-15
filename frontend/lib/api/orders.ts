// Order API functions

import { apiRequest } from '../api-client';
import type {
  Order,
  OrderListResponse,
  CreateOrderRequest,
  QueryParams,
} from '../../types';

/**
 * Create a new order
 * @param orderData - Order data with items
 * @returns Created order
 */
export async function createOrder(orderData: CreateOrderRequest): Promise<Order> {
  return apiRequest<Order>('/orders', {
    method: 'POST',
    body: JSON.stringify(orderData),
  });
}

/**
 * Get list of orders for the current user
 * @param params - Query parameters for filtering and pagination
 * @returns List of orders
 */
export async function getOrders(params?: QueryParams): Promise<OrderListResponse> {
  const queryString = params ? `?${new URLSearchParams(params as Record<string, string>).toString()}` : '';
  return apiRequest<OrderListResponse>(`/orders${queryString}`, {
    method: 'GET',
  });
}

/**
 * Get order details by ID
 * @param orderId - Order ID
 * @returns Order details with items
 */
export async function getOrderById(orderId: string): Promise<Order> {
  return apiRequest<Order>(`/orders/${orderId}`, {
    method: 'GET',
  });
}

/**
 * Get orders by status
 * @param status - Order status to filter by
 * @param params - Additional query parameters
 * @returns List of orders with the specified status
 */
export async function getOrdersByStatus(
  status: Order['status'],
  params?: QueryParams
): Promise<OrderListResponse> {
  return getOrders({ ...params, status });
}

/**
 * Get pending orders for the current user
 * @param params - Query parameters
 * @returns List of pending orders
 */
export async function getPendingOrders(params?: QueryParams): Promise<OrderListResponse> {
  return getOrdersByStatus('pending', params);
}

/**
 * Get completed orders for the current user
 * @param params - Query parameters
 * @returns List of completed orders
 */
export async function getCompletedOrders(params?: QueryParams): Promise<OrderListResponse> {
  return getOrdersByStatus('completed', params);
}
