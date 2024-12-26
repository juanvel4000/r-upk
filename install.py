import shutil
import os
import dataread
import package

def InstallPackage(file=None, root="/"):
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
        
        file = os.path.abspath(file)
        root = os.path.abspath(root)
        
        if not os.path.isdir(root):
            os.makedirs(root)

        package.extract_package(f'{root}/tmp/rupk/', file)
        manifest = dataread.parsemanifest(f'{root}/tmp/rupk/RUPK/Manifest.ini')
        if dataread.check_installed(manifest['Name'], root) == manifest['Name']:
            print("Package is already installed.")
            if os.path.isdir('{root}/tmp/upk'):
                print("Cleaning up...")
                shutil.rmtree(f'{root}/tmp/upk/')
                
            return False
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
                    print(f"Skipping {dest_file}, file already exists.")
        
        os.chdir(cdir)
        shutil.copy(f"{root}/tmp/rupk/RUPK/tree", f"{root}/var/rupk/{manifest['Name']}.index")
        shutil.rmtree(f'{root}/tmp/rupk/')
        

        if manifest is not False:
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
    with open(f'{root}/var/rupk/{name}.index', 'r') as db:
        lines = db.readlines()
        for line in lines:
            line = line.strip()
            os.remove(f'{root}/{line}') 
        dataread.remove_entry(name, root)
    os.remove(f'{root}/var/rupk/{name}.index')
    print("Removed.")