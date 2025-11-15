// Payment API functions

import { apiRequest } from '../api-client';
import type {
  Payment,
  PaymentIntentResponse,
  CreatePaymentIntentRequest,
} from '../../types';

/**
 * Create a Stripe Payment Intent for an order
 * @param orderId - Order ID to create payment for
 * @returns Payment Intent response with client secret
 */
export async function createPaymentIntent(
  orderId: string
): Promise<PaymentIntentResponse> {
  return apiRequest<PaymentIntentResponse>('/payments/intent', {
    method: 'POST',
    body: JSON.stringify({ order_id: orderId } as CreatePaymentIntentRequest),
  });
}

/**
 * Get payment details by ID
 * @param paymentId - Payment ID
 * @returns Payment details
 */
export async function getPaymentById(paymentId: string): Promise<Payment> {
  return apiRequest<Payment>(`/payments/${paymentId}`, {
    method: 'GET',
  });
}

/**
 * Get payment by order ID
 * @param orderId - Order ID
 * @returns Payment details for the order
 */
export async function getPaymentByOrderId(orderId: string): Promise<Payment> {
  // Note: This assumes the backend supports querying by order_id
  // If not, you may need to get the order first and then get the payment
  return apiRequest<Payment>(`/payments?order_id=${orderId}`, {
    method: 'GET',
  });
}

/**
 * Check if payment is successful
 * @param paymentId - Payment ID
 * @returns Boolean indicating if payment succeeded
 */
export async function isPaymentSuccessful(paymentId: string): Promise<boolean> {
  try {
    const payment = await getPaymentById(paymentId);
    return payment.status === 'succeeded';
  } catch {
    return false;
  }
}

/**
 * Poll payment status until it's no longer pending
 * @param paymentId - Payment ID
 * @param maxAttempts - Maximum number of polling attempts
 * @param intervalMs - Interval between polls in milliseconds
 * @returns Final payment status
 */
export async function pollPaymentStatus(
  paymentId: string,
  maxAttempts: number = 30,
  intervalMs: number = 2000
): Promise<Payment> {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const payment = await getPaymentById(paymentId);
    
    if (payment.status !== 'pending' && payment.status !== 'processing') {
      return payment;
    }
    
    // Wait before next poll
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
  
  // Return last known status if max attempts reached
  return getPaymentById(paymentId);
}
