from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtQml import QQmlListProperty

from . import Channel
from . import Logger
from . import Configuration


class Store(QObject):
    """ Store for the channels """

    channelsChanged = pyqtSignal()
    countChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._channels = []

    @pyqtProperty(int, notify=countChanged)
    def count(self):
        return len(self._channels)

    @pyqtProperty(QQmlListProperty, notify=channelsChanged)
    def channels(self):
        return QQmlListProperty(Channel.Channel, self, self._channels)

    def raw_channels(self):
        return self._channels

    @channels.setter
    def channels(self, channels):
        if channels != self._channels:
            self._channels = channels
            self.channelsChanged.emit()

    @pyqtSlot(QVariant)
    def create_channel(self, options):

        Logger.log_handler.info('Create channel {}'.format(options.toVariant()))
        opt = options.toVariant()
        opt['store'] = self
        self.append_channel(
            Channel.Channel(**opt)
        )

        Configuration.Configuration().save_config(self)

    def append_channel(self, channel):
        self._channels.append(channel)
        self.channelsChanged.emit()
        self.countChanged.emit()

    @pyqtSlot(str)
    def start_channel(self, index):
        channel = self._channels[index]
        channel.start()

    @pyqtSlot()
    def start_all(self):
        for channel in self._channels:
            channel.start()

    @pyqtSlot()
    def stop_all(self):
        for channel in self._channels:
            channel.stop()

    @pyqtSlot(Channel.Channel)
    def new_channel(self):
        try:
            channel = Channel.Channel(store=self)
            channel.temp = True
            return channel
        except Exception as e:
            Logger.Logger.debug('Can not create new channel because {}'.format(e))
