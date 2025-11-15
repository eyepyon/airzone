// API client for making requests to the backend

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || 'https://api.airz.one';

export class APIError extends Error {
  constructor(
    public status: number,
    public code: number,
    message: string,
    public details?: unknown
  ) {
    super(message);
    this.name = 'APIError';
  }
}

interface RequestOptions extends RequestInit {
  token?: string;
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { token, ...fetchOptions } = options;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (fetchOptions.headers) {
    Object.assign(headers, fetchOptions.headers);
  }

  // Use provided token or get from localStorage
  const authToken = token || getAuthToken();
  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }

  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...fetchOptions,
      headers,
    });

    const data = await response.json();

    if (!response.ok) {
      // Handle 401 Unauthorized - token expired
      if (response.status === 401 && authToken) {
        // Try to refresh token
        const refreshed = await refreshAccessToken();
        if (refreshed) {
          // Retry the request with new token
          return apiRequest<T>(endpoint, { ...options, token: getAuthToken()! });
        } else {
          // Refresh failed, clear tokens
          removeAuthToken();
          removeRefreshToken();
        }
      }

      throw new APIError(
        response.status,
        data.code || response.status,
        data.error || 'An error occurred',
        data.details
      );
    }

    return data.data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    if (error instanceof Error) {
      throw new APIError(0, 0, error.message);
    }
    throw new APIError(0, 0, 'Network error');
  }
}

async function refreshAccessToken(): Promise<boolean> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return false;

  try {
    const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) return false;

    const data = await response.json();
    if (data.status === 'success' && data.data.access_token) {
      setAuthToken(data.data.access_token);
      return true;
    }

    return false;
  } catch {
    return false;
  }
}

export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

export function setAuthToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('access_token', token);
}

export function removeAuthToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
}

export function getRefreshToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('refresh_token');
}

export function setRefreshToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('refresh_token', token);
}

export function removeRefreshToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('refresh_token');
}
