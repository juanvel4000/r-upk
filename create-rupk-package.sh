#!/bin/sh
set -e
mkdir -p rupk-package/usr/lib/ rupk-package/RUPK rupk-package/usr/bin
cat << EOF > rupk-package/usr/bin/rupk
#!/bin/sh
set -e
python /usr/lib/rupk.py "\$@"
EOF
chmod +x rupk-package/usr/bin/rupk
cat << EOF > rupk-package/RUPK/Manifest.ini
[Package]
Name = r-upk
Version = 0.3
Maintainer = juanvel400 <juanvel400@proton.me>
Summary = The Rewritten-UPK Package Manager.
EOF
cp rupk.py install.py dataread.py package.py rupk-package/usr/lib/
python rupk.py build rupk-package
