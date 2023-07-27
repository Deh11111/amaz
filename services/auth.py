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
from services.selenium_web import SeleniumDriverService
from ..chating_AI.chat_bot import AmazonChatBot

class AmazonAuthHandlerEvents:
    AMAZON_AUTH_CAPTCHA = 'captcha'
    AMAZON_AUTH_SUCCESSFULLY = 'signed up!'


class AmazonAuthHandler:

    def __init__(self , mediator : AmazonChatBot):
        # self.status = ""
        self.driver = SeleniumDriverService()
        self.mediator = mediator

    def login(self , email, password ):
        self.driver.open_and_submit_login(email ,  password)
        

   

    def check_frode(self,skips,count):
        if skips > 4 or count > 10:
            self.change_person()

            
    def change_person(self):
        ua = UserAgent()
        # Генерация случайного User-Agent'а для телевизора      tv_user_agent = ua.tv
        # Генерация случайного User-Agent'а для ПК
        pc_user_agent = ua.random

        self.header_overrides = {
            'User-Agent': pc_user_agent  # Замените на tv_user_agent, если нужен User-Agent для телевизора
        }

        # Получение текущего прокси-сервера и порта
        proxy_server = self.proxy.host
        proxy_port = self.proxy.port
        print(proxy_port)
        print(proxy_server)

    def __del__(self):
        self.driver.quit()



# auth_helper.py or webdriver_auth_worker.py?


   

    

   
