from google_trans_new import google_translator

translator = google_translator()

translate_text = translator.translate('สวัสดีจีน',lang_tgt='en')  
print(translate_text)
#output: Hello china


import socket
import time
import re

s = socket.socket()
s.connect(("irc.twitch.tv", 6667))
s.send("PASS {}\r\n".format("oauth:4bc5l5ahced2z9u2qj804oqufacktz").encode("utf-8"))
s.send("NICK {}\r\n".format("theshelfman").encode("utf-8"))
s.send("JOIN #{}\r\n".format("theshelfman").encode("utf-8"))

connected = False
run = True

while run:
    response = s.recv(2048).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0)
        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

        message = CHAT_MSG.sub("", response).rstrip('\n')

        if 'End of /NAMES list' in message:
            connected = True

        if ("tmi.twitch.tv" not in message):
            detectedLanguage = translator.detect(message)
            print("Detected Language: " + str(detectedLanguage))
            if ("en" not in detectedLanguage):
                translate_text = translator.translate(message, lang_tgt='en')
                print(translate_text)

