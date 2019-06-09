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

    files = []
    files.append("dealer-contact-qld.txt")
    files.append("dealer-contact-nsw.txt")
    files.append("dealer-contact-act.txt")
    files.append("dealer-contact-nt.txt")
    files.append("dealer-contact-sa.txt")
    files.append("dealer-contact-tas.txt")
    files.append("dealer-contact-vic.txt")
    files.append("dealer-contact-wa.txt")

    for f in files: 
        with open("./dealer_contact/" + f, encoding='utf8') as f:
                text = f.read().strip()
        soup = BeautifulSoup(text, "html.parser")
        for item in soup.find_all("a", {"class": "ty-find-a-dealer-result__website"}):
                dealers.append(item.get_text())
                # to find dealers state
                # print(f.name.split("-")[-1].replace(".txt","")) 
        for item in dealers:
            file.write(item.split(".")[-3].replace("http://","").replace("https://","") + "\n") 

def format_dealers():

    file = open("all-dealers.txt", "w")

    # write into all-dealers.txt
    d = open("dealer-names.txt", "r")
    for item in d:        
        file.write("https://" + str(item.replace("\n","")) + ".dealer.toyota.com.au/new-vehicles/prado/" + "\n") 

    print("finished formatting")

def deduplicate_file(file_name):

    outfile = open("dealers.txt", "w")

    lines_seen = set() # holds lines already seen    
    for line in open(file_name, "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

    print("finished deduplicate")

# remove dealers with invalid SSLs
def remove_dealers():

        r = []
        r.append("https://brianhilton.dealer.toyota.com.au/new-vehicles/prado/\n")
        r.append("https://errolmatschossmotors.dealer.toyota.com.au/new-vehicles/prado/\n")
        r.append("https://peterkittletoyota.dealer.toyota.com.au/new-vehicles/prado/\n")
        r.append("https://billbuckletoyota.dealer.toyota.com.au/new-vehicles/prado/\n")
        r.append("https://lemanstoyota.dealer.toyota.com.au/new-vehicles/prado/\n")
        r.append("https://billbuckle.dealer.toyota.com.au/new-vehicles/prado/\n")

        with open("dealers.txt", "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                        if i not in r:
                                f.write(i)
                f.truncate()
        print("removed dealers")

load_dealers()
format_dealers()
deduplicate_file("all-dealers.txt")
remove_dealers()


