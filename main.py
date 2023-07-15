from chating_AI.chat_bot import AmazonChatBot
import threading
from dotenv import load_dotenv

# Загрузить переменные среды 
load_dotenv()


email = "joctusedad@hotmail.com"
password = "qwe123"
email1 = "JamesLClark@yopmail.com"
password1 = "qwe123"

# thread1 = threading.Thread(target=run_chat_bot1)
# thread2 = threading.Thread(target=run_chat_bot2)

# thread1.start()
# thread2.start()

# # Wait for the threads to finish
# thread1.join()
# thread2.join()


chat_bot1 = AmazonChatBot(email, password)
# chat_bot2 = AmazonChatBot(email, password)

def run_chat_bot1():
    chat_bot1.run()

run_chat_bot1()
# def run_chat_bot2():
#     chat_bot2.run() 
