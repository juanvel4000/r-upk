import shutil
import os
import dataread
import package
import hashlib
def InstallPackage(file=None, root="/", replace=False):
    try:
        if file is None:
            print("Error: No file provided.")
            return False
        print(f"Checking file: {file}")
        if not os.access(file, os.R_OK):    
            print(f"Error: The file {file} is not readable.")
            return False

        cdir = os.getcwd()

        if not os.path.isdir(f'{root}/etc/rupk'):
            os.makedirs(f'{root}/etc/rupk')
        if not os.path.isfile(file):
            print(f"This is not a R-UPK Package or it doesn't exist")
            return False
        if os.path.isfile(f'{file}.sha256'):
            expected = package.compute_sha256(f'{file}')
            with open(f'{file}.sha256', 'r') as shum:
                summ = shum.read().strip()
            if summ == expected:
                print("The sums match")
            else:
                print("The sums don't match")
                return False
        else:
            print("This package could be insecure. Proceeding without SHA256 verification.")
        file = os.path.abspath(file)
        root = os.path.abspath(root)
        
        if not os.path.isdir(root):
            os.makedirs(root)

        package.extract_package(f'{root}/tmp/rupk/', file)
        manifest = dataread.parsemanifest(f'{root}/tmp/rupk/RUPK/Manifest.ini')

        if manifest.get('PreInstall'):
            preinstall_command = f"/tmp/rupk/RUPK/{manifest['PreInstall']}"
            if root != "/":
                os.system(f'chroot {root} {preinstall_command}')
            else:
                os.system(preinstall_command)
        if replace == False:
            if dataread.check_installed(manifest['Name'], root) == manifest['Name']:
                print("Package is already installed.")
                if os.path.isdir(f'{root}/tmp/upk'):
                    print("Cleaning up...")
                    shutil.rmtree(f'{root}/tmp/upk/')
                    
                return False
        else:
            print("Reinstall mode is enabled, continuing")
        tmp_dir = f"{root}/tmp/rupk"
        for dirpath, dirs, files in os.walk(tmp_dir):
            if 'RUPK' in dirs:
                dirs.remove('RUPK')  

            for dataf in files:
                src_file = os.path.join(dirpath, dataf)
                dest_file = os.path.join(root, os.path.relpath(src_file, tmp_dir))
    
                if not os.path.exists(dest_file):
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                    shutil.copy2(src_file, dest_file)
                else:
                    if replace == True:
                        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                        shutil.copy2(src_file, dest_file)        
                    else:
                        print(f"Skipping {dest_file}, file already exists.")

        if manifest.get('Uninstall'):
            shutil.copy(f"{root}/tmp/rupk/RUPK/{manifest['Uninstall']}", f"{root}/var/rupk/Uninstall/{manifest['Name']}.unf")
             
        os.chdir(cdir)
        shutil.copy(f"{root}/tmp/rupk/RUPK/tree", f"{root}/var/rupk/{manifest['Name']}.index")
        shutil.rmtree(f'{root}/tmp/rupk/')

        if manifest.get('PostInstall'):
            postinstall_command = f"/tmp/rupk/RUPK/{manifest['PostInstall']}"
            if root != "/":
                os.system(f'chroot {root} {postinstall_command}')
            else:
                os.system(postinstall_command)

        if manifest:
            dataread.add_entry(manifest['Name'], manifest['Version'], root)
            print("Package installation completed successfully.")
            return True
        else:
            print("Error: Failed to parse the Manifest file.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
def UninstallPackage(name, root="/"):
    print(f"Removing {name}...")
    if not dataread.check_installed(name, root) == name:
        print("Package is not installed")
        return False
    if not os.path.isfile(f'{root}/var/rupk/{name}.index'):
        print("Could not find the Index file for this package")

    if os.path.isfile(f'{root}/var/rupk/Uninstall/{name}.unf'):
        uninstall_command = f"/var/rupk/Uninstall/{name}.unf"
        if root != "/":
            os.system(f'chroot {root} {uninstall_command}')
        else:
            os.system(uninstall_command)

    with open(f'{root}/var/rupk/{name}.index', 'r') as db:
        lines = db.readlines()
        for line in lines:
            line = line.strip() 
            file_path = f'{root}/{line}'
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print(f"Warning: {file_path} does not exist")

    dataread.remove_entry(name, root)
    os.remove(f'{root}/var/rupk/{name}.index')
    print("Removed.")
