import os
import datetime

poll_time = .5
capturing = False
accelerometer = False
sounding = False
archive_time = 240 #how far back to archive, in seconds
start_date = datetime.datetime(year=1970,month=1,day=1)
gpio_dir = '/sys/class/gpio'
switch_pins = {'archive':'23', 'toggle':'47'}
light_pins  = {'archive':'27', 'toggle':'44'}
accelerometer_pins = {'x':'AIN5', 'y':'AIN3', 'z':'AIN1'}
sound_pin = 'AIN0'

def _get_dir(ext):
    # if os.path.exists('/media/BONESTORAGE'):
    #     if not os.path.exists('/media/BONESTORAGE/' + ext):
    #         print 'mkdiring bonestorage'
    #         os.mkdir('/media/BONESTORAGE/' + ext)
    #     return '/media/BONESTORAGE/' + ext
    return os.path.realpath(__file__)[:-10] + '/' + ext

def capture_dir():
    return _get_dir('captures')

def archive_dir():
    return _get_dir('saved')

def audio_dir():
    return _get_dir('audio')

def is_capturing():
    return capturing

def is_accelerometer():
    return accelerometer

def is_sounding():
    return sounding

def toggle_capturing(set_value=None):
    global capturing
    capturing = set_value or not capturing

def get_unixtime():
    return int((datetime.datetime.utcnow() - start_date).total_seconds()*1000000)
