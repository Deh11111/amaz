import time
from services.auth import AmazonAuthHandler , AmazonAuthHandlerEvents
from services.auth import check_start
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from services.analize import Analize
from services.tg_logger import TgLogger
from storage import AmazonStorage
import telebot
from services.selenium_web import SeleniumDriverService , SeleniumDriverServiceEvents
from ..services.logger import LogLevels
from datetime import datetime

class AmazonChatBot:

    def __init__(self, email, password):
        # self.connect = False
        self.bot_tg = telebot.TeleBot("5900799199:AAGggfpyJlSDP3Hl1SUmDTYj6ZNaf7Mvyrs")
        self.browser = SeleniumDriverService(self)
        self.logger = TgLogger()
        self.auth = AmazonAuthHandler(self)
        self.analize = Analize(self)
        self.status = 'init'
        self.tries = 0
        self.support_ignores = False
        self.support_connect = False
        self.auth.login(email, password)


    def notify_auth(self , event):
        match event:
            case AmazonAuthHandlerEvents.AMAZON_AUTH_SUCCESSFULLY:
                now_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.logger.log(f'[{now_date_time}] : Logged in')
                return
            case AmazonAuthHandlerEvents.AMAZON_AUTH_CAPTCHA:
                # logic for handling captcha
                pass
            

    def notify(self , event):    
        match event:
            case SeleniumDriverServiceEvents.CHAT_IS_PAUSED:
                # make somehow chat open
                # for example call `self.browser.click_on_start_new_chat_button()``
                pass
            case SeleniumDriverServiceEvents.CONNECTED_TO_CHAT:
                now_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.logger.log(f'[{now_date_time}] : Connected to chat')
                self.support_connect = True
                self.send_message()
                
                
            case SeleniumDriverServiceEvents.SUPPORT_IS_SILENT:

                if self.tries >= 3: self.skip()

                else: self.ping_support_with_message()

            case SeleniumDriverServiceEvents.RED_WINDOW:
                now_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.logger.log(f'[{now_date_time}] : Red window alert!' , LogLevels.ERROR_LEVEL)
                # handle red window
                # for example call `self.browser.reopen_new_chat()` or `self.auth.change_person()`
                pass
            case SeleniumDriverServiceEvents.FEEDBACK_IS_OPENED:
                pass

    def run(self):
        while True:   
            self.storage = AmazonStorage(self)

            self.browser.open_chat_window()
#####################
            message_from_support = self.get_message_from_support()

            if self.support_ignores : continue

            message_to_support = self.generate_message_to_support(message_from_support)

                
            if message_to_support:
                # Send my answer
                self.send_message(message_to_support)


                # Get support name
                name_indus = self.browser.get_indus_name_from_chat()

                # Make list of this step or result 
                result = {
                    "Name": f"{name_indus}",
                    "Message":f"{message_from_support}",
                    "My_answer":f"{message_to_support}",
                    "Status":f"{self.status}",
                    "Skip":f"{self.has_skipped or False}"
            }
                
            self.logger.log(result)


    def get_message_from_support(self):
        return self.browser.parse_amazon_support_chat_messages()


    def generate_message_to_support(self , message_from_support):
        category = self.browser.get_category_in_text(message_from_support)
        return self.browser.get_answer_from_category(category)


    def send_message(self, message):
        #    if <`repeats` from somewhere> < 3 as example  
        analize_category = self.analize.get_category_in_text(message)
        message_to_support = self.analize.get_answer_from_category(message)
        self.browser.send_message_to_support(message_to_support)


    def ping_support_with_message(self):
        self.browser.send_message_to_support("Hello?")
        #    self.tries += 1
        self.storage.update_storage({"tries" : (self.storage.get_by_key('tries') + 1)})
        time.sleep(5)
        return self.get_message_from_support()




    def skip(self):
        self.browser.stop_current_chat_session()
            # Skips plus
        # TODO::continue with skips logic
        # self.skips += 1
            # End connecting
        self.connect = False
