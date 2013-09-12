import sys
import argparse
import archive
import pinIO
import config
import control

# main presents cl utility:
# - stop: kills any running cameras
# - archive: cleverly compresses from past time X
# - start: finds cameras and starts taking pictures every 10 seconds
# - info: retrieves camera device info

def stop():
    pass

def start_poll(epoll, f_archive, f_toggle, psecs, rsecs):
    config.toggle_capturing(False)
    count = 0
    accelerometer_logger = open('/home/ubuntu/camcontrol/log_accel.txt', 'w')
    helper = None
    with f_archive, f_toggle:
        while True:
            if not helper:
                try:
                    helper = pinIO.open_ain_helper()                
                except Exception, e:
                    print e
            if helper and config.is_capturing():
                vals = pinIO.accelerometer_values(helper)
                accelerometer_logger.write('volts - x: %f, y: %f, z: %f\n' % (vals.get('x'), vals.get('y'), vals.get('z')))
                accelerometer_logger.write('gs - x: %f, y: %f, z: %f\n' % (pinIO.g(vals.get('x')), pinIO.g(vals.get('y')), pinIO.g(vals.get('z'))))
                accelerometer_logger.write('\n\n')
            count += 1
            events = epoll.poll(config.poll_time) #every 500 millisec
            for fileno, event in events:
                if fileno == f_archive.fileno():
                    pinIO.light(config.light_pins['archive'], True)
                    archive.save(config.archive_time)
                    pinIO.light(config.light_pins['archive'], False)
                if fileno == f_toggle.fileno():
                    config.toggle_capturing()
                    if config.is_capturing():
                        print 'Started Capturing'
                    else:
                        print 'Stopped Capturing'
                    pinIO.light(config.light_pins['toggle'], config.is_capturing())
            if count % psecs == 0 and config.is_capturing():
                control.capture(config.get_unixtime())
            if count > rsecs/2 and config.is_capturing():
                archive.roll(rsecs)
                count = 0
            if config.is_capturing():
                #hack: stop and record audio 
                control.sound(config.get_unixtime(), 1)


def start_time():
    pinIO.subprocess('echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device')
    pinIO.subprocess('hwclock -s -f /dev/rtc1')
    pinIO.subprocess('hwclock -w')
    
def start(psecs, rsecs=300):
    # try:
    #     output, errors = pinIO.subprocess('ls /dev/')
    #     if not 'rtc1' in output.split('\n'):
    #         start_time()
    # except Exception, e:
    #     print e
    #     sys.exit("Time not enabled")
    try:
        pinIO.open_pins()
    except Exception, e:
        print e
        pinIO.close_pins()
        sys.exit("Can't open the pins. Exiting")
    try:
        epoll, f_archive, f_toggle = pinIO.get_poll()
        start_poll(epoll, f_archive, f_toggle, psecs, rsecs)
    except Exception, e:
        print e
        pinIO.close_pins()
        sys.exit("Starting poll failed. Exiting")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control Cameras using Streamer',
                                     usage='Precedence: Stop, Start, Archive, Roll')
    parser.add_argument('--stop', help='terminate any running cameras', action="store_true")
    parser.add_argument('--start', help='finds and starts all cameras', action="store_true")
    parser.add_argument('--psecs', type=int, default=5, choices=[5,10,30,60], help='time between taking pictures')
    parser.add_argument('--archive', type=int, choices=[30, 600, 3600], help='compresses recent data')
    parser.add_argument('--roll', type=int, help='deletes older uncompressed data')

    args = parser.parse_args()
    if args.stop:
        stop()
    elif args.start:
        start(args.psecs)
    elif args.archive:
        archive.save(args.archive)
    elif args.roll:
        archive.roll(args.roll)
    else:
        print 'Doing Nothing'


