## R-UPK

R-UPK is a simple package manager written in Python, it has a letter-long syntax (**or 3-letter long syntax**) which is easy to **learn** and _understand_

## Features

*   Simple **syntax**
*   Uses **tar** and **xz**
*   Written in **Python**
*   Has **fire-throwing** powers

## Installation

### Update

You can update **R-UPK** if you have the [main repository](https://juanvel4000.serv00.net/main) enabled, run these commands to update **R-UPK**

```plaintext
sudo rupk u && sudo rupk ri rupk
```

### Bootstrapper

You can run the **R-UPK Bootstrapper** script, you only need **cURL** and **bash**

```plaintext
sudo sh -c "$(curl -fsSL https://juanvel4000.serv00.net/main/install.sh)"
```

### Manually

Clone the repository, update the R-UPK Repos, and Install RUPK

```plaintext
git clone https://github.com/juanvel4000/rupk
sudo python rupk.py u
sudo python rupk.py i rupk
rupk v
```

## Repository Setup

```plaintext
  $ mkdir myrepository
  # Dont copy the packages
  $ touch package_name # For each package, create a file with the package name
  $ echo "1.0.0" &gt;&gt; package_name # Put the package version
  $ tar -czvf myrepository.tar.gz *
  # Upload myrepository.tar.gz and all the packages to the same directory in a server
  # Add a new entry to your /etc/rupk/repos
  $ rupk u
```

## Adding entries to a repository

You just need to append this to `/etc/rupk/repos`

```plaintext
[name]
Server = https://example.com/name
```

Modify the list variable to add your repository

```plaintext
[List]
list = main, name
```

Your `/etc/rupk/repos` should look like this

```plaintext
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

```plaintext
[Package]
Name = MyPackage
Version = 1.0.0
Maintainer = John Doe <johndoe@example.com>
```

These are the required keys, but (if needed) you can use these other keys

```plaintext
[Package]
Name = MyPackage
Version = 1.0.0
Maintainer = John Doe <johndoe@example.com>
Summary = A short description of the package.
Dependencies = libfoo libfoobar libbar bar foo
Section = utils
PreInstall = preinstall.sh
PostInstall = postinstall.sh
Uninstall = uninstall.sh
```

The scripts for `PreInstall`, `PostInstall` and `Uninstall` (if exist) Must be in `(working directory)/RUPK`

## License

**R-UPK** is licensed with the **MIT** License

Please view **LICENSE** or `rupk lc`
