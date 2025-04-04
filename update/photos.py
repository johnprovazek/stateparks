"""photos.py updates parks.json photo links from Google Photos shared album links in parks.json."""

# This script is used to make it easier to gather direct image links in Google Photos shared albums. This project is
# currently setup to use Google Photos for all park photos. This script automates the process of gathering direct image
# links from Google Photos shared album links and adding them to the parks.json file. To utilize this script you first
# need to add Google Photos shared album links in the parks.json file under the appropriate park photo "share" property.
# The Google Photos shared album links can be created by going to Google Photos (https://photos.google.com/), finding
# your image and clicking Share > Create Link > Copy. Next add these share links to to the parks.json file under the
# appropriate park photo "share" property. Once that is complete you are ready to run this script. This script will pull
# the direct image link from the Google Photos shared album page's html and add it to the parks.json file under the
# appropriate park photo "photo" property. Note that this script will rely on Google Photos url and html structure
# staying consistent.This may have changed since this script was last run.

import json  # Used for loading and modifying parks.json file.
import os.path  # Used to process parks.json file.
import sys  # Used to exit script on errors.
import time  # Used to delay script execution.
import requests  # Used to get the Google Photos html files.
from bs4 import BeautifulSoup  # Used to parse Google Photos html files.

# pylint: disable=C0103

parks_json = {}  # California State Parks json.
sleep_time = 60  # Sleep time between html get requests to avoid flagging script as a robot.

def get_direct_link(url):
    """Gets the direct image link from a Google Photos shared album link."""
    try:
        req = requests.get(url, timeout=15)
    except requests.exceptions.Timeout:
        print("Request Timeout. Exiting")
        sys.exit()
    soup = BeautifulSoup(req.content, "html.parser")
    link = soup.find("meta", property="og:image")["content"].split("=")[0]
    return link

def create_photo_links():
    """Updating parks.json photo links from Google Photos shared album links in parks.json."""
    print("Creating direct image links from Google Photos shared album links")
    print("Sleep time in between requests set to " + str(sleep_time) + " seconds")
    for park in parks_json["parks"]:
        for photo_type in ["sign", "landscape1", "landscape2", "landscape3"]:
            encrypt = park["photos"][photo_type]["encrypt"]
            guest = park["photos"][photo_type]["guest"]
            if encrypt["share"] != "" and encrypt["photo"] == "":
                photo_link = get_direct_link(encrypt["share"])
                encrypt["photo"] = photo_link
                print("Gathered " + park["name"] + " " + photo_type + " encrypt direct link")
                time.sleep(sleep_time)  # Sleep to avoid Google Photos flagging script as a robot.
            if guest["share"] != "" and guest["photo"] == "":
                photo_link = get_direct_link(guest["share"])
                guest["photo"] = photo_link
                print("Gathered " + park["name"] + " " + photo_type + " guest direct link")
                time.sleep(sleep_time)  # Sleep to avoid Google Photos flagging script as a robot.
    # Outputting results to parks.json
    print("Outputting parks.json")
    json_output = json.dumps(parks_json, indent=2)
    with open("./assets/parks.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_output)
    print("Execution of photos.py complete")

# Start script execution.
print("Running photos.py")

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

# Creating direct image links from Google Photos shared albums and adding them to parks.json file.
create_photo_links()
