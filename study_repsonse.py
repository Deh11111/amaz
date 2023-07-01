import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example

# Создание пустой модели для английского языка
nlp = spacy.blank("en")
nlp.add_pipe("textcat", last=True)
# Добавление пайплайна для классификации текста
textcat = nlp.get_pipe("textcat")

# Добавление меток категорий
categories = {
    "HELLO": "Hello",
    "WAIT": "Wait",
    "LINK": "Link",
    "WHEN": "When",
    "MONEY": "Money",
    "SKIP": "SKIP"
}

for category_key, category_label in categories.items():
    textcat.add_label(category_key)

# Обучение модели на шаблонах
train_data = [
    ("Hello,how i can help you", {"cats": {"HELLO": 1.0, "SKIP": 0.0, "WHEN": 0.0}}),
    ("my name is Divya", {"cats": {"HELLO": 1.0, "SKIP": 0.0, "WHEN": 0.0}}),
    ("May I have your email associated to your amazon account? So that I can check it for you", {"cats": {"HELLO": 0.0, "SKIP": 1.0, "LINK": 0.0}}),
    ("Have you fulfilled all the terms and conditions of the promotion", {"cats": {"HELLO": 0.0, "SKIP": 1.0, "LINK": 0.0}}),
    ("In this case I kindly request you to please stay connected while I transfer your chat to the concerned team", {"cats": {"HELLO": 0.0, "SKIP": 1.0, "LINK": 0.0}}),
    ("here to help you", {"cats": {"HELLO": 1.0, "SKIP": 0.0, "WHEN": 0.0}}),
    ("Can I have the link of that promotion so that I can check it for you.", {"cats": {"HELLO": 0.0, "SKIP": 1.0, "LINK": 0.0}}),
    ("Could you please stay connected while I check this for you?", {"cats": {"HELLO": 0.0, "SKIP": 0.0, "WAIT": 1.0}}),
    ("Please give me a moment to review the previous correspondence.", {"cats": {"HELLO": 1.0, "SKIP": 0.0, "WAIT": 0.0}}),
    ("May I know when you", {"cats": {"HELLO": 0.0, "WHEN": 1.0, "SKIP": 0.0}}),
    ("If you are eligible for the promotion, you will receive an e-mail from Amazon within 7 days that indicates the dollar amount of the promotional code. The e-mail will also provide instructions on how to redeem the promotional code.", {"cats": {"HELLO": 0.0, "SKIP": 1.0, "LINK": 0.0}}),
    ("Is there anything else I can help you with at the moment?", {"cats": {"HELLO": 0.0, "SKIP": 1.0, "LINK": 0.0}}),
    ("I'll issue you manually is that fine for you?", {"cats": {"HELLO": 0.0, "MONEY": 1.0, "LINK": 0.0}}),
    ("Could you please elaborate your concern?", {"cats": {"HELLO": 1.0, "MONEY": 0.0, "LINK": 0.0}}),
    ("The chat is paused due to inactivity. To continue, start typing and an associate who knows your issue will join", {"cats": {"SKIP": 1.0, "MONEY": 0.0, "LINK": 0.0}})
]
# Compile and train the model
optimizer = nlp.begin_training()
for i in range(300):
    losses = {}
    batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        texts, annotations = zip(*batch)
        examples = []
        for text, annotation in zip(texts, annotations):
            doc = nlp.make_doc(text)
            example_dict = {"text": text, "cats": annotation["cats"]}
            examples.append(Example.from_dict(doc, example_dict))
        nlp.update(examples, sgd=optimizer, losses=losses)

    print("Losses:", losses)

# Тестирование модели
test_texts = [
    "gugag",
    "The e-mail will also provide instructions on how to redeem the promotional code.",
    "May I know when you have uploaded the photos?",
    "Hello, my name is Issath Parveen. Please give me a moment to review the previous correspondence."
]
for text in test_texts:
    doc = nlp(text)
    category = max(doc.cats, key=doc.cats.get)
    if doc.cats[category] > 0.5:
        print(f"Текст: {text}, Категория: {categories[category]}")
    else:
        with open("unknown_categories.txt", "a") as file:
            file.write(f"{text}\n")
            print(f"Текст: {text}, Неизвестная категория (записана в файл 'unknown_categories.txt')")

nlp.to_disk("trained_answers")