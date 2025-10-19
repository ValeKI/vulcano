import { apiClient } from "./ApiClient";

export interface LoginPayload {
  usernameOrEmail: string;
  password: string;
}

export interface SignUpPayload {
  email: string;
  password: string;
  username: string;
}

export const authApi = {
  login: (data: LoginPayload) =>
    apiClient.post("/auth/login", data, { withCredentials: true }),
  signUp: (data: SignUpPayload) =>
    apiClient.post("/auth/signUp", data, { withCredentials: true }),
};

export const checkTokenApi = {
  check: (token: string) =>
    apiClient.post("/auth/check", { token }, { withCredentials: true }),
};

export const refreshTokenApi = {
  refresh: () => {
    console.log("before refresh");
    return apiClient.post("/auth/refresh", undefined, { withCredentials: true });
  }
};