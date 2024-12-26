import sys
import install
import package
import dataread
import os

version = "0.2"
architecture = "any"
def checkroot():
    if not os.getuid() == 0:
        print("Run r-upk as root")
        sys.exit(1)
def displayhelp():
    print(f"rupk {version}")
    print("Usage: rupk [options]")
    print("")
    print("Package installation and removal:")
    print(" install/i <package file>          Install a package from a file")
    print(" remove/r  <package name>          Uninstall a package from the system")
    print(" ")
    print("Package Development and extraction:")
    print(" build/c   <working directory>     Build a package from a working directory")
    print(" extract/x <package file> (dir)    Extract a package, by default to /tmp/rupk")
    print("")
    print("Package Meta:")
    print(" list/l                            List the Available packages in the system")
    print("")
    print("This r-upk has fire throwing abilities")
def check_directories():
    
    if not os.path.isdir('/etc/rupk'):
        checkroot()
        os.makedirs('/etc/rupk')
    if not os.path.isdir('/var/rupk/Uninstall'):
        checkroot()
        os.makedirs('/var/rupk/Uninstall')
def display_packages():
    if not os.path.isfile('/etc/rupk/packages.db'):
        print("Could not find the package list.")
        return False
    with open('/etc/rupk/packages.db', 'r') as db:
        lines = db.readlines()
        for line in lines:
            line = line.split(':')
            print(f"{line[0]}   {line[1]}")
    return True
def ascii():
    dragon = rf"""
    
                          / \  //\           
            |\___/|      /   \//  \\            
            /0  0  \__  /    //  | \ \    r-upk {version} ({architecture})
           /     /  \/_/    //   |  \  \  
           @_^_@'/   \/_   //    |   \   \ 
           //_^_/     \/_ //     |    \    \
        ( //) |        \///      |     \     \
      ( / /) _|_ /   )  //       |      \     _\
    ( // /) '/,_ _ _/  ( ; -.    |    _ _\.-~        .-~~~^-.
  (( / / )) ,-(        _      )`-.|.-~-.           .~         `.
 (( // / ))  '/\      /                 ~-. _ .-~      .-~^-.  \
 (( /// ))      `.   (            )                   /      \  \
  (( / ))     .----~-.\        \-'                 .~         \  `. \^-.
             ///.----..>        \             _ -~             `.  ^-`  ^-_
               ///-._ _ _ _ _ _ _)^ - - - - ~                     ~-- ,.-~
                                                                  /.-~
    """
    return dragon

def handle_install(arg):
    checkroot()
    if not os.path.isfile(arg):
        print(f"Could not install {arg}, file not found")
        sys.exit(1)
    install.InstallPackage(arg, "/")

def handle_remove(arg):
    checkroot()
    install.UninstallPackage(arg, "/")

def handle_build():
    if len(sys.argv) < 3:
        print("Please provide a working directory")
        sys.exit(1)
    package.create_package(sys.argv[2])

def handle_extract():
    checkroot()
    if len(sys.argv) < 3:
        print("Please provide a Package file to extract")
        sys.exit(1)
    directory = sys.argv[3] if len(sys.argv) > 3 else "/tmp/rupk"
    package.extract_package(directory, sys.argv[2])

def main():
    check_directories()
    if len(sys.argv) < 2:
        displayhelp()
        sys.exit(0)

    action = sys.argv[1]

    actions = {
        "help": displayhelp,
        "h": displayhelp,
        "install": lambda: [handle_install(arg) for arg in sys.argv[2:]],
        "i": lambda: [handle_install(arg) for arg in sys.argv[2:]],
        "remove": lambda: [handle_remove(arg) for arg in sys.argv[2:]],
        "r": lambda: [handle_remove(arg) for arg in sys.argv[2:]],
        "build": handle_build,
        "c": handle_build,
        "extract": handle_extract,
        "x": handle_extract,
        "fire": lambda: print(ascii()),
        "--version": lambda: print(f"r-upk {version} ({architecture})"),
        "v": lambda: print(f"r-upk {version} ({architecture})"),
        "list": display_packages,
        "l": display_packages
    }

    if action in actions:
        actions[action]()
    else:
        print("Invalid command. please view \"rupk help\" for usage.")
        sys.exit(1)

if __name__ == "__main__":
    main()
