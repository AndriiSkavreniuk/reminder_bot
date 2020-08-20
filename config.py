from enum import Enum



token = 'token'
db_file = 'database.vdb'

class States(Enum):
    S_START = "0"
    S_ENTER_DATE = "1"
    S_GET_DATE = "2"
    #S_REMIND = "3"

