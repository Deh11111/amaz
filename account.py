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

class AmazonAccount:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.status = ""
        basedir = path.abspath(path.dirname(__file__))
        gecko_path = path.join(basedir, 'geckodriver')
        urbanvpn_extension_path = path.join(basedir,'urban_vpn-3.12.1.xpi')
        
        # Create a new Firefox driver instance
        profile = FirefoxProfile()
        # Создайте экземпляр настроек Firefox Options
        options = Options()
        options.headless = True
        # Установите профиль Firefox и путь к драйверу GeckoDriver в настройках Firefox Options
        options.profile = profile
        
        profile.add_extension(urbanvpn_extension_path)
        profile.set_preference('extensions.urbanvpn.region', 'Germany')
        options = webdriver.FirefoxOptions()
        options.binary_location = "/usr/lib/firefox/firefox"
        options.set_capability('marionette', False)
        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities['marionette'] = False

        self.driver = webdriver.Firefox(firefox_profile=profile, executable_path=gecko_path,
                                        firefox_binary=options.binary_location,
                                        capabilities=capabilities,
                                        options=options)
        
        self.driver.set_window_size(300, 300)
        self.driver.set_window_position(800, 40)

    def login(self):
        self.driver.get("https://www.amazon.com/ap/signin?openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fhz%2Fcontact-us%2Fcsp%3Fref_%3Dcsl_contactus%26source%3Dcontact-us&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_contactus_desktop_us&openid.mode=checkid_setup&marketPlaceId=ATVPDKIKX0DER&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=Amazon&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=3600&siteState=clientContext%3D144-7771899-1148032%2CsourceUrl%3Dhttps%253A%252F%252Fwww.amazon.com%252Fhz%252Fcontact-us%252Fcsp%253Fref_%253Dcsl_contactus%2526source%253Dcontact-us%2Csignature%3Dj2BsGgcLWpkQTzszuxUBZuTfsFDsIj3D")
        email_input = self.driver.find_element(By.ID,"ap_email")
        password_input = self.driver.find_element(By.ID,"ap_password")
        submit_button = self.driver.find_element(By.ID,"signInSubmit")
        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        submit_button.click()
        x = True
        while x ==True:
            try:
                if 'captcha' in self.driver.page_source:
                    print("CAPTCHA")
                    captcha_ready=input('Press Enter to continue after entering the CAPTCHA...')
                    self.driver.get("https://www.amazon.com/message-us?ref_=fs_hub_gateway_mu&muClientName=foresight&paradigm=foresightBotless&callflow=964d64ad-dc95-42b5-b52c-0e791a95049b&contextData=%257B%2522customerSelectedIssues%2522%253A%25229%253A%253ASomething%2520else%253A%253A%253A57%253A%253AGifts%2520%2526%2520registries%253A%253A%253A250%253A%253AReturn%2520a%2520gift%2522%257D&returnFromLogin=1&&&&captcha_verified=1&&&captcha_verified=1&")

                    x = False
                else:
                    check_login = self.driver.find_element(By.ID,"nav-belt")
                    if check_login:
                        time.sleep(1)
                        self.driver.get("https://www.amazon.com/message-us?ref_=fs_hub_gateway_mu&muClientName=foresight&paradigm=foresightBotless&callflow=964d64ad-dc95-42b5-b52c-0e791a95049b&contextData=%257B%2522customerSelectedIssues%2522%253A%25229%253A%253ASomething%2520else%253A%253A%253A57%253A%253AGifts%2520%2526%2520registries%253A%253A%253A250%253A%253AReturn%2520a%2520gift%2522%257D&returnFromLogin=1&&&&captcha_verified=1&&&captcha_verified=1&")
                    x = False
            except Exception as ex:
                print(ex)
        self.driver.set_window_position(1000, 40)

        print("Logged in successfully.")

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
            print(f"Time {15*count} sec,{self.status}")

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
   

    

   
