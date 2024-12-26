
# R-UPK

R-UPK is a simple package manager written in Python, it has a similar syntax to  **well-known package managers**

## Features

- Simple **syntax**
- Uses **tar** and **xz**
- Written in **Python**
- Has **fire-throwing** powers


## Installation

R-UPK is not installable as of now, but you can test it

### Testing
Clone the repository

```bash
  git clone https://github.com/juanvel4000/rupk

```
Use python to run rupk.py    
```bash
    python rupk.py --version
```

## Manifests
A Package Manifest is named as `Manifest.ini`, when developing a package, this file goes in `(working directory)/RUPK`
A Manifest looks like this
```ini
[Package]
Name = MyPackage
Version = 1.0.0
Maintainer = John Doe <johndoe@example.com>
```
These are the required keys, but (if needed) you can use these other keys
```ini
[Package]
Name = MyPackage
Version = 1.0.0
Maintainer = John Doe <johndoe@example.com>
Summary = A short description of the package.
Dependencies = lib1 >= 1.2.3, lib2 >= 4.5.6
Section = utils
PreInstall = preinstall.sh
PostInstall = postinstall.sh
Uninstall = uninstall.sh
```
The scripts for `PreInstall`, `PostInstall` and `Uninstall` (if exist) Must be in `(working directory)/RUPK`



## License
**R-UPK** is licensed with the **MIT** License

Please view **LICENSE**


```ascii

                          / \  //\
            |\___/|      /   \//  \\
            /0  0  \__  /    //  | \ \    
           /     /  \/_/    //   |  \  \  
           @_^_@'/   \/_   //    |   \   \ 
           //_^_/     \/_ //     |    \    \
        ( //) |        \///      |     \     \
      ( / /) _|_ /   )  //       |      \     _\
    ( // /) '/,_ _ _/  ( ; -.    |    _ _\.-~        .-~~~^-.
  (( / / )) ,-{        _      `-.|.-~-.           .~         `.
 (( // / ))  '/\      /                 ~-. _ .-~      .-~^-.  \
 (( /// ))      `.   {            }                   /      \  \
  (( / ))     .----~-.\        \-'                 .~         \  `. \^-.
             ///.----..>        \             _ -~             `.  ^-`  ^-_
               ///-._ _ _ _ _ _ _}^ - - - - ~                     ~-- ,.-~
                                                                  /.-~
```