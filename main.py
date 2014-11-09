#Piabetes Server
#A Service For The Retreival Of Nutritional Information
#Written By Michael Kersting
#xmltodict Courtesy Of Martin Blech
import os
from os import system
import sys
import textmagic.client
import datetime
import urllib2
import xmltodict
import time
import re
import time

whitelist = ['17042306940']
mode = 'b'
local_dir = str(os.getcwd())+'/'
now = datetime.datetime.now()
version = 'v1.2'
online = False
wolfram_key = str()
textmagic_key = str()
textmagic_user = str()
sms_in = {}
sms_out = str()
gpio_avail = False
credit_amount = float()

dev_mode = False
dev_number = str()

regex_parser = '\d+ \w+( oz)?'
regex_filename = ' ([^\s]+) '
regex_fileurl = ' [^\s]+ (.+)$'
regex_units = '(\d+) (\w+( oz)?) (.+)'

do_libupdate = True

info = 'Piabetes '+version+'\nWritten By Michael Kersting\nReleased Under The MIT License'

if '//' in local_dir:
    local_dir = local_dir.replace('//','/')
#
#
#
#
#
#Prevention Of Crash Loops
if os.path.isfile(local_dir+'crashcom.nt'):
    print 'Deleted a file that may have caused a crash loop'
    os.remove(local_dir+'crashcom.nt')
#
#
#
#
#
#Whitelist Saving Function
def save_whitelist():
    global whitelist
    global local_dir

    if os.path.isfile(local_dir+'Whitelist.nt'):
        os.remove(local_dir+'Whitelist.nt')
        
    fileout = open(local_dir+'Whitelist.nt','w')
        
    for i in range(0,len(whitelist)):
        fileout.write(whitelist[i]+'\n')
    fileout.close()
    return True
#
#
#
#
#
#Load Whitelist Function
def load_whitelist():
    print ''
    print 'Loading Whitelist...'
    global whitelist
    global local_dir

    if os.path.isfile(local_dir+'Whitelist.nt'):
        filein = open(local_dir+'Whitelist.nt')
        whitelist = filein.readlines()
        filein.close()
        for i in range(0,len(whitelist)):
            whitelist[i] = whitelist[i].rstrip('\n')
            print 'Whitelist Load > '+whitelist[i]
    print 'Complete'
    print ''
#
#
#
#
#
#Ping Function
def ping():
    try:
        response=urllib2.urlopen('https://www.google.com',timeout=1)
        return True
    except urllib2.URLError as err:
        return False
#
#
#
#
#
#Reformat Function
def reformat(text):
    text = text.replace('&','and')
    text = text.replace("'","")
    text = text.replace(' ','%20')
    
    return text
#
#
#
#
#
#Library Checking
if not os.path.isdir(local_dir+'Library'):
    os.mkdir(local_dir+'Library')
#
#
#
#
#
#First Time Setup
if not os.path.isfile(local_dir+'Config.nt'):
    print ''
    print '------ Piabetes Server First Time Setup ------'
    print 'This is the first time setup for the Piabetes'
    print 'server. Please do not shut down the machine'
    print 'while setup is taking place.'
    print ''
    print 'Creating config file...',

    fileout = open(local_dir+'Config.nt','w')
    fileout.write(str(datetime.datetime.today())+'\n')
    fileout.write(version+'\n')
    fileout.close()
    save_whitelist()

    print 'Done'

    print 'Please enter a number to be whitelisted'
    print 'This number will be able to whitelist others in the future'
    to_whitelist = raw_input('> ')
    whitelist.append(to_whitelist)
    save_whitelist()
    print 'Successfully added '+to_whitelist+' to the whitelist'
    
    print 'Setup complete'
    print '----------------------------------------------'
    print ''
#
#
#
#
#
#Load API Keys
print ''
print 'Loading API keys...',
if os.path.isfile(local_dir+'api_keys.nt'):
    filein = open(local_dir+'api_keys.nt')
    keys = filein.readlines()
    filein.close()
    wolfram_key = keys[0].rstrip('\n')
    textmagic_key = keys[1].rstrip('\n')
    textmagic_user = keys[2].rstrip('\n')
    print 'Done'
else:
    print 'Error'
    print 'Please enter required data'
    wolfram_key = raw_input('Wolfram Alpha Key > ')
    textmagic_user = raw_input('TextMagic Username > ')
    textmagc_key = raw_input('TextMagic Key > ')
    fileout = open(local_dir+'api_keys.nt','w')
    fileout.write(wolfram_key+'\n'+textmagic_key+'\n'+textmagic_user+'\n')
    fileout.close()
    print 'API File was created'
print ''
#
#
#
#
#
#Defaulting To Developer Mode When TextMagic API Is Unavailable
client = textmagic.client.TextMagicClient(textmagic_user,textmagic_key)
try:
    credit_amount = 'Credits: '+str(client.account()['balance'])
except Exception,e:
    print 'An error ocurred with TextMagic'
    print 'Defaulting to developer mode'
    dev_mode = True
    print 'Please note that certain functions may not work'
    print 'Enter "help" for more details'
    print ''
    print '----- Developer Mode -----'
    print 'Enter a number to "send" messages from'
    print 'Note that this number must be whitelisted'
    dev_number = raw_input('>')
    print '--------------------------'
    print ''
#
#
#
#
#
#Argument Checking
if len(sys.argv) > 1:
    
    if sys.argv[1] == '-d' and not dev_mode == True:
        print 'Piabetes will now run in developer mode'
        print 'Please note that certain functions may not work'
        print 'Enter "help" for more details'
        dev_mode = True
        print ''
        print '----- Developer Mode -----'
        print 'Enter a number to "send" messages from'
        print 'Note that this number must be whitelisted'
        dev_number = raw_input('>')
        print '--------------------------'
        print ''
#
#
#
#
#
#Config File Validation And Updating
fileout = open(local_dir+'Config.nt','w')
fileout.write(str(datetime.datetime.today())+'\n')
fileout.write(version+'\n')
fileout.close()
#
#
#
#
#
#Check Online Status
print 'Testing connection to the internet...',
online = ping()

if online:
    print 'Connection established'
else:
    print 'Failed to connect'
    print 'Quitting...'
    print ''
    sys.exit(0)
#
#
#
#
#
#Update Config File
fileout = open(local_dir+'Config.nt','w')
fileout.write(str(datetime.datetime.today())+'\n')
fileout.write(version+'\n')
fileout.close()
#
#
#
#
#
#Timestamp Function
def timestamp():
    return '['+str(datetime.datetime.today())+'] '
#
#
#
#
#
#Get Update Function
def get_update(url):
    global local_dir
    
    fileout = open(local_dir+'main_updated.py','w')

    try:
        response = urllib2.urlopen(url).read()
    except Exception:
        return False

    fileout.write(response)
    fileout.close()
    return True
#
#
#
#
#
#Get File Function
def get_file(name,url):
    global local_dir

    if os.path.isfile(local_dir+name):
        return False

    try:
        response = urllib2.urlopen(url).read()
    except Exception:
        return False

    fileout = open(local_dir+name,'w')
    fileout.write(response)
    fileout.close()
    return True
#
#
#
#
#
#TextMagic Setup
if dev_mode == False:
    try:
        credit_amount = 'Credits: '+str(client.account()['balance'])
    except Exception,error_code:
        print 'Error ['+str(error_code)+']'
        print 'The API key supplied is likely invalid'
        sys.exit(0)

    if client.account()['balance'] < 1:
        print '     ### WARNING ###'
        print 'CREDIT AMOUNT BELOW $1.00'
        print '     ###############'
        
if dev_mode:
    print 'You\'re in developer mode, so this doesn\'t matter right now'
    
print credit_amount
load_whitelist()
#
#
#
#
#
#Misc. Setup
if os.path.isfile(local_dir+'Reboot.nt'):
    filein = open(local_dir+'Reboot.nt')
    totext = filein.read()
    filein.close()
    if dev_mode:
        print 'Piabetes is back online'
    else:
        client.send('Piabetes is back online',totext)
    os.remove(local_dir+'Reboot.nt')
    print timestamp()+'Reboot file detected | administering notification to '+totext

try:
    import RPI.GPIO as gpio
except ImportError:
    print 'No GPIO Found'
    print 'Indicator LEDs will be unavailable'
    gpio_avail = False
else:
    print 'GPIO imported'
    print 'Indicator LEDs are now running (if they\'re plugged in)'
    gpio_avail = True
    gpio.setup(14,gpio.OUT)
    gpio.setup(15,gpio.OUT)
#
#
#
#
#
#GPIO Light Definitions
def processing_led(state):
    if state == 1:
        gpio.output(14,True)
    else:
        gpio.output(14,False)

def power_led(state):
    if state == 1:
        gpio.output(15,True)
    else:
        gpio.output(15,False)
#
#
#
#
#
#Query Functions
def query_carbs(food):
    global wolfram_key
    
    query_url = 'http://api.wolframalpha.com/v2/query?appid='+wolfram_key+'&input='+reformat('carbs '+str(food))+'&format=plaintext'
    response = urllib2.urlopen(query_url).read()
    return xmltodict.parse(response)

def query_fiber(food):
    global wolfram_key

    query_url = 'http://api.wolframalpha.com/v2/query?appid='+wolfram_key+'&input='+reformat('dietary fiber '+str(food))+'&format=plaintext'
    response = urllib2.urlopen(query_url).read()
    return xmltodict.parse(response)
#
#
#
#
#
#Parsing Functions
def parse_carbs(toparse):
    global regex_parser
    
    if toparse['queryresult']['@success'] == 'true':
        amount = re.search(regex_parser,toparse['queryresult']['pod'][0]['subpod']['plaintext'])
        carbs = re.search(regex_parser,toparse['queryresult']['pod'][1]['subpod']['plaintext'])
        main = 'Qty: '+amount.group(0)+'\nCarbs: '+carbs.group(0)+'\n'
    else:
        main = 'Data Unavailable\nCarbs: N/A\n'
        
    return main

def parse_fiber(toparse):
    global regex_parser
    
    if toparse['queryresult']['@success'] == 'true' and not 'data not available' in toparse['queryresult']['pod'][1]['subpod']['plaintext']:
        m = re.search(regex_parser,toparse['queryresult']['pod'][1]['subpod']['plaintext'])
        main = 'Dietary Fiber: '+m.group(0)
    else:
        main = 'Dietary Fiber: N/A'
        
    return main
#
#
#
#
#
#Library Updating Function And Management
def update_library():
    global local_dir

    print ''
    print '----- Library Update -----'
    print 'The library will now begin updating it\'s records'
    print 'Piabetes will be inaccessible during this time'
    print 'Please be patient, this may take a while'

    lib_files = os.listdir(local_dir+'Library')
    est_time = time.time()
    query_carbs('cake')
    query_fiber('cake')
    est_time = int(time.time()-est_time)
    est_time = est_time*len(lib_files)
    est_time = est_time/60
    print 'ETC: '+str(est_time)+' minute(s)'
    print 'Time At Start: '+str(datetime.datetime.now())

    for filename in lib_files:
        if not filename[:1] == '.':
            os.remove(local_dir+'Library/'+filename)
            fileout = open(local_dir+'Library/'+filename,'w')
            response = parse_carbs(query_carbs(filename))+parse_fiber(query_fiber(filename))
            fileout.write(response)
            fileout.close()
            print '[UPDATED] '+filename
        else:
            print '[SKIPPED] '+filename

    print 'The update is now complete'
    print '--------------------------'
    print ''
#
#
#
#
#
#Command Parsing
def parse_command(toparse):
    global local_dir
    global whitelist
    global sms_in
    global info
    global client
    global regex_filename
    global regex_fileurl
    global dev_mode
    global dev_number
    global do_libupdate
    global manual_libupdate

    if toparse[:12] == '--whitelist ':
        whitelist.append(toparse[12:])
        save_whitelist()
        if not dev_mode:
            client.send('You have been added to the Piabetes whitelist',toparse[12:])
        print timestamp()+'Added '+toparse[12:]+' to the whitelist'

    if toparse[:12] == '--blacklist ':
        whitelist.remove(toparse[12:])
        save_whitelist()
        print timestamp()+'Removed '+toparse[12:]+' from the whitelist'

    if toparse == '--info':
        print timestamp()+'Info requested from '+sms_in['messages'][0]['from']
        if sms_in['messages'][0]['from'] in whitelist:
            if dev_mode:
                print info
            else:
                client.send(info,sms_in['messages'][0]['from'])
            print timestamp()+'Whitelist authenticated, reply sent'
        else:
            print timestamp()+'Whitelist authentification failed'

    if toparse == '--restart':
        print timestamp()+'Restart command received'
        if sms_in['messages'][0]['from'] in whitelist:
            print timestamp()+'Whitelist authenticated'
            fileout = open(local_dir+'Reboot.nt','w')
            fileout.write(sms_in['messages'][0]['from'])
            fileout.close()
            if dev_mode:
                print 'Piabetes will notify you when the restart is complete'
            else:
                client.send('Piabetes will notify you when the restart is complete',sms_in['messages'][0]['from'])
            os.remove(local_dir+'crashcom.nt')
            system('sudo shutdown -r now')
        else:
            print timestamp()+'Whitelist authentification failed'

    if toparse == '--shutdown':
        print timestamp()+'Shutdown command received'
        if sms_in['messages'][0]['from'] in whitelist:
            print timestamp()+'Whitelist authenticated'
            os.remove(local_dir+'crashcom.nt')
            system('sudo shutdown -h now')
        else:
            print timestamp()+'Whitelist authentification failed'

    if toparse[:9] == '--update ':
        url = toparse[9:]
        print timestamp()+sms_in['messages'][0]['from']+' requested to update'
        print timestamp()+url
        if not sms_in['messages'][0]['from'] in whitelist:
            print timestamp()+sms_in['messages'][0]['from']+' is not whitelisted'
            return False
        if get_update(url):
            print 'Successfully downloaded update'
            print 'The system will now restart'
            if not dev_mode:
                client.delete_reply(int(sms_in['messages'][0]['message_id']))
            os.remove(local_dir+'crashcom.nt')
            time.sleep(3)
            system('sudo shutdown -r now')

    if toparse[:9] == '--upload ':
        url = re.search(regex_fileurl,toparse)
        name = re.search(regex_filename,toparse)
        url = url.group(1)
        name = name.group(1)
        print timestamp()+sms_in['messages'][0]['from']+' is attempting a file upload'
        if not sms_in['messages'][0]['from'] in whitelist:
            print timestamp()+sms_in['messages'][0]['from']+' is not whitelisted'
            return False
        if get_file(name,url):
            print 'The file was successfully downloaded'

    if toparse == '--exit':
        os.remove(local_dir+'crashcom.nt')
        print timestamp()+'Exit request received - Quitting...'
        sys.exit(0)

    if toparse == '--nolibupdate':
        do_libupdate = False
        print timestamp()+'Automatic library updating was disabled'

    if toparse == '--libupdate':
        do_libupdate = True
        print timestamp()+'Automatic library updating was enabled'

    if toparse == '--dolibupdate':
        print timestamp()+'The library will now be updated manually'
        update_library()
#
#
#
#
#
#Main Program
print 'Piabetes Data Log'
print '-------------------------------------------------'
filein = open(local_dir+'crashcom.nt','w')
filein.close()
print timestamp()+'Created crash file'
print timestamp()+'All exceptions after this point will be percieved as a crash'
print timestamp()+'If endless loop occurs, unplug network cable'
print '['+str(datetime.datetime.today())+'] Started logging data'

if gpio_avail:
    power_led(1)

while True:

    if dev_mode:
        request = raw_input('>')
        sms_in = {
            'messages':{
                0:{
                    'text':request,
                    'from':dev_number
                    }
                }
            }
    else:
        sms_in = client.receive(0)

    if len(sms_in['messages'])>0:
        sms_in['messages'][0]['text'] = sms_in['messages'][0]['text'].lower()
        if gpio_avail:
            processing_led(1)
        request = str(sms_in['messages'][0]['text'])
        print timestamp()+str(sms_in['messages'][0]['from'])+' requested info on '+request

        if str(sms_in['messages'][0]['from']) in whitelist and not str(sms_in['messages'][0]['text'])[:2] == '--':
            print timestamp()+str(sms_in['messages'][0]['from'])+' is on the whitelist'
            if os.path.isfile(local_dir+'Library/'+request):
                print timestamp()+'Library file found - Sending from memory'
                filein = open(local_dir+'Library/'+request,'r')
                response = filein.read()
                filein.close
            else:
                print timestamp()+'No library file found - Looking up data'
                response = parse_carbs(query_carbs(request))+parse_fiber(query_fiber(request))
                fileout = open(local_dir+'Library/'+request,'w')
                fileout.write(response)
                fileout.close()

            if dev_mode:
                print response
            else:
                try:
                    client.send(response,sms_in['messages'][0]['from'])
                except Exception,e:
                    print timestamp()+str(e)
                else:
                    print '['+str(datetime.datetime.today())+'] Sent response to '+str(sms_in['messages'][0]['from'])

        elif not str(sms_in['messages'][0]['from']) in whitelist and not str(sms_in['messages'][0]['text'])[:2] == '--':
            print timestamp()+str(sms_in['messages'][0]['from'])+' is not on the whitelist'
        else:
            print timestamp()+'Received command: '+request
            parse_command(request)
            
        if not dev_mode:
            client.delete_reply(int(sms_in['messages'][0]['message_id']))

        if gpio_avail:
            processing_led(0)

    now = datetime.datetime.now()
    if int(now.day) == 1 and int(now.hour) == 3 and do_libupdate == True:
        update_library()
