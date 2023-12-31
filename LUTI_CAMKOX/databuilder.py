"""
databuilder.py

Build data for project
"""
import os
import requests

from LUTI_CAMKOX.globals import *

"""
ensureFile
Check the local file system for the existence of a file and download it from
the givel url if it's not present. Used for installation of data file from
remote sources so we don't check "official" data into the GitHub repo.
@param localFilename The file to check for existence on the local file system
@param url Where to download it if it's not there
"""
def ensureFile(localFilename,url):
    if not os.path.isfile(localFilename):
        print("Downloading "+localFilename+" from "+url)
        #wget.download(url,localFilename) # won't allow headers to add user agent

        #use requests module instead, which doesn't set the file info like wget does - datestamp wrong!

        headers={'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, allow_redirects=True, headers=headers)
        open(localFilename, 'wb').write(r.content)
