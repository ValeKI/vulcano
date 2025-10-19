import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { checkTokenApi, refreshTokenApi } from "../api/AuthApi";
import VulcanoPage from "../pages/VulcanoPage";

interface ProtectedRouteProps {
  children: React.ReactElement;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, token, logout } = useAuth();
  const [checking, setChecking] = useState(true);
  const [valid, setValid] = useState<boolean | null>(null);

  useEffect(() => {
    let isMounted = true;
    const verify = async () => {
      if (!token) {
        setValid(false);
        setChecking(false);
        return;
      }
      try {
        const res = await checkTokenApi.check(token);
        if (isMounted) {
          if (res.data.status === "ok") {
            const resRefresh = await refreshTokenApi.refresh();
            if (resRefresh.status === 200) {
              setValid(true);
            } else {
              logout();
              setValid(false);
            }
          } else {
            logout();
            setValid(false);
          }
        }
      } catch {
        if (isMounted) {
          logout();
          setValid(false);
        }
      } finally {
        if (isMounted) setChecking(false);
      }
    };
    verify();
    return () => {
      isMounted = false;
    };
  }, [token, logout]);

  if (!isAuthenticated || valid === false) {
    return <Navigate to="/" replace />;
  }

  if (checking) {
    return <VulcanoPage />;
  }

  return children;
};

export default ProtectedRoute;
