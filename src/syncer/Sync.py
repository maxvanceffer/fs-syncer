import logging

from paramiko import SSHClient
from scp import SCPClient
from . import Logger

from datetime import datetime, timedelta
from functools import wraps


def throttle(seconds=0, minutes=0, hours=0):
    throttle_period = timedelta(seconds=seconds, minutes=minutes, hours=hours)

    def throttle_decorator(fn):
        time_of_last_call = datetime.min

        @wraps(fn)
        def wrapper(*args, **kwargs):
            now = datetime.now()
            if now - time_of_last_call > throttle_period:
                nonlocal time_of_last_call
                time_of_last_call = now
                return fn(*args, **kwargs)
        return wrapper
    return throttle_decorator


class Sync:
    client = None
    scp = None
    writting = False
    sync_queue = []
    channel = None

    def __init__(self, channel):
        Logger.Logger.debug('Init sync mon created [{}]'.format(channel.host))
        logging.getLogger('paramiko').setLevel(logging.DEBUG)

        host = str(channel.host)

        self.client = SSHClient()
        self.client.load_system_host_keys()

        try:
            self.client.connect(hostname=host, username=channel.user, key_filename=channel.key)
            self.scp = SCPClient(self.client.get_transport())
        except Exception as e:
            Logger.Logger.debug('Exception in scp syncer {}'.format(e))

        Logger.Logger.debug('Mon created')

    def sync(self, filename):
        Logger.Logger.debug('Call sync for file {}'.format(filename))

        if self.writting:
            self.sync_queue.append(filename)
            self.sync_queue = list(set(self.sync_queue))
            return

        self.writting = True
        self.sync_queue.append(filename)
        self.sync_queue = list(set(self.sync_queue))
        self.start()
        return True

    @throttle(3)
    def start(self):
        self.writting = True
        while len(self.sync_queue) > 0:
            filename = self.sync_queue.pop(0)
            Logger.Logger.debug('Sync {} to server {}'.format(filename, self.channel.host))
            try:
                self.scp.put(self.channel.watch_path + filename, filename.replace(self.channel.watch_path, self.channel.server_path))
            except Exception as e:
                Logger.Logger.debug('EXCEPTION: {}'.format(e))

            if len(self.sync_queue) == 1:
                self.sync_queue = []

        self.writting = False
        Logger.Logger.debug('Sync done {}')
