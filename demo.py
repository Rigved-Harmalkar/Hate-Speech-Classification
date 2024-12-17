from Hate.logger import logging
from Hate.exception import CustomException
import sys



# logging.info("Welcome to our Project")

try:
    a = 7 / "0"
    
except Exception as e:
    raise CustomException(e,sys) from e