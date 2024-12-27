import os
import sys
import urllib.request
from configparser import ConfigParser
import tarfile
import glob
import package 
import install
import dataread
def updaterepos(root):
    try:
        config = ConfigParser()
        config.read(f'{root}/etc/rupk/repos')
        repositories = config.get('List', 'list').split(',')
        
        if not os.path.isdir(f'{root}/etc/rupk/repos.d'):
            os.makedirs(f'{root}/etc/rupk/repos.d')
        
        for repo in repositories:
            print(f"Updating: {repo}")
            url = config[repo]['Server']
            repo_url = f'{url}/{repo}.tar.gz'
            
            try:
                with urllib.request.urlopen(repo_url) as response:
                    if response.status == 200:
                        with open(f'{root}/etc/rupk/repos.d/{repo}.tgz', 'wb') as file:
                            file.write(response.read())
                        print(f"Updated {repo}")
                    else:
                        print(f"Could not update {repo}. HTTP Status: {response.status}")
            except Exception as e:
                print(f"Error downloading {repo}: {e}")
    except Exception as e:
        print(f"Error: {e}")

def checknetpkg(root, name):
    try:
        if not os.path.isdir(f'{root}/etc/rupk/repos.d'):
            updaterepos(root)
        
        for repolist in glob.glob(f'{root}/etc/rupk/repos.d/*.tgz'):
            repo_name = os.path.basename(repolist).replace('.tgz', '')  
            os.makedirs(f'{root}/tmp/rupk/{repo_name}', exist_ok=True)
            
        
            with tarfile.open(f'{repolist}', 'r:gz') as rl:
                rl.extractall(path=f'{root}/tmp/rupk/{repo_name}', filter=package.filtar)
            if os.path.exists(f'{root}/tmp/rupk/{repo_name}/{name}'):
                with open(f'{root}/tmp/rupk/{repo_name}/{name}', 'r') as rls:
                    version = rls.read()
                
                returnable = {
                    "Name": name,
                    "Version": version,
                    "Repository": repo_name
                }
                return returnable
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
def listall(root):
    if not os.path.isdir(f'{root}/etc/rupk/repos.d/'):
        updaterepos(root)
    availablepkg = 0
    for repolist in glob.glob(f'{root}/etc/rupk/repos.d/*.tgz'):
        with tarfile.open(repolist, 'r:gz') as tg:
            tg.extractall(path=f'{root}/tmp/rupk/{repolist}/', filter=package.filtar)
        for pkg in glob.glob(f'{root}/tmp/rupk/{repolist}/*'):
            with open(pkg, 'r') as pk:
                version = pk.read()
                version = version.strip()
                repo = os.path.basename(repolist).rsplit('.tgz', 1)
                availablepkg += 1
            print(f"{repo[0]} / {os.path.basename(pkg)}:{version}")
    if availablepkg == 1:
        print(f"{availablepkg} Package")
    else:
        print(f"{availablepkg} Packages")
def download(root, name):
    try:
        doesexist = checknetpkg(root, name)
        if doesexist == False:
            print("This package does not exist")
            return False
            
        config = ConfigParser()
        config.read(f'{root}/etc/rupk/repos')
        server = config[doesexist['Repository']]['Server'].strip()
        version = doesexist['Version'].strip()
        try:
            if not os.path.isdir(f'{root}/tmp/rupk/downloads'):
                os.makedirs(f'{root}/tmp/rupk/downloads')
            with urllib.request.urlopen(f'{server}/{doesexist['Name']}-{version}.rupk') as response:
                            if response.status == 200:
                                with open(f'{root}/tmp/rupk/downloads/{doesexist['Name']}.rupk', 'wb') as file:
                                    file.write(response.read())
                            else:
                                print(f"Could not download {doesexist['Name']}. HTTP Status: {response.status}")
                                return False
            with urllib.request.urlopen(f'{server}/{doesexist['Name']}-{version}.rupk.sha256') as sharesp:
                if sharesp.status == 200:
                    with open(f'{root}/tmp/rupk/downloads/{doesexist['Name']}.rupk.sha256', 'wb') as sha2:
                        sha2.write(response.read())
                        return f'{root}/tmp/rupk/downloads/{doesexist['Name']}.rupk'
                else:
                    return f'{root}/tmp/rupk/downloads/{doesexist['Name']}.rupk'

        except Exception as e:
                    print(f"Error downloading {doesexist['Name']}: {e}")
                    return False
    except Exception as e:
        print(f"Error: {e}")
        return False
def finddepends(root, file, alsoinstall=True, processed_dependencies=None):
    try:
        if processed_dependencies is None:
            processed_dependencies = set()

        if not os.path.isdir(f'{root}/tmp/rupk/extract'):
            os.makedirs(f'{root}/tmp/rupk/extract')

        if not os.path.isfile(os.path.abspath(file)):
            print(f"Could not find {file}")
            return False
        package.extract_package(f'{root}/tmp/rupk/extract', file)

        manifest = dataread.parsemanifest(f"{root}/tmp/rupk/extract/RUPK/Manifest.ini")

        if not manifest.get('Dependencies'):
            return True

        dependencies = manifest['Dependencies'].split(' ')
        for dependency in dependencies:
            if dependency in processed_dependencies:
                continue  
            processed_dependencies.add(dependency)

            download(root, dependency)

            if alsoinstall:
                install.InstallPackage(f'{root}/tmp/rupk/downloads/{dependency}.rupk', root)

            finddepends(root, f'{root}/tmp/rupk/downloads/{dependency}.rupk', alsoinstall, processed_dependencies)

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
