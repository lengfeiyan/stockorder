# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 09:13:29 2018

@author: lengfeiyan
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
  
driver = webdriver.PhantomJS()  
driver.get('http://q.10jqka.com.cn/gn/detail/code/301490/')
#tableContent = driver.find_element_by_id('maincont').text
#nextPageEle = driver.find_elements_by_class_name('changePage')[-2]
#nextPage = nextPageEle.get_attribute('page')
#print(nextPage)
#nextPageEle.click()
driver.find_element_by_id('m-page').click();  
driver.find_elements_by_class_name('changePage')[-2].click();  
#nextPageEle.send_keys(Keys.ENTER)
newpage = WebDriverWait(driver, 10).until(  
            EC.presence_of_element_located((By.ID, "maincont"))  
        )
time.sleep(3)
#tableContent = newpage.find_element_by_id('maincont').text
print(newpage.text)
driver.quit()