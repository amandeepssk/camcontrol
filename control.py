import subprocess as sub
from time import sleep
import config

def _subprocess(command, shell=True):
    p = sub.Popen(command, stdout=sub.PIPE, stderr=sub.PIPE, shell=shell)
    output, errors = p.communicate()
    return output, errors

def stop():
    #ps aux | grep python --> get PID, kill it.
    print 'Stopping all cameras'
    config.stop_capturing()
    print 'Stopped all cameras'

def start(secs):
    #secs is how long between captures
    if not config.is_capturing():
        print 'Starting all cameras with %d time between captures' % secs
        config.start_capturing()
        _continuously_capture(secs) #use subprocess call so that it's not taking command line
    else:
        print 'Capturing already turned on'

def _continuously_capture(secs):
    cams = _get_cams()
    while config.is_capturing():
        for cam in cams:
            _capture(cam, config.get_unixtime())
        sleep(secs)

def _get_cams():
    output, errors = _subprocess('ls /dev/video*')
    if output and not errors:
        return output.strip().split('\n')
    return None

def _capture(cam, time):
    print 'Capturing from cam %s' % cam
    command = _capture_command(cam, time)
    output, errors = _subprocess(command)
    
def _capture_command(cam, time):
    pos = cam[-1]
    fout = config.capture_dir() + '/' + str(time) + '_' + pos + '.jpeg'
    return 'streamer -t 1 -r 30 -c %s -o %s -j 100 -s 960x720' % (cam, fout)

