"""sign.py generates California State Park sign and overlay svg images."""

# This script is used to generate California State Park sign and overlay svg images. This script can be ran in two
# configurations. Either the script is ran without any arguments or with both the -c/--code and -n/--name arguments
# together.
#
# Running this script without any arguments will first delete all svg images in the parks and overlay image directories.
# This script will then create new svg images based on the data pulled from parks.json.
#
# Example: [python sign.py]
#
# Running the script with both the -c/--code and -n/--name arguments will create a new svg sign and overlay image for a
# single park. The image file will be named based on the -c/--code argument and the text in the svg image will be taken
# from the -n/--name argument.
#
# Example: [python sign.py -c "536" -n "Butano State Park"]

import argparse  # Used to process command line arguments.
import json  # Used for loading parks.json file.
import os  # Used to process directories and files.
import shutil  # Used to recursively remove contents of a directory.
import sys  # Used to exit script on errors.
import cairo  # Used to create svg images.

# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=C0103

def hex_to_rgb(hex_color):
    """Converts hex color string to rgb decimal format."""
    return {
        "r": (int(hex_color[1:3], 16) / 255),
        "g": (int(hex_color[3:5], 16) / 255),
        "b": (int(hex_color[5:7], 16) / 255),
    }

def set_font(context, preset, color):
    """Setting font context."""
    context.set_source_rgb(color["r"], color["g"], color["b"])
    context.set_font_size(font_settings["sizes"][preset]["size"])
    context.select_font_face(font_settings["font"], font_settings["slant"], font_settings["weight"])

def get_text_box_data(context, line, size, dimension):
    """Getting text box data."""
    return_types = ["x", "y", "width", "height", "dx", "dy"]
    set_font(context, size, parks_brown)
    text_box_data = context.text_extents(line)
    return text_box_data[return_types.index(dimension)]

def get_line_data_max(context, line):
    """Getting line data using the largest font size that will fit."""
    line_width = get_text_box_data(context, line, "large", "width")
    line_size = "large"
    if line_width > m_w:
        line_width = get_text_box_data(context, line, "medium", "width")
        line_size = "medium"
        if line_width > m_w:
            line_width = get_text_box_data(context, line, "small", "width")
            line_size = "small"
            if line_width > m_w:
                print(line + " is too long for one line. Adjustments needed. Exiting")
                sys.exit()
    return {"line": line, "width": line_width, "size": line_size}

def get_line_data(context, line, size):
    """Getting line data at a specific size."""
    if size == "large":
        line_width = get_text_box_data(context, line, "large", "width")
    elif size == "medium":
        line_width = get_text_box_data(context, line, "medium", "width")
    elif size == "small":
        line_width = get_text_box_data(context, line, "small", "width")
    else:
        print("The size provided: " + size + '" is not "large", "medium", or "small". Exiting')
        sys.exit()
    if line_width > m_w:
        print(line + " is too long for one line. Adjustments needed. Exiting")
        sys.exit()
    return {"line": line, "width": line_width, "size": size}

def get_max_height(context, size):
    """Getting the max height of a font."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÑabcdefghijklmnopqrstuváéíóúñ"
    return get_text_box_data(context, alphabet, size, "height")

def create_overlay_svg(code, name, directory):
    """Creating state park svg overlay."""
    surface = cairo.SVGSurface(directory + code + ".svg", w, h)
    context = cairo.Context(surface)
    # Adding debugging features.
    if debug:
        # Creating background.
        context.set_source_rgb(parks_yellow["r"], parks_yellow["g"], parks_yellow["b"])
        context.rectangle(0, 0, w, h)
        context.fill()
        # Creating test background to show margin.
        debug_pink = hex_to_rgb("#FC0FC0")
        context.set_source_rgb(debug_pink["r"], debug_pink["g"], debug_pink["b"])
        context.rectangle(m, m, m_w, m_h)
        context.fill()
        # Drawing test rectangles. To show text height.
        dg_1_color = hex_to_rgb("#0a7491")
        dg_2_color = hex_to_rgb("#0d91b6")
        dg_3_color = hex_to_rgb("#55b2cb")
        dg_4_color = hex_to_rgb("#86c8da")
        for i in range(m, h - m, line_h_sm):
            if (i - m) % (line_h_sm * 2) == 0:
                context.set_source_rgb(dg_1_color["r"], dg_1_color["g"], dg_1_color["b"])
            else:
                context.set_source_rgb(dg_2_color["r"], dg_2_color["g"], dg_2_color["b"])
            context.rectangle(m, i, m_w / 2, line_h_sm)
            context.fill()
        for i in range(int(m + (line_h_sm / 2)), int(h - m - (line_h_sm / 2)), line_h_sm):
            if (i - int(m + (line_h_sm / 2))) % (line_h_sm * 2) == 0:
                context.set_source_rgb(dg_3_color["r"], dg_3_color["g"], dg_3_color["b"])
            else:
                context.set_source_rgb(dg_4_color["r"], dg_4_color["g"], dg_4_color["b"])
            context.rectangle(m + m_w / 2, i, m_w / 2, line_h_sm)
            context.fill()
        context.set_source_rgb(dg_4_color["r"], dg_4_color["g"], dg_4_color["b"])
        context.rectangle(m + m_w / 2, m, m_w / 2, line_h_sm / 2)
        context.rectangle(m + m_w / 2, h - m - (line_h_sm / 2), m_w / 2, line_h_sm / 2)
        context.fill()
    # Handling splitting text into lines and wrapping text.
    words = name.split()
    lines = []
    if len(words) == 1:
        lines.append(get_line_data(context, words[0], "small"))
    else:
        cur_line = words[0]
        for i in range(len(words) - 1):
            if get_text_box_data(context, cur_line + " " + words[i + 1], "small", "width") > m_w:
                line_data = get_line_data(context, cur_line, "small")
                lines.append(line_data)
                cur_line = words[i + 1]
            else:
                cur_line = cur_line + " " + words[i + 1]
            if i == len(words) - 2:
                line_data = get_line_data(context, cur_line, "small")
                lines.append(line_data)
    # Checking to see if park name is able to fit within height of sign.
    total_height = len(lines) * line_h_sm
    park_name_code = name + " (" + code + ")"
    if total_height > m_h:
        print(park_name_code + " name too big for overlay svg. Adjustments needed. Exiting")
        sys.exit()
    # Issuing warning if park overlay text is more than 4 lines.
    if len(lines) > 4:
        print("Warning. Reduce " + park_name_code + " name to fit within 4 lines in overlay svg")
    # Drawing overlay background.
    context.set_source_rgb(parks_yellow["r"], parks_yellow["g"], parks_yellow["b"])
    context.rectangle(m, m, m_w, len(lines) * line_h_sm)
    context.fill()
    # Drawing overlay text.
    start_height = m
    font_size = "small"
    font_offset = font_settings["sizes"][font_size]["overlay-offset"]
    set_font(context, font_size, parks_brown)
    for i, line in enumerate(lines):
        context.move_to(w / 2 - line["width"] / 2, start_height + line_h_sm * (i + 1) - font_offset)
        context.text_path(line["line"])
        context.fill()

def create_sign_svg(code, name, directory):
    """Creating state park svg sign."""
    surface = cairo.SVGSurface(directory + code + ".svg", w, h)
    context = cairo.Context(surface)
    # Adding debugging features.
    if debug:
        # Creating background.
        context.set_source_rgb(parks_yellow["r"], parks_yellow["g"], parks_yellow["b"])
        context.rectangle(0, 0, w, h)
        context.fill()
        # Creating test background to show margin.
        debug_pink = hex_to_rgb("#FC0FC0")
        context.set_source_rgb(debug_pink["r"], debug_pink["g"], debug_pink["b"])
        context.rectangle(m, m, m_w, m_h)
        context.fill()
        # Drawing test rectangles. To show text height.
        dg_1_color = hex_to_rgb("#0a7491")
        dg_2_color = hex_to_rgb("#0d91b6")
        dg_3_color = hex_to_rgb("#55b2cb")
        dg_4_color = hex_to_rgb("#86c8da")
        for i in range(m, h - m, line_h):
            if (i - m) % (line_h * 2) == 0:
                context.set_source_rgb(dg_1_color["r"], dg_1_color["g"], dg_1_color["b"])
            else:
                context.set_source_rgb(dg_2_color["r"], dg_2_color["g"], dg_2_color["b"])
            context.rectangle(m, i, m_w / 2, line_h)
            context.fill()
        for i in range(int(m + (line_h / 2)), int(h - m - (line_h / 2)), line_h):
            if (i - int(m + (line_h / 2))) % (line_h * 2) == 0:
                context.set_source_rgb(dg_3_color["r"], dg_3_color["g"], dg_3_color["b"])
            else:
                context.set_source_rgb(dg_4_color["r"], dg_4_color["g"], dg_4_color["b"])
            context.rectangle(m + m_w / 2, i, m_w / 2, line_h)
            context.fill()
        context.set_source_rgb(dg_4_color["r"], dg_4_color["g"], dg_4_color["b"])
        context.rectangle(m + m_w / 2, m, m_w / 2, line_h / 2)
        context.rectangle(m + m_w / 2, h - m - (line_h / 2), m_w / 2, line_h / 2)
        context.fill()
    # Handling splitting text into lines and wrapping text.
    words = name.split()
    lines = []
    if len(words) == 1:
        lines.append(get_line_data_max(context, words[0]))
    else:
        cur_line = words[0]
        for i in range(len(words) - 1):
            if get_text_box_data(context, cur_line + " " + words[i + 1], "large", "width") > m_w:
                line_data = get_line_data_max(context, cur_line)
                lines.append(line_data)
                cur_line = words[i + 1]
            else:
                cur_line = cur_line + " " + words[i + 1]
            if i == len(words) - 2:
                line_data = get_line_data_max(context, cur_line)
                lines.append(line_data)
    # Checking to see if park name is able to fit within height of sign.
    total_height = len(lines) * line_h
    park_name_code = name + " (" + code + ")"
    if total_height > m_h:
        print(park_name_code + " name too big for sign svg. Adjustments needed. Exiting")
        sys.exit()
    # Issuing warning if park sign text is more than 4 lines.
    if len(lines) > 4:
        print("Warning. Reduce " + park_name_code + " name to fit within 4 lines in sign svg")
    # Printing lines on sign.
    start_height = ((m_h - total_height) / 2) + m
    for i, line in enumerate(lines):
        font_size = line["size"]
        font_offset = font_settings["sizes"][font_size]["sign-offset"]
        set_font(context, font_size, parks_brown)
        context.move_to(w / 2 - line["width"] / 2, start_height + line_h * (i + 1) - font_offset)
        context.text_path(line["line"])
        context.fill()

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

# Set to True to include debugging features.
debug = False

# Dimensions settings (values were chosen based on the 3:4 photo aspect ratio).
w = 975  # svg width.
h = 1300  # svg height.
m = 50  # svg margin.
m_w = w - (2 * m)  # svg width accounting for margins.
m_h = h - (2 * m)  # svg height accounting for margins.
line_h = 150  # svg line height normal.
line_h_sm = 120  # svg line height small.

# Color settings.
parks_yellow = hex_to_rgb("#FCC917")
parks_brown = hex_to_rgb("#592626")

# Font settings.
font_settings = {
    "font": "Formata",
    "slant": cairo.FONT_SLANT_NORMAL,
    "weight": cairo.FONT_WEIGHT_NORMAL,
    "sizes": {
        "large": {"size": 125, "sign-offset": 30},
        "medium": {"size": 100, "sign-offset": 40},
        "small": {
            "size": 90,
            "sign-offset": 46,
            "overlay-offset": 29,
        },
    },
}

# Running file from command line.
if __name__ == "__main__":
    print("Running sign.py")

    def code_type_check(arg):
        """Validates code argument."""
        if not arg.isdigit():
            raise argparse.ArgumentTypeError('the code "' + arg + '" needs to be a valid integer')
        else:
            return arg

    def name_type_check(arg):
        """Validates name argument."""
        if arg == "":
            raise argparse.ArgumentTypeError("the name input cannot be empty")
        else:
            return arg

    parser = argparse.ArgumentParser(
        description="Script is used to generate state park svg sign and overlay images",
        usage='sign.py [-h] [-c CODE -n NAME] Example: sign.py -c "536" -n "Butano State Park"',
    )
    parser.add_argument(
        "-c",
        "--code",
        help="park code name for svg file. Must be used in conjunction with -n/--name argument",
        required="-n" in sys.argv,
        type=code_type_check,
    )
    parser.add_argument(
        "-n",
        "--name",
        help="park name used in svg. Must be used in conjunction with -c/--code argument",
        required="-c" in sys.argv,
        type=name_type_check,
    )
    args = vars(parser.parse_args())
    if args["code"] is not None and args["name"] is not None:
        # Creating svg sign and overlay.
        print("Creating svg sign and overlay")
        create_sign_svg(args["code"], args["name"], "../images/parks/")
        create_overlay_svg(args["code"], args["name"], "../images/overlay/")
    else:
        # Removing svg images and creating new svg images from parks.json.
        print("Removing svg images and creating new svg images from parks.json")
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
        user_input = input("Remove svg images from the parks and overlay image directories (Y/N): ")
        if user_input.lower() != "y" and user_input.lower() != "yes":
            print("Exiting")
            sys.exit()
        print("Removing svg images from the parks and overlay image directories")
        clear_directory("../images/parks")
        clear_directory("../images/overlay")
        print("Building new svg images based on parks.json")
        for park in parks_json["parks"]:
            create_sign_svg(park["code"], park["name"], "../images/parks/")
            create_overlay_svg(park["code"], park["name"], "../images/overlay/")
    print("Execution of sign.py complete")
