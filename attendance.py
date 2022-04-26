import pytz
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pytz import timezone
import datetime 
from dotenv import dotenv_values
import os

env_config = dotenv_values(".env")
utc = pytz.utc
tz = timezone('Asia/Kuala_Lumpur')
time_fmt = '%H:%M'
date_fmt = '%Y-%m-%d'
day_fmt = '%A'

my_full_day = datetime.datetime.now().astimezone(tz)
format_day = my_full_day.strftime(day_fmt)



user_course = sys.argv[1]
user_time = sys.argv[2]

sleep = False

try:
    if (sys.argv[3] =='sleep'):
        sleep = True
except:
    pass


url_params_dict = {
        "CST235" : "151073",
        "CPT113" : "127135",
        "CPT113-T" : "127136",
        "SEA205E" : "159798",
        "CPC151" : "129769",
        "CPC152" : "134280" if format_day == 'Tuesday' else "134252",
        "CPC152-T" : "161333"
    }



url_id = url_params_dict[user_course]


print(user_course)
print("Day ->", format_day)
print(f"PC sleep -> {sleep}")

while (True):
    my_full_date_time = datetime.datetime.now().astimezone(tz)
    format_time = my_full_date_time.strftime(time_fmt)
    format_date = my_full_date_time.strftime(date_fmt)
    

    time.sleep(5)

    if(user_time == format_time):

        login_url = "https://login.usm.my/adfs/ls/?wa=wsignin1.0&wct=2022-04-17T03%3A25%3A00Z&wtrealm=urn%3Afederation%3Aelearning.usm.my&wctx=OmVsZWFybmluZy51c20ubXk6c2lkYW5nMjEyMg%3D%3D"

        attendance_link =  "https://elearning.usm.my/sidang2122/mod/attendance/view.php?id={}"
        attendance_link = attendance_link.format(url_id)

        driver = webdriver.Chrome("C:/Users/Hammad/Desktop/py-selenium/chromedriver_win32/chromedriver.exe")
        driver.get(login_url)

        driver.find_element(By.ID, value="userNameInput").send_keys(env_config['EMAIL'])
        driver.find_element(By.ID, value="passwordInput").send_keys(env_config['PASSWORD'])
        driver.find_element(By.ID, value="submitButton").click()

        driver.get(attendance_link)


        driver.find_element(By.LINK_TEXT, value="Submit attendance").click()

        if(user_course == 'CPC152' & format_day != 'Tuesday'):
            driver.find_element(By.ID, value="id_studentpassword").send_keys(user_course)
            driver.find_element(By.ID, value="id_submitbutton").click()


        print("Attendance registered on ", format_date, "; ", format_time)
        
        time.sleep(10)

        
        if(sleep):
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        sys.exit()


