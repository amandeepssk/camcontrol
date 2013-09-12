import pinIO
import config
import math

zero_ref = {'x':505, 'y':395, 'z':512} #zero g ADC value ... everything is weeeird. z seems fucking right though, 
unit_ref = {'x':102, 'y':80,  'z':102} #one  g ADC jump

def accelerometer_values(helper=None, convert=False):
    if not helper:
        helper = pinIO.open_ain_helper()
    ret = {}
    for coord, pin in config.accelerometer_pins.iteritems():
        output, errors = pinIO.subprocess('cat %s/%s' % (helper, pin))
        mV = float(output.strip())
        if convert:
            ret[coord] = g(mV, coord)
        else:
            ret[coord] = mV
    return ret

def g(mV, direction):
    # return (mV - zero_ref['z'])*1.0 / unit_ref[direction]
    return (mV - zero_ref[direction])*1.0/unit_ref[direction]

def poll_acc(secs=2, helper=None):
    import time
    #secs is time between polling
    #convert is from voltage to Gs using (value - zeroOffset)/convFactor
    while 1:
        vals = accelerometer_values(helper)
        print 'mV - x: %d, y: %d, z: %d' % (vals['x'], vals['y'], vals['z'])
        print 'gs    - x: %f, y: %f, z: %f' % (g(vals['x'], 'x'), g(vals['y'], 'y'), g(vals['z'], 'z'))
        print 'Pausing'
        time.sleep(2)

def acc_vector_mag(helper, vals=None):
    vals = vals or accelerometer_values(helper, True)
    Rx = vals.get('x', 0)
    Ry = vals.get('y', 0)
    Rz = vals.get('z', 0)
    return math.sqrt(Rx*Rx + Ry*Ry + Rz*Rz)

def acc_vector_angle(helper, direction, vals=None, mag=None):
    vals = vals or accelerometer_values(helper, True)
    mag = mag or acc_vector_mag(helper, vals)
    Rdir = vals.get(direction, 0)
    return math.acos(Rdir * 1.0 / mag)


    
