

class LogLevels:
    DEBUG_LEVEL = 'debug'
    WANRING_LEVEL = 'warning'
    ERROR_LEVEL = 'error'
    INFO_LEVEL = 'info'
    
class Logger:
    
    def log(message , log_level : LogLevels = LogLevels.DEBUG_LEVEL ):
        print('[{}] : {}'.format(log_level  , message))
