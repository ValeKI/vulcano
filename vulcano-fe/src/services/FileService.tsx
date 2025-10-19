import {
  uploadFile as apiUploadFile,
  getUserFiles as apiGetUserFiles,
  type UploadFilePayload,
  type GetUserFilesResponse,
} from '../api/FileApi';

export const uploadFile = async (payload: UploadFilePayload) => {
  return await apiUploadFile(payload);
};

export const getUserFiles = async (): Promise<GetUserFilesResponse> => {
  return await apiGetUserFiles();
};
