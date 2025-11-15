// Product API functions

import { apiRequest } from '../api-client';
import type {
  Product,
  ProductListResponse,
  CreateProductRequest,
  UpdateProductRequest,
  QueryParams,
} from '../../types';

/**
 * Get list of products
 * @param params - Query parameters for filtering, sorting, and pagination
 * @returns List of products
 */
export async function getProducts(params?: QueryParams): Promise<ProductListResponse> {
  const queryString = params ? `?${new URLSearchParams(params as Record<string, string>).toString()}` : '';
  return apiRequest<ProductListResponse>(`/products${queryString}`, {
    method: 'GET',
  });
}

/**
 * Get product details by ID
 * @param productId - Product ID
 * @returns Product details
 */
export async function getProductById(productId: string): Promise<Product> {
  return apiRequest<Product>(`/products/${productId}`, {
    method: 'GET',
  });
}

/**
 * Create a new product (admin only)
 * @param productData - Product data
 * @returns Created product
 */
export async function createProduct(productData: CreateProductRequest): Promise<Product> {
  return apiRequest<Product>('/products', {
    method: 'POST',
    body: JSON.stringify(productData),
  });
}

/**
 * Update an existing product (admin only)
 * @param productId - Product ID
 * @param productData - Updated product data
 * @returns Updated product
 */
export async function updateProduct(
  productId: string,
  productData: UpdateProductRequest
): Promise<Product> {
  return apiRequest<Product>(`/products/${productId}`, {
    method: 'PUT',
    body: JSON.stringify(productData),
  });
}

/**
 * Delete a product (admin only)
 * @param productId - Product ID
 * @returns Success status
 */
export async function deleteProduct(productId: string): Promise<void> {
  return apiRequest<void>(`/products/${productId}`, {
    method: 'DELETE',
  });
}

/**
 * Get active products only
 * @param params - Query parameters
 * @returns List of active products
 */
export async function getActiveProducts(params?: QueryParams): Promise<ProductListResponse> {
  return getProducts({ ...params, is_active: true });
}

/**
 * Get products that require a specific NFT
 * @param nftId - NFT ID
 * @param params - Query parameters
 * @returns List of products requiring the NFT
 */
export async function getProductsByNFTRequirement(
  nftId: string,
  params?: QueryParams
): Promise<ProductListResponse> {
  return getProducts({ ...params, required_nft_id: nftId });
}
