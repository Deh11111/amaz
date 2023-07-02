import telebot

class TelegramAccount:
    def __init__(self):
        self.repeat = 0
        self.skips = 0
        self.bot_tg = telebot.TeleBot("5900799199:AAGggfpyJlSDP3Hl1SUmDTYj6ZNaf7Mvyrs")

    def send_message_tg(self,data):
        self.bot_tg.send_message(544591866,f"'Status':'{data['Status']}',\n'Message':'{data['Message']}',\n'Skips':'{data['Skip']}',\n'My_answer':'{data['My_answer']}'")

    def one_signal_tg(self):
        self.bot_tg.send_message(544591866,f"'Paused!")
