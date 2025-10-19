import { apiClient } from "./ApiClient";
export interface UploadFilePayload {
  file: File;
}

export const uploadFile = async (payload: UploadFilePayload) => {
  const formData = new FormData();
  formData.append("file", payload.file);

  const response = await apiClient.post("/files/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    withCredentials: true
  });

  return response.data;
};

export const getUserFiles = async () => {
  const response = await apiClient.get("/files/user", { withCredentials: true });
  return response.data;
};