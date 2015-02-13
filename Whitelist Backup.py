#Piabetes Whitelist Backup Script
#Should Be Run BEFORE Piabetes and Update Script
#Written By Michael Kersting Jr.
import os
from os import system
import sys
import datetime
import shutil

local_dir = str(os.getcwd())+'/'
#
#
#
#
#
#Backup Directory Setup
print ''
print '----- Piabetes Whitelist Backup-----'

if not os.path.isdir(local_dir+'Whitelist Backups/'):
    print '           First Time Setup'
    print ''
    print 'Creating directory...',
    os.mkdir(local_dir+'Whitelist Backups/')
    print 'Done'
    print ''
#
#
#
#
#
#Backup Process
if os.path.isfile(local_dir+'Whitelist.nt'):
    print 'Whitelist found'
    print 'Backing up...',
    date = str(datetime.datetime.today()).replace(':','.')
    shutil.copyfile(local_dir+'Whitelist.nt',local_dir+'Whitelist Backups/'+date+'.nt')
    print 'Done'
else:
    print 'No whitelist found'
    print 'Oh well, it\'ll be backed up next time'
print '------------------------------------'
print ''
