import logging

class common_logger:
    
    format_string = "[%(asctime)s][%(levelname)s]" + \
                    " %(filename)s:%(lineno)d" + \
                    " %(message)s"
    
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(self.format_string)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
