from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import os
from datetime import datetime
from collections import namedtuple
from collections import defaultdict
import itertools

from .Course import Course 



def load_course(term, course, course_no):

    # driver = webdriver.Chrome('./chromedriver')
    # driver = webdriver.Chrome('./api/chromedriver')
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

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
    time.sleep(5)

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

def main(term, inputs):
    course = 'ECON'
    course_no = '282'

    course_dic = defaultdict(list)
    for usr_in in inputs:
        course = usr_in[:len(usr_in) - 3]
        course_no = usr_in[-3:]
        course_full = course + course_no 

        data = load_course(term, course, course_no)

        info = []
        info_lab = []
        info_sem = []
        for class_id, section, days, times, location, open_seats, instructor, meeting_dates in data:
            if ("LEC" in section):
                course = Course(course_full, class_id, section, days, times, location, open_seats, instructor)
                info.append(course)
            elif ("SEM" in section):
                course_full += " SEM"
                course = Course(course_full, class_id, section, days, times, location, open_seats, instructor)
                info_sem.append(course)
            elif ("LAB" in section):
                course_full += " LAB"
                course = Course(course_full, class_id, section, days, times, location, open_seats, instructor)
                info_lab.append(course)
            else:
                print("Unknown secion: " + section)

        if info_lab:
            course_dic[course_full + "_lab"] = info_lab
        if info_sem:
            course_dic[course_full + "_sem"] = info_sem
        course_dic[course_full] = info

    # for c, info in course_dic.items():
    #     print(c)
    #     for course in info:
    #         print(course)

    course_infos = []
    for course, info in course_dic.items():
        course_infos.append(info)

    all_combos = []
    for i in itertools.product(*course_infos):
        all_combos.append(i)
    
    i = 0
    res = []
    while i < len(all_combos):
        j = 0
        k = 0
        combo = all_combos[i]
        overlapped = False
        valid = False
                
        # print('-----')
        # for c in combo:
        #     print(c, end='')
        #     print("  ", end='')
        # print('')

        while (j < len(combo) - 1) and (not overlapped):
            c1 = combo[j]
            k = j + 1
            while (k < len(combo)) and (not overlapped):
                c2 = combo[k]
                # print(c1)
                # print(c2)
                if c1 == c2:
                    # print('overlap')
                    overlapped = True
                    break
                else:
                    valid = True
                k += 1
            j += 1
        if overlapped == False and valid:
            res.append(combo)
        i += 1

    # for combo in res:
    #     for c in combo:
    #         print(c, end='')
    #         print(" ^ ", end='')
    #     print('')

    # print(len(res))
    
    return (res)



# inputs = ['ECON282', 'ECON281']
# term = '1690 - Fall Term 2019' 

# main(term, inputs)