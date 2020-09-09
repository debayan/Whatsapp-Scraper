from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re
import time 
import csv
import geckodriver_autoinstaller


geckodriver_autoinstaller.install() 

LAST_MESSAGES = 4
WAIT_FOR_CHAT_TO_LOAD = 2 # in secs

message_dic = {}
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 600)

def chats():
    name = driver.find_element_by_xpath("//div[@class='DP7CM']/span").text
    print("name",name)
    message_dic[name] = []
    messages = driver.find_elements_by_xpath("//div[@class='_274yw']")
    #print(messages)
    for message in messages:
        nametimestamphtml = message.get_attribute('innerHTML')
        #print("nametimestamphtml : ", nametimestamphtml)
        nametimestamp = re.search('data-pre-plain-text=\"\[(.+?): \">', nametimestamphtml).group(1)
        print("nametimestamp:", nametimestamp)
        messagehtml = message.find_element_by_xpath(".//div[@class='eRacY']").get_attribute('innerHTML')
        #print(messagehtml)
        rem = re.search('span>(.*?)</span>', messagehtml)
        message = None
        if rem:
            message = rem.group(1)
            print('message : ', message)
        else:
            message = '<emoji>'
            print('emoji')
        message_dic[name].append((nametimestamp,message))

def scrape(prev):
    recentList = driver.find_elements_by_xpath("//div[@class='_210SC']")
    #recentList.sort(key=lambda x: int(x.get_attribute('style').split("translateY(")[1].split('px')[0]), reverse=False)

    next_focus = None
    start = 0
    print("recentList", recentList)
    for idx,tab in enumerate(recentList):
        if tab == prev:
            start = idx
            break

    for l in recentList[start:]:
        l.click()
        time.sleep(WAIT_FOR_CHAT_TO_LOAD)
        while True:
            res = driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
            begin = None
            try:
                begin = driver.find_element_by_xpath("//div[@class='_3sKvP']")
            except Exception as e:
                print("Top not yet found, scroll up ...")
            if begin:
                print("Top reached")
                break
            time.sleep(1)
        chats()
        next_focus = l
    if prev == next_focus:
        return
    scrape(next_focus)

def save_to_csv():
    rows = [[key]+message_dic[key] for key in message_dic]

    with open('chats.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(rows)
    writeFile.close()

if __name__ == '__main__':
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)
    
    x_arg = '//img[@class="Qgzj8 gqwaM"]'
    #group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    time.sleep(10)
    scrape(None)
    save_to_csv()
