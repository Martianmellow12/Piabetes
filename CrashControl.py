#Crash Control Script
#Reboots The Computer If A Crash (in Piabetes) Occurs
#Written By Michael Kersting Jr.
import os
from os import system
import sys
import textmagic.client

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
    print 'Notifying Michael of the crash...',

    sms_in = client.receive(0)
    try:
        client.send('17042306940','Piabetes crashed | '+str(sms_in['messages'][0]['from'])+' | '+str(sms_in['messages'][0]['text']))
    except Exception:
        print 'Failed'
    else:
        print 'Done'

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
