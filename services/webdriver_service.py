import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from os import path
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

from auth.account import AmazonAuthHandlerEvents
from chating_AI.chat_bot import AmazonChatBot

class WebDriverServiceEvents:
    CONNECTED_TO_CHAT = 'connected!'
    CHAT_IS_PAUSED = 'paused'
    SUPPORT_IS_SILENT = 'no anwser'
    FEEDBACK_IS_OPENED = 'feedback opened'
    RED_WINDOW = 'red window'
    SUPPORT_IS_IGNORING = 'support ignoring'



class WebDriverService:

    webdriver = None

    AMAZON_SPINNER_SELECTOR = "LoadingSpinner__loadingGraphic___1no8h"
    AMAZON_ERROR_OVERLAY_SELECTOR = "ErrorOverlay__errorOverlay___3RAac"
    AMAZON_CHAT_INPUT_SELECTOR = "ChatInput__chatInputRow___1HmKN"
    AMAZON_START_NEW_CHAT_BUTTON_SELECTOR = "Interstitial__buttonInput___39Z4o"
    AMAZON_FEEDBACK_PAGE_LINK_SELECTOR = "a-size-base a-color-state"
    AMAZON_SUPPORT_CHAT_MESSAGE_SELECTOR = "Message__message___1YUAv.Message__agentVariant___2NLqJ"
    AMAZON_SUPPORT_CHAT_MESSAGE_TEXT_SELECTOR = "Message__textContent___ugH_K"
    AMAZON_INDUS_CHAT_NAME_SELECTOR = "Message__messageDisplayName___1U_jv"

    LEAVE_CHAT_SCRIPT = """
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


    AUTH_WITH_REDIRECT_TO_CONTACT_PAGE_URL = "https://www.amazon.com/ap/signin?openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fhz%2Fcontact-us%2Fcsp%3Fref_%3Dcsl_contactus%26source%3Dcontact-us&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_contactus_desktop_us&openid.mode=checkid_setup&marketPlaceId=ATVPDKIKX0DER&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=Amazon&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=3600&siteState=clientContext%3D144-7771899-1148032%2CsourceUrl%3Dhttps%253A%252F%252Fwww.amazon.com%252Fhz%252Fcontact-us%252Fcsp%253Fref_%253Dcsl_contactus%2526source%253Dcontact-us%2Csignature%3Dj2BsGgcLWpkQTzszuxUBZuTfsFDsIj3D"
    CONTACT_SUPPORT_PAGE_URL = "https://www.amazon.com/message-us?ref_=fs_hub_gateway_mu&muClientName=foresight&paradigm=foresightBotless&callflow=964d64ad-dc95-42b5-b52c-0e791a95049b&contextData=%257B%2522customerSelectedIssues%2522%253A%25229%253A%253ASomething%2520else%253A%253A%253A57%253A%253AGifts%2520%2526%2520registries%253A%253A%253A250%253A%253AReturn%2520a%2520gift%2522%257D&returnFromLogin=1&&&&captcha_verified=1&&&captcha_verified=1&"
    AMAZON_AUTHENTICATED_NAVBAR_SELECTOR = "nav-belt"

    def __init__(self , mediator : AmazonChatBot):
        

        # options = Options()
        # options.headless = True
        # options.profile = profile
        # перезапись options
        _options = webdriver.FirefoxOptions()
        _basedir = path.abspath(path.dirname(__file__))
        _gecko_path = path.join(_basedir, 'geckodriver')
        # _urbanvpn_extension_path = path.join(_basedir,'urban_vpn-3.12.1.xpi')

        _profile = FirefoxProfile()
        _options.binary_location = "/usr/lib/firefox/firefox"
        _options.set_capability('marionette', False)

        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities['marionette'] = False
        self.webdriver = webdriver.Firefox(firefox_profile=_profile, executable_path=_gecko_path,
                                        firefox_binary=_options.binary_location,
                                        capabilities=capabilities,
                                        options=_options)
        self.chatbot = mediator


   


    def open_and_submit_login(self  , email ,password):
        self.webdriver.set_window_size(300, 300)
        self.webdriver.set_window_position(800, 40)
        self.webdriver.get(self.AUTH_WITH_REDIRECT_TO_CONTACT_PAGE_URL)
        email_input = self.webdriver.find_element(By.ID,"ap_email")
        password_input = self.webdriver.find_element(By.ID,"ap_password")
        submit_button = self.webdriver.find_element(By.ID,"signInSubmit")
        email_input.send_keys(email)
        password_input.send_keys(password)
        submit_button.click()

        self.wait_auth_response()

               
    def wait_auth_response(self):
        if(self.chatbot is None): return
        
        while True:
            if 'captcha' in self.webdriver.page_source:
                self.chatbot.notify(AmazonAuthHandlerEvents.AMAZON_AUTH_CAPTCHA) ; break
        
            if self.webdriver.find_elements(By.ID, self.AMAZON_AUTHENTICATED_NAVBAR_SELECTOR):
                time.sleep(1)
                self.chatbot.notify(AmazonAuthHandlerEvents.AMAZON_AUTH_SUCCESSFULLY) ; break
        
        self.webdriver.set_window_position(1000, 40)
        



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
                return self.chatbot.notify(WebDriverServiceEvents.CONNECTED_TO_CHAT)
            except:
                pass

            try:
                leave_support_txt = "The chat is paused due to inactivity. To continue, start typing and an associate who knows your issue will join."
                element = self.webdriver.find_element(By.XPATH, "//*[contains(text(), '{}')]".format(leave_support_txt))
                if leave_support_txt.strip().lower() == element.text.strip().lower() :
                    return self.chatbot.notify(WebDriverServiceEvents.CHAT_IS_PAUSED)
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
                return self.chatbot.notify(WebDriverServiceEvents.RED_WINDOW)
            except:
                pass
            # Checking feedback page 
            try:
                feedback = self.webdriver.find_element(By.CLASS_NAME, self.AMAZON_FEEDBACK_PAGE_LINK_SELECTOR)
                return self.chatbot.notify(WebDriverServiceEvents.FEEDBACK_IS_OPENED)
            except:
                pass
            tries += 1
            # if tries == 7:
            #     self.login.driver.close()
            #     self.login.driver.quit()
            #     result = "Count > 7. Change Vpn and restart"
            
            # print(f"Time {15*count} sec,{self.status}")


    def parse_amazon_support_chat_messages(self):
        try:
            message_element_answer = self.webdriver.find_elements(By.CLASS_NAME, self.AMAZON_SUPPORT_CHAT_MESSAGE_SELECTOR)
            # waiting = self.login.driver.find_elements(By.CLASS_NAME, "SystemMessage__systemMessage___3u5N2")
            if len(message_element_answer) == 0:
                self.send_message_to_support("Hello.From what team are you?")
                time.sleep(7)
                pass
            #От 0 до 1
             
            answer = ""
            # Находим блоки
            for one in message_element_answer:
                div_text = one.find_elements(By.CLASS_NAME, self.AMAZON_SUPPORT_CHAT_MESSAGE_TEXT_SELECTOR)[-1]
                answer_text = div_text.text
                if answer_text is None:
                    continue
                answer += answer_text
            answer = " ".join(answer.split())  
            
            return answer
            
        except:
            pass
        

    def get_indus_name_from_chat(self):
        return self.webdriver.find_elements(By.CLASS_NAME,self.AMAZON_INDUS_CHAT_NAME_SELECTOR )[-1]
    
    def send_message_to_support(self  , message):
        message_input = self.webdriver.find_elements(By.XPATH, "//textarea[@placeholder='Write a message...']")
        message_input[0].send_keys(message)
        message_input[0].send_keys(Keys.ENTER)
        time.sleep(4)


    def stop_current_chat_session(self):
        leave_chat_script = self.LEAVE_CHAT_SCRIPT
        self.webdriver.execute_script(leave_chat_script)
            
        # Wait for the script to finish running
        self.webdriver.implicitly_wait(10)
        time.sleep(1.7)
        self.webdriver.refresh()


            


   
    

            

        