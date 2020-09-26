from enum import Enum
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


token = os.environ.get('bot_token')
db_file = os.environ.get('db')


class States(Enum):
    S_START = "0"
    S_ENTER_DATE = "1"
    S_GET_DATE = "2"
    # S_REMIND = "3"
