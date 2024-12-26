
# R-UPK

R-UPK is a simple package manager written in Python, it has a similar syntax to  **well-known package managers**

## Features

- Simple **syntax**
- Uses **tar** and **xz**
- Written in **Python**
- Has **fire-throwing** powers


## Installation

Clone the repository, update the R-UPK Repos, and Install RUPK


```bash
  $ git clone https://github.com/juanvel4000/rupk
  $ sudo python rupk.py u
  $ sudo python rupk.py i rupk
  $ rupk v

```
## Repository Setup
```bash
  $ mkdir myrepository
  # Dont copy the packages
  $ touch package_name # For each package, create a file with the package name
  $ echo "1.0.0" >> package_name # Put the package version
  $ tar -czvf myrepository.tar.gz *
  # Upload myrepository.tar.gz and all the packages to the same directory in a server
  # Add a new entry to your /etc/rupk/repos
  $ rupk u
```
## Adding entries to a repository
You just need to append this to `/etc/rupk/repos`
```ini
[name]
Server = https://example.com/name
```
Modify the list variable to add your repository
```ini
[List]
list = main, name
```
Your `/etc/rupk/repos` should look like this
```ini
[List]
list = main, name
[main]
Server = https://juanvel4000.serv00.net/main
[name]
Server = https://example.com/name
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