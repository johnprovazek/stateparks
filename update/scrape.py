# scrape.py is used to gather the latest California State Parks data from the official California State Parks website.
# The script will then generate/update the parks.json file and the parks and overlay image directories with SVG images.
# Note that this script will rely on the California State Parks url and html structure staying consistent. This may have changed since this script was last run.
# There is a copy of the California State Parks html file as it was on 9/25/2023 in the assets directory for reference.

import requests
from bs4 import BeautifulSoup
import re
import json
import os
import sys
from sign import createSignSVG, createOverlaySVG
import shutil

parks_url = "https://www.parks.ca.gov/?page_id=21805"
parks_types_list = [
  "State Park",
  "State Historic Park",
  "State Beach",
  "State Recreation Area",
  "State Natural Reserve",
  "State Vehicular Recreation Area"
]
parks_coords = {}
parks_json = {
  "parks": []
}

# Handles adding new coordinate to a park.
def addCoords(code, name):
  if code in parks_coords.keys():
    return parks_coords[code]
  else:
    firstRun = True
    while True:
      if firstRun:
        user_input = input("The park " + name + " (" + code + ") is missing coordinate info in coords.json. Enter new coordinates or type \"skip\" to skip: ")
      else:
        user_input = input("Error. Invalid coordinates string. Omit any spaces in coordinates. Enter new coordinates or type \"skip\" to skip: ")
      if re.match("^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$", user_input):
        parks_coords[code] = user_input
        print("Updating the coords.json with new coordinates for the park " + name + " (" + code + ")")
        json_output = json.dumps(parks_coords, indent=2)
        with open("./assets/coords.json", "w") as outfile:
          outfile.write(json_output)
        return user_input
      elif user_input.lower() == "skip":
        return ""
      firstRun = False

# Clears contents of a directory.
def removeDirectoryContents(path):
  for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    try:
      if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
      elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
    except Exception as e:
      print('Failed to delete %s. Reason: %s' % (file_path, e))

# Scraping California State Parks website.
def scrape():
  # Pulling state parks data.
  print("Pulling state parks data from: %s" % parks_url)
  new_parks_data = []
  req = requests.get(parks_url)
  soup = BeautifulSoup(req.content, "html.parser")
  for results_lists in soup.find_all("ul", {"class": "results-area"}):
    for list_item in results_lists.find_all("li"):
      park_code = list_item.find("a")["href"].split("page_id=",1)[1]
      park_name = re.sub(r"[^a-zA-ZÀ-ÿ0-9 -.]+", "", list_item.text).strip()
      park_type = "Other"
      for type in parks_types_list:
        if type in park_name:
          park_type = type
      new_parks_data.append({
        "code" : park_code,
        "name" : park_name,
        "type" : park_type
      })
  
  # Verify new parks data name and id are unique.
  print("Verifying California State Parks website parks name's and id's are unique")
  for i, p_i in enumerate(new_parks_data):
    for j, p_j in enumerate(new_parks_data):
      if i != j:
        if p_i["code"] == p_j["code"]:
          print("Duplicate parks with code (" + p_i["code"] + ") pulled from park website. Exiting Script.")
          sys.exit()
        if p_i["name"] == p_j["name"]:
          print("Duplicate parks with name \"" + p_i["name"] + "\" pulled from park website. Exiting Script.")
          sys.exit()

  # Constructing parks.json.
  if not parks_json["parks"]:
    # Creating fresh parks.json build.
    print("Constructing a fresh build of parks.json and park SVG images")
    print("Clearing SVG images from the ../img/parks and ../img/overlay directories.")
    removeDirectoryContents('../img/parks')
    removeDirectoryContents('../img/overlay')
    print("Adding park data to parks.json and creating SVG images.")
    for park in new_parks_data:
      parks_json["parks"].append({
        "code": park["code"],
        "name": park["name"],
        "type": park["type"],
        "coordinates": addCoords(park["code"], park["name"]),
        "visited": False,
        "overlay": False,
        "photos": {
          "sign": {
            "encrypt": {
              "share": "",
              "photo": "",
            },
            "guest": {
              "share": "",
              "photo": "",
            }
          },
          "landscape1": {
            "encrypt": {
              "share": "",
              "photo": "",
            },
            "guest": {
              "share": "",
              "photo": "",
            }
          },
          "landscape2" : {
            "encrypt": {
              "share": "",
              "photo": "",
            },
            "guest": {
              "share": "",
              "photo": "",
            }
          },
          "landscape3" : {
            "encrypt": {
              "share": "",
              "photo": "",
            },
            "guest": {
              "share": "",
              "photo": "",
            }
          }
        }
      })
      createSignSVG(park["code"], park["name"], "../img/parks/")
      createOverlaySVG(park["code"], park["name"], "../img/overlay/")
  else:
    # Modifying existing parks.json with new data.
    print("Modifying existing parks.json with new data and building park SVG images where necessary")
    # Adding a removed flag field to check if parks have been removed.
    for park in parks_json["parks"]:
      park["removed"] = True
    # Parsing new parks data.
    for park in new_parks_data:
      opc = next((x for x in parks_json["parks"] if x["code"] == park["code"]), None)
      opn = next((x for x in parks_json["parks"] if x["name"] == park["name"]), None)
      if opc == opn and opc != None and opn != None: # Same code same name.
        createSignSVG(park["code"], park["name"], "../img/parks/")
        createOverlaySVG(park["code"], park["name"], "../img/overlay/")
        opc["removed"] = False
      elif opc: # Same code new name.
        print("Park \"" + opc["name"] + " (" + opc["code"] + ")\" has name \"" + park["name"] + "\" on California State Parks site.")
        user_input = input("Accept changes (Y/N): ")
        if user_input.lower() == "y" or user_input.lower() == "yes":
          print("Accepting changes")
          opc["name"] = park["name"]
          createSignSVG(park["code"], park["name"], "../img/parks/")
          createOverlaySVG(park["code"], park["name"], "../img/overlay/")
        else:
          print("Keeping current name.")
        opc["removed"] = False
      elif opn: # Same name new code.
        print("Park \"" + opn["name"] + " (" + opn["code"] + ")\" has code (" + park["code"] + ") on California State Parks site.")
        user_input = input("Accept changes (Y/N): ")
        if user_input.lower() == "y" or user_input.lower() == "yes":
          print("Accepting changes")
          if os.path.isfile("../img/parks/" + opn["code"] + ".svg"):
            os.remove("../img/parks/" + opn["code"] + ".svg")
          if os.path.isfile("../img/overlay/" + opn["code"] + ".svg"):
            os.remove("../img/overlay/" + opn["code"] + ".svg")
          opn["code"] = park["code"]
          createSignSVG(park["code"], park["name"], "../img/parks/")
          createOverlaySVG(park["code"], park["name"], "../img/overlay/")
        else:
          print("Keeping current code.")
        opn["removed"] = False
      else: # new name new code.
        parks_json["parks"].append({
          "code": park["code"],
          "name": park["name"],
          "type": park["type"],
          "coordinates": addCoords(park["code"], park["name"]),
          "visited": False,
          "overlay": False,
          "photos" : {
          "sign": {
            "encrypt": {
              "share": "",
              "photo": "",
            },
            "guest": {
              "share": "",
              "photo": "",
            }
          },
          "landscape1": {
            "encrypt": {
              "share": "",
              "photo": "",
            },
            "guest": {
              "share": "",
              "photo": "",
            }
          },
          "landscape2" : {
            "encrypt": {
              "share": "",
              "photo": "",
            },
            "guest": {
              "share": "",
              "photo": "",
            }
          },
          "landscape3" : {
            "encrypt": {
              "share": "",
              "photo": "",
            },
            "guest": {
              "share": "",
              "photo": "",
            }
          }
          },
          "removed": False
        })
        createSignSVG(park["code"], park["name"], "../img/parks/")
        createOverlaySVG(park["code"], park["name"], "../img/overlay/")
    # Prompting user to delete parks that are not included in website.
    for park in parks_json["parks"]:
      if park["removed"]:
        user_input = input("\"" + park["name"] + "\" no longer exists on California State Parks site. Remove park from parks.json and SVG images from image directories (Y/N): ")
        if user_input.lower() == "y" or user_input.lower() == "yes":
          parks_json["parks"].remove(park)
          if os.path.isfile("../img/parks/" + park["code"] + ".svg"):
            os.remove("../img/parks/" + park["code"] + ".svg")
          if os.path.isfile("../img/overlay/" + park["code"] + ".svg"):
            os.remove("../img/overlay/" + park["code"] + ".svg")
    # Removing "removed" flag from parks.json.
    for park in parks_json["parks"]:
      del park['removed']

  # Alphabetically sorting parks_json by name.
  parks_json["parks"].sort(key=lambda x: x["name"])

  # Outputting results to parks.json.
  print("Outputting parks.json")
  json_output = json.dumps(parks_json, indent=2)
  with open("./assets/parks.json", "w") as outfile:
    outfile.write(json_output)
  print("Execution of scrape.py complete")

# Start script execution.
print("Running scrape.py")

# Loading coords.json file.
if os.path.isfile("./assets/coords.json"):
  print("Opening coords.json")
  coords_json_file = open("./assets/coords.json")
  try:
    parks_coords = json.load(coords_json_file)
    coords_json_file.close()
  except ValueError as e:
    print("Invalid coords.json file: %s" % e)
    sys.exit()
else:
  print("Missing coords.json file.")
  sys.exit()

# Loading parks.json file.
if os.path.isfile("./assets/parks.json"):
  print("Opening parks.json")
  parks_json_file = open("./assets/parks.json")
  try:
    parks_json = json.load(parks_json_file)
    parks_json_file.close()
  except ValueError as e:
    print("Invalid parks.json file: %s" % e)
    user_input = input("Overwrite parks.json with all new data (Y/N): ")
    if user_input.lower() != "y" and user_input.lower() != "yes":
      print("Exiting Script")
      parks_json_file.close()
      sys.exit()
else:
  print("File parks.json doesn't exist. Creating new parks.json")

# Scraping California State Parks website.
scrape()