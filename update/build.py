"""build.py compiles html files from data in parks.json utilizing jinja html templates."""

# This script is used to compile html files from data in parks.json and jinja html templates. This script also builds an
# encrypted html file by adapting code from PageCrypt (https://github.com/MaxLaumeister/pagecrypt). This allows the
# image links in the html file to be encrypted and stored publicly while still taking advantage of GitHub pages free
# hosting.
#
# main.html
# This file is the main content in your application and this file can be used for local testing without having to enter
# a passphrase. This file should not be exposed in your GitHub repo, to keep image links hidden. It is included in the
# .gitignore file. This html file will be encrypted with PageCrypt and added to the index.html file to be used with
# GitHub pages.
#
# index.html
# This file is the login page that contains the encrypted main.html code. This file was adapted from PageCrypt
# (https://github.com/MaxLaumeister/pagecrypt).
#
# guest.html
# This file serves as the guest page that should only contain image links that you don't mind being publicly accessible.
# This file also acts as a demo page for this website.

from base64 import b64encode  # Used to encrypt html file.
import json  # Used for loading parks.json file.
import os.path  # Used to process parks.json file.
import sys  # Used to exit script on errors.
import jinja2  # Used to build html files based on jinja html templates.
from Crypto import Random  # Used to encrypt html file.
from Crypto.Cipher import AES  # Used to encrypt html file.
from Crypto.Hash import SHA256  # Used to encrypt html file.
from Crypto.Protocol.KDF import PBKDF2  # Used to encrypt html file.

# pylint: disable=C0103
# pylint: disable=W0718


def build_html(template_path, result_path, context):
    """Builds html file using jinja templates."""
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
    with open(result_path, mode="w", encoding="utf-8") as results:
        results.write(environment.get_template(template_path).render(context))
        print(f"... wrote {result_path}")


# Start script execution.
print("Running build.py")

# Loading parks.json file.
if os.path.isfile("./assets/parks.json"):
    print("Opening parks.json")
    with open("./assets/parks.json", encoding="utf-8") as parks_json_file:
        try:
            parks_json = json.load(parks_json_file)
            parks_json_file.close()
        except ValueError as e:
            print("Invalid parks.json file: " + str(e))
            print("Exiting")
            parks_json_file.close()
            sys.exit()
else:
    print("File parks.json doesn't exist")
    print("Exiting")
    sys.exit()

# Loading passphrase.txt file.
if os.path.isfile("./assets/passphrase.txt"):
    print("Opening passphrase.txt")
    with open("./assets/passphrase.txt", encoding="utf-8") as passphrase_txt_file:
        try:
            passphrase = passphrase_txt_file.readline().rstrip()
            passphrase_txt_file.close()
        except ValueError as e:
            print("Invalid passphrase.txt file: " + str(e))
            print("Exiting")
            parks_json_file.close()
            sys.exit()
else:
    print("File passphrase.txt doesn't exist")
    print("Exiting")
    sys.exit()

# Initializing jinja template variables.
print("Initializing jinja template variables")
parks_encrypt = []
parks_guest = []
parks_visit_stats = {
    "all": {"count": 0, "visited": 0},
    "state-park": {"count": 0, "visited": 0},
    "state-historic-park": {"count": 0, "visited": 0},
    "state-beach": {"count": 0, "visited": 0},
    "state-recreation-area": {"count": 0, "visited": 0},
    "state-natural-reserve": {"count": 0, "visited": 0},
    "state-vehicular-recreation-area": {"count": 0, "visited": 0},
    "other": {"count": 0, "visited": 0},
}

# Building jinja template variables.
for park in parks_json["parks"]:
    park_data = {
        "code": park["code"],
        "name": park["name"],
        "type": park["type"].replace(" ", "-").lower(),
        "visited": park["visited"],
        "overlay": park["overlay"],
        "coordinates": park["coordinates"],
    }
    # Keeping track of number of parks per type.
    parks_visit_stats[park_data["type"]]["count"] += 1
    parks_visit_stats["all"]["count"] += 1
    if park["visited"]:
        # Keeping track of number of parks visited per type.
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
build_html(
    "./assets/main.html.jinja2",
    "../main.html",
    {
        "firstname": parks_json["firstname"],
        "lastname": parks_json["lastname"],
        "parks": parks_encrypt,
        "stats": parks_visit_stats,
    },
)

# Building guest.html.
print("Building guest.html")
build_html(
    "./assets/main.html.jinja2",
    "../guest.html",
    {
        "firstname": parks_json["firstname"],
        "lastname": parks_json["lastname"],
        "parks": parks_guest,
        "stats": parks_visit_stats,
    },
)

# Building index.html adding encrypted main.html file.
# Adapted from this PageCrypt (https://github.com/MaxLaumeister/pagecrypt).
print("Building index.html")

# Sanitizing input.
print("Sanitizing main.html for encryption")
try:
    with open("../main.html", "rb") as main_html_file:
        data = main_html_file.read()
except Exception as e:
    print("Cannot open file main.html: " + str(e))
    sys.exit()

# Encrypting input.
print("Encrypting main.html for index.html")
salt = Random.new().read(32)
key = PBKDF2(passphrase.encode("utf-8"), salt, count=100000, dkLen=32, hmac_hash_module=SHA256)
iv = Random.new().read(16)
cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
encrypted, tag = cipher.encrypt_and_digest(data)
encryptedHTML = f'"{b64encode(salt+iv+encrypted+tag).decode("utf-8")}"'

# Building index.html.
build_html(
    "./assets/index.html.jinja2",
    "../index.html",
    {
        "encryptedHTML": encryptedHTML,
    },
)
print("Execution of build.py complete")
