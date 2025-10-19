import {
  getQuestionById as apiGetQuestionById,
  getQuestionsByUserId as apiGetQuestionsByUserId,
  insertQuestion as apiInsertQuestion,
  type Question,
  type InsertQuestionRequest,
  type GetQuestionByIdResponse,
  type GetQuestionsByUserIdResponse,
  type InsertQuestionResponse,
} from "../api/ChatApi";

export const getQuestionById = async (questionId: number): Promise<GetQuestionByIdResponse> => {
  return await apiGetQuestionById(questionId);
};

export const getQuestionsByUserId = async (): Promise<GetQuestionsByUserIdResponse> => {
  return await apiGetQuestionsByUserId();
};

export const insertQuestion = async (payload: InsertQuestionRequest): Promise<InsertQuestionResponse> => {
  return await apiInsertQuestion(payload);
};

export type {
  Question,
  InsertQuestionRequest,
  GetQuestionByIdResponse,
  GetQuestionsByUserIdResponse,
  InsertQuestionResponse,
};