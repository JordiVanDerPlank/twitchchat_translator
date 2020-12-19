from google_trans_new import google_translator
import webbrowser

from tkinter import *


import socket, string, threading

global NICK, PASS

HOST = "irc.twitch.tv"
NICK = ""
PORT = 6667
PASS = ""


# -------------------------------ADAH FRAMES LOOKS---------------------------#

class Screen(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()


# SCREEN SIZE AND TITLE
gui = Tk()
gui.geometry("640x200")
gui.configure(bg="#18181b")
app = Screen(master=gui)
app.master.title("Twitch Chat Translator v0.1")
app.configure(bg="#18181b")

# STOP PROGRAM WHEN RED CROSS IS PRESSED
gui.protocol("WM_DELETE_WINDOW", gui.destroy)

scroll = Scrollbar(gui)
scroll.pack(side=RIGHT, fill=Y)

# TEXT SHOWN ON SCREEN
eula = Text(gui, wrap=NONE, yscrollcommand=scroll.set, bg="#18181b", foreground="white")

global connected


def showGui():
    if (btnText.get() != "Connect"):
        connected = True
    eula.pack(side="bottom")
    global NICK, PASS
    NICK = str.lower(nickName.get())
    PASS = auth.get()
    # connected = False
    firstStart()


def sendToAuth():
    webbrowser.open("https://twitchapps.com/tmi/")


btnText = StringVar()
btn = Button(app, textvariable=btnText, command=showGui, foreground="white")
btnText.set("Connect")
# Set the position of button on the top of window
btn.pack(side='top')
btn.configure(bg="#9147ff")

btnOAuth = Button(app, text="Get OAuth", command=sendToAuth, foreground="white")
btnOAuth.pack(side='right', padx="5")
btnOAuth.configure(bg="#9147ff")

# nickname input
nickNameLabelText = StringVar()
nickNameLabelText.set("Nickname")
nickNameLabelDir = Label(app, textvariable=nickNameLabelText, height=4)
nickNameLabelDir.configure(foreground="white", bg="#18181b")
nickNameLabelDir.pack(side="left")

nickName = Entry(app)
nickName.pack(side="left")

# authorization code chat
authLabelText = StringVar()
authLabelText.set("Authorization key")
authLabelDir = Label(app, textvariable=authLabelText, height=4)
authLabelDir.configure(foreground="white", bg="#18181b")
authLabelDir.pack(side="left")

auth = Entry(app, show="*")
auth.pack(side="left")

# ---------------------------------READING CHAT AND TRANSLATING---------------------------------------#

global s
translator = google_translator()

def send_message(message):
    s.send(bytes("PRIVMSG #" + NICK + " :" + message + "\r\n", "UTF-8"))

restart = False


def translate():
    while restart == False:
        try:
            # print("hello")
            response = s.recv(2048).decode("utf-8")
            if response == "PING :tmi.twitch.tv\r\n":
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            else:
                username = re.search(r"\w+", response).group(0)
                CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

                message = CHAT_MSG.sub("", response).rstrip('\n')

                if 'End of /NAMES list' in message:
                    connected = True

                if ("tmi.twitch.tv" not in message and "@" not in message):
                    detectedLanguage = translator.detect(message)
                    # print("Detected Language: " + str(detectedLanguage))
                    if ("en" not in detectedLanguage):
                        translate_text = translator.translate(message, lang_tgt='en')
                        if (message != translate_text):
                            # print(translate_text)
                            s.send("PRIVMSG #{} :{}\r\n".format("theshelfman", username + " said '" + translate_text + "'").encode("utf-8"))
        except:
            return

def checkConnection():
    if (NICK == "" or PASS == ""):
        eula.delete("1.0", "end")
        eula.insert("1.0", "Nickname or Password has not been entered")
    else:
        nickName.delete('0', 'end')
        nickName.forget()
        nickNameLabelText.set("Connected")
        auth.delete('0', 'end')
        authLabelText.set("")
        auth.forget()
        btn.forget()
        btnOAuth.forget()
        eula.insert("1.0", "Translating chat for " + NICK + "\n")
        eula.insert("1.0", "Successfully started\n")

        thread = threading.Thread(target=translate)
        thread.start()


def firstStart():
    try:
        global s
        s = socket.socket()
        s.connect((HOST, PORT))
        s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
        s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
        s.send(bytes("JOIN #" + NICK + " \r\n", "UTF-8"))
        checkConnection()


    except Exception as e:
        eula.insert("1.0", "Something went wrong, couldn't connect")


app.mainloop()
