from langchain import ChainingLanguageModel
from langchain.prompts import SimplePrompt
from langchain.schema import CompletionConfig
from openai import OpenAIClient
from core.data_definition import Parameters, Settings

settings = Settings()
parameters = Parameters()

def create_chat_bot():
    # Создание клиента OpenAI
    openai_client = OpenAIClient(api_key="your_openai_api_key_here")

    # Настройка модели с использованием клиента OpenAI
    language_model = ChainingLanguageModel(openai_client)

    # Создание простого запроса
    prompt = SimplePrompt("Hello! How can I assist you today?")

    # Конфигурация для запроса к API
    completion_config = CompletionConfig(
        max_tokens=150,
        temperature=0.9,
        stop_sequences=["\n"]
    )

    # Обработка ответа
    response = language_model.complete(prompt, completion_config)
    print("ChatBot:", response.text)

    return response.text

if __name__ == "__main__":
    # Запуск чат-бота
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("ChatBot: Goodbye!")
            break
        # Обновление запроса с пользовательским вводом
        create_chat_bot().prompt.prompt_text = user_input
        create_chat_bot()