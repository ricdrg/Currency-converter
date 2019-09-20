"""
Currency converter script retrieving rates from exchangerate-api.com
1° Checking for internet connection to connect to the web API
2° Retrieving country codes from a csv file and assign it to a variable
3° Asking datas to the user (what currency country need to be converted to which currency country and the amount)
4° Getting the country code matching the country names entered by the user
5° Returning the value to the user



Missing function to check internet connection
Missing error handling

"""
############################ Internet connection checking function
def test_intConnection():
    try :
        import socket
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysock.connect(('www.google.com', 80))
        return True
    except OSError:
        pass
    return False


############################ Prompt user
# Gathering values to prepare the conversion
def promptUserdata():
    while True :
        fromCountry = input('Please enter the country from where you want to convert the currency :\n').upper()
    #Checking that no digits are in the input
        if any(char.isdigit() for char in fromCountry) :
            print("Please do not include any digits")
            continue
        else :
            break

    while True :
        toCountry = input('Please enter the country to where you want to convert the currency :\n').upper()
        if any(char.isdigit() for char in toCountry) :
            print("Please do not include any digits")
            continue
        else :
            break

    while True :
        money = input('Please enter the value that you want to convert :\n')
                 #Checking that the value entered is digits only
        if not money.isdigit() :
            print('Please enter digits only')
            continue
        else :
            break

    money = int(money)
    return fromCountry, toCountry, money


############################ Country code Retrieving
def getCountrycode(from_value, to_value):
    CodeandName_csv = list()
# Loading the CSV file which contains country codes and currency codes into a variable
    import csv
    with open(r'data/country-currency.csv') as csvDataFile :
        csvReader = csv.reader(csvDataFile, delimiter=';')
        for rows in csvReader:
            CodeandName_csv.append(rows)
# Searching the country code matching the fromCountry value entered
    for line in CodeandName_csv :
        if from_value in line :
            fromCountryCode = line[0]
# Searching the country code matching the toCountry value entered
    for line in CodeandName_csv :
        if to_value in line :
            toCountryCode = line[0]

    return fromCountryCode, toCountryCode



############################ Getting country code from the web with the fromCountryCode input
def getRate(fromCode):
    try :
        import urllib.request
        page = urllib.request.urlopen("https://api.exchangerate-api.com/v4/latest/" + fromCode)
        web_exchangeRateApi = page.read()

        import json
        json_exchangeRateApi = json.loads(web_exchangeRateApi)
        # Selecting the rates array to a python formatted dictionnary
        exchangeRateApi_rates = json_exchangeRateApi["rates"]
        exchangeRateApi_date = json_exchangeRateApi["date"]
        #print(exchangeRateApi_rates)
        return exchangeRateApi_rates, exchangeRateApi_date

        #print(type(toCountryrate))
    except : #y ajouter un code retour pour une possibilité de boucle dans le code principal
        print("Country currency not included in the converter, please try again")

############################ Conversion
def conversionOperation(int_value, code1, code2, rates, date):
    toCountryrate = rates[code2]
    # Math operation to get the conversion
    moneyConverted = int_value * toCountryrate
    print("So," , int_value , code1 , "equals" , moneyConverted , code2)
    # Selecting the rate that matches the toCountryCode
    print("As of" , date , "," , "1" , code1 , "is sold" , toCountryrate , code2)


#Checking internet connection availability
connection_value = test_intConnection()

if connection_value == True :
    print('Device connected to internet, checking the most up to date rates')

    allUserinput = promptUserdata()
    fromCountry = allUserinput[0]
    toCountry = allUserinput[1]
    amount = allUserinput[2]

    bothCountryCode = getCountrycode(fromCountry, toCountry)
    fromCountryCode = bothCountryCode[0]
    toCountryCode = bothCountryCode[1]

    exchangeRateApiDatas = getRate(fromCountryCode)
    apiRate = exchangeRateApiDatas[0]
    apiDate = exchangeRateApiDatas[1]

    #Insert in the function the amount, rates, , date, toCountryCode
    conversionOperation(amount, fromCountryCode, toCountryCode, apiRate, apiDate)

else :
    import time
    import sys
    print("Internet connection required. Please check it before using this script. Bye bye !")
    time.sleep(5)
    sys.exit()


##########################################################################################
