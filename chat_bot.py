import time
from login import AmazonLogin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AmazonChatBot:
    def __init__(self, email, password):
        self.login = AmazonLogin(email, password)
        self.current_step = None
        self.previous_message = None
        self.previous_step = None
        self.connection_support = None
    
    def run(self):
        self.login.login()
        while True:
            message = self.get_user_message()
            if message is not None:
                self.respond_to_user(message)
    
    def get_user_message(self):
        while self.connection_support:
            try:
                avatar = self.login.driver.find_element(By.CLASS_NAME,"SystemMessage__messageBody___3zi_y")
                if avatar:
                    print("Connection Good")
                    time.sleep(15)
                    support = True
                    
            except Exception as ex:
                load = self.login.driver.find_element(By.CLASS_NAME,"InitialLoadingSpinner__message-us-loader-text___19C22")
                if load:
                    print("Wait conection")
                else:
                    print("Conection not found")
        
        messages = self.login.driver.find_elements(By.CLASS_NAME,"Message__textContent___ugH_K")
        latest_message = messages[-1].text if messages else None
        return latest_message
    
    def respond_to_user(self, message):
        category, step = self.get_category_and_step(message)
        response = self.get_response(category, step)
        try:
            if category != "SKIP":
                if self.current_step_unchanged(message, step):
                    self.send_message("You help me???")
                    time.sleep(90)
                    if self.current_step_unchanged(message, step):
                        self.skip()
                else:
                    self.mark_step(step)
                    self.send_message(response)
                    self.previous_message = message
                    self.previous_step = step
                    time.sleep(35)
            else:
                self.skip()
        except:
            return 

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
        self.driver.execute_script(leave_chat_script)
        
        # Wait for the script to finish running
        self.driver.implicitly_wait(10)

        self.driver.refresh()
    
    def get_category_and_step(self, message):
        # Define the categories, keywords, and fixed steps
        categories = {
            "FIRST": {
                "keywords": ["Hi","Hello", "Hope you are doing well?", "How are you", "I'm here to help you", "help you today"],
                "step": 1
            },
            "WAIT": {
                "keywords": ["hold", "1-2 minutes"],
                "step": 2
            },
            "SKIP": {
                "keywords": ["Once completed","order number","you receive any emai","promotion link","haven't placed", "they can help you","tranlaste to department","share the link","terms", "you received any email", "order","delivered","Anything else I can assist you with today?"],
                "step": 3
            }
        }

        # Loop through the categories and keywords to find a match
        for category, values in categories.items():
            for keyword in values["keywords"]:
                if keyword in message:
                    return category, values["step"]

        # If no match is found, return None
        return None, None
    
    def get_response(self, category, step):
        # Define the responses for each step
        if category == "FIRST":
            if step == 1:
                return "Hello.I have fulfilled all the conditions of the promotion Amazon photo, but I haven't received the credit that was promised to me. This is unacceptable, and I expect a prompt resolution to this issue?Can you check?"
        elif category == "WAIT":
            if step == 2:
                return "I m wait you"
        elif category == "SKIP":
            if step == 3:
                return "Can you help me?"
        else:
            print(f"Dont know category in this {self.get_user_message()}")
    
    def mark_step(self, step):
        self.current_step = step
    
    def send_message(self, message):
        form =self.login.driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/div[3]/form/div[1]/textarea[1]")
        form.send_keys(message)
        form.send_keys(Keys.ENTER)
        
    def current_step_unchanged(self,message, step):
        # Check if the current step has changed
        return self.previous_message == message and self.previous_step == step