import { apiClient } from "./ApiClient";

export interface Question {
  id: number;
  content: string;
  user_id: number;
  content_file_id?: number | null;
  created_at: string;
}

export interface InsertQuestionRequest {
  content: string;
}

export interface GetQuestionByIdResponse extends Question {}

export interface GetQuestionsByUserIdResponse {
  questions: Question[];
}

export interface InsertQuestionResponse {
  id: number;
}

export const getQuestionById = async (questionId: number): Promise<GetQuestionByIdResponse> => {
  const response = await apiClient.get(`/chat/questions/${questionId}`, { withCredentials: true });
  return response.data;
};

export const getQuestionsByUserId = async (): Promise<GetQuestionsByUserIdResponse> => {
  const response = await apiClient.get(`/chat/questions/user`, { withCredentials: true });
  return response.data;
};

export const insertQuestion = async (payload: InsertQuestionRequest): Promise<InsertQuestionResponse> => {
  const response = await apiClient.post(`/chat/questions`, payload, { withCredentials: true });
  return response.data;
};