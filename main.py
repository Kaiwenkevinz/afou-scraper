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

from Course import Course 

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

def time_overlaped(t1, t2):
    days1 = t1[0]
    days2 = t2[0]

    if days1 != days2:
        return False
    
    Range = namedtuple('Range', ['start', 'end'])

    tp1 = t1[1].split(" - ")
    tp2 = t2[1].split(" - ")

    tp1_a = tp1[0]
    tp1_b = tp1[1]

    tp2_a = tp2[0]
    tp2_b = tp2[1]

    FMT = '%I:%M%p'
    tp1_a_obj = datetime.strptime(tp1_a, FMT)
    tp1_b_obj = datetime.strptime(tp1_b, FMT)
    tp2_a_obj = datetime.strptime(tp2_a, FMT)
    tp2_b_obj = datetime.strptime(tp2_b, FMT)

    r1 = Range(start=tp1_a_obj, end=tp1_b_obj)
    r2 = Range(start=tp2_a_obj, end=tp2_b_obj)

    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)
    time_delta = latest_start - earliest_end

    if time_delta.days < 0:
        return True
    else:
        return False

def load_course(term, course, course_no):
    # driver = webdriver.Chrome('./chromedriver.exe')
    driver = webdriver.Chrome('./chromedriver')
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
        info_lab = []
        info_sem = []
        for class_id, section, days, times, location, open_seats, instructor, meeting_dates in data:
            course = Course(course_full, class_id, section, days, times, location, open_seats, instructor)
            if ("LEC" in section):
                info.append(course)
            elif ("SEM" in section):
                info_sem.append(course)
            elif ("LAB" in section):
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

    for combo in res:
        for c in combo:
            print(c, end='')
            print(" ^ ", end='')
        print('')


inputs = ['ECON282', 'ECON281', 'CMPUT201']
main(inputs)