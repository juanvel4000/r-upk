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
Version = 0.4.2
Maintainer = juanvel400 <juanvel400@proton.me>
Summary = The Rewritten-UPK Package Manager.
EOF
mkdir -p rupk-package/usr/lib/rupk
cp rupk.py remote.py install.py dataread.py package.py rupk-package/usr/lib/rupk/
python rupk.py build rupk-package
rm -rf rupk-package rupk-*.sha256