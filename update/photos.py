# photos.py is used to update parks.json with direct image links found in Google Photos shared album links.
# This project is currently setup to use Google Photos for all park photos.
# This script is intended to help automate the process of gathering the direct image links from Google Photos shared album links.
# To utilize this script you first need to add Google Photos shared album links to the parks.json file under the appropriate park photo "share" property.
# The Google Photos shared album links can be created and copied by going to https://photos.google.com/ finding your image and clicking Share > Create Link > Copy
# Next add these share links to to the parks.json file under the appropriate park photo "share" property.
# Once that is complete you are ready to run this script.
# This script will pull the direct image link from the Google Photos shared album link's html and add it to the parks.json file under the appropriate park photo "photo" property.

import requests
from bs4 import BeautifulSoup
import json
import os.path
import sys
import time

parks_json = {}
sleep_time = 60

# Gets the direct image link from a Google Photos shared album link.
def getDirectLink(url):
  req = requests.get(url)
  soup = BeautifulSoup(req.content, "html.parser")
  link = soup.find("meta", property="og:image")["content"].split("=")[0]
  return link

# Creating direct image links from Google Photos shared albums and adding them to parks.json file.
def createPhotoLinks():
  print("Creating direct image links from Google Photos shared albums and adding them to parks.json file")
  print("Sleep time in between requests set to " + str(sleep_time) + " seconds")
  for park in parks_json["parks"]:
    for photo_type in ["sign", "landscape1", "landscape2", "landscape3"]:
      if park["photos"][photo_type]["encrypt"]["share"] != "" and park["photos"][photo_type]["encrypt"]["photo"] == "":
        photo_link = getDirectLink(park["photos"][photo_type]["encrypt"]["share"])
        park["photos"][photo_type]["encrypt"]["photo"] = photo_link
        print("Gathered " + park["name"] + " " + photo_type + " encrypt direct link")
        time.sleep(sleep_time) # sleep to avoid Google Photos from flagging script as a robot.
      if park["photos"][photo_type]["guest"]["share"] != "" and park["photos"][photo_type]["guest"]["photo"] == "":
        photo_link = getDirectLink(park["photos"][photo_type]["guest"]["share"])
        park["photos"][photo_type]["guest"]["photo"] = photo_link
        print("Gathered " + park["name"] + " " + photo_type + " guest direct link")
        time.sleep(sleep_time) # sleep to avoid Google Photos from flagging script as a robot.
  # Outputting results to parks.json
  print("Outputting parks.json")
  json_output = json.dumps(parks_json, indent=2)
  with open("./assets/parks.json", "w") as outfile:
    outfile.write(json_output)
  print("Execution of photos.py complete")

# Start script execution.
print("Running photos.py")

# Loading parks.json file.
if os.path.isfile("./assets/parks.json"):
  print("Opening parks.json")
  parks_json_file = open("./assets/parks.json")
  try:
    parks_json = json.load(parks_json_file)
    parks_json_file.close()
  except ValueError as e:
    print("Invalid parks.json file: %s" % e)
    print("Exiting")
    parks_json_file.close()
    sys.exit()
else:
  print("File parks.json doesn't exist.")
  print("Exiting Script")
  sys.exit()

# Creating direct image links from Google Photos shared albums and adding them to parks.json file.
createPhotoLinks()