import select
import subprocess as sub
import config

def subprocess(command, shell=True):
    p = sub.Popen(command, stderr=sub.STDOUT, stdout=sub.PIPE, shell=shell)
    output, errors = p.communicate()
    return output, errors

def open_pins():
    _open_pins(config.switch_pins, 'in', rising=True)
    _open_pins(config.light_pins, 'out')
    return True

def _open_pins(pins, direction, rising=False):
    gpio_dir = config.gpio_dir
    for ty, pin in pins.iteritems():
        subprocess('echo %s > %s/export' % (pin, gpio_dir))
        subprocess('echo %s > %s/gpio%s/direction' % (direction, gpio_dir, pin))
        if rising:
            subprocess('echo rising > %s/gpio%s/edge' % (gpio_dir, pin))

def close_pins():
    _close_pins(config.switch_pins)
    _close_pins(config.light_pins)
    return True

def _close_pins(pins):
    for ty, pin in pins.iteritems():
        subprocess('echo 0 > %s/gpio%s/value' % (config.gpio_dir, pin))
        subprocess('echo %s > %s/unexport' % (pin, config.gpio_dir))

def get_poll():
    archive = open(config.gpio_dir + '/gpio%s/value' % config.switch_pins['archive'], 'r')
    toggle = open(config.gpio_dir + '/gpio%s/value' % config.switch_pins['toggle'], 'r')
    epoll = select.epoll()
    epoll.register(archive, select.EPOLLIN | select.EPOLLET)
    epoll.register(toggle,  select.EPOLLIN | select.EPOLLET)
    return epoll, archive, toggle

def light(pin, on):
    value = '1' if on else '0'
    subprocess('echo %s > %s/gpio%s/value' % (value, config.gpio_dir, pin))
        
    
