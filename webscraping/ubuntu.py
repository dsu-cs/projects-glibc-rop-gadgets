# Might be nice to sort the files into subfolders so directories don't become a mess
# Still need to look into depacking these and extracting our libc files
# Way to filter results so we only go back to 2020 to match up with Fedora group
#I think this does inlcude the multi-architecture things which we still need to ask about

#Make sure Beautiful Soup intalled in WSL terminal
    #pip install beautifulsoup4 requests


from bs4 import BeautifulSoup
import requests
import subprocess
import re
import os

url_prefix = "https://archive.ubuntu.com/ubuntu/pool/main/g/glibc/"

# Where I want things to download to, you can change to whatever you want
download_dir = '../GlibcDownloads'
gadgets_dir = '../Gadgets'
#makes sure dir exists
os.makedirs(download_dir, exist_ok=True)
os.makedirs(gadgets_dir, exist_ok=True)


ubuntu_glibc = requests.get(url_prefix)
soup = BeautifulSoup(ubuntu_glibc.text, 'html.parser')

#Find only the packages we need, these formats
# libc6_<ver>_<arch>.deb
# libc6-i386_<ver>_amd64.deb
# libc6-amd64_<ver>_i386.deb
# libc6-x32_<ver>_amd64.deb
# Match only plain "libc6" packages
match = re.compile(r"^libc6_[0-9].*_(amd64|i386|arm64|armhf)\.deb$")


#Skip over the stuff we dont need
skip = re.compile(r"(-dev|-dbg|-bin|-doc|-locale|-prof|_all\.deb$)")
count = 0
for link in soup.find_all('a', href=True):
    name = link.text.strip()
    if not name.endswith(".deb"): #if not a deb file, skip
        continue
    if skip.search(name): #Checks for the other types, dev, dpkg, etc
        continue
    if match.match(name): # Found a match, download
        file_path = os.path.join(download_dir, name)
        if os.path.exists(file_path):
            print(f"Skipping (already exists): {name}")
            continue
        print(f"Downloading: {name}")
        link_download = requests.get(url_prefix + name, stream=True)
        with open(file_path, mode="wb") as file:
            for chunk in link_download.iter_content(chunk_size=10 * 1024):
                file.write(chunk)
        count += 1

        # Unpack using the full path
        subprocess.run(["debx", "unpack", file_path])
        dir_path = file_path[:-4]

        #walk the files and find the libc.so.6
        libc_path = ""
        #check if folder contains data.tar.zst
        data_tar_zst_path = os.path.join(dir_path, "data.tar.zst")
        data_tar_path = os.path.join(dir_path, "data.tar")
        data_path = os.path.join(dir_path, "data")

        libc = "libc.so.6"

        if os.path.isfile(data_tar_zst_path):
            subprocess.run(['zstd', '-d', data_tar_zst_path, '-o', data_tar_path], check=True)
            subprocess.run(['tar', '-xf', data_tar_path, '-C', dir_path], check=True)
            for root, dirs, files in os.walk(os.path.join(dir_path, "usr", "lib")):
                if libc in files:
                    libc_path = os.path.join(root, libc)
        else:
            for root, dirs, files in os.walk(os.path.join(dir_path, "data", "lib")):
                if libc in files:
                    libc_path = os.path.join(root, libc)
        print(f"libc path is {libc_path}")
        gadget_path = os.path.join(gadgets_dir, name[:-4] + ".txt")
        with open(gadget_path, "w") as out:
            subprocess.run(
                ["ropper", "--nocolor", "--file", libc_path],
                stdout=out,
                stderr=subprocess.STDOUT,
                check=True,
                text=True)

print(f"\nDone — {count} files downloaded to {download_dir}")