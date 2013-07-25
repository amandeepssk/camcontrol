import subprocess as sub
from time import sleep
import config

def _subprocess(command, shell=True):
    p = sub.Popen(command, stdout=sub.PIPE, stderr=sub.PIPE, shell=shell)
    output, errors = p.communicate()
    return output, errors

def stop():
    print 'Stopping all cameras'
    config.stop_capturing()
    print 'Stopped all cameras'

def start(secs):
    #secs is how long between captures
    print config.is_capturing()
    if not config.is_capturing():
        print 'Starting all cameras with %d time between captures' % secs
        config.start_capturing()
        print config.is_capturing()
        _continuously_capture(secs) #use subprocess call so that it's not taking command line
    else:
        print 'Capturing already turned on'

def _continuously_capture(secs):
    cams = _get_cams()
    print config.is_capturing()
    while config.is_capturing():
        for cam in cams:
            if cam[-1] != '1': 
                _capture(cam, config.get_unixtime())
        sleep(secs)

def _get_cams():
    output, errors = _subprocess('ls /dev/video*')
    if output and not errors:
        return output.strip().split('\n')
    return None

def _capture(cam, time):
    command = _capture_command(cam, time)
    output, errors = _subprocess(command)
    
def _capture_command(cam, time):
    pos = cam[-1]
    fout = config.capture_dir() + '/' + str(time) + '_' + pos + '.jpeg'
    return 'streamer -t 1 -r 30 -c %s -o %s -s 960x720' % (cam, fout)

