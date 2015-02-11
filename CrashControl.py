#Crash Control Script
#Reboots The Computer If A Crash (in Piabetes) Occurs
#Written By Michael Kersting Jr.
import os
from os import system
import sys
import textmagic.client
import time

local_dir = os.getcwd()+'/'
local_dir = local_dir.replace('//','/')
textmagic_user = str()
textmagic_key = str()
keys = []

apifile = open(local_dir+'api_keys.nt')
keys = apifile.readlines()
apifile.close()
textmagic_user = keys[2].rstrip('\n')
textmagic_key = keys[1].rstrip('\n')

client = textmagic.client.TextMagicClient(textmagic_user,textmagic_key)
print textmagic_user+" | "+textmagic_key
#
#
#
#
#
#Check For Reboot File
if os.path.isfile(local_dir+'crashcom.nt'):
    print ''
    print '----- FATAL ERROR -----'
    print 'Crash file detected'
    print 'Deleting file...',
    os.remove(local_dir+'crashcom.nt')
    print 'Done'

    while True:
        print 'Receiving data from TextMagic...',
        try:
            sms_in = client.receive(0)
        except:
            print 'Failed'
        else:
            print 'Done'
    
        print 'Notifying Michael of the crash...',
        try:
            info = str(sms_in['messages'][0]['from'])+' | "'+str(sms_in['messages'][0]['text'])+'"'
        except:
            info = 'Internal Issues'
        try:
            client.send('Piabetes crashed | '+info,'17042306940')
        except Exception,exc:
            print 'Failed'
            print 'Reason: '+str(exc)
            time.sleep(10)
        else:
            print 'Done'
            break

    print 'Deleting message that made Piabetes crash...'
    if len(sms_in['messages'])>0:
        client.delete_reply(sms_in['messages'][0]['message_id'])
        print 'Done'
    else:
        print 'No message to delete'
    
    print 'Sending restart command...',
    system('sudo shutdown -r now')
    print 'Done'
    print '-----------------------'
    print ''
else:
    print ''
    print 'No crash detected'
    print 'Commencing regular bootup'
