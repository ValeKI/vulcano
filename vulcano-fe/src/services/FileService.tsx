import {
  uploadFile as apiUploadFile,
  getUserFiles as apiGetUserFiles,
  getFilesByAnswerId as apiGetFilesByAnswerId,
  downloadFile as apiDownloadFile,
  type UploadFilePayload,
  type GetUserFilesResponse,
  type GetFilesByAnswerIdResponse,
} from '../api/FileApi';

export const uploadFile = async (payload: UploadFilePayload) => {
  return await apiUploadFile(payload);
};

export const getUserFiles = async (): Promise<GetUserFilesResponse> => {
  return await apiGetUserFiles();
};

export const getFilesByAnswerId = async (answerId: number): Promise<GetFilesByAnswerIdResponse> => {
  return await apiGetFilesByAnswerId(answerId);
};

export const downloadFile = async (file_id: number): Promise<Blob> => {
  return await apiDownloadFile(file_id);
};