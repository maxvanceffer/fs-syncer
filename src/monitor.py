import logging
import os
import os.path
import re
import time

from paramiko import SSHClient
from scp import SCPClient
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.throttle import throttle

cwd = os.getcwd() + '/'

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)


# '54.161.73.219', '52.87.94.227'
class ServerConfig:
    host = None
    user = None
    key = None

    def __init__(self, host, user, key):
        self.host = host
        self.user = user
        self.key = key


_MONITORS = []
_WATCHING_DIR = b'../ami-apid/'
_SERVER_DIR = '/opt/ami-apid/'
_SERVER_USER = 'ec2-user'
_PEM_KEY = '/home/dev06/.ssh/ppapucciu_sebastian.pem'
_ACCEPT = ['.*\.(py)$']
_DISMISS_DIRS = ['schema', 'gui', 'build', 'conf', 'deploy', 'redhat', 'sessions']
_SERVER = [
    ServerConfig(host='34.204.8.73', user=_SERVER_USER, key=_PEM_KEY),
    # ServerConfig(host='34.227.162.141', user=_SERVER_USER, key=_PEM_KEY)
]




def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


class Watcher:
    DIRECTORY_TO_WATCH = _WATCHING_DIR

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Exit"

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):

        if event.is_directory:
            return None

        # elif event.event_type == 'created':
        #     # Take any action here when a file is first created.
        #     print "Received created event - %s." % event.src_path
        #
        # elif event.event_type == 'modified':
        #     # Taken any action here when a file is modified.
        #     print "Received modified event - %s." % event.src_path

        elif event.event_type == 'moved':
            combined = "(" + ")|(".join(_ACCEPT) + ")"
            filename = None
            if re.match(combined, event.dest_path):
                filename = event.dest_path

            elif re.match(combined, event.src_path):
                filename = event.src_path

            if filename:
                _LOGGER.info('Detected file %s - %s - %s' % (filename, event.dest_path, event.src_path))
                for mon in _MONITORS:
                    mon.sync(filename)

if __name__ == '__main__':
    _configure_logging()
    for srv in _SERVER:
        m = Monitor(srv)
        _MONITORS.append(m)
        # m.full_sync()

    w = Watcher()
    w.run()
