import schedule
import time
import main

#create function for reminder
schedule.every(1).days.do(main.remind(), main.overwritting())


while True:
    schedule.run_pending()
    time.sleep(1)
