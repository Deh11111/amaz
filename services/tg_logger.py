from logger import Logger , LogLevels
import telebot


class TgLogger(Logger):
    def log(message, log_level: LogLevels = LogLevels.DEBUG_LEVEL):
         super().log(message , log_level)
