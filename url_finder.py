import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

#Calling the Firefox Driver
driver = webdriver.Firefox(executable_path="ENTER DRIVER PATH HERE")
site = "ENTER URL HERE"
driver.get(site)

#When going onto the StockX website for the first time it will ask you to select your country that you are in.
#This checks if that pop up comes up and clicks on the confirm button to allow you to proceed.
try:
	location_info = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/section/div/div[2]/button').click()
except Exception as e:
	print(e)
	pass

#Once you click on the confirm button for your country the website seems to reload, this time.sleep allows for this to happen without causing any errors.
#Will change this to the proper sleep method for Selenium which is with Wait.
time.sleep(3)

soup = BeautifulSoup(driver.page_source, features='lxml')

#This finds each shoes unique URL. At the moment it doesn't actually store this information anywhere.
#Planning on setting up a database for the urls to be stored in so you don't need to run this script everytime to get the URLS.
for x in soup.findAll('div', class_="tile browse-tile false"):
	for y in x.findAll('div', class_="tile Tile-c8u7wn-0 bCufAv"):
		for a in y.findAll('a', href=True):
			print(a['href'])