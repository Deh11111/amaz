from chating_AI.chat_bot import AmazonChatBot
import spacy


class Filter:
    def __init__(self):
        self.nlp = spacy.load('chating_Ai/trained_answers')
        self.repeat = 0

    # Фильтр по тексту,ответ категория 
    def get_category_by_text(self, text):
        trained_model = self.nlp(text)
        category = max(trained_model.cats, key=trained_model.cats.get)
        response = self.get_answer_from_category(category)
        
        return response
    
    #Убожество!!Исправить
    def get_answer_from_category(self, category):
        answers = {
            "HELLO": "Hello! I received a notification about a limited-time promotional offer that provides a $20 credit for Amazon Locker services, and I decided to take advantage of this offer when purchasing a new phone. However, when I tried to use the promo code <PICKUP10OFF>, I did not receive the discount. Can you help me get a $20 credit for my purchase? Thank you",
            "REPEAT": "You here?????",
            "REPEAT_2": "Can you help me???",
            "WAIT": "I'm wait",
            "LINK": "https://www.amazon.com/b/ref=hubm_us_gwy_inc_q123_00115_new_dtULP?node=72731536011?",
            "WHEN": "2 weeks ago uploaded photo and wait credit! Now this don't see in checkout!!",
            "MONEY": "Wait please.I check",
            "Waiting_chat":"Waiting_chat"
        }

        if answers[category] == "SKIP":
            return "SKIP"
        elif answers[category] == "Waiting_chat":
            return "SKIP"
        
        return answers[category]
    
    def check_repeat(self):
        
        return self.repeat