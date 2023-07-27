from selenium.webdriver.common.by import By
from services.auth import check_start

class AmazonStorage:
    def __init__(self , mediator):
        self.skips = 0
        self.repeated = False
        self.count = 0
        self.mediator = mediator
        self.last_message = None
        self.current_message = None
        self.tries = 0
        self.support_ignores = False
        self.status = check_start()


    def update_storage(self , **kwargs):
        for key , value in kwargs.items():
            try: setattr(self , key , value)
            except AttributeError:
                continue

    def get_by_key(self  , key):
        return getattr(self , key)


    

   