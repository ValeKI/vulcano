import random


def call_ai_to_generate_answer(question, file_list):
    print("[AI] file_list ricevuti:", file_list)
    risposta = f"Risposta generata per la domanda: {question}"
    sampled_files = random.sample(file_list, min(2, len(file_list)))
    print("[AI] sampled_files scelti:", sampled_files)
    file_ids = [file['file_id'] for file in sampled_files]
    print("[AI] file_ids estratti:", file_ids)
    return {
        "answer": risposta,
        "file_ids": file_ids
    }