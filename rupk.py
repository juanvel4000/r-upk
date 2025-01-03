import sys
import install
import package
import dataread
import os
import remote
import shutil
version = "0.4.2"
architecture = "any"
def checkroot():
    if not os.getuid() == 0:
        print("Run r-upk as root")
        sys.exit(1)
def displayhelp():
    print(f"rupk {version}")
    print("Usage: rupk [options]")
    print(" ")
    print("Package networking:")
    print("  i <pkg>                     Install a package from a Repository")
    print("  u                           Update the repositories")
    print("  ch <pkg>                    Check if a package exists in the repositories")
    print("  dl <pkg>                    Download a package from a repository")
    print("  ln                          List every package available to install")
    print("  ri <pkg>                    Reinstall a package from a Repository")
    print(" ")
    print("Package installation and removal:")
    print("  li <pkg file>               Install a package from a file")
    print("  lri <pkg file>              Reinstall a package from a file")
    print("  r   <pkg name>              Uninstall a package from the system")
    print(" ")
    print("Package Development and extraction:")
    print("  c <workdir>                 Build a package from a working directory")
    print("  x <pkg file> (dir)          Extract a package, by default to /tmp/rupk")
    print(" ")
    print("Package Meta:")
    print("  l                            List the Available packages in the system")
    print(" ")
    print("R-UPK Meta")
    print("  lc                           Show the MIT License")
    print("  h                            This help message")
    print("  v                            Show the r-upk version")
    print("This r-upk has fire throwing abilities")
def check_directories():
    if not os.path.isdir('/etc/rupk'):
        checkroot()
        os.makedirs('/etc/rupk')
    if not os.path.isfile('/etc/rupk/repos'):
        checkroot()
        print("Creating a repository file")
        with open('/etc/rupk/repos', 'w') as db:
            db.write(f'''
        [List]\n
        list = main\n
        [main]\n
        Server = https://juanvel4000.serv00.net/main\n            
            
            ''')
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
            line = line.strip()
            line = line.split(':')
            print(f"{line[0]}    {line[1]}")
    return True
def ascii():
    dragon = rf"""
    
                          / \  //\           
            |\___/|      /   \//  \\            
            /0  0  \__  /    //  | \ \    r-upk {version} ({architecture})
           /     /  \/_/    //   |  \  \  Copyright (c) 2024 juanvel400
           @_^_@'/   \/_   //    |   \   \  Licensed under the MIT License
           //_^_/     \/_ //     |    \    \ View "rupk license" for the license text
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
def handle_reinstall(arg):
    checkroot()
    if not os.path.isfile(arg):
        print(f"Could not reinstall {arg}, file not found")
        sys.exit(1)
    install.InstallPackage(arg, "/", True)
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
def handle_check():
    checkroot()
    if len(sys.argv) < 3:
        print("Please provide a Package name to check")
        sys.exit(1)
    package = remote.checknetpkg('/', sys.argv[2])
    if package == False:
        print("Package not found")
        sys.exit(1)
    version = package['Version'].strip()
    print(f"{package['Repository']}/{package['Name']}:{version}")
    return f"{package['Repository']}/{package['Name']}:{version}"
def handle_download():
    checkroot()
    if len(sys.argv) < 3:
        print("Please provide a Package name to download")
        sys.exit(1)
    package = remote.download('/', sys.argv[2])
    if package == False:
        print("Package not found")
        sys.exit(1)
    print(f"Package downloaded to {package}")
def handle_dlin():
    checkroot()
    if len(sys.argv) < 3:
        print("Please provide a Package name to download")
        sys.exit(1)
    package = remote.download('/', sys.argv[2])
    if package == False:
        print("Package not found")
        sys.exit(1)
    dependencies = remote.finddepends('/', package, alsoinstall=True)
    handle_install(package)
def handle_rdlin():
    checkroot()
    if len(sys.argv) < 3:
        print("Please provide a Package name to download")
        sys.exit(1)
    package = remote.download('/', sys.argv[2])
    if package == False:
        print("Package not found")
        sys.exit(1)
    dependencies = remote.finddepends('/', package, alsoinstall=True)
    handle_reinstall(package)
def license():
    print(r"""

Copyright 2024 juanvel400

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""")
def listnetpkg():
    remote.listall('/')
def handle_update():
    checkroot()
    remote.updaterepos('/')
def main():
    check_directories()
    if len(sys.argv) < 2:
        displayhelp()
        sys.exit(0)

    action = sys.argv[1]

    actions = {
        "help": displayhelp,
        "h": displayhelp,
        "li": lambda: [handle_install(arg) for arg in sys.argv[2:]],
        "r": lambda: [handle_remove(arg) for arg in sys.argv[2:]],
        "c": handle_build,
        "x": handle_extract,
        "fire": lambda: print(ascii()),
        "v": lambda: print(f"r-upk {version} ({architecture})"),
        "l": lambda: display_packages(),
        "u": lambda: handle_update(),
        "ch": lambda: handle_check(),
        "dl": lambda: handle_download(),
        "i": lambda: handle_dlin(),
        "lc": lambda: license(),
        "ln": lambda: listnetpkg(),
        "ri": lambda: handle_rdlin(),
        "lri": lambda: [handle_reinstall(arg) for arg in sys.argv[2:]]
    }

    if action in actions:
        actions[action]()
    else:
        print(f"Invalid command: {action}. please view \"rupk help\" for usage.")
        sys.exit(1)
    if os.path.isdir('/tmp/rupk'):
        shutil.rmtree('/tmp/rupk/')

if __name__ == "__main__":
    main()
