import { apiClient } from "./ApiClient";

export interface LoginPayload {
  usernameOrEmail: string;
  password: string;
}

export const authApi = {
  login: (data: LoginPayload) =>
    apiClient.post("/auth/login", data),
};


export const checkTokenApi = {
  check: (token: string) =>
    apiClient.post("/auth/check", { token }),
};