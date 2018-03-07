import datetime
import time
    
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



#Gebruik lijst.txt om momenten te plaatsen die je wil reserveren.
#Per regel dd-mm-yy,bu:bm,eu:em,ks
#dd = dag, mm = maand, yy = jaar, bu = vroegste uur, bm is vroegste minuut, eu het uiterste uur, em de uiterste minuut, ks in {zw, sq} (zw voor zwemmen, sq voor squashen)
#in het kort: bu:bm is het vroegste tijdstip om te beginnen met sporten, eu:em het laatste moment om te beginnen met sporten. 
print("Ingevoerde sportmomenten")
with open("lijst.txt") as f:
    fileContents = f.readlines()
for input in fileContents:
    dag = int(input[0:2])
    maand = int(input[3:5])
    jaar = int(input[6:10])
    begin = input[11:16]
    beginUur = int(begin[0:2])
    beginMin = int(begin[3:5])
    eind = input[17:22]
    eindUur = int(eind[0:2])
    eindMin = int(eind[3:5])
    keuze = input[23:25]
    if(keuze in "squash"):
        ks = "Squash"
    else:
        ks = "Zwemmen"
    print(ks + " van: " + datetime.datetime(year = jaar, month = maand, day = dag, hour = beginUur, minute = beginMin, second=0, microsecond = 0).strftime("%Y-%m-%d %H:%M:%S") + " tot " + datetime.datetime(year = jaar, month = maand, day = dag, hour = eindUur, minute = eindMin, second=0, microsecond = 0).strftime("%Y-%m-%d %H:%M:%S"))


loginData = login()


if 'authError' in loginData:
    print("Fout tijdens inloggen: {}").format(loginData['error'])
else:
    token = loginData['token']
    klantid = loginData['klantId']     
#    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text='{}'".format(API_KEY, CHAT_ID ,"Bot gestart!"))
    print("Bot gestart.")
    while(True):
        tijden = get_agenda().json()
        for input in fileContents:
            dag = int(input[0:2])
            maand = int(input[3:5])
            jaar = int(input[6:10])
            begin = input[11:16]
            beginUur = int(begin[0:2])
            beginMin = int(begin[3:5])
            eind = input[17:22]
            eindUur = int(eind[0:2])
            eindMin = int(eind[3:5])
            keuze = input[23:25]
            if(keuze in "squash"):
                keuzeSport = "squash student"
            else:
                keuzeSport = "zwemmen"

            vanaf =     datetime.datetime(year = jaar, month = maand, day = dag, hour = beginUur, minute = beginMin, second=0, microsecond = 0)
            tot =       datetime.datetime(year = jaar, month = maand, day = dag, hour = eindUur, minute = eindMin, second=0, microsecond = 0)
            
            for tijd in tijden:
                startTijd = datetime.datetime.fromtimestamp(int(tijd['start']))
                if (startTijd >= vanaf and startTijd < tot):
                    print(tijd['poolNaam'], keuzeSport, tijd['inschrijvingen'])
                    if(int(tijd['inschrijvingen']) < 10 and tijd['poolNaam'] == "zwemmen" and keuzeSport == "zwemmen"):
                        print ("Er zijn plekken vrij op tijd {}".format(startTijd))
                        booking = book(tijd).json()
                        print("Zwemmen geboekt op tijd {}".format(startTijd))
                    if(int(tijd['inschrijvingen']) < 4 and tijd['poolNaam'] == "squash student" and keuzeSport == "squash student"):
                        print ("Er zijn plekken vrij op tijd {}".format(startTijd))
                        booking = book(tijd).json()
                        print("Squash geboekt op tijd {}".format(startTijd))
    #                    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text='{}'".format(API_KEY, CHAT_ID ,"Ik heb een inschrijving gemaakt voor tijd: {}".format(startTijd)))
            print("Wacht 5 minuten...")
            time.sleep(300)

