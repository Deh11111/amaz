import time
import spacy
from login import AmazonLogin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import asyncio   Я бы Хотел в run(),чтобыбыло асинхроно
import telebot

bot_tg = telebot.TeleBot("5900799199:AAGggfpyJlSDP3Hl1SUmDTYj6ZNaf7Mvyrs")

class AmazonChatBot:
    def __init__(self, email, password):
        self.step = 0
        self.last_len_message = 0
        self.repeat = 0
        self.skips = 0
        self.nlp = spacy.load('trained_answers')
        self.login = AmazonLogin(email, password)
        self.connect = False
        self.last_message = [None, 0]
        self.email = email
        self.password = password

    def run(self):
        self.login.login()
        while True:   
            # Check status chat
            check_start = self.check_start()
            # Check on repeat and category
            message = self.get_user_message(check_start)
            # Filter category by (keyword,AI????)
            answer = self.get_category_by_text(message)
            
            if answer :
                # Send my answer
                self.send_message(answer)
                # Fix status
                self.status = check_start
                # Get support name
                name_indus = self.login.driver.find_elements(By.CLASS_NAME, "Message__messageDisplayName___1U_jv")[-1]

                # Make list of this step or result 
                result = {
                    "Name": f"{name_indus}",
                    "Status":f"{self.status}",
                    "Message":f"{message}",
                    "My_answer":f"{answer}",
                    "Skip":f"{self.skips}"
            }
            self.send_message_tg(result)

    def check_start(self):
        count = 0
        while count < 15:  # Добавляем ограничение на количество попыток
            try:
                load = WebDriverWait(self.login.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "LoadingSpinner__loadingGraphic___1no8h")))
                continue  # если элемент load найден, начинаем цикл заново
            except:
                pass  # если элемент load не найден, проверяем наличие элементов form и error
            try:
                form = self.login.driver.find_element(By.CLASS_NAME, "ChatInput__chatInputRow___1HmKN")
                return 'Connected!'
            except:
                pass

            # ИСпроавить текст,найти !!!!!!!
            # try:
            #     pause_txt = "The chat is paused due to inactivity. To continue, start typing and an associate who knows your issue will join. "
            #     element = self.login.driver.find_element(By.XPATH, "//*[contains(text(), '{}')]".format(pause_txt))
            #     if pause_txt.strip().lower() == element.text.strip().lower() :
            #         return 'Pause chat'
            # except:
            #     pass
            # Check supports leave

            try:
                leave_support_txt = "The chat is paused due to inactivity. To continue, start typing and an associate who knows your issue will join."
                element = self.login.driver.find_element(By.XPATH, "//*[contains(text(), '{}')]".format(leave_support_txt))
                if leave_support_txt.strip().lower() == element.text.strip().lower() :
                    return 'Pause chat'
            except:
                pass
            # Checking button?
            try:
                new_chat = self.login.driver.find_element(By.CLASS_NAME, "Interstitial__buttonInput___39Z4o")
                new_chat.click()
                continue
            except:
                pass
            # Checking red window 
            try:
                error = self.login.driver.find_element(By.CLASS_NAME, "ErrorOverlay__errorOverlay___3RAac")
                return 'Red window'
            except:
                pass
            # Checking feedback page 
            try:
                feedback = self.login.driver.find_element(By.CLASS_NAME,"a-size-base a-color-state")
                return 'Feedback page'
            except:
                pass
            
            time.sleep(5)
            # Сounter plus 
            count += 1
            if count == 7:
                self.login.driver.close()
                self.login.driver.quit()
                result = "Count > 7. Change Vpn and restart"
            
            print(f"Time {15*count} sec,{self.status}")

    #Заполнить 
    async def action_from_status(self,check_start):
        if check_start != "Connected!":
            if check_start == "Pause chat":
                self.one_signal_tg()
                body = self.login.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.F5)
            elif check_start == "Red window":
                self.login.driver.close()
                self.login.driver.quit()
                result = "REDDD!!"
                # self.send_message_tg(message, answer, self.step, self.skips)
                # return result
            elif check_start == "Feedback page":
                self.login.login()
            elif check_start == "Chat_waiting":
                self.skip()
        else:
            message = self.get_user_message()
            answer = self.get_category_by_text(message)
            if answer == "SKIP":
                self.skip()
            elif answer == "REPEAT":
                self.send_message("You help me?")
            elif answer == "REPEAT_2":
                self.send_message("You here??")
            elif answer == "REPEAT_3":
                self.skip()

        
        
    def get_user_message(self):
        while True:
            try:
                #####?????????????
                message_element_answer = self.login.driver.find_elements(By.CLASS_NAME, "Message__message___1YUAv.Message__agentVariant___2NLqJ")
                # waiting = self.login.driver.find_elements(By.CLASS_NAME, "SystemMessage__systemMessage___3u5N2")
                obj = len(message_element_answer)
                if obj == 0:
                    return "None"
                
                # if waiting == 0:
                #     return "Waiting_chat"
                
                if self.last_len_message < obj and obj != 1:   
                    length_blocks = obj - self.last_len_message 
                    self.last_len_message = length_blocks
                    message_element_answer[:-length_blocks]
                    answer = ""
                    for one in message_element_answer:
                        div_text = one.find_elements(By.CLASS_NAME, "Message__textContent___ugH_K")[-1]
                        answer_text = div_text.text
                        if answer_text is None:
                            continue
                        answer += answer_text

                    answer = " ".join(answer.split())  
                    
                    return answer
                
            except:
                pass

    # Фильтр по тексту,ответ категория 
    def get_category_by_text(self, text):
        # Проверка есть ли сообщение 
        # Надо поменять Эту хуйнЮ,другая проверка и не зднсь
        if text == 'None':
            wait_message = 1
            return response

        trained_model = self.nlp(text)
        category = max(trained_model.cats, key=trained_model.cats.get)

        # Проверить сообщение на пустоту,выявить ответ
        if self.last_message[0] is None:
            self.last_message[0] = text
            self.last_message[1] = self.repeat + 1
            # Получить ответ по категории 
            response = self.get_answer_from_category(category)
            # first_message = time.sleep(2 sec)->continue ,if first_messsage > 1 -> "HEy??" or skip? or wait for status and reload
        
        # Проверка на повторение 
        elif self.last_message[0] == text:
            self.last_message[1] += 1
            self.check_repeat()

        # Получить ответ по категории
        else:
            self.last_message[0] = text
            self.last_message[1] = 1
            response = self.get_answer_from_category(category)
        
        return response
    
    def check_repeat(self):
        repeat = self.repeat
        if repeat == 2:
            category = "REPEAT"
        elif repeat == 3:
            category = "REPEAT_2"
        elif repeat == 4:
            category = "REPEAT_3"

        return category

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
    

    def send_message(self, message):
        message_input = self.login.driver.find_elements(By.XPATH, "//textarea[@placeholder='Write a message...']")
        message_input[0].send_keys(message)
        message_input[0].send_keys(Keys.ENTER)
        time.sleep(4)
    
    def send_message_tg(self, data):
        bot_tg.send_message(544591866,f"'Status':'{data['Status']}',\n'Message':'{data['Message']}',\n'Skips':'{data['Skip']}',\n'My_answer':'{data['My_answer']}'")

    def one_signal_tg(self):
        bot_tg.send_message(544591866,f"'Paused!")

    def skip(self):
            leave_chat_script = """
                let e = ['https://www.amazon.com/message-us/log-data?metricName=PROMPT_END_CHAT&applicationName=MessageUs&platform=desktop&currentIngress=standard-mu',
                'https://www.amazon.com/message-us/log-data?metricName=REQUEST_END_CHAT&applicationName=MessageUs&platform=desktop&currentIngress=standard-mu',
                'https://www.amazon.com/message-us/chat-session',
                'https://www.amazon.com/message-us/log-data?metricName=CANCEL_END_CHAT_PROMPT&applicationName=MessageUs&platform=desktop&currentIngress=standard-mu',
                'https://www.amazon.com/message-us/log-data?metricName=HANDLE_CHAT_ENDED&applicationName=MessageUs&platform=desktop&currentIngress=standard-mu',
                'https://www.amazon.com/message-us/log-data?metricName=REGISTER_CHAT_COMPLETE&applicationName=MessageUs&platform=desktop&currentIngress=standard-mu',
                'https://www.amazon.com/message-us/log-data?metricName=DELETE_CURRENT_SESSION&applicationName=MessageUs&platform=desktop&currentIngress=standard-mu'];
                (async()=>{
                    document.body.innerText = "Starting";
                    await fetch(e[0]);
                    await fetch(e[1]);
                    await fetch(e[2], {method: "DELETE"});
                    await fetch(e[3]);
                    await fetch(e[4]);
                    await fetch(e[5]);
                    await fetch(e[6]);
                    document.body.innerText = "Done!";
                    window.location.reload();
                })();
            """
            self.login.driver.execute_script(leave_chat_script)
            
            # Wait for the script to finish running
            self.login.driver.implicitly_wait(10)
            time.sleep(1.7)
            self.login.driver.refresh()
            self.connect = False