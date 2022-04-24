import xml.etree.ElementTree as ET

def getVehicles(path):
    file = path + "/vehicles.xml"
    data = ET.parse(file)
    root = data.getroot()
    price = 0

    for vehicle in root:
        if vehicle.tag == "vehicle":
            price += sellPriceVehicle(vehicle)

    return price


def sellPriceVehicle(vehicle):
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

def getFarmLand(path, map):
    "Path of game folder and path of list of feilds for map"
    file = path + "/farmland.xml"
    data = ET.parse(file)
    root = data.getroot()
    feildList = []
    price = 0
    for land in root:
        if land.attrib["farmId"] == "1":
            feildList.append(int(land.attrib["id"]))

    map = open(map, "r")
    mapDict = {}

    for feild in map:
        mapDict[int(feild.split(" ")[0])] = int(feild.split(" ")[1])
    
    for i in feildList:
        price += mapDict.get(i)

    return price

def getPlaceables(path):
    file = path + "/placeables.xml"
    data = ET.parse(file)
    root = data.getroot()
    price = 0

    for placeables in root:
        if placeables.attrib["farmId"] == "1":
            price += float(placeables.attrib["price"])
    
    return price

def getLoan(path):
    file = path + "/farms.xml"
    data = ET.parse(file)
    root = data.getroot()
    loan = 0
    money = 0

    for farm in root:
        if farm.attrib["farmId"] == "1":
            loan += -float(farm.attrib["loan"]) 
            money += float(farm.attrib["money"])

    return loan, money


def getValue(path, map):
    value = getVehicles(path) + getFarmLand(path,map) + getPlaceables(path)
    loan, money = getLoan(path)
    value += money + loan
    return int(value)

# TODO ask user for path 

path = "C:\\Users\\josh\\Documents\\My Games\\FarmingSimulator2022\\savegame1" 
map = "C:/Local/Personal/FarmingSimulator/ElmCreek.txt"
loan = int(getLoan(path)[0])
money = int(getLoan(path)[1])
placeables  = int(getPlaceables(path))
vehicles = int(getVehicles(path))
farmland = int(getFarmLand(path, map))
valuation = int(getValue(path,map))
maxLoan = int((valuation-money)*0.3)
print("Valuation is total value of farm minus any loans, max loan is 30% of total value minus liquid assets\n")
print(f"Valuation: €{valuation} \nLoan: €{loan} \nMoney: €{money} \nPlaceables: €{placeables} \nVehicles & Equipment €{vehicles} \nFarmland €{farmland} \n\nMax Loan: €{maxLoan}")



