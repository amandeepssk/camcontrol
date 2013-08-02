import os
import datetime

poll_time = .5
capturing = False
archive_time = 600 #how far back to archive, in seconds
start_date = datetime.datetime(year=1970,month=1,day=1)
gpio_dir = '/sys/class/gpio'
switch_pins = {'archive':'23', 'toggle':'22'}
light_pins  = {'archive':'27', 'toggle':'44'}

def _get_dir(ext):
    if os.path.exists('/media/BONESTORAGE/uEnv.txt'):
        if not os.path.exists('/media/BONESTORAGE/' + ext):
            os.mkdir('/media/BONESTORAGE/' + ext)
        return '/media/BONESTORAGE/' + ext
    return os.path.realpath(__file__)[:-10] + '/' + ext

def capture_dir():
    return _get_dir('captures')

def archive_dir():
    return _get_dir('saved')

def audio_dir():
    return _get_dir('audio')

def is_capturing():
    return capturing

def toggle_capturing(set_value=None):
    global capturing
    capturing = set_value or not capturing

def get_unixtime():
    return int((datetime.datetime.utcnow() - start_date).total_seconds()*1000000)
