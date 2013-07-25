import os
import datetime

capturing = False
start_date = datetime.datetime(year=1970,month=1,day=1)

def mkdir(ext):
    import subprocess as sub
    dir = _get_dir(ext)
    p = sub.Popen('mkdir -p %s' % dir, stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()
    print 'mkdir: %s, %s' % (output, errors)

def _get_dir(ext):
    return os.getcwd() + '/' + ext

def capture_dir():
    return _get_dir('captures')

def archive_dir():
    return _get_dir('archived')

def audio_dir():
    return _get_dir('audio')

def is_capturing():
    return capturing

def start_capturing():
    global capturing
    capturing = True

def stop_capturing():
    global capturing
    capturing = False

def get_unixtime():
    return int((datetime.datetime.utcnow() - start_date).total_seconds()*1000000)

def cwd():
    return os.getcwd()

def capture_dir():
    return cwd() + '/captures'

def archive_dir():
    return cwd() + '/archived'
