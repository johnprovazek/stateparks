"""scrape.py gathers the latest California State Parks data from the official website."""

# This script is used to gather the latest California State Parks data from the official California State Parks website.
# This script will then generate/update the parks.json file and the parks and overlay image directories with svg images.
# Note that this script will rely on the California State Parks url and html structure staying consistent. This may have
# changed since this script was last run. There is a copy of the California State Parks html file as it was on 9/25/2023
# in the assets directory for reference.


import json  # Used for creating, loading, and modifying json files.
import os  # Used to process directories and files.
import re  # Used to match regex patterns.
import shutil  # Used to recursively remove contents of a directory.
import sys  # Used to exit script on errors.
import requests  # Used to get the state parks html file.
from bs4 import BeautifulSoup  # Used to parse the state parks html file.
from sign import create_sign_svg, create_overlay_svg  # Used to generate state parks svg files.

# pylint: disable=W1401
# pylint: disable=W0718
# pylint: disable=C0103
# pylint: disable=W0603
# pylint: disable=E0601


def add_coords(code, name):
    """Handles adding new coordinate to a park."""
    global coords
    global coords_message
    # Skips park coordinates if flag is set.
    if not coords:
        return ""
    # Return park coordinates found in coords.json if they exist.
    if code in coords_json.keys():
        return coords_json[code]
    # Message user once that "skip-all" is an available command.
    if coords_message:
        print(
            'Adding missing coordinates. Typing "skip-all" during any enter coordinate prompt '
            + "will skip all further coordinate prompts"
        )
        coords_message = False
    # New park without coordinate information.
    park_name_code = name + " (" + code + ")"
    first_prompt = True
    while True:
        if first_prompt:
            user_input_coords = input(
                park_name_code + ' is missing coordinates. Enter new coordinates or type "skip" to skip: '
            )
        else:
            user_input_coords = input(
                "Invalid coordinates."
                + ' Valid example: "36.30952528162378,-121.88637073076984".'
                + ' Enter new coordinates or type "skip" to skip: '
            )
        if re.match(COORDS_RE, user_input_coords):
            coords_json[code] = user_input_coords
            print("Updating coords.json with new coordinates for the park " + park_name_code)
            json_output = json.dumps(coords_json, indent=2)
            with open("./assets/coords.json", "w", encoding="utf-8") as outfile:
                outfile.write(json_output)
            return user_input_coords
        if user_input_coords.lower() == "s" or user_input_coords.lower() == "skip":
            return ""
        if user_input_coords.lower() == "skip-all":
            coords = False
            return ""
        first_prompt = False


def clear_directory(path):
    """Clears contents in a directory."""
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as d_e:
            print("Failed to delete " + file_path + ". Reason: " + str(d_e))
            print("Exiting")
            sys.exit()


def new_park_entry(park_code, park_name, park_type):
    """Handles creating a new park entry."""
    return {
        "code": park_code,
        "name": park_name,
        "type": park_type,
        "coordinates": add_coords(park_code, park_name),
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
                },
            },
            "landscape1": {
                "encrypt": {
                    "share": "",
                    "photo": "",
                },
                "guest": {
                    "share": "",
                    "photo": "",
                },
            },
            "landscape2": {
                "encrypt": {
                    "share": "",
                    "photo": "",
                },
                "guest": {
                    "share": "",
                    "photo": "",
                },
            },
            "landscape3": {
                "encrypt": {
                    "share": "",
                    "photo": "",
                },
                "guest": {
                    "share": "",
                    "photo": "",
                },
            },
        },
    }


def add_overrides(park_code, park_name, park_type):
    """Adds park overrides if available."""
    if overrides:
        alc = next((x for x in overrides_json["overrides"] if x["code"] == park_code), None)
        aln = next((x for x in overrides_json["overrides"] if x["name"] == park_name), None)
        if alc == aln and alc is not None and aln is not None:
            park_name_override = alc["alias"]
            park_type_override = park_type
            if "type" in alc:
                park_type_override = alc["type"]
            return {"code": park_code, "name": park_name_override, "type": park_type_override}
    return {"code": park_code, "name": park_name, "type": park_type}


def scrape():
    """Scraping California State Parks website."""
    print("Pulling state parks data from: " + PARKS_URL)
    new_parks_data = []
    try:
        req = requests.get(PARKS_URL, timeout=15)
    except requests.exceptions.Timeout:
        print("Request Timeout. Exiting")
        sys.exit()
    soup = BeautifulSoup(req.content, "html.parser")
    small_name = ""
    small_len = 1000
    for results_lists in soup.find_all("ul", {"class": "results-area"}):
        for list_item in results_lists.find_all("li"):
            park_code = list_item.find("a")["href"].split("page_id=", 1)[1]
            park_name = re.sub(r"[^a-zA-ZÀ-ÿ0-9 -.]+", "", list_item.text).strip()
            park_type = "Other"
            for valid_type in parks_types_list:
                if valid_type in park_name:
                    park_type = valid_type
                    break
            if len(park_name) < small_len:
                small_len = len(park_name)
                small_name = park_name
            new_parks_data.append(add_overrides(park_code, park_name, park_type))
    print(small_name)
    # Verify new parks data name and id are unique.
    print("Verifying California State Parks website parks name's and id's are unique")
    for i, p_i in enumerate(new_parks_data):
        for j, p_j in enumerate(new_parks_data):
            if i != j and p_i["code"] == p_j["code"]:
                print("Duplicate parks with code (" + p_i["code"] + ") in park website. Exiting")
                sys.exit()
            if i != j and p_i["name"] == p_j["name"]:
                print("Duplicate parks with name (" + p_i["name"] + ") in park website. Exiting")
                sys.exit()
    # Constructing parks.json.
    if not parks_json["parks"]:
        # Creating fresh parks.json build.
        print("Clearing svg images from the ../images/parks and ../images/overlay directories")
        clear_directory("../images/parks")
        clear_directory("../images/overlay")
        print("Adding park data to parks.json and creating svg images")
        for park in new_parks_data:
            parks_json["parks"].append(new_park_entry(park["code"], park["name"], park["type"]))
            create_sign_svg(park["code"], park["name"], "../images/parks/")
            create_overlay_svg(park["code"], park["name"], "../images/overlay/")
    else:
        # Modifying existing parks.json with new data.
        print("Modifying parks.json with new data and building park svg images if necessary")
        # Adding a removed flag field to check if parks have been removed.
        for park in parks_json["parks"]:
            park["removed"] = True
        # Parsing new parks data.
        for park in new_parks_data:
            opc = next((x for x in parks_json["parks"] if x["code"] == park["code"]), None)
            opn = next((x for x in parks_json["parks"] if x["name"] == park["name"]), None)
            if opc == opn and opc is not None and opn is not None:  # Same code same name.
                create_sign_svg(park["code"], park["name"], "../images/parks/")
                create_overlay_svg(park["code"], park["name"], "../images/overlay/")
                opc["removed"] = False
            elif opc:  # Same code new name.
                print(
                    'Park "'
                    + opc["name"]
                    + " ("
                    + opc["code"]
                    + ')" has name "'
                    + park["name"]
                    + '" on California State Parks site'
                )
                user_input_changes = input("Accept changes (Y/N): ")
                if user_input_changes.lower() == "y" or user_input_changes.lower() == "yes":
                    print("Accepting changes")
                    opc["name"] = park["name"]
                    create_sign_svg(park["code"], park["name"], "../images/parks/")
                    create_overlay_svg(park["code"], park["name"], "../images/overlay/")
                else:
                    print("Keeping current name")
                opc["removed"] = False
            elif opn:  # Same name new code.
                print(
                    'Park "'
                    + opn["name"]
                    + " ("
                    + opn["code"]
                    + ')" has code ('
                    + park["code"]
                    + ") on California State Parks site"
                )
                user_input_changes = input("Accept changes (Y/N): ")
                if user_input_changes.lower() == "y" or user_input_changes.lower() == "yes":
                    print("Accepting changes")
                    if os.path.isfile("../images/parks/" + opn["code"] + ".svg"):
                        os.remove("../images/parks/" + opn["code"] + ".svg")
                    if os.path.isfile("../images/overlay/" + opn["code"] + ".svg"):
                        os.remove("../images/overlay/" + opn["code"] + ".svg")
                    opn["code"] = park["code"]
                    create_sign_svg(park["code"], park["name"], "../images/parks/")
                    create_overlay_svg(park["code"], park["name"], "../images/overlay/")
                else:
                    print("Keeping current code")
                opn["removed"] = False
            else:  # new name new code.
                parks_json["parks"].append(new_park_entry(park["code"], park["name"], park["type"]))
                create_sign_svg(park["code"], park["name"], "../images/parks/")
                create_overlay_svg(park["code"], park["name"], "../images/overlay/")
        # Prompting user to delete parks that are not included in website.
        for park in parks_json["parks"]:
            if park["removed"]:
                user_input_remove = input(
                    park["name"]
                    + " no longer exists on California State Parks site."
                    + " Remove park from parks.json and svg images from image directories (Y/N): "
                )
                if user_input_remove.lower() == "y" or user_input_remove.lower() == "yes":
                    parks_json["parks"].remove(park)
                    if os.path.isfile("../images/parks/" + park["code"] + ".svg"):
                        os.remove("../images/parks/" + park["code"] + ".svg")
                    if os.path.isfile("../images/overlay/" + park["code"] + ".svg"):
                        os.remove("../images/overlay/" + park["code"] + ".svg")
        # Removing "removed" flag from parks.json.
        for park in parks_json["parks"]:
            del park["removed"]
    # Alphabetically sorting parks_json by name.
    parks_json["parks"].sort(key=lambda x: x["name"])
    # Outputting results to parks.json.
    print("Outputting parks.json")
    json_output = json.dumps(parks_json, indent=2)
    with open("./assets/parks.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_output)
    print("Execution of scrape.py complete")


PARKS_URL = "https://www.parks.ca.gov/?page_id=21805"  # California State Parks Url to scrape.
parks_types_list = [  # California State Parks types of parks.
    "State Park",
    "State Historic Park",
    "State Beach",
    "State Recreation Area",
    "State Natural Reserve",
    "State Vehicular Recreation Area",
]
parks_json = {"firstname": "", "lastname": "", "parks": []}  # California State Parks json.
coords = True  # Flag sets whether or not to have user enter coords.
coords_message = True  # Flag to print coordinates skip-all command once.
coords_json = {}  # California State Parks coordinates.
overrides_json = {}  # Abbreviations for park names and park type overrides.
overrides = True  # Flag sets whether or not to use park overrides.

# Regex used to test if a coordinate is valid.
COORDS_RE = "^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"

# Start script execution.
print("Running scrape.py")

# Loading parks.json file.
if os.path.isfile("./assets/parks.json"):
    print("Opening parks.json")
    with open("./assets/parks.json", encoding="utf-8") as parks_json_file:
        try:
            parks_json = json.load(parks_json_file)
            parks_json_file.close()
        except ValueError as e:
            print("Invalid parks.json file: " + str(e))
            user_input = input("Overwrite parks.json with all new data (Y/N): ")
            if user_input.lower() != "y" and user_input.lower() != "yes":
                print("Exiting")
                parks_json_file.close()
                sys.exit()
else:
    print("File parks.json doesn't exist. Will create new parks.json")

# Loading coords.json file.
if os.path.isfile("./assets/coords.json"):
    print("Opening coords.json")
    with open("./assets/coords.json", encoding="utf-8") as coords_json_file:
        try:
            coords_json = json.load(coords_json_file)
            coords_json_file.close()
        except ValueError as e:
            print("Invalid coords.json file: " + str(e))
            print("Exiting.")
            coords_json_file.close()
            sys.exit()
else:
    print("File coords.json doesn't exist")
    user_input = input("Would you like to skip coordinates during setup (Y/N): ")
    if user_input.lower() == "y" or user_input.lower() == "yes":
        coords = False

# Loading overrides.json file.
if overrides:
    if os.path.isfile("./assets/overrides.json"):
        print("Opening overrides.json")
        with open("./assets/overrides.json", encoding="utf-8") as overrides_json_file:
            try:
                overrides_json = json.load(overrides_json_file)
                overrides_json_file.close()
            except ValueError as e:
                print("Invalid overrides.json file: " + str(e))
                print("Exiting")
                sys.exit()
    else:
        print("File overrides.json doesn't exist. Ignoring park overrides")
        overrides = False

# Scraping California State Parks website.
scrape()
