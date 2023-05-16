Specification: Project 2 is a text-based question and answer system using WolframAlpha's computational knowledge engine. Questions to your Q&A system are expressed as Twitter Tweets. The question and resulting answer are "spoken" using IBM Watson's text-to-speech (TTS) translation API.

The system uses two machines (laptop, desktop, virtual machine, Raspberry Pi, etc.) following the client/server model discussed in class. The server is iterative and connection-oriented. Communication among client and server is handled via stream-oriented sockets.
Workflow:
The client program captures a Twitter status object (Tweet) containing the question text.
The client bulds and sends a question "payload" to the server via sockets. 
The server unpacks the payload, speaks the question, and sends the question to the WolframAlpha engine and receives the answer.
The server builds and sends an answer "payload" back to the client.
The client unpacks the payload, speaks the answer, and displays the answer on the monitor.

Additional information: 
Instead of two machines, there will be 2 separate instances of the client and server on a single machine. This will be done using the Windows Powershell terminal.
An issue with IBM Watson's text-to-speech occurred during the development process, the python text-to-speech library will be used as a replacement.
In order for the Twitter tweets to be recongized inside the Python code, the Tweepy library will be used as well as a Twitter development account, as the Tweepy library will require an API key. 
The format of "question" tweet will look like: #ECE4564TXX "question_text". Example: #ECE4564T18 "How old is the moon?"
