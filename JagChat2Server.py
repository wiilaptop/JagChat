#Made with love from Texas by Wiilaptop

#Importing required modules. Socket for connections, and daemon threads for running each client.
import socket
from threading import Thread

#Host and Port to host the server on.
host = str("0.0.0.0")
port = int("123")

#Version of the server. If clients do not match this verison, they will not be able to connect.
serverVer = str(1.0)

#Initalizing the set and list for sockets and usernames respectively.
client_sockets=set()
totalUsersInRoom = []

#Opening the socket for clients to connect.
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host,port))
sock.listen(5)
print (f"We are listening for anything on {host} & {port}...")

def MessageBroadcast(usersocket, Name):
    while True:
        try:
            message = usersocket.recv(1024).decode()
        except ConnectionResetError as e:
            print (f"[!] {e} found! Handling...")

        #If a message is empty (Only possible if someone disconnects)
        #Remove that socket from the list, and continue the iteration.
        if message == "":
            print (f"[* - DISCONNECT] {Name} left the server!")
            client_sockets.remove(usersocket)
            totalUsersInRoom.remove(Name)
            continue

        #Command Processing if the first character of the message begins with /
        try:
            if message[0] == "/":
                print (f"[*] {Name} RAN COMMAND: {message}")
                if message == "/list":
                    totalUsers = "Users currently connected: "
                    for i in totalUsersInRoom: 
                        totalUsers += f"{i} | "
                    usersocket.send(totalUsers.encode())
                    continue
                if message == "/set":
                    print (f"This is the set: {client_sockets}")
        
        #Catching IndexError if a message is sent with no content.
        #The Clients should catch any empty messages, and the server inteprets empty messages
        #as a disconnect, but this is here just in case. May be depricated, but more testing is needed.
        except IndexError:
            pass

        print (f"[*] MESSAGE SENT: {message}")

        #Replicating the message sent from a client to each connected client.
        #note: USERSOCKET - each individual user. CLIENT_SOCKETS - everyone connected.
        try:
            for usersocket in client_sockets:
                usersocket.send(message.encode())

        #Catching BrokenPipeError Exception since it occurs if a client force-closes.
        except BrokenPipeError:
            pass

while True:
    #Accepting the socket connection
    usersocket, client_address = sock.accept()

    #The client will send the name of the user & its version to the server.
    clientInfo = usersocket.recv(1024).decode()
    Name, ClientVer = clientInfo.split(",")
    print (f"\n[*] Connection from {usersocket} - Name: {Name}, Client Ver - {ClientVer}\n")

    #If the client's version does NOT match the server's version, send that client a disconnect message
    #and do NOT add them to the client_sockets - the set of approved users to recieve messages.
    if ClientVer != serverVer:
        mismatchVer = f"[!] This client does not match the version of the server."
        usersocket.send(mismatchVer.encode())
        continue
    else:
        connectionGood = f"[✓] Connection Successful!"
        usersocket.send(connectionGood.encode())

    #If a client passes the version check, add their name and connection to the set.
    client_sockets.add(usersocket)
    totalUsersInRoom.append(Name)

    #Start the daemon for processing incoming messages
    t = Thread(target=MessageBroadcast, args=(usersocket, Name, ))
    t.daemon = True
    t.start()