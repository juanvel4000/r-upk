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

def add_entry(name, version, root="/"):
    if not os.path.isdir(f'{root}/etc/rupk'):
        os.makedirs(f'{root}/etc/rupk')
    with open(f'{root}/etc/rupk/packages.db', 'a') as db:
        db.write(f'{name}:{version}\n')
    return True
def check_installed(name, root="/"):
    if not os.path.isfile(f"{root}/etc/rupk/packages.db"):
        print("The Package Database doesnt exist")
        return False
    with open(f"{root}/etc/rupk/packages.db", 'r') as db:
        for line in db:
            if line.startswith(name):
                return name
    return False
def remove_entry(name, root="/"):
    try:
        with open(f'{root}/etc/rupk/packages.db', 'r') as file:
            lines = file.readlines()
        
        with open(f'{root}/etc/rupk/packages.db', 'w') as file:
            for line in lines:
                if not line.startswith(name):
                    file.write(line)
    except Exception as e:
        print(f"Error: {e}")