// Authentication API functions

import { apiRequest, setAuthToken, setRefreshToken, removeAuthToken, removeRefreshToken } from '../api-client';
import type {
  AuthResponse,
  RefreshTokenResponse,
  GoogleAuthRequest,
  RefreshTokenRequest,
  User,
} from '../../types';

/**
 * Authenticate user with Google OAuth
 * @param idToken - Google ID token from OAuth flow
 * @returns Authentication response with user, wallet, and tokens
 */
export async function authenticateWithGoogle(
  idToken: string
): Promise<AuthResponse> {
  const response = await apiRequest<AuthResponse>('/auth/google', {
    method: 'POST',
    body: JSON.stringify({ id_token: idToken } as GoogleAuthRequest),
  });

  // Store tokens in localStorage
  if (response.access_token) {
    setAuthToken(response.access_token);
  }
  if (response.refresh_token) {
    setRefreshToken(response.refresh_token);
  }

  return response;
}

/**
 * Refresh access token using refresh token
 * @param refreshToken - Refresh token
 * @returns New access token
 */
export async function refreshToken(
  refreshToken: string
): Promise<RefreshTokenResponse> {
  const response = await apiRequest<RefreshTokenResponse>('/auth/refresh', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken } as RefreshTokenRequest),
  });

  // Store new access token
  if (response.access_token) {
    setAuthToken(response.access_token);
  }

  return response;
}

/**
 * Get current authenticated user information
 * @returns Current user data
 */
export async function getCurrentUser(): Promise<User> {
  return apiRequest<User>('/auth/me', {
    method: 'GET',
  });
}

/**
 * Logout user by clearing tokens
 */
export function logout(): void {
  removeAuthToken();
  removeRefreshToken();
}
