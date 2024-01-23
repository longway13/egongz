# pip install bs4
# pip install pandas
# pip install selenium
# pip install webdriver_manager

import re
import time
import json
import urllib.parse
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from openpyxl import Workbook,load_workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://everytime.kr/timetable'

# User info
USER_ID = 'km9844'
USER_PW = 'tjddbs9844'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)
driver.implicitly_wait(5)

# 로그인 정보 입력
driver.find_element(By.NAME, 'id').send_keys(USER_ID)
driver.find_element(By.NAME, 'password').send_keys(USER_PW)
driver.find_element(By.XPATH, '/html/body/div[1]/div/form/input').click()
driver.implicitly_wait(5)

# 수업 목록에서 검색 클릭
driver.find_element(By.XPATH, '//*[@id="container"]/ul/li[1]').click()
driver.implicitly_wait(6)

pre_count = 0


# #스크롤 맨아래로 내리기
while True:
    #tr요소 접근
    element = driver.find_elements(By.CSS_SELECTOR, "#subjects > div.list > table > tbody > tr")
    
    # tr 마지막 요소 접근
    result = element[-1]
    # scroll
    driver.execute_script('arguments[0].scrollIntoView(true);', result)
    time.sleep(2)

    #현재 접근한 요소의 갯수
    current_count = len(element)
    
    # 모든 요소를 load했을 때
    if pre_count == current_count:
        break
    
    # load할 요소가 남아있을 때
    pre_count = current_count
    
# links_elems : 강의 평가 페이지로 이동하는 link 요소 저장.     
links_elems = driver.find_elements(By.CSS_SELECTOR, "#subjects > div.list > table > tbody > tr > td:nth-child(9) > a")

# 현재 페이지 html code 저장.
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
trs = soup.select('#subjects > div.list > table > tbody > tr')

results = []
result_dict = {
    "grade": [],          # 학년
    "type": [],           # 종별
    "course_id": [],      # 학정번호
    "credits": [],        # 학점
    "course_name": [],    # 강의명
    "prof_name": [],      # 담당교수
    "time":[],            # 시간
    "lecture_room": [],   # 강의실
    "avg_score" : [],     # 강의 평가 점수
    "add_num": [],        # 담은 인원
    "notice": []          # 유의사항
}


        
cnt = 1;
for tr, link in zip(trs, links_elems):
    result=[]
    tds = tr.select('#subjects > div.list > table > tbody > tr > td')
    result.append(tds[0].text) #학년
    result_dict.get('grade').append(tds[0].text)
    result.append(tds[1].text) #종별
    result_dict.get('type').append(tds[1].text)
    result.append(tds[2].text) #학정번호
    result_dict.get('course_id').append(tds[2].text)
    result.append(tds[3].text) #학점
    result_dict.get('credits').append(tds[3].text)
    result.append(tds[4].text) #교과목명
    result_dict.get('course_name').append(tds[4].text)
    result.append(tds[5].text) #담당교수
    result_dict.get('prof_name').append(tds[5].text)
    result.append(tds[6].text) #강의시간
    result_dict.get('time').append(tds[6].text)
    result.append(tds[7].text) #강의실
    
    driver.execute_script("arguments[0].click();", link)
    time.sleep(2)
    # switching to new tab
    driver.switch_to.window(driver.window_handles[-1])
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
        
    # 강의 평가가 존재하지 않을 때
    avg = soup.select_one("span[class='average']").text
    # 강의 평가가 존재할 때
    print(avg)
    result.append(avg)
    result_dict.get('avg_score').append(avg)
    
    driver.close()
    # switching to previous tab
    driver.switch_to.window(driver.window_handles[0])
    print(cnt)
    cnt += 1
    
    result_dict.get('lecture_room').append(tds[7].text)
    result.append(tds[9].text) #담은인원
    result_dict.get('add_num').append(tds[9].text)
    result.append(tds[10].text) #유의사항
    result_dict.get('notice').append(tds[10].text)  
    
    results.append(result)



    
if results:
    print("성공!!")

# excel로 저장
excel_column = 11
write_wb = Workbook()
write_ws = write_wb.create_sheet('result.xls')
for data in results:
    write_ws = write_wb.active
    write_ws.append(data)
write_wb.save('C:/Users/dlatj/OneDrive/Desktop/crawling_test/result.xls')

# Json으로 저장
file_path = "./course_handbook.json"
with open(file_path, 'w', encoding='UTF-8') as json_file:
    json.dump(result_dict, json_file, indent=2, ensure_ascii=False)