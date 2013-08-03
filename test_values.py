import os
import control
import pinIO

def test():
    print 'Starting Tests'
    cams = control._get_cams()
    print 'Cams: %s' % cams
    test_saturation(cams)
    print 'Tested Saturation'
    test_brightness(cams)
    print 'Tested Brightness'
    test_gain(cams)
    print 'Tested Gain'
    test_contrast(cams)
    print 'Tested Contrast'
    print 'Completed'

def test_saturation(cams):
    _test_ty_range(cams, 'saturation', 0, 250)
    
def test_brightness(cams):
    _test_ty_range(cams, 'brightness', 0, 250)

def test_contrast(cams):
    _test_ty_range(cams, 'contrast', 0, 250)

def test_gain(cams):
    _test_ty_range(cams, 'gain', 0, 250)

def _test_ty_range(cams, ty, minRange, maxRange):
    for cam in cams:
        default = get_default(cam, ty)
        for value in range(minRange, maxRange, 15):
            set_ctrl(cam, ty, value)
            take_pic(cam, ty, value)
        set_ctrl(cam, ty, default)
            
def get_default(cam, ty):
    output, errors = pinIO.subprocess('v4l2-ctl -d%s --get-ctrl %s' % (cam[-1], ty))
    return output.strip().split(' ')[1]

def take_pic(cam, ty, val):
    f = '%s_%s_%d' % (ty, cam[-1], val)
    pinIO.subprocess(capture_command(cam, f))
    
def set_ctrl(cam, ty, value):
    pinIO.subprocess('v4l2-ctl -d%s --set-ctrl %s=%s' % (cam[-1], ty, value))

def capture_command(cam, f):
    fout = '/home/ubuntu/camcontrol/tests/' + f + '.jpeg'
    return 'streamer -t 1 -r 30 -c %s -o %s -j 100 -s 960x720' % (cam, fout)
