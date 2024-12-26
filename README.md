
# R-UPK

R-UPK is a simple package manager written in Python, it has a similar syntax to  **well-known package managers**

## Features

- Simple **syntax**
- Uses **tar** and **xz**
- Written in **Python**
- Has **fire-throwing** powers


## Installation

You can create the R-UPK Package and install it

```bash
  $ git clone https://github.com/juanvel4000/rupk
  # sh create-rupk-package.sh
  # python rupk.py install r-upk-0.2.rupk
  $ rupk v

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