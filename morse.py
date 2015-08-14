from Tkinter import *
from time import *
import socket
import threading

tLock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print "Incoming: " + str(data)
                if(str(data) == "0"):
                    kurz(False)
                if(str(data) == "1"):
                    lang(False)
                
        except:
            pass
        finally:
            tLock.release()

host = '127.0.0.1'
port = 0

server = ('127.0.0.1',5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread",s))
rT.start()



# Ereignisbehandlung
#1 lang, 0 kurz
MorseAlph =  {'a': "01", "b": "1000", "c": "101", "d": "100",  "e": "0", "f": "0010",  "g": "110",  "h": "0000",
               "i": "00", "j": "0111", "k": "101", "l": "0100", "m": "11", "n": "10", "o": "111", "p": "0110", "q": "1101", "r": "010", "s": "000", "t": "1",
                "u": "001", "v": "0001", "w": "011", "x": "1001", "y": "1011", "z": "1100", "1":"00001","2":"00011","3":"00111","4":"01111","5":"11111","6":"011111","7":"00111","8":"00011","9":"00001", " ": " "}


#Reverses keys and values of MorseAlph
MorseAlphRev = dict (zip(MorseAlph.values(),MorseAlph.keys()))
MorsePhrase = ""

global lastsave
lastsave = 0

def kurzPush(event):
 #   tLock.acquire()
    global lastsave
    global MorsePhrase
    canvas.delete("all")
    lastsave = clock()
    MorsePhrase = MorsePhrase + "0"
    #transmission
    
    canvas.delete("all")
    id_kreis = canvas.create_oval(180, 110, 220, 150, fill='yellow')
    s.sendto("0", server)
    canvas.update()
    sleep(0.5)
    canvas.delete("all")
    canvas.update()
  #  tLock.release()
    sleep(0.7) #Wait between two letters
    
    
def langPush(event):
 #   tLock.acquire()
    global lastsave
    global MorsePhrase
    canvas.delete("all")
    lastsave = clock()
    MorsePhrase = MorsePhrase + "1"
    #transmission  
    canvas.delete("all")
    id_kreis = canvas.create_oval(180, 110, 220, 150, fill='yellow')
    s.sendto("1", server)
    canvas.update()
    sleep(1.0)
    canvas.delete("all")
    canvas.update()
   # tLock.release()
    sleep(0.7) #Wait between two letters
    
def kurz(sender):
    canvas.delete("all")
    id_kreis = canvas.create_oval(180, 110, 220, 150, fill='yellow')
    if(sender):
        s.sendto("0", server)
    canvas.update()
    sleep(0.5)
    canvas.delete("all")
    canvas.update()
    sleep(0.7) #Wait between two letters

def lang(sender):
    canvas.delete("all")
    id_kreis = canvas.create_oval(180, 110, 220, 150, fill='yellow')
    if(sender):
        s.sendto("1", server)
    canvas.update()
    sleep(1.0)
    canvas.delete("all")
    canvas.update()
    sleep(0.7) #Wait between two letters
    
def morse(self):
    print "----------------START OF TRANSMISSION----------------"
    for c in str(e1.get()):
        if(c == " "):
            sleep(2.0)
            print "Leerzeichen"
        else:
            for x in MorseAlph[c]:
                if(x == "0"):
                    # transmission
                    print "short"
                    kurz(True)
                else:
                    #transmission
                    
                    print "long"
                    lang(True)
        print("\n")
    print "----------------END OF TRANSMISSION----------------"

# Erzeugung der Komponenten
tkFenster = Tk()
tkFenster.title('Morse-Test')
tkFenster.geometry('420x320')
# Leinwand zum Zeichnen
canvas = Canvas(master=tkFenster, background='black')
canvas.place(x=20, y=30, width=380, height=280)
# Grafikobjekte
# Ereignisse
canvas.bind('<Button-1>', kurzPush)
canvas.bind('<Button-3>', langPush)
Label(tkFenster, text="Morse: ").grid(row=0, column=2)

e1 = Entry(tkFenster)
e1.grid(row=0, column=3)
e1.bind('<Return>', morse)

def task():
    global lastsave
    global MorsePhrase
    plaintextResult=""
    #print(clock() - lastsave)
    if((clock() - lastsave) > 3.5 ):
        currentLetter = ""
        if(MorsePhrase!=""):
         for x in MorsePhrase:
                   currentLetter = currentLetter + x
         try:
             plaintextResult = MorseAlphRev[currentLetter]
         except:
             print "Error"
        if(plaintextResult!=""):
            print "Letter:" + plaintextResult
        MorsePhrase = ""
        lastsave = clock()
        
    tkFenster.after(1000, task)  # reschedule event in 1 second
    
s.sendto("hello", server)
print "--------------------------------------------------------"
print " ------------------------MORSEPY----------------------"
print "--------------------------------------------------------"
print "WELCOME TO MORSEPY. LEFT CLICK = SHORT, RIGHT CLICK = LONG. TYPE IN A TEXT IN THE TEXTFIELD, PRESS ENTER AND MORSEPY WILL MORSE THE TEXT. THANK YOU FOR USING MORSEPY"

tkFenster.after(1000, task)
# Aktivierung der Ereignisschleife
tkFenster.mainloop()

