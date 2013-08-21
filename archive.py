import os
import config
import tarfile

def save(secs=600):
    #secs is how far back to save
    secs = secs * 1000000
    current_time = config.get_unixtime()
    print 'Archiving at time %s' % current_time
    min_time = last_archive_time()
    if min_time < current_time - secs:
        min_time = current_time - secs
    _compress_files(current_time, _retrieve_save_files(min_time))

def next_gz_annotate(directory):
    gzs = [int(name.split('.tar.gz')[0].split('/')[-1]) for name in os.listdir(directory)]
    sgzs = sorted(gzs, reverse=True)
    if len(sgzs) == 0:
        return 1
    return sgzs[0] + 1
    
def _compress_all_files(directory):
    print 'compress all files'
    if len(os.listdir(directory)) == 0:
        return
    with tarfile.open(config.archive_dir() + '/' + str(next_gz_annotate(config.archive_dir())) + '.tar.gz', "w:gz") as tar:
        for f in os.listdir(directory):
            tar.add(directory + '/' + f, arcname=f.split('/')[-1])
    for f in os.listdir(directory):
        os.remove(directory + '/' + f)

def _compress_files(now, save_files):
    if len(save_files) > 0:
        with tarfile.open(config.archive_dir() + '/' + str(now) + '.tar.gz', "w:gz") as tar:
            for f in save_files:
                tar.add(f, arcname=f.split('/')[-1])
        for f in save_files:
            os.remove(f)

def _retrieve_save_files(previous):
    save_files = []
    save_files = _add_to_save_files(config.capture_dir(), save_files, previous)
    save_files = _add_to_save_files(config.audio_dir(), save_files, previous)
    return save_files

def _add_to_save_files(d, files, previous):
    for f in os.listdir(d):
        try:
            f_time = int(f.split('_')[0])
            if f_time > previous:
                files.append(d + '/' + f)
        except Exception, e:
            print e
    return files
    
def last_archive_time():
    directory = config.archive_dir()
    ret = 0
    for f in os.listdir(directory):
        try:
            f_time = int(f.split('.')[0])
            if f_time > ret:
                ret = f_time
        except Exception, e:
            print e
    return ret

def roll(secs):
    #secs is how far back to delete, i.e. 3600 would be deleting everything > 1 hr before
    current_time = config.get_unixtime()
    print 'Rolling at time %s' % current_time
    secs = secs * 1000000
    _roll_dir(config.capture_dir(), secs, current_time)
    _roll_dir(config.audio_dir(), secs, current_time)

def _roll_dir(d, secs, current_time):
    for f in os.listdir(d):
        try:
            f_time = int(f.split('_')[0])
            if current_time - f_time > secs:
                os.remove(d + '/' + f)
        except Exception, e:
            print e
    
    
    
