'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api, { setCsrfToken } from './api';

export interface User {
  id: number;
  email: string;
  full_name: string | null;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (credentials: Record<string, unknown>) => Promise<void>;
  register: (userData: Record<string, unknown>) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // In a real app, you would hit a `/api/auth/me` endpoint here to validate the cookie 
  // on page reload and retrieve the user profile and a fresh CSRF token.
  useEffect(() => {
    setLoading(false);
  }, []);

  const login = async (credentials: Record<string, unknown>) => {
    const res = await api.post('/api/auth/login', credentials);
    // Securely set the CSRF token in memory
    setCsrfToken(res.data.csrf_token);
    // Mock user retrieval. Ideally fetch from /api/auth/me
    setUser({ id: 1, email: credentials.email as string, full_name: null, is_active: true });
  };

  const register = async (userData: Record<string, unknown>) => {
    await api.post('/api/auth/register', userData);
  };

  const logout = async () => {
    try {
      await api.post('/api/auth/logout');
    } finally {
      setCsrfToken(null);
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
