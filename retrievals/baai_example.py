import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-large')
model = AutoModelForSequenceClassification.from_pretrained('BAAI/bge-reranker-large')
model.to("cuda")


qa_pairs = [
    ("как купить машину?", "Чтобы приобрести автомобиль надо пойти на рынок, выбрать подходящий и заплатить деньги продавцу"),
    ("как купить машину?", "Для постройки дома надо нанять бригаду и заплатить им деньги"),
    ("как купить машину?", "Чтобы узнать за сколько можно продать машину, надо купить каталог, посмотреть, сколько стоит похожая машина")
]


inputs = tokenizer(qa_pairs,
                   padding=True,
                   truncation=True,
                   return_tensors='pt',
                   max_length=512)

# Передача данных на устройство
inputs = {key: value.to("cuda") for key, value in inputs.items()}

# Вычисление оценок модели
with torch.no_grad():
    scores = model(**inputs, return_dict=True).logits.view(-1).float()


for i, (qa, score) in enumerate(sorted(list(zip(qa_pairs, scores.tolist())), key=lambda x: x[1], reverse=True)):
    print(f"Rank {i + 1}: {qa} (Score: {score:.4f})")
