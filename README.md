# Webscraping_Project


How to run the scrappers

#BEAUTIFUL SOUP AND SELENIUM

Beautiful soup and Selenium can be run using any python interpretor. The output is saved as a csv file named BS_output or Selenium ouput respectively in the directory.
You can however uncomment the print lines in the code to see the results in the terminal as it is being scrapped

#SCRAPY

The name of the spider is 'homespider' which must be used any time you want to run the scrapper
Scrapy on the other hand must be run in the scrapy project folder named virginia_homedata
Input the scrapy crawl command(s) in the terminal.
The results of scrapy is shown on the terminal or commandline.
However running the following line will yield a csv file named Scrapy_output.csv in the directory
'scrapy crawl homespider -o Scrapy_output'
