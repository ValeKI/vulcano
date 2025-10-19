import {
  uploadFile as apiUploadFile,
  getUserFiles as apiGetUserFiles,
  getFilesByAnswerId as apiGetFilesByAnswerId,
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
}