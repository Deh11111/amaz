from chating_AI.chat_bot import AmazonChatBot
import spacy
from selenium.webdriver.common.by import By

class AnalizeHandlerEvents:
    AMAZON_AUTH_CAPTCHA = 'repeat'
    AMAZON_AUTH_SUCCESSFULLY = 'signed up!'

class Analize:
    def __init__(self , mediator : AmazonChatBot):
        self.chatbot = mediator
        self.nlp = spacy.load('chating_Ai/trained_answers')

    
    # Фильтр по тексту,ответ категория 
    def get_category_in_text(self, text):
        trained_model = self.nlp(text)
        category = max(trained_model.cats, key=trained_model.cats.get)
        response = self.get_answer_from_category(category)
        
    #Убожество!!Исправить
    def get_answer_from_category(self, category):
        answers = {
            "HELLO": "Hello! I received a notification about a limited-time promotional offer that provides a $20 credit for Amazon Locker services, and I decided to take advantage of this offer when purchasing a new phone. However, when I tried to use the promo code <PICKUP10OFF>, I did not receive the discount. Can you help me get a $20 credit for my purchase? Thank you",
            "WAIT": "I'm wait",
            "LINK": "https://www.amazon.com/b/ref=hubm_us_gwy_inc_q123_00115_new_dtULP?node=72731536011?",
            "WHEN": "2 weeks ago uploaded photo and wait credit! Now this don't see in checkout!!",
            "MONEY": "Wait please.I check",
        }
        
        return answers[category]