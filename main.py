#Piabetes Server
#A Service For The Retreival Of Nutritional Information
#Written By Michael Kersting Jr.
import os
from os import system
import sys
import textmagic.client
import datetime
import urllib2
import wolframalpha as wolf
import time
import re

whitelist = ['17042306940']
mode = 'b'
local_dir = str(os.getcwd())+'/'
now = datetime.datetime.now()
version = 'v1.4'
online = False
wolfram_key = str()
textmagic_key = str()
textmagic_user = str()
sms_in = {}
sms_out = str()
gpio_avail = False
credit_amount = float()

uptime_start = float()
uptime = {
    'seconds':int(),
    'minutes':int(),
    'hours':int(),
    'days':int()
    }

dev_mode = False
dev_number = str()

regex_parser = '\d+\.?\d+? \w+( oz)?'
regex_filename = ' ([^\s]+) '
regex_fileurl = ' [^\s]+ (.+)$'
regex_units = '(\d+) (\w+( oz)?) (.+)'
regex_title = '([^|]+)'
regex_qty = '\d+\.?\d+? \w+ ?( oz)?'
query_regex = '([^:]*):([^:]+)'

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
    textmagic_key = raw_input('TextMagic Key > ')
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
    print 'Please note that certain functions may not work correctly'
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
        print 'Please note that certain functions may not work correctly'
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
#File Structure Integrity Check
def integrity_check():
    global local_dir
    fail_rate = int()
    
    #Levels decide how important files are
    #Level 1 - Not necessary for operation
    #Level 2 - Features will be missing, but Piabetes can still function
    #Level 3 - Vital, Piabetes will be nonfunctional without it
    files = {
        'Changelog.txt':1,
        'textmagic':3,
        'Config.nt':1,
        'wolframalpha':3,
        'Whitelist.nt':1,
        'Updater.py':2,
        'api_keys.nt':3,
        'Whitelist Backup.py':2,
        'CrashControl.py':2,
        'License.txt':1,
        }

    print ''
    print '----- Filesystem Integrity Check -----'

    for filename in files:
        if os.path.isfile(local_dir+filename) or os.path.isdir(local_dir+filename):
            print '[ ok ] '+filename
        else:
            print '[fail] '+filename
            fail_rate = fail_rate+files[filename]

    fail_rate = int((100/len(files))*fail_rate)
    print 'Integrity Rating: '+str(100-fail_rate)+'%'
    print '--------------------------------------'
    print ''
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
#Query Function
def query(food):
    global wolfram_key
    global query_regex

    #Check For Misentries
    if not ':' in food:
        food = ':'+food

    parsed_request = re.search(query_regex,food)
    qty = parsed_request.group(1)
    food_name = parsed_request.group(2)
    wc = wolf.Client(wolfram_key)
    
    response = wc.query('carbs in '+qty+' '+food_name)
    #Modify For Carb Info Discrepancies
    try:
        carbs = response.pods[1].text
    except Exception:
        carbs = 'N/A'
    if '|' in carbs:
        carbs = 'N/A'

    response = wc.query('dietary fiber in '+qty+' '+food_name)
    #Modify For Dietary Fiber Info Discrepancies
    try:
        fiber = response.pods[1].text
    except Exception:
        fiber = 'N/A'
    if '|' in fiber:
        fiber = 'N\A'

    #Modify Qty Label For Blank Return
    if qty == '':
        qty = 'N/A'

    final_response = food_name+'\n'+'Qty: '+qty+'\n'+'Carbs: '+carbs+'\n'+'Dietery Fiber: '+fiber
    return final_response
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
    query('cake')
    est_time = int(time.time()-est_time)
    est_time = est_time*len(lib_files)
    est_time = est_time/60
    print 'ETC: '+str(est_time)+' minute(s)'
    print 'Time At Start: '+str(datetime.datetime.now())

    for filename in lib_files:
        if not filename[:1] == '.':
            os.remove(local_dir+'Library/'+filename)
            fileout = open(local_dir+'Library/'+filename,'w')
            response = query(filename)
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
    global uptime_start
    global uptime

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
        if not dev_mode:
            client.delete_reply(int(sms_in['messages'][0]['message_id']))
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

    if toparse == '--uptime':
        print timestamp()+sms_in['messages'][0]['from']+' requested the uptime'
        if not sms_in['messages'][0]['from'] in whitelist:
            print timestamp()+sms_in['messages'][0]['from']+' is not whitelisted'
            return False
        else:
            uptime_string = str(uptime['days'])+' days\n'+str(uptime['hours'])+' hours\n'+str(uptime['minutes'])+' minutes\n'+str(uptime['seconds'])+' seconds'
            if dev_mode:
                print uptime_string
            else:
                client.send(uptime_string,sms_in['messages'][0]['from'])
            
            print timestamp()+sms_in['messages'][0]['from']+' whitelisted, uptime sent ('+uptime_string.replace('\n',', ')+')'

    if toparse == '--integrity':
        print timestamp()+sms_in['messages'][0]['from']+' requested an integrity check'

        if dev_mode == True:
            integrity_check()
        else:
            print timestamp()+'Integrity checks not available via text message'
            if sms_in['messages'][0]['from'] in whitelist:
                client.send('Integrity checks not available via text message',sms_in['messages'][0]['from'])
                print timestamp()+'They have been notified of this'
            else:
                print timestamp()+'No matter, they\'re not whitelisted anyway'

    if toparse == '--flushlib':
        print timestamp()+sms_in['messages'][0]['from']+' requested a library flush'

        if sms_in['messages'][0]['from'] in whitelist:
            print timestamp()+'Authenticated '+sms_in['messages'][0]['from']+' with the whitelist'
            print timestamp()+'Flushing the library...',
            if not os.path.isdir(local_dir+'Library'):
                print 'Failed'
            else:
                lib_files = os.listdir(local_dir+'Library')
                for filename in lib_files:
                    if not filename[:1] == '.':
                        os.remove(local_dir+'Library/'+filename)
                print 'Done'
                print timestamp()+'The library was successfully flushed'

    if toparse == '--addlib':
        print timestamp()+sms_in['messages'][0]['from']+' requested a manual addition to the library'
        if not sms_in['messages'][0]['from'] in whitelist:
            print timestamp()+sms_in['messages'][0]['from']+' is not on the whitelist'
            return
        if not dev_mode:
            print timestamp()+'Library additions are not allowed via text message'
            client.send('Library additions cannot be made via text message',sms_in['messages'][0]['from'])
        name = raw_input('Name of food: ')
        amount = raw_input('Quantity of food: ')
        carbs = raw_input('Carbs in amount given: ')
        fiber = raw_input('Dietary fiber in amount given: ')
        try:
            fileout = open(local_dir+'Library/'+str(amount)+':'+str(name),'w')
        except:
            print 'Error occured when attempting to open the file'
            return
        fileout.write(name+'\nQty: '+str(amount)+'\nCarbs: '+str(carbs)+'\nDietary Fiber: '+str(fiber))
        fileout.close()
        print timestamp()+'Library file successfully created'
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
uptime_start = time.time()

if gpio_avail:
    power_led(1)

while True:
    try:
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
    except Exception,e:
        print timestamp()+'There may have been a network error'
        print timestamp()+'Piabetes will idle until a connection is established'

        while not ping():
            time.sleep(10)
            print timestamp()+'IDLE'

        print timestamp()+'Piabetes is now back online'
        uptime_start = time.time()

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
                response = query(request)
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

    uptime['seconds'] = int(time.time()-uptime_start)
    if uptime['seconds']>=60:
        uptime['minutes'] = uptime['minutes']+1
        uptime['seconds'] = 0
        uptime_start = time.time()
    if uptime['minutes']>=60:
        uptime['hours'] = uptime['hours']+1
        uptime['minutes'] = 0
    if uptime['hours']>=24:
        uptime['days'] = uptime['days']+1
        uptime['hours'] = 0
