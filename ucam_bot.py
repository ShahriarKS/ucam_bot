import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Open the Chrome browser automatically
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    # 2. Navigate to the UCAM login page
    driver.get("https://ucam.uiu.ac.bd/Security/Login.aspx")
    
    # 3. Wait for the login page to load
    print("Waiting for the UCAM login page to load...")
    wait = WebDriverWait(driver, 10)
    
    username_field = wait.until(EC.presence_of_element_located((By.ID, "logMain_UserName")))
    password_field = driver.find_element(By.ID, "logMain_Password")
    
    # 4. Type credentials and Login
    print("Typing credentials...")
    username_field.send_keys("0112410092") 
    password_field.send_keys("SaikatUIU1!")
    password_field.send_keys(Keys.ENTER)
    
    # 5. Wait for dashboard to fully load
    print("Waiting for dashboard to load...")
    time.sleep(8)
    print("[✔] Login successful!")

    # 6. Extract the Completed Credit using the ID you found earlier
    print("Fetching Completed Credit...")
    credit_element = driver.find_element(By.ID, "ctl00_MainContainer_Status_CompletedCr")
    completed_credit = credit_element.text
    
    # 7. Print the final result on the terminal
    print("\n====================================")
    print(f" Your Current Completed Credit: {completed_credit}")
    print("====================================\n")

except Exception as e:
    print("\n[!] An error occurred:")
    print(e)

finally:
    # Close the browser session
    driver.quit()