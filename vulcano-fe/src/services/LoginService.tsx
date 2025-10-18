import { authApi } from "../api/AuthApi";

export interface LoginCredentials {
  usernameOrEmail: string;
  password: string;
}

export const LoginService = {
  login: async ({ usernameOrEmail, password }: LoginCredentials): Promise<string> => {
    try {
      const response = await authApi.login({ usernameOrEmail, password });
      const token = response.data?.token;
      if (!token) throw new Error("Token mancante");
      return token;
    } catch (error: any) {
      console.error("Errore login:", error);
      throw error.response?.data?.error || "Errore sconosciuto";
    }
  },
};
