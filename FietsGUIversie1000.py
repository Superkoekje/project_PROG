#Fietsenstalling

from tkinter import Tk, Label, Button, Entry, END, PhotoImage, Text, Scrollbar
import csv
import random
import threading
import datetime
import time

"""
antirobotbeveiliging
telegrambeveiliging
"""

def bluebutton(buttontext, function):
    button = Button(text = buttontext,
                    height = 2,
                    width = 15,
                    font = ('Helvetica',16),
                    background = 'blue',
                    foreground = 'white',
                    command = function)
    return button

def yellowlabel(labeltext):
    label = Label(text = labeltext,
                  background = 'yellow',
                  foreground = 'blue',
                  font = ('Helvetica',16))
    return label

def display(index):
    global que
    for item in que[index]:
        item.grid(row = index, column = que[index].index(item))

def forget(index):
    global que
    for item in range(index, 5):
        for subitem in que[item]:
            subitem.grid_forget()

def invalidinput(index):
    global que
    global invalidlabel
    invalidlabel = yellowlabel('Ongeldige invoer. Probeer opnieuw')
    que[index].append(invalidlabel)
    for item in que[index]:
        if type(item) == Entry:
            item.delete(0, END)
    invalidlabel.grid(row = 10, columnspan = 2)

def invalidpassword(index):
    global que
    global invalidpasswordlabel
    global gebruiker
    pogingen = str(5 - int(gebruiker[6]))
    invalidpasswordlabel = yellowlabel('Ongeldige wachtwoord. Nog '+ pogingen +' pogingen')
    que[index].append(invalidpasswordlabel)
    for item in que[index]:
        if type(item) == Entry:
            item.delete(0, END)
    invalidpasswordlabel.grid(row = 10, columnspan = 2)

def consequencemessage(index):
    consequencelabel = yellowlabel('Uw account is op dit moment geblokkeerd')
    que[index] = [consequencelabel]
    consequencelabel.grid(row = 10, columnspan = 3)

def get_register():
    global registerList
    with open('register.csv', 'r') as f:
        reader = csv.reader(f)
        registerList = list(reader)
    for i in registerList:
        if i == []:
            registerList.remove(i)

def update_register():
    global registerList
    with open("register.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(registerList)

def maketime():
    global kaas
    kaas = True
    while kaas:
        currenttime = str(datetime.datetime.now())
        labeltext = currenttime[0:16]
        label = yellowlabel(labeltext)
        label.grid(row = 0, column = 10)
        time.sleep(10)
        label.grid_forget()

def main():
    global root
    root = Tk()
    root.configure(background = 'yellow')
    root.geometry("1920x1020")
    get_register()
    initiate()
    timethread = threading.Thread(target=maketime)
    timethread.start()
    root.mainloop()

def initiate():
    global que
    global titlelabel
    global stallenbutton
    global ophalenbutton
    global informatiebutton
    global overigebutton
    global menukeuze
    menukeuze = ''
    que =[[],[],[],[],[]]
    forget(0)
    titlelabel = yellowlabel('NS fietsenstalling      ')
    registerbutton = bluebutton('Registreer', register)
    stallenbutton = bluebutton('Stal fiets', stallen_login)
    ophalenbutton = bluebutton('Haal fiets op', ophalen_login)
    informatiebutton = bluebutton('Informatie opvragen', informatie_login)
    overigebutton = bluebutton('Overige', overige)
    que[0] = [registerbutton, stallenbutton, ophalenbutton, informatiebutton, overigebutton, titlelabel]
    display(0)

def register():
    forget(1)
    global naamentry
    global telefoonnummerentry
    global ovkaartnummerentry
    global registerverifybutton
    naamlabel = yellowlabel('naam:')
    telefoonnummerlabel = yellowlabel('Telefoonnr: ')
    naamentry = Entry(root)
    telefoonnummerentry = Entry(root)
    registerverifybutton = bluebutton('Registreren', register_verify)
    que[1] = [naamlabel, telefoonnummerlabel, naamentry, telefoonnummerentry, registerverifybutton]
    naamlabel.grid(row = 2 ,column = 0)
    telefoonnummerlabel.grid(row = 3, column = 0)
    naamentry.grid(row = 2, column = 1)
    telefoonnummerentry.grid(row = 3, column = 1)
    registerverifybutton.grid(row = 4, column = 0)

def register_verify():
    global registerList
    naam = naamentry.get()
    telefoonnummer = telefoonnummerentry.get()
    kaas = True
    try:
        telefoonnummerint = int(telefoonnummer)
        for i in registerList:
            if telefoonnummer in i or len(telefoonnummer) != 10:
                kaas = False
        if kaas == True:
            forget(1)
            fietsnummer = str(random.randrange(10000,100000))
            for i in registerList:
                while fietsnummer in i:
                    fietsnummer = random.randrange(10000, 100000)
            wachtwoord = str(random.randrange(10000, 100000))
            wachtwoordlabel = yellowlabel('uw wachtwoord is: '+wachtwoord)
            fietsnummerlabel = yellowlabel("Uw fietsnummer is : "+fietsnummer)
            que[1]=[wachtwoordlabel, fietsnummerlabel]
            fietsnummerlabel.grid(row = 1, columnspan = 2)
            wachtwoordlabel.grid(row = 2, columnspan = 2)
            registerList.append([naam, telefoonnummer, fietsnummer, wachtwoord, '0', '0', '0'])
            update_register()
        else:
            invalidinput(1)
    except:
        invalidinput(1)

def stallen_login():
    forget(1)
    global fietsnummerentry
    global wachtwoordentry
    global loginbutton
    fietsnummerlabel = yellowlabel('Fietsnummer: ')
    wachtwoordlabel = yellowlabel('Wachtwoord:')
    fietsnummerentry = Entry()
    wachtwoordentry = Entry()
    loginbutton = bluebutton('Stallen', stallen_verify)
    que[1] = [fietsnummerlabel, wachtwoordlabel, fietsnummerentry, wachtwoordentry, loginbutton]
    fietsnummerlabel.grid(row = 2 ,column = 0)
    wachtwoordlabel.grid(row = 3, column = 0)
    fietsnummerentry.grid(row = 2, column = 1)
    wachtwoordentry.grid(row = 3, column = 1)
    loginbutton.grid(row = 4, column = 0)

def ophalen_login():
    forget(1)
    global fietsnummerentry
    global wachtwoordentry
    global loginbutton
    fietsnummerlabel = yellowlabel('Fietsnummer: ')
    wachtwoordlabel = yellowlabel('Wachtwoord:')
    fietsnummerentry = Entry()
    wachtwoordentry = Entry()
    loginbutton = bluebutton('Ophalen', ophalen_verify)
    que[1] = [fietsnummerlabel, wachtwoordlabel, fietsnummerentry, wachtwoordentry, loginbutton]
    fietsnummerlabel.grid(row = 2 ,column = 0)
    wachtwoordlabel.grid(row = 3, column = 0)
    fietsnummerentry.grid(row = 2, column = 1)
    wachtwoordentry.grid(row = 3, column = 1)
    loginbutton.grid(row = 4, column = 0)

def informatie_login():
    forget(1)
    global fietsnummerentry
    global wachtwoordentry
    global loginbutton
    fietsnummerlabel = yellowlabel('Fietsnummer: ')
    wachtwoordlabel = yellowlabel('Wachtwoord:')
    fietsnummerentry = Entry()
    wachtwoordentry = Entry()
    loginbutton = bluebutton('Informatie', informatie_verify)
    que[1] = [fietsnummerlabel, wachtwoordlabel, fietsnummerentry, wachtwoordentry, loginbutton]
    fietsnummerlabel.grid(row = 2 ,column = 0)
    wachtwoordlabel.grid(row = 3, column = 0)
    fietsnummerentry.grid(row = 2, column = 1)
    wachtwoordentry.grid(row = 3, column = 1)
    loginbutton.grid(row = 4, column = 0)

def stallen_verify():
    global fietsnummer
    global wachtwoord
    global registerList
    global gebruiker
    if len(registerList) < 500:
        kaas = False
        gebruiker = []
        fietsnummer = fietsnummerentry.get()
        wachtwoord = wachtwoordentry.get()
        for item in registerList:
            if item[2] == fietsnummer:
                gebruiker = item
                kaas = True
                break
        if gebruiker[6] == '5':
            consequencemessage(1)
            consequence()
        elif kaas == True and wachtwoord == gebruiker[3]:
            stallen()
        elif kaas == True:
            gebruiker[6] = str(int(gebruiker[6]) + 1)
            invalidpassword(1)
        else:
            invalidinput(1)
    else:
        vollestallinglabel = yellowlabel('Sorry, alle stallingen zijn vol')
        que[1] = [vollestallinglabel]
        vollestallinglabel.grid(row = 1, columnspan = 2)

def ophalen_verify():
    global fietsnummer
    global wachtwoord
    global registerList
    global gebruiker
    kaas = False
    gebruiker = []
    fietsnummer = fietsnummerentry.get()
    wachtwoord = wachtwoordentry.get()
    for item in registerList:
        if item[2] == fietsnummer:
            gebruiker = item
            kaas = True
            break
    if gebruiker[6] == '5':
        consequencemessage(1)
        consequence()
    elif kaas == True and wachtwoord == gebruiker[3]:
        ophalen()
    elif kaas == True:
        gebruiker[6] = str(int(gebruiker[6]) + 1)
        invalidpassword(1)
    else:
        invalidinput(1)

def informatie_verify():
    global fietsnummer
    global wachtwoord
    global registerList
    global gebruiker
    kaas = False
    gebruiker = []
    fietsnummer = fietsnummerentry.get()
    wachtwoord = wachtwoordentry.get()
    for item in registerList:
        if item[2] == fietsnummer:
            gebruiker = item
            kaas = True
            break
    if gebruiker[6] == '5':
        consequencemessage(1)
        consequence()
    elif kaas == True and wachtwoord == gebruiker[3]:
        informatie()
    elif kaas == True:
        gebruiker[6] = str(int(gebruiker[6]) + 1)
        invalidpassword(1)
    else:
        invalidinput(1)

def stallen():
    forget(1)
    global registerList
    global gebruiker
    nummerlijst = []
    for item in registerList:
        nummerlijst.append(item[4])
    for number in range(500):
        if str(number) not in nummerlijst:
            stalnummer = str(number)
            break
    if gebruiker[5] != '0':
        gestaldlabel = yellowlabel('Uw fiets is al gestald')
        que[1] = [gestaldlabel]
        gestaldlabel.grid(row = 1, columnspan = 2)
    else:
        time = datetime.datetime.now()
        gebruiker[4] = stalnummer
        gebruiker[5] = time
        stallenlabel = yellowlabel('Uw stalnummer is: '+stalnummer)
        que[1]=[stallenlabel]
        stallenlabel.grid(row = 1, columnspan = 2)
        update_register()

def ophalen():
    forget(1)
    global registerList
    global gebruiker
    if gebruiker[5] == '0':
        ongestaldlabel = yellowlabel('Uw fiets is niet gestald')
        que[1] = [ongestaldlabel]
        ongestaldlabel.grid(row = 1, columnspan = 2)
    else:
        nummer = gebruiker[4]
        gebruiker[4] = '0'
        gebruiker[5] = '0'
        ophalenlabel =  yellowlabel('Uw stalnummer is: '+nummer)
        que[1]=[ophalenlabel]
        ophalenlabel.grid(row = 1, columnspan = 2)
        update_register()

def informatie():
    forget(1)
    global gebruiker
    if gebruiker[5] == '0':
        ongestaldlabel = yellowlabel('Uw fiets is niet gestald')
        que[1] = [ongestaldlabel]
        ongestaldlabel.grid(row = 1, columnspan = 2)
    else:
        staltime = datetime.datetime.strptime(gebruiker[5], "%Y-%m-%d %H:%M:%S.%f")
        stalledtime = str(datetime.datetime.now() - staltime)
        stallnumber = gebruiker[4]
        staltimelabel = yellowlabel('Uw fiets is gestald op: '+str(staltime))
        stalledtimelabel = yellowlabel('Uw fiets is '+stalledtime+' gestald')
        stallnumberlabel = yellowlabel('Uw fiets is gestald in stalnummer: '+stallnumber)
        que[1] = [staltimelabel, stalledtimelabel, stallnumberlabel]
        staltimelabel.grid(row = 1, columnspan = 3)
        stalledtimelabel.grid(row = 2, columnspan = 3)
        stallnumberlabel.grid(row = 3, columnspan = 3)
        update_register()

def overige():
    forget(1)
    print('overige')

def consequence():
    global gebruiker
    global consequencegebruiker
    consequencegebruiker = gebruiker
    consequencethread = threading.Thread(target = consequenceloop)
    consequencethread.start()

def consequenceloop():
    global consequencegebruiker
    time.sleep(300)
    consequencegebruiker[6]= '0'

main()
