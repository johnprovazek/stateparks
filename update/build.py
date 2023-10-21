# build.py is used to compile html files from data in parks.json and jinja html templates.
# This script also builds an encrypted html file by adapting code from this PageCrypt project (https://github.com/MaxLaumeister/pagecrypt)

# main.html is the main project html.
# This file can be used for local testing without having to enter a passphrase.
# This file should not be exposed in your GitHub repo, to keep image links hidden. It is included in the .gitignore.
# This html file will later be encrypted into a variable and added to the index.html file to be used with GitHub pages.

# guest.html is meant to be exposed in your GitHub repo.
# This file should contain image links that you don't mind being publicly accessible.
# This file acts as a demo of the website.

# index.html
# This file is the login page that contains the encrypted main.html code.
# This file was adapted from this PageCrypt project (https://github.com/MaxLaumeister/pagecrypt)

import jinja2
import json
import os.path
import sys

from Crypto import Random
from Crypto.Util.py3compat import bchr
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from base64 import b64encode
from getpass import getpass
import codecs

# Builds HTML file using jinja templates.
def buildHTML(templatePath, resultPath, context):
  environment = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
  with open(resultPath, mode="w", encoding="utf-8") as results:
    results.write(environment.get_template(templatePath).render(context))
    print(f"... wrote {resultPath}")

# Start script execution.
print("Running build.py")

# Loading parks.json file.
if os.path.isfile("./assets/parks.json"):
  print("Opening parks.json")
  parks_json_file = open("./assets/parks.json")
  try:
    parks_json = json.load(parks_json_file)
    parks_json_file.close()
  except ValueError as e:
    print("Invalid parks.json file: %s" % e)
    print("Exiting script")
    parks_json_file.close()
    sys.exit()
else:
  print("File parks.json doesn't exist")
  print("Exiting script")
  sys.exit()

# Loading passphrase.txt file.
if os.path.isfile("./assets/passphrase.txt"):
  print("Opening passphrase.txt")
  passphrase_txt = open("./assets/passphrase.txt")
  try:
    passphrase = passphrase_txt.readline().rstrip()
    passphrase_txt.close()
  except ValueError as e:
    print("Invalid passphrase.txt file: %s" % e)
    print("Exiting script")
    parks_json_file.close()
    sys.exit()
else:
  print("File passphrase.txt doesn't exist")
  print("Exiting script")
  sys.exit()

# Initializing jinja template variables.
print("Initializing jinja template variables")
parks_complete = parks_json["parks"]
parks_encrypt = []
parks_guest = []
parks_visit_stats = {
  "all": {
    "count": 0,
    "visited": 0
  },
  "state-park": {
    "count": 0,
    "visited": 0
  },
  "state-historic-park": {
    "count": 0,
    "visited": 0
  },
  "state-beach": {
    "count": 0,
    "visited": 0
  },
  "state-recreation-area": {
    "count": 0,
    "visited": 0
  },
  "state-natural-reserve": {
    "count": 0,
    "visited": 0
  },
  "state-vehicular-recreation-area": {
    "count": 0,
    "visited": 0
  },
  "other": {
    "count": 0,
    "visited": 0
  }
}

# Building jinja template variables.
for park in parks_json["parks"]:
  park_data = {
    "code": park["code"],
    "name": park["name"],
    "type": park["type"].replace(" ", "-").lower(),
    "visited": park["visited"],
    "overlay": park["overlay"],
    "coordinates": park["coordinates"]
  }

  # Keeping track of number of parks per category.
  parks_visit_stats[park_data["type"]]["count"] += 1
  parks_visit_stats["all"]["count"] += 1

  if park["visited"]:
    # Keeping track of number of parks visited per category.
    parks_visit_stats[park_data["type"]]["visited"] += 1
    parks_visit_stats["all"]["visited"] += 1
    # Gathering links for encrypted site.
    park_data_encrypt = park_data.copy()
    park_data_encrypt["sign"] = park["photos"]["sign"]["encrypt"]["photo"]
    park_data_encrypt["landscape1"] = park["photos"]["landscape1"]["encrypt"]["photo"]
    park_data_encrypt["landscape2"] = park["photos"]["landscape2"]["encrypt"]["photo"]
    park_data_encrypt["landscape3"] = park["photos"]["landscape3"]["encrypt"]["photo"]
    parks_encrypt.append(park_data_encrypt)
    # Gathering links for guest site.
    park_data_guest = park_data.copy()
    park_data_guest["sign"] = park["photos"]["sign"]["guest"]["photo"]
    if park["photos"]["landscape1"]["guest"]["photo"] != "":
      park_data_guest["landscape1"] = park["photos"]["landscape1"]["guest"]["photo"]
    else:
      park_data_guest["landscape1"] = park["photos"]["landscape1"]["encrypt"]["photo"]
    if park["photos"]["landscape2"]["guest"]["photo"] != "":
      park_data_guest["landscape2"] = park["photos"]["landscape2"]["guest"]["photo"]
    else:
      park_data_guest["landscape2"] = park["photos"]["landscape2"]["encrypt"]["photo"]
    if park["photos"]["landscape3"]["guest"]["photo"] != "":
      park_data_guest["landscape3"] = park["photos"]["landscape3"]["guest"]["photo"]
    else:
      park_data_guest["landscape3"] = park["photos"]["landscape3"]["encrypt"]["photo"]
    parks_guest.append(park_data_guest)
  else:
    parks_encrypt.append(park_data)
    parks_guest.append(park_data)

# Building main.html.
print("Building main.html")
buildHTML("./assets/main.html.jinja2","../main.html", {
  "parks": parks_encrypt,
  "stats": parks_visit_stats
})

# Building guest.html.
print("Building guest.html")
buildHTML("./assets/main.html.jinja2","../guest.html", {
  "parks": parks_guest,
  "stats": parks_visit_stats
})

# Encrypting main.html in index.html.
# Adapted from this PageCrypt project (https://github.com/MaxLaumeister/pagecrypt).
print("Building index.html")

# Sanitizing input.
print("Sanitizing main.html for encryption")
main_html = "../main.html"
try:
  with open(main_html, "rb") as f:
    data = f.read()
except:
  print("Cannot open file: %s"%main_html)
  exit(1)

# Encrypting input.
print("Encrypting main.html for index.html")
salt = Random.new().read(32)
key = PBKDF2(
  passphrase.encode('utf-8'),
  salt,
  count=100000,
  dkLen=32,
  hmac_hash_module=SHA256
)
iv = Random.new().read(16)
cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
encrypted, tag = cipher.encrypt_and_digest(data)
encryptedHTML = f'"{b64encode(salt+iv+encrypted+tag).decode("utf-8")}"'

# Building index.html.
buildHTML("./assets/index.html.jinja2","../index.html", {
  "encryptedHTML": encryptedHTML,
})
print("Execution of build.py complete")