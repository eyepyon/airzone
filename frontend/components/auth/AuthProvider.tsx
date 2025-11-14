'use client';

import { GoogleOAuthProvider } from '@react-oauth/google';
import { useEffect, ReactNode } from 'react';
import { useAuthStore } from '@/stores/auth-store';
import { useRouter, usePathname } from 'next/navigation';

interface AuthProviderProps {
  children: ReactNode;
}

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '';

// Public routes that don't require authentication
const PUBLIC_ROUTES = ['/captive', '/login', '/'];

export default function AuthProvider({ children }: AuthProviderProps) {
  const { loadUser, isAuthenticated, isLoading, refreshToken } = useAuthStore();
  const router = useRouter();
  const pathname = usePathname();

  // Load user on mount
  useEffect(() => {
    loadUser();
  }, [loadUser]);

  // Set up token refresh interval (every 50 minutes for 1-hour tokens)
  useEffect(() => {
    if (!isAuthenticated) return;

    const refreshInterval = setInterval(
      async () => {
        try {
          await refreshToken();
        } catch (error) {
          console.error('Token refresh failed:', error);
          // If refresh fails, user will be logged out by the store
        }
      },
      50 * 60 * 1000
    ); // 50 minutes

    return () => clearInterval(refreshInterval);
  }, [isAuthenticated, refreshToken]);

  // Redirect to login if not authenticated and on protected route
  useEffect(() => {
    if (isLoading) return;

    const isPublicRoute = PUBLIC_ROUTES.some((route) =>
      pathname.startsWith(route)
    );

    if (!isAuthenticated && !isPublicRoute) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, pathname, router]);

  if (!GOOGLE_CLIENT_ID) {
    console.error('NEXT_PUBLIC_GOOGLE_CLIENT_ID is not set');
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-2">
            Configuration Error
          </h1>
          <p className="text-gray-600">
            Google Client ID is not configured. Please check your environment
            variables.
          </p>
        </div>
      </div>
    );
  }

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      {children}
    </GoogleOAuthProvider>
  );
}
