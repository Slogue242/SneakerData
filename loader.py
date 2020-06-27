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
import sqlite3

checker = True

#Calling Firefox as driver to run headless
driver = webdriver.Firefox(executable_path="ENETER DRIVER PATH HERE")
#Loading wellington rubbish website
site = "ENTER PAGE URL HERE"
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

#This clicks on the sales data button on the shoes webpage.
click_on_sales = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[3]/a').click()

#This is to allow the sales data to load. I found this sometimes takes a while and will cause the program to error out since it won't be able to find the "Load More" button.
time.sleep(15)

#This find the "Load More" button and clicks it can be found.
#If it can't then set checker to False and move on.
while checker == True:
	try:
		time.sleep(5)
		if not driver.find_element_by_xpath('//button[text()="Load More"]'):
			pass
		elif load_page := driver.find_element_by_xpath('//button[text()="Load More"]'):
			load_page.click()
		else:
			pass
	except Exception as e:
		checker = False
		pass

soup = BeautifulSoup(driver.page_source, features='lxml')

#Grabs the first table that can be found in the source code.
table = soup.find_all('table')[0]

data = []

row_marker = 0
#Goes through the contents of the table that was found and strips out any of the tags and appends it to the list called data.
for row in table.find_all('tr'):
    columns = row.find_all('td')
    for column in columns:
        new_string = column.string.strip("</td>")
        data.append(new_string)

#This is to move all the data in the list to a database so it can be worked with on other scripts.
print("Opening Database.")
conn = sqlite3.connect('sneakers.db')
print("Database opened.")

c = conn.cursor()

print("Committing data now. Please wait.")

for i in range(0,len(data), 4):
	c.execute("INSERT INTO desert_ore VALUES (?,?,?,?)", (data[i], data[i+1], data[i+2], data[i+3]))
	conn.commit()

print("Data committed to database.")
conn.close()
print("Connection closed.")
