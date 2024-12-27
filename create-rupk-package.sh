#!/bin/sh
set -e
mkdir -p rupk-package/usr/lib/ rupk-package/RUPK rupk-package/usr/bin
cat << EOF > rupk-package/usr/bin/rupk
#!/bin/sh
set -e
python /usr/lib/rupk/rupk.py "\$@"
EOF
chmod +x rupk-package/usr/bin/rupk
cat << EOF > rupk-package/RUPK/Manifest.ini
[Package]
Name = rupk
Version = 0.4.1
Maintainer = juanvel400 <juanvel400@proton.me>
Summary = The Rewritten-UPK Package Manager.
EOF
mkdir -p rupk-package/etc/rupk rupk-package/tmp/rupk rupk-package/var/rupk/Uninstall
cat << EOF > rupk-package/etc/rupk/repos
[List]
list = main
[main]
Server = https://juanvel4000.serv00.net/main
EOF
mkdir -p rupk-package/usr/lib/rupk
cp rupk.py remote.py install.py dataread.py package.py rupk-package/usr/lib/rupk/
python rupk.py build rupk-package