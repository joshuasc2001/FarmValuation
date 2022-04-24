class FarmValuation():
    
    def __init__(self, path, map):
        self.path = path
        self.map = map


    def getVehicles(self):
        """Gets the value of all vehicles in the farm"""

        import xml.etree.ElementTree as ET
        file = self.path + "/vehicles.xml"
        data = ET.parse(file)
        root = data.getroot()
        price = 0

        for vehicle in root:
            if vehicle.tag == "vehicle":
                price += self.sellPriceVehicle(vehicle)

        return price


    def sellPriceVehicle(self, vehicle):
        """Gets the sell price of a vehicle"""

        price = float(vehicle.attrib["price"])
        age = float(vehicle.attrib["age"])
        ageInt = int(age)
        operatingTime = float(vehicle.attrib["operatingTime"])

        if ageInt <= 12:
            ageLoss = 0.12
        elif ageInt < 50 & ageInt > 12:
            ageLoss = -0.00009*age**2 + 0.01*age +0.0694
        else:
            ageLoss = -0.000006*age**2 + 0.0021*age + 0.2397    

        operatingLoss = operatingTime*0.00004

        price = price - price*ageLoss - price*operatingLoss
        
        sellPrice = price
        
        return sellPrice

    def getFarmLand(self):
        """Gets the value of all farm land in the farm"""

        import xml.etree.ElementTree as ET
        file = self.path + "/farmland.xml"
        data = ET.parse(file)
        root = data.getroot()
        feildList = []
        price = 0
        for land in root:
            if land.attrib["farmId"] == "1":
                feildList.append(int(land.attrib["id"]))

        mapFile = open(map, "r")
        mapDict = {}

        for feild in mapFile:
            mapDict[int(feild.split(" ")[0])] = int(feild.split(" ")[1])
        
        for i in feildList:
            price += mapDict.get(i)

        return price

    def getPlaceables(self):
        """Gets the value of all placeables in the farm"""

        import xml.etree.ElementTree as ET
        file = self.path + "/placeables.xml"
        data = ET.parse(file)
        root = data.getroot()
        price = 0

        for placeables in root:
            if placeables.attrib["farmId"] == "1":
                price += float(placeables.attrib["price"])
        
        return price

    def getLoan(self):
        """Gets the value of all loans in the farm and gets the vale of the money in account"""

        import xml.etree.ElementTree as ET
        file = self.path + "/farms.xml"
        data = ET.parse(file)
        root = data.getroot()
        loan = 0
        money = 0

        for farm in root:
            if farm.attrib["farmId"] == "1":
                loan += -float(farm.attrib["loan"]) 
                money += float(farm.attrib["money"])

        return loan, money


    def getValue(self):
        """Gets the total value of the farm"""
        value = self.getVehicles() + self.getFarmLand() + self.getPlaceables()
        loan, money = self.getLoan()
        value += money + loan
        return int(value)

    def toString(self):
        """Returns a string with the formatted value of the farm"""
        loan = int(self.getLoan()[0])
        money = int(self.getLoan()[1])
        placeables  = int(self.getPlaceables())
        vehicles = int(self.getVehicles())
        farmland = int(self.getFarmLand())
        valuation = int(self.getValue())
        maxLoan = int((valuation-money)*0.3)

        return "Valuation is total value of farm minus any loans, max loan is 30% of total value minus liquid assets\n\nValuation: {valuation} \nLoan: {loan} \nMoney: {money} \nPlaceables: {placeables} \nVehicles & Equipment {vehicles} \nFarmland {farmland} \n\nMax Loan: {maxLoan}".format(valuation=valuation, loan=loan, money=money, placeables=placeables, vehicles=vehicles, farmland=farmland, maxLoan=maxLoan)

class FarmValuationGUI():

    def __init__(self):
        self.guiSetup()
    
    def submit(self, farm, path, map):
        import tkinter as tk

        text =  tk.Text(farm, height=15, width=50)
        text.pack(fill='x', expand=True)

        text.insert(tk.END, FarmValuation(path.get(), map.get()).toString())
        text.config(state=tk.DISABLED)

    def guiSetup(self):
        import tkinter as tk

        root = tk.Tk()
        root.title("Farm Valuation")
        root.geometry("410x400")

        path = tk.StringVar()
        map = tk.StringVar()
        
        farm = tk.Frame(root)
        farm.pack(padx=10, pady=10,fill='x', expand=True)


        pathLabel = tk.Label(farm, text="Path to save folder: ")
        pathLabel.pack(fill='x', expand=True)

        pathEntry = tk.Entry(farm, textvariable=path)
        pathEntry.pack(fill='x', expand=True)
        pathEntry.focus()

        mapLabel = tk.Label(farm, text="Path to map file: ")
        mapLabel.pack(fill='x', expand=True)

        mapEntry = tk.Entry(farm, textvariable=map)
        mapEntry.pack(fill='x', expand=True)
        mapEntry.focus()

        # submit_button = tk.Button(farm, text="Submit", command=lambda: showinfo(title="Farm Valuation", message=FarmValuation(path.get(), map.get()).toString()))
        # submit_button.pack(fill='x', expand=True)

        submit_button = tk.Button(farm, text="Submit", command=lambda: self.submit(farm, path, map))
        submit_button.pack(fill='x', expand=True)

        

        root.mainloop()

    
        

# "C:/Users/YOUR_USER_HERE/Documents/My Games/FarmingSimulator2022/savegame4" 
# "C:/PATH/TO/FARM/MAPFILE.txt"

FarmValuationGUI()
