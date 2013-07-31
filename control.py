import select
import subprocess as sub
import config
import pinIO

gpio_dir = config.gpio_dir

def capture():
    now = config.get_unixtime()
    cams = _get_cams()
    for cam in cams:
        _capture(cam, now)
    
def _get_cams():
    output, errors = pinIO.subprocess('ls /dev/video*')
    if output and not errors:
        return output.strip().split('\n')
    return []

def _capture(cam, time):
    print 'Capturing from cam %s at time %d' % (cam, time)
    pinIO.subprocess(_capture_command(cam, time))
    
def _capture_command(cam, time):
    pos = cam[-1]
    fout = config.capture_dir() + '/' + str(time) + '_' + pos + '.jpeg'
    return 'streamer -t 1 -r 30 -c %s -o %s -j 100 -s 960x720' % (cam, fout)

