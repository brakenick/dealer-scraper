import requests
import urllib.request
import csv
from helpers import print_to_txt
from helpers import print_to_csv
from helpers import init_csv
from bs4 import BeautifulSoup

dealer_state = {}

file = open("dealer_names.txt", "w")
allDealers = open("all_dealers.txt", "w")

files = []
files.append("dealer-contact-qld.txt")
files.append("dealer-contact-nsw.txt")
files.append("dealer-contact-act.txt")
files.append("dealer-contact-nt.txt")
files.append("dealer-contact-sa.txt")
files.append("dealer-contact-tas.txt")
files.append("dealer-contact-vic.txt")
files.append("dealer-contact-wa.txt")

# scrape contact details from https://www.toyota.com.au/find-a-dealer#QLD 
# requires html content saved into dealer-contact.txt
def load_dealers():    

    duplicated_list = []

    for f in files:        
        # set name of state     
        name = f.split("-")[-1].replace(".txt","") 
                
        with open("./dealer_contact/" + f, encoding='utf8') as f:
                text = f.read().strip()
        soup = BeautifulSoup(text, "html.parser")
        for item in soup.find_all("a", {"class": "ty-find-a-dealer-result__website"}):
                #file.write(item.get_text().split(".")[-3].replace("http://","").replace("https://","") + "\n") 
                duplicated_list.append(item.get_text().split(".")[-3].replace("http://","").replace("https://",""))
                # add dealer name and state to dict for lookup later
                dealer_state[item.get_text().split(".")[-3].replace("http://","").replace("https://","")] = name   
        
        print("finished load dealers " + name)  
        
        # remove duplicate dealers
    print("all dealers: " + str(len(duplicated_list)))    

    dealer_list = list(dict.fromkeys(duplicated_list))  

    print("deduplicated dealers: " + str(len(dealer_list)))

    dealer_list = remove_dealers(dealer_list)
     
    print("finished load all dealers")       

    return dealer_list 

# remove dealers with invalid SSLs
def remove_dealers(d):

        dlist = d

        r = []
        r.append("brianhilton")
        r.append("errolmatschossmotors")
        r.append("peterkittletoyota")
        r.append("billbuckletoyota")
        r.append("lemanstoyota")
        r.append("billbuckle")

        for i in dlist:
                if i in r:
                    dlist.remove(str(i))

        print("removed invalid dealers")
        print("dealers remaining: " + str(len(dlist)))

        return d

