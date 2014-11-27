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

local_dir = str(os.getcwd())+'/'

do_update = True
local_dir = local_dir.replace('//','/')
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
    
    print 'Piabetes will now be updated to version '+str(info[0])
    print 'Please don\'t power off the computer until the update is complete'
    print ''
    
    #Backup all user-specific files
    print 'Backing up user-specific data...',
    if os.path.isfile(local_dir+'Whitelist.nt'):
        filein = open(local_dir+'Whitelist.nt','r')
        whitelist_contents = filein.read()
        filein.close()
    if os.path.isfile(local_dir+'config.nt'):
        filein = open(local_dir+'config.nt','r')
        config_contents = filein.read()
        filein.close()
    if os.path.isfile(local_dir+'api_keys.nt'):
        filein = open(local_dir+'api_keys.nt','r')
        api_contents = filein.read()
        filein.close()
    print 'Done'

    #Delete all old data
    print 'Deleting all info for v'+str(local_version)+'...',
    files = os.listdir(local_dir)
    for i in files:
        if os.path.isfile(local_dir+i):
            os.remove(local_dir+i)
        if os.path.isdir(local_dir+i):
            shutil.rmtree(local_dir+i)
    print 'Done'

    #Download and unpack the new version
    print 'Donwloading v'+str(info[0])+'...',
    try:
        fileout = open(local_dir+'Piabetes.zip','w')
        fileout.write(urllib2.urlopen(info[1]).read())
        fileout.close()
    except:
        print 'Failed'
        print 'An exception occured, you\'ll have to do it manually'
        sys.exit(0)
    print 'Done'

    print 'Unpacking...',
    zipped = zipfile.PyZipFile(local_dir+'Piabetes.zip')
    zipped.extractall()
    zipped.close()
    print 'Done'
    os.remove(local_dir+'Piabetes.zip')
    print 'Deleted zipped package'

    #Replace user-specific files
    print 'Replacing user-specific data...',
    fileout = open(local_dir+'Whitelist.nt','w')
    fileout.write(whitelist_contents)
    fileout.close()
    fileout = open(local_dir+'config.nt','w')
    fileout.write(config_contents)
    fileout.close()
    fileout = open(local_dir+'api_keys.nt','w')
    fileout.write(api_contents)
    fileout.close()
    print 'Done'

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
    print 'No update found'
    sys.exit(0)

print 'An update was found for Piabetes'
print 'Version '+str(remote_version)+' is available, and your current'
print 'version is '+str(local_version)+'. Press Ctrl-c to enter update'
print 'menu, or Piabetes will continue in 5 seconds.'

if do_update  == False:
    sys.exit(0)

print ''
print '----- Piabetes Update Menu -----'
print '[1] Update to v'+str(remote_version)
print '[2] Exit update menu'


try:
    selection = int(raw_input('> '))
except:
    print 'An exception ocurred: you probably entered an option incorrectly'
    sys.exit(0)

if selection == 1:
    update_piabetes(update_info)

if selection == 2:
    print 'Quitting update utility'
    print '----------------------------'
    print ''
    sys.exit(0)
