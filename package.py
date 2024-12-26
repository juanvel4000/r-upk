import tarfile
import os
import dataread
def create_package(workdir):
    cdir = os.getcwd()
    if not os.path.isdir(workdir):
        print("Error: the Working directory doesnt exist")
        return False
    workdir = os.path.abspath(workdir)
    os.chdir(workdir)
    os.mkdir(f'{workdir}/RUPK-OUTPUT')
    if not os.path.isdir(f'{workdir}/RUPK'):
        print("Could not find a RUPK directory")
        return False
    if not os.path.isfile(f'{workdir}/RUPK/Manifest.ini'):
        print("Could not find the Manifest file in RUPK/Manifest.ini file.")
        return False
    manifest = dataread.parsemanifest(f'{workdir}/RUPK/Manifest.ini')
    print(f"Creating {manifest['Name']}...")
    if manifest == False:
        print("An error occurred during Manifest parsing")
        return False
    os.chdir(workdir)
    with open(f"{workdir}/RUPK/tree", 'w') as tree:
        for root, dirs, files in os.walk(workdir):
            if 'RUPK' in dirs:
                dirs.remove('RUPK')
            if 'RUPK-OUTPUT' in dirs:
                dirs.remove('RUPK-OUTPUT')
            if files:
                for file in files:
                    full_path = os.path.join(root, file)
                    if full_path.startswith(workdir):
                        full_path = full_path[len(workdir):]  
                    tree.write(f'{full_path}\n')
    os.chdir(f"{workdir}/RUPK")
    with tarfile.open(f'{workdir}/RUPK-OUTPUT/info.tar.xz', 'w|xz') as txz:
        txz.add('Manifest.ini')
        txz.add('tree')
        if "PostInstall" in manifest:
            if not os.path.isfile(f'{workdir}/RUPK/{manifest['PostInstall']}'):
                print("Could not find the postinstall script")
                return False
            txz.add(manifest['PostInstall'])
        if "PreInstall" in manifest:
            if not os.path.isfile(f'{workdir}/RUPK/{manifest['PreInstall']}'):
                print("Could not find the preinstall script")
                return False
            txz.add(manifest['PreInstall'])
        if "Uninstall" in manifest:
            if not os.path.isfile(f'{workdir}/RUPK/{manifest['Uninstall']}'):
                print("Could not find the Uninstall script")
                return False
            txz.add(manifest['Uninstall'])
    os.chdir(workdir)
    with tarfile.open(f'{workdir}/RUPK-OUTPUT/data.tar.xz', 'w|xz') as txz:
        for line in f'{workdir}/RUPK/tree':
                file_path = line.strip()
                
                if os.path.isfile(file_path):
                    txz.add(file_path, arcname=os.path.basename(file_path))
    os.chdir(f'{workdir}/RUPK-OUTPUT')
    with tarfile.open(f'{cdir}/{manifest['Name']}-{manifest['Version']}.rupk', 'w|xz') as txz:
        txz.add(f'{workdir}/RUPK-OUTPUT/data.tar.xz', arcname="data.txz")
        txz.add(f"{workdir}/RUPK-OUTPUT/info.tar.xz", arcname="info.txz")
    os.remove(f'{workdir}/RUPK-OUTPUT/data.tar.xz')
    os.remove(f'{workdir}/RUPK-OUTPUT/info.tar.xz')
    os.rmdir(f'{workdir}/RUPK-OUTPUT')
    print(f"Successfully built {manifest['Name']}-{manifest['Version']}.rupk")
    os.chdir(cdir)
    return True
create_package('package/')