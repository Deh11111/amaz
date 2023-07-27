from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from fake_useragent import UserAgent
from os import path
from services.selenium_web import SeleniumDriverService,SeleniumDriverServiceEvents
from ..chating_AI.chat_bot import AmazonChatBot

class ChatWindowHandlerEvents:
    CHAT_IS_PAUSED = 'paused'
    RED_WINDOW = 'red window'

class ChatWindowService:

    def __init__(self , mediator : AmazonChatBot):
        self.driver = SeleniumDriverService()
        self.mediator = mediator

    def open_chat_window(self):
        if(self.chatbot == None): return

        tries = 0
        while tries < 15:  # Добавляем ограничение на количество попыток
            try:
                load = WebDriverWait(self.webdriver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, self.AMAZON_SPINNER_SELECTOR)))
                continue  # если элемент load найден, начинаем цикл заново
            except:
                pass  # если элемент load не найден, проверяем наличие элементов form и error

            try:
                form = self.webdriver.find_element(By.CLASS_NAME,self.AMAZON_CHAT_INPUT_SELECTOR)
                return self.chatbot.notify(SeleniumDriverServiceEvents.CONNECTED_TO_CHAT)
            except:
                pass

            try:
                leave_support_txt = "The chat is paused due to inactivity. To continue, start typing and an associate who knows your issue will join."
                element = self.webdriver.find_element(By.XPATH, "//*[contains(text(), '{}')]".format(leave_support_txt))
                if leave_support_txt.strip().lower() == element.text.strip().lower() :
                    return self.chatbot.notify(SeleniumDriverServiceEvents.CHAT_IS_PAUSED)
            except:
                pass

            # Checking button?
            try:
                new_chat = self.webdriver.find_element(By.CLASS_NAME, self.AMAZON_START_NEW_CHAT_BUTTON_SELECTOR)
                new_chat.click()
                continue
            except:
                pass
            # Checking red window 
            try:
                error = self.webdriver.find_element(By.CLASS_NAME, self.AMAZON_ERROR_OVERLAY_SELECTOR )
                return self.chatbot.notify(SeleniumDriverServiceEvents.RED_WINDOW)
            except:
                pass
            # Checking feedback page 
            try:
                feedback = self.webdriver.find_element(By.CLASS_NAME, self.AMAZON_FEEDBACK_PAGE_LINK_SELECTOR)
                return self.chatbot.notify(SeleniumDriverServiceEvents.FEEDBACK_IS_OPENED)
            except:
                pass
            tries += 1
            # if tries == 7:
            #     self.login.driver.close()
            #     self.login.driver.quit()
            #     result = "Count > 7. Change Vpn and restart"
            
            # print(f"Time {15*count} sec,{self.status}")