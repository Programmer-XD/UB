import os
from subprocess import getoutput as r


SESSION = input("Enter you Pyrogram V-2 Session: ")
if len(SESSION) < 50:
    print("[Sophia System] Enter session correctly!")
    exit()
API_ID = input("Enter Api ID: ")
API_HASH = input("Enter Api hash: ")
ACCESS_CODE = input("Enter ACCESS_CODE: ")
ACCESS_PIN = input("Enter ACCESS_PIN: ")
MONGO_DB_URI = input("Enter MONGO_DB_URI: ")
YOUR_REPO_LINK = input("Enter your forked repo link: ")

print("[INFO] Processing values...")

try:
  os.environ['API_ID'] = API_ID
  os.environ['API_HASH'] = API_HASH
  os.environ['SESSION'] = SESSION
  os.environ['YOUR_REPO_LINK'] = YOUR_REPO_LINK
  os.environ['ACCESS_CODE'] = ACCESS_CODE
  os.environ['ACCESS_PIN'] = ACCESS_PIN
  os.environ['MONGO_DB_URI'] = MONGO_DB_URI
except Exception as e:
  raise e
  r("python3 -m setup.py")
  exit()

print("[INFO] Success, Starting Sophia..")
r("python3 -m Sophia")
