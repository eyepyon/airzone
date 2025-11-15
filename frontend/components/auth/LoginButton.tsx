'use client';

import { GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { useAuthStore } from '@/stores/auth-store';
import { useState } from 'react';

interface LoginButtonProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
  className?: string;
  children?: React.ReactNode;
}

export default function LoginButton({
  onSuccess,
  onError,
  className,
}: LoginButtonProps) {
  const { login } = useAuthStore();
  const [error, setError] = useState<string | null>(null);

  const handleSuccess = async (credentialResponse: CredentialResponse) => {
    try {
      setError(null);
      
      if (!credentialResponse.credential) {
        throw new Error('No credential received from Google');
      }

      // credentialResponse.credential contains the ID token
      await login(credentialResponse.credential);

      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      const error =
        err instanceof Error ? err : new Error('Authentication failed');
      setError(error.message);
      console.error('Login error:', error);
      if (onError) {
        onError(error);
      }
    }
  };

  const handleError = () => {
    const error = new Error('Google login failed');
    setError(error.message);
    console.error('Login error:', error);
    if (onError) {
      onError(error);
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <div className={className}>
        <GoogleLogin
          onSuccess={handleSuccess}
          onError={handleError}
          useOneTap
        />
      </div>
      {error && (
        <p className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
