# carscraper
Python program to pull data from two car websites to analyze the market for a car buyer

## What does it do?
Carscraper is a program written in Python using BS4 and requests to parse data from two popular car buying websites. One website represents the JDM market (carsfromjapan.com) and one represents the U.S market (autotrader.com). My goal it so gather information relating to price, mileage, make, model and year to compare the used/new car market for both regions. While owning a car is expensive in Japan, there are some cases where buying certain brands or models of cars are actually cheaper then in the U.S. While this program does not interpret data gathered from these sites the idea would be you can take the output from carscraper for analytics.

## Function
This program functions by feeding it shorted URLs of the search listings for either carsfromjapan.com or autotrader.com. From there it parses HTML elements and makes a CSV file for data interpretation.

initFile() - Makes headers for the CSV file, combines the shorted URL(make, model, year of the car) with the base URL(carsfromjapan.com or autotrader.com)* and starts the program's loop. 

writeCSV() - Writes data from the scrapeCarData or scrapeCarData2 functions to the CSV file initialized by initFile() using .writerow()

scrapeCarData/scrapeCarData2 - Takes the complete URL from initFile() and begins parsing the HTML for data.

## Use cases
Data from this application could be used to help overturn car import laws in the U.S or study market trends by comparing pricing, availability, or "newness" of cars in different markets.

*If I had more time I would write a program that made a database of every make, model and car that would be dynamically combined with the base url so any car would be indexable.
