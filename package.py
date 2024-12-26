import tarfile
import os
import dataread
import shutil
import hashlib

def compute_sha256(file_path, save=True):
    sha256_hash = hashlib.sha256()  
    with open(file_path, "rb") as f:  
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block) 
    if save == True:
        with open(f'{file_path}.sha256', 'w') as shum:
            shum.write(sha256_hash.hexdigest())
    return sha256_hash.hexdigest()
def create_package(workdir):
    try:
        if os.path.isdir(f'{workdir}/RUPK-OUTPUT'):
            shutil.rmtree(f'{workdir}/RUPK-OUTPUT')
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
                        txz.add(f'{workdir}/{full_path}', arcname=full_path)
        os.chdir(f'{workdir}/RUPK-OUTPUT')
        with tarfile.open(f'{cdir}/{manifest['Name']}-{manifest['Version']}.rupk', 'w|xz') as txz:
            txz.add(f'{workdir}/RUPK-OUTPUT/data.tar.xz', arcname="data.txz")
            txz.add(f"{workdir}/RUPK-OUTPUT/info.tar.xz", arcname="info.txz")
        shutil.rmtree(f"{workdir}/RUPK-OUTPUT")
        print(f"Successfully built {manifest['Name']}-{manifest['Version']}.rupk")
        compute_sha256(f'{cdir}/{manifest['Name']}-{manifest['Version']}.rupk', True)
        os.chdir(cdir)
        os.remove(f'{workdir}/RUPK/tree')
        return True
    except Exception as e:
        print(f"Error: {e}")
def filtar(tarinfo, other):
    return tarinfo
def extract_package(outputdir, file):
    try:
        print(f"Preparing to extract {file}...")
        if not os.path.isfile(file):
            print(f"The provided file doesn't appear to be a R-UPK Package")
            return False
        if not os.path.isdir(outputdir):
            os.makedirs(outputdir)
        outputdir = os.path.abspath(outputdir)
        file = os.path.abspath(file)
        
        with tarfile.open(file, 'r|xz') as txz:
            txz.extractall(path=outputdir, filter=filtar)
        
        with tarfile.open(f'{outputdir}/data.txz', 'r|xz') as txz:
            txz.extractall(path=outputdir, filter=filtar)
        
        with tarfile.open(f"{outputdir}/info.txz", 'r|xz') as txz:
            txz.extractall(path=f"{outputdir}/RUPK", filter=filtar)
        
        os.remove(f'{outputdir}/data.txz')
        os.remove(f"{outputdir}/info.txz")
        
        print(f"Extraction completed.")
        return True
    except Exception as e:
        print(f"Error: {e}")