import pytz
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytz import timezone
import datetime 
from dotenv import dotenv_values
import os
from playsound import playsound


dir_path = "C:/Users/Hammad/Desktop/py-selenium"

env_config = dotenv_values(dir_path + "/.env")

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
        "CPC151" : "189298",
        "CPC152" : "181772" if format_day == 'Tuesday' else "181767",
        "CPC152-T" : "161333"
    }



url_id = url_params_dict[user_course]


print(user_course)
print(f"Day -> {format_day}")
print(f"PC sleep -> {sleep}")


bool_check = True

while (bool_check):
    my_full_date_time = datetime.datetime.now().astimezone(tz)
    format_time = my_full_date_time.strftime(time_fmt)
    format_date = my_full_date_time.strftime(date_fmt)
    

    time.sleep(5)

    if(user_time == format_time):

        try:

            login_url = "https://login.usm.my/adfs/ls/?wa=wsignin1.0&wct=2022-04-17T03%3A25%3A00Z&wtrealm=urn%3Afederation%3Aelearning.usm.my&wctx=OmVsZWFybmluZy51c20ubXk6c2lkYW5nMjEyMg%3D%3D"

            attendance_link =  "https://elearning.usm.my/sidang2122/mod/attendance/view.php?id={}"
            attendance_link = attendance_link.format(url_id)

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--headless")


            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                
            
            browser.get(login_url)

            browser.find_element(By.ID, value="userNameInput").send_keys(env_config['EMAIL'])
            browser.find_element(By.ID, value="passwordInput").send_keys(env_config['PASSWORD'])
            browser.find_element(By.ID, value="submitButton").click()

            browser.get(attendance_link)


            browser.find_element(By.LINK_TEXT, value="Submit attendance").click()

            if(user_course == 'CPC152' or user_course == 'CPC152T'):
                browser.find_element(By.ID, value="id_studentpassword").send_keys(user_course)
                browser.find_element(By.ID, value="id_submitbutton").click()


            print("Attendance registered on ", format_date, "; ", format_time)

            # for playing mp3 file
            playsound(dir_path + "/attendance-successful.wav")
            bool_check = False

            time.sleep(10)

                
            if(sleep):
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            sys.exit()
        
        except Exception as e:
            bool_check = False
            playsound(dir_path + "/attendance-error.wav")
            print(e)
            
        finally:
            bool_check = False
            sys.exit()
        
        

        
        


