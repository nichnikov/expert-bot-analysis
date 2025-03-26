#Бесчеловечный код
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

import torch
from core.data_types import Parameters
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import List, Tuple, Optional


class DenseRetriever:
    def __init__(self, settings: Parameters):
        """
        Инициализация DenseRetriever: загружает модель и токенизатор на указанное устройство.
        :param model_name: Имя предобученной модели (например, 'BAAI/bge-reranker-large').
        :param device: Устройство для выполнения вычислений ('cuda' или 'cpu'). Если None, выбирается автоматически.
        """
        self.settings = settings
        self.device = self.settings.device if self.settings.device else ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.settings.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.settings.model_name)
        self.model.eval()
        self.model.to(self.device)

    def rank(self, qa_pairs: List[Tuple[str, str]]) -> List[Tuple[Tuple[str, str], float]]:
        """
        Ранжирует пары вопрос-ответ на основе предсказаний модели.
        :param qa_pairs: Список кортежей (вопрос, ответ).
        :param rank_num: Максимальное количество возвращаемых результатов.
        :return: Список кортежей ((вопрос, ответ), оценка), отсортированный по убыванию оценки.
        """
        if not isinstance(qa_pairs, list) or not all(isinstance(pair, tuple) and len(pair) == 2 for pair in qa_pairs):
            raise ValueError("qa_pairs должен быть списком кортежей вида (вопрос, ответ).")

        # Токенизация входных данных
        inputs = self.tokenizer(
            qa_pairs,
            padding=True,
            truncation=True,
            return_tensors='pt',
            max_length=512
        )

        # Передача данных на устройство
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        # Вычисление оценок модели
        with torch.no_grad():
            scores = self.model(**inputs, return_dict=True).logits.view(-1).float()

        return scores.tolist() # [(pair, score) for pair, score in zip(qa_pairs, scores.tolist())]
        


    def __call__(self, queries_pairs):
        return self.rank(queries_pairs)


# Пример использования
if __name__ == "__main__":
    import os
    import sys

    sett = Parameters()
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    sys.path.append(project_root)
    ranker = DenseRetriever(sett)


    # Пример данных
    '''
    qa_pairs = [
        # ("What is the capital of France?", "The capital of France is Paris."),
        ("What is the capital of France?", "The capital of France is Ryazan."),
        ("What is the capital of France?", "The capital of France is Leon."),
        ("What is the capital of France?", "The capital of France is Marseille."),
    ]
    
    qa_pairs = [
        ("What is the capital of Russia?", "The capital of Russia is Moscow"),
        ("What is the capital of Russia?", "The capital of Russia is Paris."),
        ("What is the capital of Russia?", "The capital of Russia is Vladimir"),
        ("What is the capital of Russia?", "The capital of Russia is Leon."),
        ("What is the capital of Russia?", "The capital of Russia is Ryazan."),
        ("What is the capital of Russia?", "The capital of Russia is Marseille."),
        ("What is the capital of Russia?", "The capital of Russia is Saint Petersburg")
    ]

    qa_pairs = [
        ("What is the capital of Russian Empire?", "The capital of Russian Empire is Moscow"),
        ("What is the capital of Russian Empire?", "The capital of Russian Empire is Paris."),
        ("What is the capital of Russian Empire?", "The capital of Russian Empire is Vladimir"),
        ("What is the capital of Russian Empire?", "The capital of Russian Empire is Leon."),
        ("What is the capital of Russian Empire?", "The capital of Russian Empire is Ryazan."),
        ("What is the capital of Russian Empire?", "The capital of Russian Empire is Marseille."),
        ("What is the capital of Russian Empire?", "The capital of Russian Empire is Saint Petersburg")
    ]'''
    
    qa_pairs = [("Who is the great Russian poet?", "The great Russian poet is Alexander Pushkin"),
     ("Who is the great Russian poet?", "The great Russian poet is Fyodor Dostoevsky"),
     ("Who is the great Russian poet?", "The great Russian poet is Dmitri Mendeleev"),
     ("Who is the great Russian poet?", "The great Russian poet is Anna Glazkova"),
     ("Who is the great Russian poet?", "The great Russian poet is Valery Chkalov"),
     ]

    # Получение топ-2 результатов
    ranked_results = ranker(qa_pairs)
    print(ranked_results)

    for i, (qa, score) in enumerate(sorted(list(zip(qa_pairs, ranked_results)), key=lambda x: x[1], reverse=True)):
        print(f"Rank {i + 1}: {qa} (Score: {score:.4f})")

    print(ranked_results)