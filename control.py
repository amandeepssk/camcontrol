import select
import subprocess as sub
import config
import pinIO

gpio_dir = config.gpio_dir

def capture(stamp=0):
    cams = _get_cams()
    for cam in cams:
        _capture(cam, stamp)
    
def _get_cams():
    output, errors = pinIO.subprocess('ls /dev/video*')
    if output and not errors:
        return output.strip().split('\n')
    return []

def _capture(cam, stamp):
    pinIO.subprocess(_capture_command(cam, stamp))
    
def _capture_command(cam, stamp):
    fout = config.capture_dir() + '/' + str(stamp) + '_' + cam[-1] + '.jpeg'
    return 'streamer -t 1 -r 30 -c %s -o %s -j 100 -s 960x720' % (cam, fout)

def _get_pcm():
    #should be smarter
    return 'plughw:CARD=U0x46d0x81b,DEV=0', '46d0x81b'

def _sound_command(secs, stamp):
    pcm, abbr = _get_pcm()
    fout = config.audio_dir() + '/' + str(stamp) + '_' + abbr + '.wav'
    return 'arecord -f cd -D ' + pcm + ' -d %d %s' % (secs, fout)

def sound(stamp=None, secs=0):
    stamp = stamp or config.get_unixtime()
    pinIO.subprocess(_sound_command(secs, stamp))
