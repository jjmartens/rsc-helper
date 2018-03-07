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
keuzeSport = raw_input("Welke sport? (Keuze uit {squash student, zwemmen}): ")
if(keuzeSport in "squash student"):
    keuzeSport = "squash student"
    print("Keuze is squash.")
else:
    keuzeSport = "zwemmen"
    print("Keuze is zwemmen.")

keuzeBegin = int(raw_input("Begintijd? (uur): "))
keuzeEind = int(raw_input("Eindtijd? (uur): "))
keuzeDagen = int(raw_input("Hoeveel dagen vooruit kijken?: "))

#"zwemmen"/"squash student" 
if 'authError' in loginData:
    print("Fout tijdens inloggen: {}").format(loginData['error'])
else:
    token = loginData['token']
    klantid = loginData['klantId']     
#    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text='{}'".format(API_KEY, CHAT_ID ,"Bot gestart!"))
    print("Bot gestart voor {}".format(keuzeSport))
    while(True):
        tijden = get_agenda().json()
        vanaf = datetime.datetime.now() + datetime.timedelta(days=keuzeDagen)
        vanaf = vanaf.replace(hour=keuzeBegin, minute=0, second=0, microsecond = 0)
        tot = vanaf.replace(hour=keuzeEind, minute=0, second=0, microsecond = 0)

        for tijd in tijden:
            startTijd = datetime.datetime.fromtimestamp(int(tijd['start']))
            if (startTijd > vanaf and startTijd < tot):
                if(int(tijd['inschrijvingen']) < 10 and tijd['poolNaam'] == "zwemmen" and keuzeSport == "zwemmen"):
                    print ("Er zijn plekken vrij op tijd {}".format(startTijd))
                    booking = book(tijd).json()
                    print("Zwemmen geboekt op tijd {}".format(startTijd))
                if(int(tijd['inschrijvingen']) < 4 and tijd['poolNaam'] == "squash student" and keuzeSport == "squash student"):
                    print ("Er zijn plekken vrij op tijd {}".format(startTijd))
                    booking = book(tijd).json()
                    print("Squash geboekt op tijd {}".format(startTijd))
#                    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text='{}'".format(API_KEY, CHAT_ID ,"Ik heb een inschrijving gemaakt voor tijd: {}".format(startTijd)))
        print("Niks vrij atm.")
        time.sleep(60)
