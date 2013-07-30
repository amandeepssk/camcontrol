import select
import subprocess as sub
import config

gpio_dir = '/sys/class/gpio'
pins = {'archive':'23', 'toggle':'22'}

#green light on end is pin 27
#
#Other light is pin 44
def _subprocess(command, shell=True):


    p = sub.Popen(command, stdout=sub.PIPE, stderr=sub.PIPE, shell=shell)
    output, errors = p.communicate()
    return output, errors

def open_pins_for_input():
    for ty, pin in pins.iteritems():
        try:
            if pin:
                output, errors = _subprocess('echo %s > %s/export' % (pin, gpio_dir))
                print 'pin %s - output: %s, errors: %s' % (pin, output, errors)
                output, errors = _subprocess('echo in > %s/gpio%s/direction' % (gpio_dir, pin))
                print 'echo inning %s - output: %s, errors: %s' % (pin, output, errors)
        except Exception, e:
            _subprocess('echo %s > %sunexport' % (pin, gpio_dir))
            print e

def register_poll():
    #Did you run open_pins_for_input first?
    poll = select.poll()
    for pin in pins.values():
        if pin:
            file_dir = gpio_dir + '/gpio%s/value' % pin
            print file_dir
            poll.register(open(file_dir, 'r'), select.POLLIN)
    return poll

def start_polling():
    poll = register_poll()
    count = 0
    while 1:
        count += 1
        events = poll.poll(30000) #Look for half a second, return, on twenty of these, take pictures
        print events
        if events:
            break
        if len(events) == 0:
            #no events
            print 'hey, there was no events this half second'
        else:
            #yes events
            #check what event
            print 'hey event: %s' % events
        # if count == 20:
        #     #take_picture
        #     count = 0
        #     pass
