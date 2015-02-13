#Piabetes Updater Script
#Used to update Piabetes from a remote location
#Written By Michael Kersting Jr.
import sys
import os
from os import system
import sys
import urllib2
from time import sleep
import re
import json
import shutil
import zipfile
import platform

if platform.system() == 'Windows':
    local_dir = str(os.getcwd())+'\\'
else:
    local_dir = str(os.getcwd())+'/'
print local_dir

safelist = [
    'Library',
    'Whitelist Backup'
    'config.nt',
    'Whitelist.nt',
    'api_keys.nt'
    ]

do_update = True
info_url = 'http://piabetes.weebly.com/uploads/9/2/1/4/9214413/info.txt'
update_file_regex = '^[^\.]\.upd$'
#
#
#
#
#
#Update Piabetes Function
def update_piabetes(info):
    global local_version
    global local_dir
    global safelist
    
    print 'Piabetes will now be updated to version '+str(info[0])
    print 'Please don\'t power off the computer until the update is complete'
    print ''

    #Delete all old data
    print 'Deleting all info for v'+str(local_version)+'...',
    print local_dir
    files = os.listdir(local_dir)
    for i in files:
        print local_dir+i
        if os.path.isfile(local_dir+i) and not i in safelist:
            os.remove(local_dir+i)
        if os.path.isdir(local_dir+i) and not 'Library' in i and not 'Whitelist Backup' in i:
            shutil.rmtree(local_dir+i)
    print 'Done'

    #Create Synthetic Config File
    print 'Creating synthetic configuration file...',
    try:
        fileout = open(local_dir+'config.nt','w')
        fileout.write('[TIME]\n')
        fileout.write('v'+str(info[0])+'\n')
        fileout.close()
    except Exception,e:
        print 'Failed'
        print str(e)
        print 'You will need to enter a default phone number'
    else:
        print 'Done'

    #Download and unpack the new version
    print 'Downloading v'+str(info[0])+'...',
    try:
        response = urllib2.urlopen(info[1])
        fileout = open(local_dir+'Piabetes.zip','wb')
        fileout.write(response.read())
        fileout.close()
    except:
        print 'Failed'
        print 'An exception occured, you\'ll have to do it manually'
        sys.exit(0)
    print 'Done'

    print 'Unpacking...',
    zipped = zipfile.PyZipFile(local_dir+'Piabetes.zip')
    zipped.extractall(local_dir)
    zipped.close()
    print 'Done'
    os.remove(local_dir+'Piabetes.zip')
    print 'Deleted zipped package'

    print 'Update Complete'
    print '------------------------------'
    print ''
#
#
#
#
#
#Check For Remote Updates
update_info = urllib2.urlopen(info_url).read()
update_info = json.loads(update_info)
remote_version = update_info[0]

try:
    filein = open(local_dir+'config.nt')
except:
    print 'No config file found'
    print 'Maybe this is your first time running Piabetes'
    sys.exit(0)

local_version = filein.readlines()
filein.close()
local_version = local_version[1].replace('\n','')
local_version = float(local_version.replace('v',''))

if local_version == remote_version:
    print 'Piabetes is up to date'
    sys.exit(0)

print 'An update was found for Piabetes'
print 'Version '+str(remote_version)+' is available, and your current'
print 'version is '+str(local_version)+'. Press Ctrl-c to enter update'
print 'menu, or Piabetes will continue in 5 seconds.'

if do_update  == False:
    sys.exit(0)


update_piabetes(update_info)
