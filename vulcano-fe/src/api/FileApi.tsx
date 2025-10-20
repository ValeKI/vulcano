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
    withCredentials: true,
    timeout: 10 * 60 * 1000
  });

  return response.data;
};

export interface UserFile {
  file_id: number;
  file_name: string;
  format: string;
  user_id: number;
}

export interface GetUserFilesResponse {
  files: UserFile[];
}

export const getUserFiles = async (): Promise<GetUserFilesResponse> => {
  const response = await apiClient.get("/files/list", { withCredentials: true });
  return response.data;
};

export interface GetFilesByAnswerIdResponse {
  files: UserFile[];
}

export const getFilesByAnswerId = async (answerId: number): Promise<GetFilesByAnswerIdResponse> => {
  const response = await apiClient.get(`/files/list_by_answer_id?answer_id=${answerId}`, { withCredentials: true });
  return response.data;
};

export const downloadFile = async (file_id: number): Promise<Blob> => {
  const response = await apiClient.get(`/files/download?file_id=${file_id}`, {
    responseType: "blob",
    withCredentials: true
  });
  return response.data;
};