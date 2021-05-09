from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np 

# Here we creeate list to save scrapped items
title_list = []
price_list = []
Nbed_list = []
Nbath_list = []
Nsize_list = []
loc_list = []
link_list = []

#Defining Links
main_base_url = "https://www.homes.com/virginia-beach-va/homes-for-sale/p"


#For pagination we create a string list to contain the number of pages to be scraped
# The list items are the string values of the pages to be scrapped
# We tried using 'pages = str(range(1,100))' but wasn't scrapping items right 
pages =['1','2','3','4','5','6','7','8','9','10'] #This scrapes the fisrt 10 pages. You may increase the list to the pages of your choice 
for n in pages:
  url = main_base_url+ n

  html = requests.get(url)


  base_url = "https://www.homes.com"
  
  #Creating BS object
  soup = BeautifulSoup(html.text, 'lxml')

# Here is where the scraping starts. You can uncomment print functions to see the resuts as they are being scraped 
  articles = soup.find_all(
      'article', class_='f1vrb3k6 radius-5 box-shadow-cards relative overflow-hidden c1or1u3b')

  for article in articles:
      # scraping for price
      price = article.find(
          'span', class_= 'flex font-family-title font-size-xxl line-height--1 pointer').text
      #print(price)
      price_list.append(price)
      
      #scraping for the bed, bath and size details
      details = article.find('div', class_='mb-1/2 font-size-m').text
      sub_detail = details.split(" | ")

      #Bed details
      try:
        No_of_Beds = sub_detail[0].split(" ")[0]
      except:
        No_of_Beds = "N/A"
      Nbed_list.append(No_of_Beds)
      #print(No_of_Beds)
      
      #Bath details
      try:
        No_of_Baths = sub_detail[1].split(" ")[0]
      except:
        No_of_Baths = "N/A"
      Nbath_list.append(No_of_Baths)
      #print(No_of_Baths)

      #Size details
      try:
        Property_size = sub_detail[2].split(" ")[0]
      except:
        Property_size = "N/A"
      Nsize_list.append(Property_size)
      #print(Property_size)


      #Scraping for the Location
      try:
        Address = article.find('div', class_='a16jsq91 font-size-s font-weight-regular truncate').text
      except:
        Address = "N/A"
      loc_list.append(Address)
      #print(Address)


      #Scraping for the Property Type
      try:
        Post_title = article.find('div', class_='mt-1 font-size-s').text
      except:
        Address = "N/A"
      title_list.append(Post_title)
      #print(Post_title)

      
      #Scraping for link to the property
      try:
        link_href = article.find('a', class_='no-underline', href=True)['href']
        full_link = base_url + link_href
      except:
        link_href = "N/A"
        full_link = "N/A"
      link_list.append(full_link)   
      #print(full_link) 

	  #The out is finally printed and saved in a csv file
else:
    dict_R = pd.DataFrame(
        {'Property Type':title_list,
        'Price':price_list,
        'Number of Beds':Nbed_list,
        'Number of Baths':Nbath_list,
        'Size in Sqft':Nsize_list,
        'Address':loc_list,
        'Link':link_list})
    print(dict_R)
    dict_R.to_csv('BS_output.csv')

     
      