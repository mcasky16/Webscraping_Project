#Here we import required selenium components
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

#Here we import time to control the time
import time

#Here we define the driver and the path
driver = webdriver.Chrome(executable_path="C:\\Program Files (x86)\\chromedriver.exe")

#Here we define the webpage to be scrapped
driver.get("https://homes.com")

#Since the aim of the project is to scrap data for houses in virginia beach only,
#here the scrapper enters the criteria in to the search bar
search_city = driver.find_element_by_xpath("//*[@id='root']/main/div[1]/section/div/section[1]/form/div[2]/div[1]/input")
time.sleep(2)
search_city.send_keys("Virginia Beach")
time.sleep(2)
search_city.send_keys(Keys.RETURN)

#Empty lists are created to store all scrapped data 
title_list = []
price_list = []
Nbed_list = []
Nbath_list = []
Nsize_list = []
loc_list = []
link_list = []

#The count and click variables are defined to control the pagination and the number of pages to be scrapped.
count = 0   #counts the number of pages once the next button is clicked
click = True  #This controls whether the scrapper should still continue or quit. True is to continue, False is to quit

#Here is when the scrapping starts
def start():
	global title_list #All the empty lists were declared global for it to be used whilst outside the start() function
	global price_list
	global Nbed_list
	global Nbath_list
	global Nsize_list
	global loc_list
	global link_list
	global dict_M
	global count
	if count < 100:  #Here you can limit the number of pages to be scrapped. Default has been set to 100 as required

		try:
			class_item = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.CLASS_NAME,"c12kybvb"))
			)
			time.sleep(3)
			ads = class_item.find_element(By.TAG_NAME,"article")
		
		except:
			driver.quit()	#This exception quits the driver when the items to scrap fail to load on an instance

		time.sleep(2)

		#All information to be scrapped were defined here by XPATHS
		info_show = ads.find_element(By.XPATH,"//*[@id='root']/main/div[1]/section/div/section/section[1]/div[1]/div[2]/article[1]/button[2]")
		info_show.click()
		prices = ads.find_elements(By.XPATH,"//*[@id='root']/main/div[1]/section/div/section/section[1]/div[1]/div[2]/article/span/div[2]/div[1]/span[1]")
		details = ads.find_elements(By.XPATH,"//*[@id='root']/main/div[1]/section/div/section/section[1]/div[1]/div[2]/article/span/div[2]/div[2]")
		titles = ads.find_elements(By.XPATH,"//*[@id='root']/main/div[1]/section/div/section/section[1]/div[1]/div[2]/article/span/div[2]/div[3]")
		prop_url = ads.find_elements(By.XPATH,"//*[@id='root']/main/div[1]/section/div/section/section[1]/div[1]/div[2]/article/span/div[2]/a")
		links = [url.get_attribute('href') for url in prop_url]
		locs = ads.find_elements(By.XPATH,"//*//*[@id='root']/main/div[1]/section/div/section/section[1]/div[1]/div[2]/article/span/div[2]/a/div")


		#Here are the codes to print out results in the terminal before rendering is into a csv file.
		#Remove comment from print functions in this section to view the results in terminal whilst scrapping
		for link in links:
			#print(link)
			
			link_list.append(link)
		for loc in locs:
			#print(loc.text)
			
			loc_list.append(loc.text)

		for title in titles:
			#print(title.text)
			
			title_list.append(title.text)

		for price in prices:
			#print(price.text)
			
			price_list.append(price.text)

		for detail in details:
			#Here we used the try and exception to control the listings where some information were missing 
			try:
				Nbed = detail.text.split(" | ")[0]
				Nbed_num = Nbed.split(" ")[0]
				#print(Nbed_num)
				
				Nbed_list.append(Nbed_num)
			except:
				Nbed = "N/A"
				Nbed_num = "N/A"
				#print(Nbed_num)
				
				Nbed_list.append(Nbed_num)


			try:
				Nbath = detail.text.split(" | ")[1]
				Nbath_num = Nbath.split(" ")[0]
				#print(Nbath_num)
				
				Nbath_list.append(Nbath_num)
			except:
				Nbath = "N/A"
				Nbath_num = "N/A"
				#print(Nbath_num)
				
				Nbath_list.append(Nbath_num)

			try:
				size = detail.text.split(" | ")[2]
				Nsize = size.split(" ")[0]
				#print(Nsize)
				
				Nsize_list.append(Nsize)

			except:
				size = "N/A"
				Nsize = "N/A"
				#print(Nsize)
				
				Nsize_list.append(Nsize)
		

			#Here we use the try and exception to control the pagination 
		try:
			next_button = driver.find_element_by_css_selector("#root > main > div.page.page--full-width.search-results > section > div > section > section.c11plm64.relative.overflow-y-scroll.momentum-scroll.n19kvjwb > div.flex.items-center.justify-center.my-2 > a.flex.items-center.justify-center.radius-5.border-1.border-gray-lighter.bngq86v.bg-gray.ml-1.w1pflkr")
			time.sleep(2)
			next_button.click()
		except:
			global click
			click = False #Sets the click value to false when no button was clicked for the next page. This quits the program
			print("MAXIMUM OF ",count," PAGE(S) SCRAPPED")

		if click == True:
			count += 1

		print("Page ",count," scrapped") # This informs the user the current number of pages that has been scrapped

	else:
		print("MAXIMUM OF ",count," PAGE(S) SCRAPPED") # This informs the user the total pages scrapped
		click = False

#Here, the loop is controlled by the next page click value. If there is still a next page that is lesser than the
#max defined, the scrapper starts again on that page. If it it quits. 
while click:
	start()
else:
	# At this point, all information gathered is stored into a pdf with the name 'newd_data.csv' in the directory
	driver.implicitly_wait(10)
	dict_R = pd.DataFrame({'Property Type':title_list,'Price':price_list,'Number of Beds':Nbed_list, 'Number of Baths':Nbath_list,'Size in Sqft':Nsize_list, 'Address':loc_list, 'Link':link_list})
	print(dict_R)
	dict_R.to_csv('Selenium_output.csv')
	driver.quit()