import requests
from getpass import getpass
import datetime
import time
import requests

# config for telegram bot
API_KEY = "API_KEY"
CHAT_ID  = "CHAT_ID"

baseurl = "https://publiek.usc.ru.nl/app/api/v1/?module={module}&method={method}"

def login(): 
    username = raw_input("Username: ")
    password = getpass("Password:")
    response = requests.post(baseurl.format(module="user", method="logIn"), {'username':username, 'password':password})
    return (response.json())

def get_agenda():
    response = requests.post(baseurl.format(module="locatie", method="getLocaties"), {'klantId': klantid, 'token':token})
    return (response)

def book(tijdObject):
    response = requests.post(baseurl.format(module="locatie", method="addLinschrijving"), {
        'klantId': klantid, 
        'token':token,
        'inschrijvingId': tijdObject['inschrijvingId'],
        'poolId': tijdObject['poolId'],
        'laanbodId': tijdObject['laanbodId'],
        'start': tijdObject['start'],
        'eind': tijdObject['eind'] 
        })
    return (response)


loginData = login()
if 'authError' in loginData:
    print("Fout tijdens inloggen: {}").format(loginData['error'])
else:
    token = loginData['token']
    klantid = loginData['klantId']     
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text='{}'".format(API_KEY, CHAT_ID ,"Bot gestart!"))

    while(True):
        tijden = get_agenda().json()
        vanaf = datetime.datetime.now() + datetime.timedelta(days=1)
        vanaf = vanaf.replace(hour=15, minute=30, second=0, microsecond = 0)
        tot = vanaf.replace(hour=18, minute=0, second=0, microsecond = 0)

        for tijd in tijden:
            startTijd = datetime.datetime.fromtimestamp(int(tijd['start']))
            if (startTijd > vanaf and startTijd < tot):
                if(int(tijd['inschrijvingen']) < 10 and tijd['poolNaam'] == "zwemmen"):
                    print ("Er zijn plekken vrij op tijd {}".format(startTijd))
                    booking = book(tijd).json()
                    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text='{}'".format(API_KEY, CHAT_ID ,"Ik heb een inschrijving gemaakt voor tijd: {}".format(startTijd)))
        print("Niks vrij")
        time.sleep(60)