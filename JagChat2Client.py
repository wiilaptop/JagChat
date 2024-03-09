#Made with love from Texas by Wiilaptop

import socket
from threading import Thread

#Declaring variables for debugging purposes
clientVer = str(1.0)

while True:
    name = input(f"Name: ")
    if name.find(":") != -1:
        print (f"A username cannot contain special characters!")
    else:
        break

host = str("0.0.0.0")
port = int("123")

sock = socket.socket()
print(f"[*] Connecting to {host}:{port}...")

sock.connect((host,port))

userInfo = f"{name},{clientVer}"
sock.send(userInfo.encode())
serverConnectionStatus = sock.recv(1024).decode()
print (serverConnectionStatus)

#For debugging purposes. Future Jayden: For when you make the client handle the disconnection
#from the server, throw it in a while True and intrepret the disconnection method. You didn't
#do it because you still need to test and typing the host and port everytime is annoying.

def ListeningForMessages():
    while True:
        message = sock.recv(1024).decode()
        print(f"\n{message}")

t = Thread(target=ListeningForMessages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

#While true for keeping the message prompt open to the User.
while True:
        
    #This is the message send prompt.
    while True:
        chatmessage = input(f"")
        if len(chatmessage) == 0:
            print (f"You can't send an empty message.")
            continue
        break
    
    if chatmessage[0] == "/":
        sock.send(chatmessage.encode())
        continue

    chatmessage = (f"<{name}>: {chatmessage}")
    sock.send(chatmessage.encode())