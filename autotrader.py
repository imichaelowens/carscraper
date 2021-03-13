#import libraries
from bs4 import BeautifulSoup
import requests
import time
import csv

#Old Phone User-Agent
headers = {'User-Agent': 'Nokia5310XpressMusic_CMCC/2.0 (10.10) Profile/MIDP-2.1 '\
'Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; '\
'Nokia5310XpressMusic) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile'}

url_base = "https://www.autotrader.com/"

#url_list in order:
#Mercedes S Class
#Lexus ES Series (350)
#BMW 5 Series
#Mercedes C Class Sedan
#Honda Accord
#Toyota Camry
#Volkswagen Golf GTI
#Volkswagen Tiguan
#Audi A4 Sedan
#Porsche 911

url_list = [
    'cars-for-sale/all-cars?zip=33606&makeCodeList=MB&modelCodeList=S_CLASS&seriesCodeList=S_CLASS',
    'cars-for-sale/all-cars?zip=33606&makeCodeList=LEXUS&modelCodeList=ES350',
    'cars-for-sale/all-cars?zip=33606&makeCodeList=BMW&modelCodeList=5_SERIES&seriesCodeList=5_SERIES',
    'cars-for-sale/all-cars?zip=33606&makeCodeList=MB&modelCodeList=C_CLASS&seriesCodeList=C_CLASS',
    'cars-for-sale/all-cars?zip=33606&makeCodeList=HONDA&modelCodeList=ACCORD',
    'cars-for-sale/all-cars?zip=33606&makeCodeList=TOYOTA&modelCodeList=CAMRY',
    'cars-for-sale/all-cars?zip=33606&makeCodeList=VOLKS&modelCodeList=GTI',
    'cars-for-sale/all-cars?zip=33606&makeCodeList=VOLKS&modelCodeList=TIGUAN',
    'cars-for-sale/all-cars?zip=33606&makeCodeList=AUDI&modelCodeList=A4',
    'cars-for-sale/all-cars?zip=33606&makeCodeList=POR&modelCodeList=911']




def scrapeCarData(carModelUrl):
    #set soup parameters
    print(carModelUrl)
    page = requests.get(carModelUrl, headers=headers)
    soup =  BeautifulSoup(page.content, 'html.parser')
    
    #get car rows from page
    carPageRows = soup.findAll('div', {'class' : 'item-card-content'})
    
    
    for i, carPage in enumerate(carPageRows):
        if i < 20:
        
            #empty list for scraped data
            scrapedData = []

            #get children
            
            writeCarPageUrl = carPage.find('a').attrs['href']
            writeModelAndYear = carPage.find('h2').text

            try:
                writeDriven = carPage.findAll('div',  {'class' : 'text-bold'})[1].text
            except:
                writeDriven = 'No Mileage Data'
            
            writeCarPrice = carPage.find('span', {'class' : 'first-price'}).text

            #(writeDriven) - Remove "miles" from string and remove comma
            writeDriven = writeDriven.replace('miles','')
            writeDriven = writeDriven.replace(',','')

            #(writePrice) - Remove comma
            writeCarPrice = writeCarPrice.replace(',','')
            writeCarPrice = writeCarPrice.replace('MSRP','')

            #place elems into list
            scrapedData.extend((writeCarPageUrl,writeModelAndYear,writeDriven,writeCarPrice))
            #print(scrapedData)

            #Call CSV Function
            writeCSV(scrapedData)
        else:
            break
    return None

#write CSV scraped data
def writeCSV(writeRowData):
    outputFile = open('autoTrader.csv', 'a', newline='')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(writeRowData)
    outputFile.close()
    return None

def initFile():
    outputFile = open('autoTrader.csv', 'a', newline='')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow((['Unique URL', 'Model and Year', 'Miles Driven', 'Price']))
    outputFile.close()
    for carURL in url_list:
        combinedUrl = url_base + carURL
        scrapeCarData(combinedUrl)
    return 

initFile()

