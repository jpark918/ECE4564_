# We need to import the socket library implementation
import socket
import ClientKeys
from cryptography.fernet import Fernet
import pyttsx3
import wolframalpha
import ServerKeys
import pickle
# We will need the following module to generate randomized packet loss
import random

# We need this library to print messages on the screen
import sys

n = len(sys.argv) # needs to be 7 exact arguments
valid_cmd = False
if n == 5 or n == 1:
    valid_cmd = True
print(n)

if valid_cmd:
    if n == 1:
        port = 2250
        socket_s = 1024
        ipaddress = 'localhost'

    elif n == 5:
        port = int(sys.argv[2])
        socket_s = int(sys.argv[4])
        ipaddress = socket.gethostbyname(socket.gethostname())

# Set the Server listening port
#port = 2250
# Create a TCP socket
# Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assign localhost IP address and port number to sock
server_adress = (ipaddress, port)
serverSocket.bind(server_adress)
#Print Debug information on the console
print('Started our TCP Ping Server on address %s port %s' % server_adress)

# TCP is a connection-oriented protocol, so we need to listen to the port
serverSocket.listen(1)
go = True

while go:
    print("Waiting for a connection at port %s" % port)
    # Accept the incoming connection
    socketConnection, client_address = serverSocket.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        if True:
            # Receive the client data in a buffer of 1024 bytes
            clientdata = socketConnection.recv(20*1024)
            #print ('received "%s"' % clientdata)
            # go = False

            db = pickle.loads(clientdata[10:])

            key = ClientKeys.Encryptionkey
            fernet = Fernet(db[1])
            # decrypt the encrypted string with the
            # Fernet instance of the key,
            # that was used for encrypting the string
            # encoded byte string is returned by decrypt method,
            # so decode it to string with decode methods
            decMessage = fernet.decrypt(db[2]).decode()

            print("decrypted string: ", decMessage)

            engine = pyttsx3.init()

            # We can use file extension as mp3 and wav, both will work
            engine.say(decMessage)
            engine.save_to_file(decMessage, 'speech.wav')

            # Wait until above command is not finished.
            engine.runAndWait()

            question = decMessage

            # App id obtained by the above steps
            app_id = ServerKeys.wolf_id

            # Instance of wolf ram alpha
            # client class
            client = wolframalpha.Client(app_id)

            # Stores the response from
            # wolf ram alpha
            res = client.query(question)

            # Includes only text from the response
            answer = next(res.results).text

            print(answer)
            encMessage = fernet.encrypt(answer.encode())
            db2 = {1: encMessage, 2: db[3]}
            # db = (key, encMessage, result)
            msg = pickle.dumps(db2)
            msg = bytes(f"{len(msg):<{10}}", 'utf-8') + msg
            print(msg)
            socketConnection.sendall(msg)
            go = False

    finally:
        # Clean up the connection via closing the Socket
        socketConnection.close()

print ('Server received "%s"' % clientdata)