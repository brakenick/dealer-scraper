import requests
import urllib.request
import csv
from helpers import print_to_txt
from helpers import print_to_csv
from helpers import init_csv
from bs4 import BeautifulSoup

dealers = []

# scrape contact details from https://www.toyota.com.au/find-a-dealer#QLD 
# requires html content saved into dealer-contact.txt
def load_dealers():

    file = open("dealer-names.txt", "w")

    with open('dealer-contact.txt', encoding='utf8') as f:
        text = f.read().strip()

    soup = BeautifulSoup(text, "html.parser")

    for item in soup.find_all("a", {"class": "ty-find-a-dealer-result__website"}):
            dealers.append(item.get_text()) 

    for item in dealers:
        file.write(item.split(".")[-3].replace("http://","") + "\n") 


def insert_all_dealers():

    file = open("all-dealers.txt", "w")

    # write into all-dealers.txt
    d = open("dealer-names.txt", "r")
    for item in d:        
        file.write("https://" + str(item.replace("\n","")) + ".dealer.toyota.com.au/new-vehicles/prado/" + "\n") 

def deduplicate_dealers():

    outfile = open("dealers.txt", "w")

    lines_seen = set() # holds lines already seen    
    for line in open("all-dealers.txt", "r"):
        print("before if" + line)
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            print(line)
            lines_seen.add(line)
    outfile.close()

    print("finished insert all")

# load_dealers()
# insert_all_dealers()
deduplicate_dealers()

