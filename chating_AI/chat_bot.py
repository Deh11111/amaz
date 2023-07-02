import time
from account import AmazonAccount
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from filter import Filter
# import asyncio   Я бы Хотел в run(),чтобыбыло асинхроно

filter = Filter

class AmazonChatBot:
    def __init__(self, email, password):
        self.repeat = 0
        self.skips = 0
        self.login = AmazonAccount(email, password)
        self.connect = False
        self.last_message = ""
        self.email = email
        self.password = password

    def run(self):
        self.login.login()
        while True:   
            check_start = self.login.check_start()

            message = self.get_user_message()
            category = filter.get_category_by_text(message)
            answer = filter.get_answer_from_category(category)

            if answer:
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

    def get_user_message(self):
        while True:
            try:
                #####?????????????
                message_element_answer = self.login.driver.find_elements(By.CLASS_NAME, "Message__message___1YUAv.Message__agentVariant___2NLqJ")
                # waiting = self.login.driver.find_elements(By.CLASS_NAME, "SystemMessage__systemMessage___3u5N2")
                obj = len(message_element_answer)
                if obj == 0:
                    # оставть ждать чат,через continue или написать первому
                    return "None"
                #От 0 до 1
                 
                answer = ""
                # Находим блоки
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

    
    
    def check_repeat(self):
        repeat = self.repeat
        if repeat == 2:
            category = "REPEAT"
        elif repeat == 3:
            category = "REPEAT_2"
        elif repeat == 4:
            category = "REPEAT_3"

        return category
    
    

    def send_message(self, message):
        if message == "REPEAT_1":
            message_input = self.login.driver.find_elements(By.XPATH, "//textarea[@placeholder='Write a message...']")
            message_input[0].send_keys("You here")
            message_input[0].send_keys(Keys.ENTER)
            
            message_input = self.login.driver.find_elements(By.XPATH, "//textarea[@placeholder='Write a message...']")
            message_input[0].send_keys(message)
            message_input[0].send_keys(Keys.ENTER)
            time.sleep(4)
    

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

            # End connecting
            self.connect = False