Client.py:
The client for this project is going to use a user’s twitter account to send tweets to the server. 
In this file we import the tweepy library to set the connection to the user’s account. 
The client side will read in a bearers token and screen name of the twitter account. Using those keys, 
we use tweepy functions to authenticate login into the twitter account. Once the connection is set, 
we extract the tweets from the account and encrypt them using an encryption key which is stored in the ClientsKey.py file. Once the question is encrypted, it is sent over to the server side using pickle. The server side will answer the question using wolfram alpha. Once the question is answered by the server, the question will be spoken to the server. After being spoken, it will send an encrypted answer back to the client in a .wav file. The client will use our speech algorithm to read out the answer.
Server.py:
The server script will wait for the client to send the question payload before decrypting the encrypted tweet before 
speaking the question via the pyttsx3 library. The question then gets forwarded to the wolframalpha library to get 
the question answered. Then the answer payload will encrypt the answer and send it to the client through a payload.

ClientKeys.py
Twitter login identification.
Note that in order for the text-to-speech to function properly, 
we imported the pyttsx3 library as our group had problems with the creation of an IBM cloud account
Encryption/Decryption Key

ServerKeys.py:
Note that in order for the text-to-speech to function properly, 
we imported the pyttsx3 library as our group had problems with the creation of an IBM cloud account	
Wolframalpha identification
