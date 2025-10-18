import React, { createContext, useContext, useState, useEffect, type FC } from "react";
import type { ReactNode } from "react";
import { checkTokenApi } from "../api/AuthApi";
import { jwtDecode } from "jwt-decode";

interface User { username: string; email?: string; }
interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const rawUser = localStorage.getItem("user");
  let initialUser: User | null = null;
  try {
    if (rawUser && rawUser !== "undefined") {
      initialUser = JSON.parse(rawUser);
    }
  } catch {
    initialUser = null;
  }
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [user, setUser] = useState<User | null>(initialUser);

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  const login = (newToken: string) => {
  localStorage.setItem("token", newToken);
  setToken(newToken);
  const decoded = jwtDecode<User>(newToken);
  setUser(decoded);
};

  useEffect(() => {
    const verifyToken = async () => {
      if (token) {
        try {
          const response = await checkTokenApi.check(token);
          if (response.data.status === "ok") {
            setUser(response.data.user);
          } else {
            logout();
          }
        } catch {
          logout();
        }
      }
    };
    verifyToken();
  }, [token]);

  const isAuthenticated = !!token;

  return (
    <AuthContext.Provider value={{ isAuthenticated, token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
}
