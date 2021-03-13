#import libraries
from bs4 import BeautifulSoup
import requests
import time
import csv


url_base = "https://carfromjapan.com/"

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
    'cheap-used-mercedes-benz-s-class-for-sale?minYear=2015&sort=priceUSD&page=1', 'cheap-used-lexus-es-for-sale?minYear=2015&sort=priceUSD&page=1',
    'cheap-used-bmw-5-series-for-sale?minYear=2015&sort=priceUSD&page=1', 'cheap-used-mercedes-benz-c-class-for-sale?minYear=2015&sort=priceUSD&page=1',
    'cheap-used-honda-accord-for-sale?minYear=2015&sort=priceUSD&page=1', 'cheap-used-toyota-camry-for-sale?minYear=2015&sort=priceUSD&page=1',
    'cheap-used-volkswagen-golf-gti-for-sale?minYear=2015&sort=priceUSD&page=1', 'cheap-used-volkswagen-tiguan-for-sale?minYear=2015&sort=priceUSD&page=1',
    'cheap-used-audi-a4-for-sale?minYear=2015&sort=priceUSD&page=1', 'cheap-used-porsche-911-for-sale?minYear=2015&sort=priceUSD&page=1']

url_list_page_2 = [
    'cheap-used-mercedes-benz-s-class-for-sale?minYear=2015&sort=priceUSD&page=2', 'cheap-used-lexus-es-for-sale?minYear=2015&sort=priceUSD&page=2',
    'cheap-used-bmw-5-series-for-sale?minYear=2015&sort=priceUSD&page=2', 'cheap-used-mercedes-benz-c-class-for-sale?minYear=2015&sort=priceUSD&page=2',
    'cheap-used-honda-accord-for-sale?minYear=2015&sort=priceUSD&page=2', 'cheap-used-toyota-camry-for-sale?minYear=2015&sort=priceUSD&page=2',
    'cheap-used-volkswagen-golf-gti-for-sale?minYear=2015&sort=priceUSD&page=2', 'cheap-used-volkswagen-tiguan-for-sale?minYear=2015&sort=priceUSD&page=2',
    'cheap-used-audi-a4-for-sale?minYear=2015&sort=priceUSD&page=2', 'cheap-used-porsche-911-for-sale?minYear=2015&sort=priceUSD&page=2']

#Page 1
def scrapeCarData(carModelUrl):
    #set soup parameters
    page = requests.get(carModelUrl)
    soup =  BeautifulSoup(page.content, 'html.parser')

    #get car rows from page
    carPageRows = soup.findAll('tr', {'class' : 'car-row'})
    
    for carPage in carPageRows:
        #empty list for scraped data
        scrapedData = []

        #get children 'td' and iterate over them
        rowData = carPage.findAll('td')
        writeCarPageUrl = rowData[1].find('a', {'class' : 'strong-color'}).attrs['href']
        writeModel = rowData[1].find('h2').text
        writeModelYear = rowData[2].find('span').text
        writeDriven = rowData[3].find('span').text
        writePrice = rowData[6].find('span').text
        
        #Remove commas + Convert to float + caluclate km to miles + cast to string
        writeDriven = writeDriven.replace(',','')
        writeDriven = float(writeDriven)
        writeDriven = writeDriven * 0.62137
        writeDriven = round(writeDriven, 2)
        writeDriven = str(writeDriven)
        writePrice = writePrice.replace(',','')
        writePrice = writePrice.replace('US$ ','')
        
        #place elems into list
        scrapedData.extend((writeCarPageUrl,writeModel,writeModelYear,writeDriven, writePrice))
        writeCSV(scrapedData)
        
    return None

#Page 2
def scrapeCarData2(carModelUrl):
    #set soup parameters
    page = requests.get(carModelUrl)
    soup =  BeautifulSoup(page.content, 'html.parser')

    #get car rows from page
    carPageRows = soup.findAll('tr', {'class' : 'car-row'})
    
    
    for i, carPage in enumerate(carPageRows):
        if i < 5:
            #empty list for scraped data
            scrapedData = []

            #get children 'td' and iterate over them
            rowData = carPage.findAll('td')
            writeCarPageUrl = rowData[1].find('a', {'class' : 'strong-color'}).attrs['href']
            writeModel = rowData[1].find('h2').text
            writeModelYear = rowData[2].find('span').text
            writeDriven = rowData[3].find('span').text
            writePrice = rowData[6].find('span').text
            
            #Remove commas + Convert to float + caluclate km to miles + cast to string
            writeDriven = writeDriven.replace(',','')
            writeDriven = float(writeDriven)
            writeDriven = writeDriven * 0.62137
            writeDriven = round(writeDriven, 2)
            writeDriven = str(writeDriven)
            writePrice = writePrice.replace(',','')
            writePrice = writePrice.replace('US$ ','')

            #place elems into list
            scrapedData.extend((writeCarPageUrl,writeModel,writeModelYear,writeDriven, writePrice))
            writeCSV(scrapedData)
        else:
            break
    return None


def writeCSV(writeRowData):
    outputFile = open('carsFromJapan.csv', 'a', newline='')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(writeRowData)
    print(writeRowData)
    outputFile.close()
    return None


def initFile():
    #Create File Headers
    outputFile = open('carsFromJapan.csv', 'a', newline='')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow((['Unique URL', 'Model', 'Model Year', 'Miles Driven', 'Price']))
    outputFile.close()

    #Page 1
    for carURL in url_list:
        combinedUrl = url_base + carURL
        scrapeCarData(combinedUrl)

    #Page 2
    for carURL in url_list_page_2:
        combinedUrl = url_base + carURL
        scrapeCarData2(combinedUrl)

    return None

initFile()

