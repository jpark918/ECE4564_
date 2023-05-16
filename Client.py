import socket
import time
import subprocess
import tweepy
from cryptography.fernet import Fernet
import wolframalpha
import json
from os.path import join, dirname
import ClientKeys
import pyttsx3
import sys
import hashlib
import pickle

n = len(sys.argv) # needs to be 7 exact arguments
valid_cmd = False
if n == 7 or n == 1:
    valid_cmd = True
print(n)
bearer_token = ClientKeys.twitterbearer
screen_name = ClientKeys.twitterName

client = tweepy.Client(bearer_token)

twitterid = client.get_user(username=screen_name)
#print(type(twitterid))  # to confirm the type of object
#print(f"The Twitter ID is {twitterid.data.id}.")

# Get User's Tweets

# This endpoint/method returns Tweets composed by a single user, specified by
# the requested user ID

user_id = twitterid.data.id

response = client.get_users_tweets(user_id)
tweetobj = response.data[0]
tweetobj = tweetobj.text

brek = []
for i in range(0, len(tweetobj)):
    if tweetobj[i] == '"':
        brek.append(i)
if len(brek) != 2:
    print("You messed up the format ex: #ECE4564T18 “How old is the moon?”")

brek[0] = brek[0] + 1
hold = tweetobj[brek[0]:brek[1]]
tweetobj = hold

# By default, only the ID and text fields of each Tweet will be returned
for tweet in response.data:
    print(tweet.id)
    print(tweet.text)
# By default, the 10 most recent Tweets will be returned
# You can retrieve up to 100 Tweets by specifying max_results
response = client.get_users_tweets(user_id, max_results=100)

key = ClientKeys.Encryptionkey

# Instance the Fernet class with the key

fernet = Fernet(key)

# then use the Fernet class instance
# to encrypt the string, the string must
# be encoded to byte string before encryption
encMessage = fernet.encrypt(tweetobj.encode())
decMessage = fernet.decrypt(encMessage).decode()

result = hashlib.md5(encMessage)
print("The hexadecimal equivalent of hash is : ", end ="")
print(result.hexdigest())

print("original string: ", tweetobj)
print("encrypted string: ", encMessage)

#CLIENT CODE START
if valid_cmd:
    if n == 1:
        host = 'localhost'
        port = 2250
        socket_s = 1024
    elif n == 7:
        host = sys.argv[2]
        port = int(sys.argv[4])
        socket_s = int(sys.argv[6])

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_adress = (host, port)
# serverSocket.bind(server_adress)
# with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
serverSocket.connect(server_adress)
serverSocket.settimeout(3)

seqnum = 1
# msg = 'Ping ' + str(seqnum) + " " + str(begin)

db = {1:key, 2: encMessage, 3:result.digest()}
#db = (key, encMessage, result)
msg = pickle.dumps(db)
msg = bytes(f"{len(msg):<{10}}", 'utf-8')+msg
print(msg)
# Its important to use binary mode
message = serverSocket.sendall(msg)

while seqnum < 21:
    try:
        data = serverSocket.recv(20 * socket_s)
    except:  # subprocess.TimeoutExpired:
        print("Request Time Out from Ping " + str(seqnum))
        msg = 'Ping ' + str(seqnum) + " "# + str(begin)
        message = serverSocket.sendall(msg.encode())
        print("Sending again: ")
        continue
    if data:
        db = pickle.loads(data[10:])
        decMessage = fernet.decrypt(db[1]).decode()
        print(db)
        print("decrypted string: ", decMessage)

        engine = pyttsx3.init()

        # We can use file extension as mp3 and wav, both will work
        engine.say(decMessage)
        engine.save_to_file(decMessage, 'speech.wav')

        # Wait until above command is not finished.
        engine.runAndWait()
serverSocket.close()

#CLIENT CODE END
