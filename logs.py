import time
import sys
import logging


logger = logging.getLogger(__name__)
logfile = "coffee_log.log"

formatter = logging.Formatter('%(asctime)s - %(name)s : %(threadName)s - %(levelname)s - %(message)s')
screen_handler = logging.StreamHandler(sys.stdout)
screen_handler.setLevel(logging.DEBUG)
screen_handler.setFormatter(formatter)

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(screen_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

start_time = time.time()