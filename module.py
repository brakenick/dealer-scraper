import requests
import urllib.request
import csv
from helpers import print_to_txt
from helpers import print_to_csv
from helpers import init_csv
from dealers import load_dealers
from dealers import write_dealers
from dealers import remove_dealers
from dealers import dealer_state
from bs4 import BeautifulSoup

dealer_list = load_dealers()

dealers = []
models = ["gx", "gxl", "vx", "kakadu"]

# import dealers from txt file
def import_dealers():
    with open('dealers.txt') as dealer_file:
        for line in dealer_file:
            stripped = line.replace("\n","")
                 
            # add dealer URLs for each model to be scraped
            for model in models:
                dealers.append(stripped + model + "/diesel/")         

def scrape_cars():

        results_list = []
        
        i = 0
        while i < len(dealers):
                dealer_name = dealers[i].split(".")
                dealer_name = dealers[i].replace("https://", "")
                dealer_name = dealer_name.split(".")[0]
                model = dealers[i].split("/")[5]

                print("Started dealer: " + dealer_name + " " + model)
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
                        price = item.find("div", {"class": "inventory--price--figure"})
                        
                        if stock is not None and price is not None:
                                title = item.find("div", {"class": "inventory--overview"}).findChildren()[0].get_text()
                                
                                vin = item.find("p", {"class": "inventory--detail__vin"})                       
                                transmission = item.find("ul", {"class": "reset reset--all"}).find_all("li")[0].get_text()
                                engine = item.find("ul", {"class": "reset reset--all"}).find_all("li")[1].get_text()
                                interior = item.find("ul", {"class": "reset reset--all"}).find_all("li")[2].get_text()                        

                                title = title.replace('\n', "")
                                title = title.replace('Brand New', "")
                                colour_options = title.split("(")[1]
                                colour = colour_options.split(")")[0]
                                if "with" in colour_options:
                                        options = colour_options.split("with ")[1]
                                else:
                                        options = ""
                                colour = colour_options.split(")")[0]
                                title = title.split("(")[0]
                                if price is not None:
                                        price = price.get_text()
                                        price = price.replace(",","")
                                if vin is not None:
                                        vin = vin.get_text()
                                        vin = vin.replace("VIN: ","")
                                
                                link = "https://" + dealer_name + ".dealer.toyota.com.au/inventory/prado/" + model + "/diesel/" + title[1:5] + "/" + vin

                                state = dealer_state.get(dealer_name)

                                print_to_txt(dealer_name, state, price, model, title, colour, options, transmission, engine, interior, vin, link)
                                print_to_csv(dealer_name, state, price, model, title, colour, options, transmission, engine, interior, vin, link)                        
                
                results_list = []
                
                print("Finished dealer: " + dealer_name + " " + model)

                i = i + 1

        print("finished all dealers")

write_dealers(dealer_list)

init_csv()
import_dealers()
scrape_cars()