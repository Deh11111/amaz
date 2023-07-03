from selenium.webdriver.common.by import By
from filter import Filter

filter = Filter()
class AmazonStorage:
    def __init__(self):
        self.skips = 0
        self.repeat = 0
        self.count = 0
        self.last_message = None
        self.current_message = None

    def extract_text_from_blocks(self,blocks):

        if blocks is None:
           return False
        
        for block in blocks:
            div_text = block.find_elements(By.CLASS_NAME, "Message__textContent___ugH_K")[-1]
            answer_text = div_text.text
            answer += answer_text

        answer = " ".join(answer.split())  
        
        return answer

    def filter_from_answer(self,answer):

        category = filter.get_category_in_text(answer)
        answer = filter.get_answer_from_category(category)

        return answer

   