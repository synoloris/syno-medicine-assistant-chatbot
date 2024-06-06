import openai
import os
from chatbot.rag import MedicineRAG
from openai.error import APIError, RateLimitError, Timeout, InvalidRequestError, AuthenticationError

openai.api_key = os.getenv("OPENAI_API_KEY")

class DoctorChatbot:
    def __init__(self):
        print('Initializing DoctorChatbot...')
        self.rag = MedicineRAG()
        self.chat_history = []

    def get_initial_prompt(self, name):
        print('Getting initisl prompt...')
        initial_message = f"Hello, {name}! How can I assist you today?"
        self.chat_history.append({"role": "system", "content": initial_message})
        return initial_message

    def get_response(self, user_input):
        print('Getting response...')
        self.chat_history.append({"role": "user", "content": user_input})
        response = self.generate_response(user_input)
        self.chat_history.append({"role": "assistant", "content": response})
        return response

    def generate_response(self, user_input):
        print('Generating response...')
        retrieved_info = self.rag.retrieve(user_input)
        if retrieved_info:
            data_prompt = "\n".join([info['text'] for info in retrieved_info])
        else:
            data_prompt = "I couldn't find any relevant information in my database to address your query."

        return self.generate_model_response(user_input, data_prompt)

    def generate_model_response(self, user_input, data_prompt):
        print('Generating model response...')
        role_prompt = "Your name is Syno and you're a medical assistant. Your main task is assisting a doctor with medical information. Provide accurate and concise answers based on the provided RAG dataset. Your goal is to help the doctor with their queries and provide necessary medical information efficiently. Engage in small talk if necessary, but always return to important questions and answer briefly in compact sentences. Don't ask more than one question at a time. Be persistent and help the doctor with his questions. If you can't prescribe a medicine, advise them on what to do. The conversation ends if the doctor has no more questions and is satisfied with the prognosis and prescribed medicine. When prescribing a medicine, tell the user how regularly and how many times the medicine should be taken. Decide what the further steps are. If the provided concern is not health-related and cannot be treated with medicine, advise that another health department is needed for the problem. If you've served the doctor, try to end the conversation politely and tell him what to do next."
        
        messages = [
            {"role": "system", "content": role_prompt},
            *self.chat_history,
            {"role": "user", "content": user_input},
            {"role": "system", "content": data_prompt}
        ]
        
        # Retry logic
        for _ in range(3):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=150
                )
                return response.choices[0].message['content'].strip()
            except (APIError, RateLimitError, Timeout, InvalidRequestError, AuthenticationError) as e:
                print(f"API error occurred: {e}. Retrying...")

        # If all retries fail, return a fallback message
        return "I'm sorry, but I couldn't process your request at the moment. Please try again later."

    def reset(self):
        print('Resetting chat history...')
        self.chat_history = []

    def load_chat_history(self, chat_history):
        print('Loading chat history...')
        self.chat_history = chat_history
