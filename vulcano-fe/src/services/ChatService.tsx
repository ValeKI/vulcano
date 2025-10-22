import {
  getQuestionById as apiGetQuestionById,
  getQuestionsByUserId as apiGetQuestionsByUserId,
  insertQuestion as apiInsertQuestion,
  getAnswerByQuestionId as apiGetAnswerByQuestionId,
  type Question,
  type InsertQuestionRequest,
  type GetQuestionByIdResponse,
  type GetQuestionsByUserIdResponse,
  type InsertQuestionResponse,
  type GetAnswerByQuestionIdResponse,
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

export const getAnswerByQuestionId = async (questionId: number): Promise<GetAnswerByQuestionIdResponse> => {
  return await apiGetAnswerByQuestionId(questionId);
};

export type {
  Question,
  InsertQuestionRequest,
  GetQuestionByIdResponse,
  GetQuestionsByUserIdResponse,
  InsertQuestionResponse,
  GetAnswerByQuestionIdResponse,
};