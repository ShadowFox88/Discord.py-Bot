from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "1 Owner = Bushcamper8903#3815 /--/> 1 Webserver = Online /--/> 1 Discord Bot = Online /--/> 1 TOKEN_V1 = Valid /--/> 1 TOKEN_N = ``````````````````````````````````````````````````````````` /--/> 1 API = Connected /--/> 1 Application = Hosted /--/> 1 Language = Python, JavaScript /--/> 1 Libraries = Discord.py, Discord.js, Node.js /--/> 1 ID = 767793401234980914 /--/> 1 Name = Premium Support /--/> 1 Similar Models = Admin Support /--/> 1 Default Prefix = ? /--/> 1 Suggested Prefix = ? /--BREAK--/ 2 Owner = Bushcamper8903#3815 /--/> 2 Webserver = Offline /--/> 2 Discord Bot = Online /--/> 2 TOKEN_V1 = Valid /--/> 2 TOKEN_N = ``````````````````````````````````````````````````````````` /--/> 2 API = Connected /--/> 2 Application = Not Hosted /--/> 2 Language = Python /--/> 2 Libraries = Discord.py /--/> 2 ID = 738098758876659724 /--/> 2 Name = Admin Support /--/> 2 Similar Models = Premium Support /--/> 2 Default Prefix = ? /--/> 2 Suggested Prefix = ? /--BREAK--/"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
