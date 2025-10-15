# Might be nice to sort the files into subfolders so directories don't become a mess
# Still need to look into depacking these and extracting our libc files
# Way to filter results so we only go back to 2020 to match up with Fedora group
#I think this does inlcude the multi-architecture things which we still need to ask about

#Make sure Beautiful Soup intalled in WSL terminal
    #pip install beautifulsoup4 requests


from bs4 import BeautifulSoup
import requests
import re
import os

url_prefix = "https://archive.ubuntu.com/ubuntu/pool/main/g/glibc/"

# Where I want things to download to, you can change to whatever you want
download_dir = "/home/drian/CSC470SoftwareEngineeringProject/stdlibTest"
#makes sure dir exists
os.makedirs(download_dir, exist_ok=True)


ubuntu_glibc = requests.get(url_prefix)
soup = BeautifulSoup(ubuntu_glibc.text, 'html.parser')

#Find only the packages we need, these formats
# libc6_<ver>_<arch>.deb
# libc6-i386_<ver>_amd64.deb
# libc6-amd64_<ver>_i386.deb
# libc6-x32_<ver>_amd64.deb
match = re.compile(
    r"^libc6(-[a-z0-9]+)?_[0-9].*_(amd64|i386|arm64|armhf|x32)\.deb$"
)


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
        #From what i saw online, using chunks is good practice for memory stuff
            #Can be slightly faster too

print(f"\nDone — {count} files downloaded to {download_dir}")