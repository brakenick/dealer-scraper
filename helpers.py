file = open("cars.txt", "w")

def print_to_txt(dealer_name, price, model, title, colour, options, transmission, engine, interior, vin):
        file.write(dealer_name + " " + str(price) + " Model: " + str(model) + str(title) + "Colour: " + str(colour) + " Options:  " + str(options) + "Transmission:" + str(transmission) + " Engine:" + str(engine) + "Interior: " + str(interior) + " " + str(vin) + "\n")   

def print_to_csv(dealer_name, price, model, title, colour, options, transmission, engine, interior, vin):
        model = model.upper()                
        r = [dealer_name, price, model, title, colour, options, transmission, engine, interior, vin]        
        row = ",".join(r)

        with open("cars.csv", "a") as file:
                file.write(row)
                file.write("\n")

def init_csv():
        f = open("cars.csv", "w")
        f.truncate()
        f.write("dealer_name, price, model, title, colour, options, transmission, engine, interior, vin")
        f.write("\n")
        f.close()

