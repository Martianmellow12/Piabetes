#Piabetes Updater Script
#Used to update Piabetes from a remote location
#Written By Michael Kersting
import sys
import os
from os import system

local_dir = str(os.getcwd())+'/'

local_dir.replace('//','/')
#
#
#
#
#
#Check For An Update
if os.path.isfile(local_dir+'main_updated.py'):
    print ''
    print 'Update found - Installing...'

    os.remove(local_dir+'main.py')
    system('cp main_updated.py main.py')
    os.remove(local_dir+'main_updated.py')

    print 'Update complete'
    print ''
