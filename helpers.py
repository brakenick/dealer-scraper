file = open("cars.txt", "w")

def print_to_txt(dealer_name, state, price, model, title, colour, options, transmission, engine, interior, vin, link):
        file.write(dealer_name + " " + str(price) + " Model: " + str(model) + str(title) + "Colour: " + str(colour) + " Options:  " + str(options) + "Transmission:" + str(transmission) + " Engine:" + str(engine) + "Interior: " + str(interior) + " " + str(vin) + " " + str(link) + "\n")   

def print_to_csv(dealer_name, state, price, model, title, colour, options, transmission, engine, interior, vin, link):
        model = model.upper()                
        r = [dealer_name, state, price, model, title, colour, options, transmission, engine, interior, vin, link]        
        row = ",".join(r)

        with open("cars.csv", "a") as file:
                file.write(row)
                file.write("\n")

def init_csv():
        f = open("cars.csv", "w")
        f.truncate()
        f.write("dealer_name, state, price, model, title, colour, options, transmission, engine, interior, vin, link")
        f.write("\n")
        f.close()

