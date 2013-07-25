import argparse
import control
import archive

# main presents cl utility:
# - stop: kills any running cameras
# - archive: cleverly compresses from past time X
# - start: finds cameras and starts taking pictures every 10 seconds
# - info: retrieves camera device info

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control Cameras using Streamer',
                                     usage='Precedence: Stop, Start, Archive, Roll')
    parser.add_argument('--stop', help='terminate any running cameras', action="store_true")
    parser.add_argument('--start', help='finds and starts all cameras', action="store_true")
    parser.add_argument('--psecs', type=int, default=10, choices=[10,20,30,60], help='time between taking pictures')
    parser.add_argument('--archive', type=int, choices=[30, 600, 3600], help='compresses recent data')
    parser.add_argument('--roll', type=int, help='deletes older uncompressed data')

    args = parser.parse_args()
    if args.stop:
        control.stop()
    elif args.start:
        control.start(args.psecs)
    elif args.archive:
        archive.save(args.archive)
    elif args.roll:
        archive.roll(args.roll)
    else:
        print 'Doing Nothing'


