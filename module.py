import requests
import urllib.request
import time
import csv
from bs4 import BeautifulSoup

def print_to_txt(dealer_name, price, title, transmission, engine, interior, vin):
        file.write(dealer_name + " " + str(price) + str(title) + " Transmission:" + str(transmission) + " Engine:" + str(engine) + "Interior: " + str(interior) + " " + str(vin) + "\n")   

def print_to_csv(dealer_name, price, title, transmission, engine, interior, vin):
                
        r = [dealer_name, price, title, transmission, engine, interior, vin]        
        row = ",".join(r)

        with open("cars.csv", "a") as file:
                file.write(row)
                file.write("\n")

file = open("cars.txt", "w")

results_list = []
dealers = []

# bs4 had an issue when loading from file
# with open('dealers.txt') as dealer_file:
#    for line in dealer_file:
#        dealers.append(line) 

dealers.append("https://southsidetoyota.dealer.toyota.com.au/new-vehicles/prado/gxl/diesel")
dealers.append("https://scifleettoyota.dealer.toyota.com.au/new-vehicles/prado/gxl/diesel")
dealers.append("https://torquetoyota.dealer.toyota.com.au/new-vehicles/prado/gxl/diesel")
dealers.append("https://oldmactoyotaspringwood.dealer.toyota.com.au/new-vehicles/prado/gxl/diesel")
dealers.append("https://downtowntoyota.dealer.toyota.com.au/new-vehicles/prado/gxl/diesel")
dealers.append("https://motoramatoyota.dealer.toyota.com.au/new-vehicles/prado/gxl/diesel")

i = 0
while i < len(dealers):
        dealer_name = dealers[i].split(".")
        dealer_name = dealers[i].replace("https://", "")
        dealer_name = dealer_name.split(".")
        dealer_name = dealer_name[0]

        print("Started dealer: " + dealer_name)
        url = dealers[i]  

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find("ul", {"id": "results"})

        # add div for each car to array
        for item in results.find_all("li", {"class": "inventory"}):
                results_list.append(item)        

        # iterate over results list to extract fields for each car
        for item in results_list:
                stock = item.find("div", {"class": "inventory--stock--status--inner"})
                
                if stock is not None:
                        title = item.find("div", {"class": "inventory--overview"}).findChildren()[0].get_text()
                        price = item.find("div", {"class": "inventory--price--figure"})
                        vin = item.find("p", {"class": "inventory--detail__vin"})                       
                        transmission = item.find("ul", {"class": "reset reset--all"}).find_all("li")[0].get_text()
                        engine = item.find("ul", {"class": "reset reset--all"}).find_all("li")[1].get_text()
                        interior = item.find("ul", {"class": "reset reset--all"}).find_all("li")[2].get_text()

                        title = title.replace('\n', "")
                        title = title.replace('Brand New', "")
                        if price is not None:
                                price = price.get_text()
                                price = price.replace(",","")
                        if vin is not None:
                                vin = vin.get_text()

                        print_to_txt(dealer_name, price, title, transmission, engine, interior, vin)
                        print_to_csv(dealer_name, price, title, transmission, engine, interior, vin)


        print("Finished Dealer: " + dealer_name)
        i = i + 1

print("finished all dealers")