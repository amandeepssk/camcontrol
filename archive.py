import os
import config
import tarfile

def save(secs=600):
    #secs is how far back to save
    secs = secs * 1000000
    current_time = config.get_unixtime()
    min_time = last_archive_time()
    if min_time < current_time - secs:
        min_time = current_time - secs
    _compress_files(current_time, _retrieve_save_files(min_time))

def _compress_files(now, save_files):
    if len(save_files) > 0:
        with tarfile.open(config.archive_dir() + '/' + str(now) + '.tar.gz', "w:gz") as tar:
            for f in save_files:
                tar.add(f, arcname=f.split('/')[-1])
        for f in save_files:
            os.remove(f)

def _retrieve_save_files(previous):
    save_files = []
    capture_directory = config.capture_dir()
    for f in os.listdir(capture_directory):
        try:
            f_time = int(f.split('_')[0])
            if f_time > previous:
                save_files.append(capture_directory + '/' + f)
        except Exception, e:
            print e
    return save_files
    
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
    directory = config.capture_dir()
    current_time = config.get_unixtime()
    secs = secs * 1000000
    for f in os.listdir(directory):
        try:
            f_time = int(f.split('_')[0])
            if current_time - f_time > secs:
                os.remove(directory + '/' + f)
        except Exception, e:
            print e
