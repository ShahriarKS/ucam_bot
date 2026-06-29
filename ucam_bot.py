import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HISTORY_FILE = "grades_history.json"
CHECK_INTERVAL_MINUTES = 30  # Adjust the gap time here (in minutes)

def check_ucam_results():
    # Fetch current computer time
    current_time_str = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    print(f"\n[🔄] {current_time_str} - Checking UCAM for updates...")

    # 1. Initialize Chrome in Headless Mode (Hidden Browser)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Runs Chrome in the background
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    try:
        # 2. Navigate to login
        driver.get("https://ucam.uiu.ac.bd/Security/Login.aspx")
        wait = WebDriverWait(driver, 10)
        
        username_field = wait.until(EC.presence_of_element_located((By.ID, "logMain_UserName")))
        password_field = driver.find_element(By.ID, "logMain_Password")
        
        # 3. Login
        username_field.send_keys("0112410092") 
        password_field.send_keys("SaikatUIU1!")
        password_field.send_keys(Keys.ENTER)
        
        # 4. Wait for dashboard and fetch CGPA/Credits
        dashboard_wait = WebDriverWait(driver, 20)
        cgpa_element = dashboard_wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContainer_Status_CGPA")))
        credit_element = driver.find_element(By.ID, "ctl00_MainContainer_Status_CompletedCr")
        
        overall_cgpa = cgpa_element.text.strip()
        completed_credit = credit_element.text.strip()
        
        # 5. Move to Course History
        course_history_url = "https://ucam.uiu.ac.bd/Student/StudentCourseHistory.aspx?mmi=40545a1642555b514e63"
        driver.get(course_history_url)
        time.sleep(5)
        
        # 6. Parse Table Rows
        rows = driver.find_elements(By.CSS_SELECTOR, "#ctl00_MainContainer_gvRegisteredCourse tr.rowCss")
        
        latest_trimester = 0
        valid_rows_data = []
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 6:
                tri_code_text = cols[0].text.strip()
                if tri_code_text.isdigit():
                    tri_code = int(tri_code_text)
                    if tri_code > latest_trimester:
                        latest_trimester = tri_code
                    valid_rows_data.append((tri_code, cols))

        # 7. Load History and Compare
        prev_grades = {}
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                prev_grades = json.load(f)

        current_grades = {}
        new_updates = []
        latest_courses_list = []
        
        for tri_code, cols in valid_rows_data:
            if tri_code == latest_trimester:
                course_code = cols[1].text.strip()
                course_name = cols[2].text.strip()
                grade = cols[4].text.strip()
                status = cols[5].text.strip()
                
                current_grades[course_code] = grade
                latest_courses_list.append((course_code, course_name, grade, status))
                
                # Grade checking logic
                if course_code in prev_grades:
                    if prev_grades[course_code] != grade and grade != "":
                        new_updates.append(f"{course_code} - {course_name} (New Grade: {grade})")
                elif grade != "":
                    new_updates.append(f"{course_code} - {course_name} (Grade: {grade})")

        # Save history for next loop
        with open(HISTORY_FILE, "w") as f:
            json.dump(current_grades, f)

        # 8. PRINT THE REPORT TO TERMINAL
        print("==============================================")
        print("         UCAM ACADEMIC SUMMARY REPORT         ")
        print("==============================================")
        print(f" 🎯 Overall CGPA      : {overall_cgpa}")
        print(f" 🎓 Completed Credit : {completed_credit}")
        
        if new_updates:
            print("----------------------------------------------")
            for update in new_updates:
                print(f" ✨ NEW UPDATE DETECTED AT {datetime.now().strftime('%I:%M %p')} -> {update}")
        else:
            print(" 🔍 No new grade updates detected since last check.")
            
        print("----------------------------------------------")
        print(f" 📅 Current Trimester Status: {latest_trimester}")
        print("----------------------------------------------")
        
        for course_code, course_name, grade, status in latest_courses_list:
            final_grade = grade if grade else status
            print(f" 📖 {course_code} - {course_name} | Grade/Status: {final_grade}")
                    
        print("==============================================")
        print(f"😴 Sleeping for {CHECK_INTERVAL_MINUTES} minutes... Bot will check again automatically.")

    except Exception as e:
        print(f"\n[!] An error occurred during this check: {e}")
    finally:
        driver.quit()

# Infinite loop to keep the bot running continuously
if __name__ == "__main__":
    print("🤖 UCAM Auto-Monitor Bot is now active!")
    print("Press 'Ctrl + C' in the terminal anytime to stop the bot.")
    
    while True:
        check_ucam_results()
        # Convert minutes to seconds for time.sleep
        time.sleep(CHECK_INTERVAL_MINUTES * 60)