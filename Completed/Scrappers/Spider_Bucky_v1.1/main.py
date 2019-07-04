"""
    Usage: main.py [-h] [-wk] -f <file> | -u <homepage> [-q <file>] [-c <file>] [-p <project>] [-j <number>]
    Examples:
        main.py -p ../thenewboston -u https://thenewboston.com      # Specified project folder
        main.py -u https://thenewboston.com                         # Creates project folder thenewboston.com
        main.py -wku https://thenewboston.com -j20                  # 20 threads, wipe existing files, keep queue data
        main.py -f config.json -q best_queue.txt                    # Load config but specfify queue file (will override config)
        main.py -h                                                  # Displays usage
    Config file parameters:
    {
        "homepage": "url",
        "crawled_file": "filename",
        "queue_file": "filename",
        "project_folder": "folder name"
    }
"""
import gc
import getopt
import signal
import sys
import threading
import time
from queue import Queue

from Completed.Scrappers.Spider.config import *
from Completed.Scrappers.Spider.domain import *
from Completed.Scrappers.Spider.general import *
from Completed.Scrappers.Spider.spider import Spider

PROJECT_FOLDER = ''
HOMEPAGE = ''
DOMAIN_NAME = ''
QUEUE_FILE = ''
CRAWLED_FILE = ''
NUMBER_OF_THREADS = 8
queue = Queue()
keep = False

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
# Do the next job in the queue

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()
        crawls = Spider.crawl_page(threading.current_thread().name, url)
        # Change the table and column to reflect your database
        val = (crawls,)
        try:
            queue.task_done()
            gc.collect()
        except Exception as e:
            print(e)
            return None


# Each queued link is a new job
def create_jobs():
    for link in queue.file_to_set(QUEUE_FILE):
        queue.put(link)
        time.sleep(.500)
    queue.join()
    time.sleep(.500)
    crawl()

def crawl():
    queued_links = queue.file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_jobs()


def quit_gracefully(signal=None, frame=None):
    print("\nQuitting.")
    with queue.mutex:
        queue.queue.clear()
    if not keep:
        try:
            delete_file_contents(QUEUE_FILE)
        except:
            pass
    sys.exit(0)


# Enable process termination
def register_signal_handler():
    signal.signal(signal.SIGINT, quit_gracefully)
    signal.signal(signal.SIGTERM, quit_gracefully)


# Print short usage and exit
def usage():
    print('Usage: ' + sys.argv[
        0] + ' [-h] [-wk] -f <file> | -u <homepage> [-q <file>] [-c <file>] [-p <project>] [-j <number>]')
    sys.exit()


# Print detailed usage and exit
def detailed_usage():
    print('\nUsage: ' + sys.argv[
        0] + ' [-h] [-wk] -f <file> | -u <homepage> [-q <file>] [-c <file>] [-p <project>] [-j <number>]\n\n'
             'Options:\n\n'
             '-h\t\tDisplays this help\n'
             '-w\t\tWipe existing files (start fresh)\n'
             '-k\t\tKeep the queue file contents (continue crawling at a different time)\n'
             '-j <number>\tSpecify number of crawling threads (default 8)\n\n'
             '-u <url>\tThe homepage/starting point\n'
             '-p <project>\tSpecify a specific output folder\n'
             '-c <filename>\tSpecify a specific filename for the crawled file (default crawled.txt)\n'
             '-q <filename>\tSpecify a specific filename for the queue file (default queue.txt)\n'
             '-f <filename>\tLoad in a json config file\n\n'
             'Config file:\n'
             '{\n'
             '    "homepage": "url",\n'
             '    "crawled_file": "filename",\n'
             '    "queue_file": "filename",\n'
             '    "project_folder": "folder name"\n'
             '}\n')

    sys.exit()


# Set constants to values provided by command line
def options():
    global PROJECT_FOLDER
    global HOMEPAGE
    global NUMBER_OF_THREADS
    global DOMAIN_NAME
    global QUEUE_FILE
    global CRAWLED_FILE
    global keep
    wipe = False
    opts = None
    args = None
    crawled_filename = '/crawled.txt'
    queue_filename = '/queue.txt'
    config_file = '/config.txt'

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hwkf:q:c:p:u:j:')
    except getopt.GetoptError as e:
        print(str(e))
        usage()

    if len(args) != 0:
        usage()

    for opt, val in opts:
        if opt == '-h':
            detailed_usage()
        elif opt == '-f':
            config_file = val
        elif opt == '-w':
            wipe = True
        elif opt == '-p':
            PROJECT_FOLDER = val
        elif opt == '-u':
            HOMEPAGE = val
        elif opt == '-k':
            keep = True
        elif opt == '-q':
            if '/' not in val:
                queue_filename = '/' + val
            else:
                print('Value for option -q should not contain "/"')
                usage()
        elif opt == '-c':
            if '/' not in val:
                crawled_filename = '/' + val
            else:
                print('Value for option -c should not contain "/"')
                usage()
        elif opt == '-j':
            try:
                NUMBER_OF_THREADS = int(val)
            except:
                print('Value for option -j should be an integer.')
                usage()

    # config file given
    if config_file is not None:
        constants = None

        try:
            constants = load_config(config_file)
        except FileNotFoundError:
            print('File ' + config_file + ' does not exist.')
            usage()
        except Exception as e:
            print('There was a problem with your JSON: ' + str(e))
            usage()

        if HOMEPAGE == '':
            try:
                HOMEPAGE = constants['homepage']
            except:
                print('You didn\'t specify a homepage/starting point')
                usage()

        if PROJECT_FOLDER == '':
            try:
                PROJECT_FOLDER = constants['project_folder']
            except:
                PROJECT_FOLDER = ''

        if queue_filename == '/queue.txt':

            try:
                if '/' not in constants['queue_file']:
                    queue_filename = '/' + constants['queue_file']
                else:
                    print('Value for "queue_file" contained "/". Using ' + PROJECT_FOLDER + '/queue.txt')
            except:
                queue_filename = '/queue.txt'

        if crawled_filename == '/crawled.txt':

            try:
                if '/' not in constants['crawled_file']:
                    crawled_filename = '/' + constants['crawled_file']
                else:
                    print('Value for "crawled_file" contained "/". Using ' + PROJECT_FOLDER + '/crawled.txt')
            except:
                crawled_filename = '/crawled.txt'

    if HOMEPAGE == '':
        usage()

    if NUMBER_OF_THREADS <= 0:
        print('Value for option -j should be greater than 0.')
        usage()

    if PROJECT_FOLDER == '':
        PROJECT_FOLDER = get_domain_name(HOMEPAGE)

    DOMAIN_NAME = get_domain_name(HOMEPAGE)

    if DOMAIN_NAME == '':
        usage()

    QUEUE_FILE = PROJECT_FOLDER + queue_filename
    CRAWLED_FILE = PROJECT_FOLDER + crawled_filename
    try:
        if len(file_to_set(QUEUE_FILE)) == 0 and len(file_to_set(CRAWLED_FILE)) != 0:
            wipe = True
    except:
        pass
    finally:
        if wipe:
            try:
                delete_file_contents(QUEUE_FILE)
            except:
                pass

            try:
                delete_file_contents(CRAWLED_FILE)
            except:
                pass


def main():
    register_signal_handler()
    options()
    Spider(PROJECT_FOLDER, HOMEPAGE, DOMAIN_NAME, QUEUE_FILE, CRAWLED_FILE)
    create_workers()
    crawl()


if __name__ == '__main__':
    main()
