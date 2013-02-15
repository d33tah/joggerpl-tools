import logging

format_string = "[%(asctime)s][%(levelname)s]" + \
                " %(filename)s:%(lineno)d" + \
                " %(message)s"

def common_logger(name):
    
    global format_string
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format_string)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
