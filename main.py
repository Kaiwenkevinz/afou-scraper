from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import os

from collections import defaultdict

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

def load_course(term, course, course_no):
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get('https://www.beartracks.ualberta.ca/psc/uahegprd/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?')

    # term
    select = Select(driver.find_element_by_id('CLASS_SRCH_WRK2_STRM$35$'))
    select.select_by_visible_text(term)
    time.sleep(2)

    # course category
    inputCategory = driver.find_element_by_id("ZSS_DERIVED_SUBJECT$0")
    inputCategory.send_keys(course)

    # course number
    inputElement = driver.find_element_by_id("SSR_CLSRCH_WRK_CATALOG_NBR$1")
    inputElement.click()
    inputElement.send_keys(course_no)
    time.sleep(1)
    inputElement.send_keys(Keys.ENTER)
    time.sleep(3)

    table = driver.find_element_by_id("ACE_$ICField48$0")
    tds = table.find_elements_by_xpath("//td[@class='PSLEVEL3GRIDROW']")

    res = []
    temp = []
    for td in tds:
        text = td.text
        if (text == ''):
            res.append(temp)
            temp = []
        else:
            temp.append(text)

    return res

def main(input):
    term = '1690 - Fall Term 2019'
    course = 'ECON'
    course_no = '282'

    course_dic = defaultdict(list)
    for usr_in in inputs:
        course = usr_in[:len(usr_in) - 3]
        course_no = usr_in[-3:]
        course_full = course + course_no 

        data = load_course(term, course, course_no)

        info = []
        for class_id, section, days, times, location, open_seats, instructor, meeting_dates in data:
            info.append([days, times, location, instructor])
        course_dic[course_full] = info

    for course, info in course_dic.items():
        print (course)
        print (info)
        
inputs = ['ECON281', 'ECON282']
main(inputs)