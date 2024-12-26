import os
import sys
from configparser import ConfigParser
def parsemanifest(file):
    if not os.path.isfile(file):
        print(f"Could not find {file}")
        return None
    dictionary = {}
    config = ConfigParser()
    try:
        config.read(file)
    except MissingSectionHeaderError:
        print(f"Error: File '{file}' is not a valid manifest.")
        return None
    if not config.has_section("Package"):
        print("Manifest parsing error: could not find the \"Package\" section")
        return False
    options = ["Name", "Version", "Maintainer"]
    for option in options:
        if not config.has_option("Package", option):
            print(f"Could not find {option}")
            return False
        dictionary[option] = config['Package'][option]
    optionals = ["Summary", "Dependencies", "PostInstall", "PreInstall", "Uninstall", "Section"]
    for option in optionals:
        if config.has_option("Package", option):
            dictionary[option] = config['Package'][option]
    return dictionary

