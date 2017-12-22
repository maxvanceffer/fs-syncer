import re

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant
from . import Watcher
from . import Logger
from . import Sync


class Channel(QObject):
    """ Channel for syncing """

    hostChanged = pyqtSignal()
    nameChanged = pyqtSignal()
    acceptsChanged = pyqtSignal()
    runningChanged = pyqtSignal()
    watchPathChanged = pyqtSignal()
    keyChanged = pyqtSignal()
    eventsChanged = pyqtSignal()
    serverPathChanged = pyqtSignal()
    status = pyqtSignal()
    userChanged = pyqtSignal()

    store = None
    watcher = None
    syncer = None

    def __init__(self,
                 store, hostname='', name='', accepts=None,
                 watch_path='', server_path='', key='', events=None, user='',
                 *args, **kwargs):

        super().__init__(*args, **kwargs)

        Logger.Logger.debug('Create channel from config {}'.format(kwargs))

        if events is None:
            events = []

        if accepts is None:
            accepts = []

        self._hostname = hostname
        self._name = name
        self._accepts = accepts
        self._events = events
        self._server_path = server_path
        self._key = key
        self._user = user
        self._watch_path = watch_path
        self.store = store

    def get_watcher(self):
        if not self.watcher:
            self.watcher = Watcher.Watcher(path=self._watch_path, store=self.store)

        return self.watcher

    def get_syncer(self):
        if not self.syncer:
            self.syncer = Sync.Sync(self)

        return self.syncer

    def serialize(self):
        config = {}

        for key, value in vars(self).items():
            if key.startswith('_'):
                config[key] = value

        Logger.Logger().debug('Ser {}'.format(config))
        return config

    @pyqtProperty('QString', notify=hostChanged)
    def host(self):
        return self._hostname

    @pyqtProperty('QString', notify=userChanged)
    def user(self):
        return self._user

    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self._name

    @pyqtProperty('QStringList', notify=acceptsChanged)
    def accepts(self):
        return self._accepts

    @pyqtProperty('QString', notify=watchPathChanged)
    def watch_path(self):
        return self.get_watcher().path

    @pyqtProperty('QString', notify=serverPathChanged)
    def server_path(self):
        return self._server_path

    @pyqtProperty('bool', notify=runningChanged)
    def running(self):
        return self.get_watcher().running

    @pyqtProperty('QStringList', notify=runningChanged)
    def events(self):
        return self._events

    @pyqtProperty('QString', notify=keyChanged)
    def key(self):
        return self._key

    @name.setter
    def name(self, name):
        if name != self._name:
            self._name = name
            self.nameChanged.emit()

    @accepts.setter
    def accepts(self, patterns):
        if patterns != self._accepts:
            self._accepts = patterns

    @host.setter
    def host(self, name):
        if not hasattr(self, '_hostname'):
            self._hostname = name
            self.hostChanged.emit()

        if name != self._hostname:
            self._hostname = name
            self.hostChanged.emit()

    @user.setter
    def user(self, user):
        if user != self._user:
            self._user = user
            self.userChanged.emit()

    @key.setter
    def key(self, key):
        if key != self._key:
            self._key = key
            self.keyChanged.emit()

    @events.setter
    def events(self, events):
        if events != self._events:
            self._events = events
            self.eventsChanged.emit()

    def is_accept_file(self, filename):
        combined = "(" + ")|(".join(self._accepts) + ")"
        Logger.Logger().debug('Check if file {} is eq {}'.format(filename, combined))
        return re.match(combined, filename)

    @pyqtSlot()
    def start(self):
        Logger.Logger().debug('Channel {} start'.format(self._hostname))
        if self.get_watcher().running:
            return

        self.get_watcher().run()
        self.runningChanged.emit()

    @pyqtSlot()
    def stop(self):
        Logger.Logger().debug('Channel {} stop'.format(self._hostname))
        if not self.get_watcher().running:
            return

        self.get_watcher().stop()
        self.runningChanged.emit()

    @pyqtSlot()
    def has_event(self, event):
        Logger.Logger.debug('Check if event {} is handled by channels events {}'.format(event, ','.join(self._events)))
        return self._events.count(event) > 0

    def sync(self, filename):
        Logger.Logger().debug('Sync file filename {}'.format(filename))
        self.get_syncer().sync(filename=filename)
        pass

    def to_config(self):
        conf = dict((key, value) for key, value in vars(self).items() if key.startswith('_'))
        return conf

    @staticmethod
    def from_config(properties, store):
        clean_dict = {key[1:]: item for key, item in properties.items()}
        clean_dict['store'] = store
        return Channel(**clean_dict)
