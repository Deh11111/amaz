from chat_bot import AmazonChatBot
import threading

# Replace with your Amazon login credentials
email = "jamesjclark@yopmail.com"
password = "qwe123"

email1 = "JamesLClark@yopmail.com"
password1 = "qwe123"
# Initialize the chat bot with the login credentials
# Initialize the chat bots with the login credentials
chat_bot1 = AmazonChatBot(email, password)
# chat_bot2 = AmazonChatBot(email, password)

# Define functions to run each chat bot instance in a separate thread
def run_chat_bot1():
    chat_bot1.run()

run_chat_bot1()
# def run_chat_bot2():
#     chat_bot2.run() 

# # Create threads for each chat bot instance and start them
# thread1 = threading.Thread(target=run_chat_bot1)
# thread2 = threading.Thread(target=run_chat_bot2)

# thread1.start()
# thread2.start()

# # Wait for the threads to finish
# thread1.join()
# thread2.join()

