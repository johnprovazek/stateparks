# sign.py is used to generate California State Park SVG sign and overlay images.
# This script can be ran in two configurations.
# Either the script is ran without any arguments or with both the -c/--code and -n/--name arguments together.
#
# Running the script without any arguments will first delete all SVG images in the parks and overlay image directories. 
# The script will then create new SVG images based on the data pulled from parks.json.
# Example: python sign.py
#
# Running the script with both the -c/--code and -n/--name arguments will create a new SVG sign and overlay image.
# The file will be named based on the -c/--code argument and the text in the SVG image will be taken from the -n/--name argument.
# Example script execution: python sign.py -c "405" -n "Hungry Valley State Vehicular Recreation Area"

import cairo
import argparse
import sys
import os
import shutil
import json

# Converting hex color string to rgb decimal format.
def hex_to_rgb(hex):
  return {
    "r" : (int(hex[1:3], 16)/255),
    "g" : (int(hex[3:5], 16)/255),
    "b" : (int(hex[5:7], 16)/255)
  }

# Set to True to include debugging features.
debug = False

# Dimensions settings (values were chosen based on the 3:4 photo aspect ratio).
width = 975
height = 1300
margin = 50
m_width = width - (2 * margin)
m_height = height - (2 * margin)
line_height = 150
line_height_small = 120

# Color settings.
parks_yellow = hex_to_rgb("#FCC917")
parks_brown = hex_to_rgb("#592626")

# Font settings.
font_settings = {
  "font": "Formata",
  "slant": cairo.FONT_SLANT_NORMAL,
  "weight": cairo.FONT_WEIGHT_NORMAL,
  "sizes": {
    "large": {
      "size" : 125,
      "sign-offset" : 30
    },
    "medium": {
      "size" : 100,
      "sign-offset" : 40
    },
    "small": {
      "size" : 90,
      "sign-offset" : 46,
      "overlay-offset": 29,
    } 
  }
}

# Setting font context.
def setFont(context, preset, color):
  context.set_source_rgb(color["r"], color["g"], color["b"])
  context.set_font_size(font_settings["sizes"][preset]["size"])
  context.select_font_face(font_settings["font"], font_settings["slant"], font_settings["weight"])

# Getting text box data.
def getTextBoxData(context, line, size, type):
  return_types = ["x", "y", "width", "height", "dx", "dy"]
  setFont(context, size, parks_brown)
  text_box_data = context.text_extents(line)
  return text_box_data[return_types.index(type)]

# Getting line data using the biggest font size that will fit.
def getLineDataMax(context, line):
  line_width = getTextBoxData(context, line, "large", "width")
  line_size = "large"
  if line_width > m_width:
    line_width = getTextBoxData(context, line, "medium", "width")
    line_size = "medium"
    if line_width > m_width:
      line_width = getTextBoxData(context, line, "small", "width")
      line_size = "small"
      if line_width > m_width:
        print("\"" + line + "\" is too long for one line. Adjustments needed. Exiting.")
        sys.exit()
  return {
    "line": line,
    "width" : line_width,
    "size": line_size
  }

# Getting line data using a specific size.
def getLineData(context, line, size):
  if size == "large":
    line_width = getTextBoxData(context, line, "large", "width")
  elif size == "medium":
    line_width = getTextBoxData(context, line, "medium", "width")
  elif size == "small":
    line_width = getTextBoxData(context, line, "small", "width")
  else: 
    print("The size provided: \"" + size + "\" is not in the format \"large\", \"medium\", or \"small\". Exiting.")
    sys.exit()
  if line_width > m_width:
    print("\"" + line + "\" is too long for one line. Adjustments needed. Exiting.")
    sys.exit()
  return {
    "line": line,
    "width" : line_width,
    "size": size
  }

# Getting the max height of a font.
def getMaxHeight(context, size):
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÑabcdefghijklmnopqrstuváéíóúñ"
  return getTextBoxData(context, alphabet, size, "height")

# Creating State Park SVG Overlay.
def createOverlaySVG(code, name, dir):
  surface = cairo.SVGSurface(dir + code + ".svg", width, height)
  context = cairo.Context(surface)
  
  # Adding debugging features.
  if debug:
    # Creating background.
    context.set_source_rgb(parks_yellow["r"], parks_yellow["g"], parks_yellow["b"])
    context.rectangle(0, 0, width, height)
    context.fill()
    # Creating test background to show margin.
    debug_pink = hex_to_rgb("#FC0FC0")
    context.set_source_rgb(debug_pink["r"], debug_pink["g"], debug_pink["b"])
    context.rectangle(margin, margin, m_width, m_height)
    context.fill()
    # Drawing test rectangles. To show text height.
    dg_1_color = hex_to_rgb("#0a7491")
    dg_2_color = hex_to_rgb("#0d91b6")
    dg_3_color = hex_to_rgb("#55b2cb")
    dg_4_color = hex_to_rgb("#86c8da")
    for i in range(margin, height - margin, line_height_small):
      if((i - margin) % (line_height_small * 2) == 0):
        context.set_source_rgb(dg_1_color["r"], dg_1_color["g"], dg_1_color["b"])
      else:
        context.set_source_rgb(dg_2_color["r"], dg_2_color["g"], dg_2_color["b"])
      context.rectangle(margin, i, m_width/2, line_height_small)
      context.fill()
    for i in range(int(margin + (line_height_small/2)), int(height - margin - (line_height_small/2)), line_height_small):
      if((i - int(margin + (line_height_small/2))) % (line_height_small * 2) == 0):
        context.set_source_rgb(dg_3_color["r"], dg_3_color["g"], dg_3_color["b"])
      else:
        context.set_source_rgb(dg_4_color["r"], dg_4_color["g"], dg_4_color["b"])
      context.rectangle(margin + m_width/2, i, m_width/2, line_height_small)
      context.fill()
    context.set_source_rgb(dg_4_color["r"], dg_4_color["g"], dg_4_color["b"])
    context.rectangle(margin + m_width/2, margin, m_width/2, line_height_small/2)
    context.rectangle(margin + m_width/2, height - margin - (line_height_small/2), m_width/2, line_height_small/2)
    context.fill()

  # Handling splitting text into lines and wrapping text.
  words = name.split()
  lines = []
  if len(words) == 1:
    lines.append(getLineData(context, words[0], "small"))
  else:
    cur_line = words[0]
    for i in range(len(words) - 1):
      if getTextBoxData(context, cur_line + " " + words[i+1], "small", "width") > m_width:
        line_data = getLineData(context, cur_line, "small")
        lines.append(line_data)
        cur_line = words[i+1]
      else:
        cur_line = cur_line + " " + words[i+1]
      if i == len(words) - 2:
        line_data = getLineData(context, cur_line, "small")
        lines.append(line_data)

  # Checking to see if park name is able to fit within height of sign.
  total_height = len(lines) * line_height_small
  if total_height > m_height:
    print("\"" + name + "\" has a name too big for the overlay SVG. Adjustments needed. Exiting.")
    sys.exit()

  # Issuing warning if park overlay text is more than 4 lines.
  if len(lines) > 4:
    print("\"" + name + "\" (" + code + ") overlay SVG text is too long. Consider modifying park text to fit within 4 lines.")

  # Drawing overlay background.
  context.set_source_rgb(parks_yellow["r"], parks_yellow["g"], parks_yellow["b"])
  context.rectangle(margin, margin, m_width, len(lines)*line_height_small)
  context.fill()

  # Drawing overlay text.
  start_height = margin
  font_size = "small"
  font_offset = font_settings["sizes"][font_size]["overlay-offset"]
  setFont(context, font_size, parks_brown)
  for i in range(len(lines)):
    context.move_to(width/2 - lines[i]["width"]/2, start_height + line_height_small*(i+1) - font_offset)
    context.text_path(lines[i]["line"])
    context.fill()

# Creating State Park SVG Sign.
def createSignSVG(code, name, dir):
  surface = cairo.SVGSurface(dir + code + ".svg", width, height)
  context = cairo.Context(surface)

  # Adding debugging features.
  if debug:
    # Creating background.
    context.set_source_rgb(parks_yellow["r"], parks_yellow["g"], parks_yellow["b"])
    context.rectangle(0, 0, width, height)
    context.fill()
    # Creating test background to show margin.
    debug_pink = hex_to_rgb("#FC0FC0")
    context.set_source_rgb(debug_pink["r"], debug_pink["g"], debug_pink["b"])
    context.rectangle(margin, margin, m_width, m_height)
    context.fill()
    # Drawing test rectangles. To show text height.
    dg_1_color = hex_to_rgb("#0a7491")
    dg_2_color = hex_to_rgb("#0d91b6")
    dg_3_color = hex_to_rgb("#55b2cb")
    dg_4_color = hex_to_rgb("#86c8da")
    for i in range(margin, height - margin, line_height):
      if((i - margin) % (line_height * 2) == 0):
        context.set_source_rgb(dg_1_color["r"], dg_1_color["g"], dg_1_color["b"])
      else:
        context.set_source_rgb(dg_2_color["r"], dg_2_color["g"], dg_2_color["b"])
      context.rectangle(margin, i, m_width/2, line_height)
      context.fill()
    for i in range(int(margin + (line_height/2)), int(height - margin - (line_height/2)), line_height):
      if((i - int(margin + (line_height/2))) % (line_height * 2) == 0):
        context.set_source_rgb(dg_3_color["r"], dg_3_color["g"], dg_3_color["b"])
      else:
        context.set_source_rgb(dg_4_color["r"], dg_4_color["g"], dg_4_color["b"])
      context.rectangle(margin + m_width/2, i, m_width/2, line_height)
      context.fill()
    context.set_source_rgb(dg_4_color["r"], dg_4_color["g"], dg_4_color["b"])
    context.rectangle(margin + m_width/2, margin, m_width/2, line_height/2)
    context.rectangle(margin + m_width/2, height - margin - (line_height/2), m_width/2, line_height/2)
    context.fill()

  # Handling splitting text into lines and wrapping text.
  words = name.split()
  lines = []
  if len(words) == 1:
    lines.append(getLineDataMax(context, words[0]))
  else:
    cur_line = words[0]
    for i in range(len(words) - 1):
      if getTextBoxData(context, cur_line + " " + words[i+1], "large", "width") > m_width:
        line_data = getLineDataMax(context, cur_line)
        lines.append(line_data)
        cur_line = words[i+1]
      else:
        cur_line = cur_line + " " + words[i+1]
      if i == len(words) - 2:
        line_data = getLineDataMax(context, cur_line)
        lines.append(line_data)

  # Checking to see if park name is able to fit within height of sign.
  total_height = len(lines) * line_height
  if total_height > m_height:
    print("\"" + name + "\" has a name too big for the sign SVG. Adjustments needed. Exiting.")
    sys.exit()

  # Issuing warning if park sign text is more than 4 lines.
  if len(lines) > 4:
    print("\"" + name + "\" (" + code + ") sign SVG text is too long. Consider modifying park text to fit within 4 lines.")

  # Printing lines on sign.
  start_height = ((m_height - total_height) / 2) + margin
  for i in range(len(lines)):
    font_size = lines[i]["size"]
    font_offset = font_settings["sizes"][font_size]["sign-offset"]
    setFont(context, font_size, parks_brown)
    context.move_to(width/2 - lines[i]["width"]/2, start_height + line_height*(i+1) - font_offset)
    context.text_path(lines[i]["line"])
    context.fill()

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
      print("Failed to delete %s. Reason: %s" % (file_path, e))

# Running file from command line.
if __name__ == "__main__":
  print("Running sign.py")
  def codeTypeCheck(arg):
    if not arg.isdigit():
      raise argparse.ArgumentTypeError("the code \"" + arg + "\" needs to be a valid integer")
    else:
      return arg
  def nameTypeCheck(arg):
    if arg == "":
      raise argparse.ArgumentTypeError("the name input cannot be empty")
    else:
      return arg
  parser = argparse.ArgumentParser(
    description="Script is used to generate state park SVG sign and overlay images",
    usage="sign.py [-h] [-c CODE -n NAME] Example: sign.py -c \"405\" -n \"Hungry Valley State Vehicular Recreation Area\""
  )
  parser._positionals.title = "Positional arguments"
  parser._optionals.title = "Optional arguments"
  parser.add_argument("-c", "--code", help="Park code integer value to name SVG file", required="-n" in sys.argv, type=codeTypeCheck)
  parser.add_argument("-n", "--name", help="The name of the park to put in SVG image", required="-c" in sys.argv, type=nameTypeCheck)
  args = vars(parser.parse_args())
  if args["code"] != None and args["name"] != None:
    # Creating SVG sign and overlay.
    print("Creating SVG sign and overlay")
    createSignSVG(args["code"], args["name"], "../img/parks/")
    createOverlaySVG(args["code"], args["name"], "../img/overlay/")
  else:
    # Removing SVG images and creating new SVG images from parks.json.
    print("Removing SVG images and creating new SVG images from parks.json")
    # Loading parks.json file.
    if os.path.isfile("./assets/parks.json"):
      print("Opening parks.json")
      parks_json_file = open("./assets/parks.json")
      try:
        parks_json = json.load(parks_json_file)
        parks_json_file.close()
      except ValueError as e:
        print("Invalid parks.json file: %s" % e)
        print("Exiting Script")
        parks_json_file.close()
        sys.exit()
    else:
      print("File parks.json doesn't exist.")
      print("Exiting Script")
      sys.exit()
    user_input = input("Remove SVG images from the parks and overlay image directories (Y/N): ")
    if user_input.lower() != "y" and user_input.lower() != "yes":
      print("Exiting Script")
      sys.exit()
    print("Removing SVG images from the parks and overlay image directories.")
    removeDirectoryContents("../img/parks")
    removeDirectoryContents("../img/overlay")
    print("Building new SVG images based on parks.json")
    for park in parks_json["parks"]:
      createSignSVG(park["code"], park["name"], "../img/parks/")
      createOverlaySVG(park["code"], park["name"], "../img/overlay/")
  print("Execution of sign.py complete")