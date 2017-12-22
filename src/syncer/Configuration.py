import json
import io

from . import Logger
from . import Channel


class Configuration:

    @staticmethod
    def save_config(store):
        channels = store.raw_channels()
        config_file = io.open('conf.json', 'w', encoding='utf8')

        if len(channels) == 0 and config_file:
            Logger.log_handler.info.info('Channels empty, just erase channel config')
            return

        if not config_file:
            Logger.log_handler.info.error('Can not open config file')
            return

        data = []
        for channel in channels:
            data.append(channel.to_config())

        Logger.Logger.debug('JSON: {}'.format(data))
        config_file.write(json.dumps(data))

    @staticmethod
    def load_config(store):
        obj = Channel.Channel(store=store)
        try:
            buffer = io.open('conf.json', encoding='utf8')
            channels = json.loads(buffer.read())
            for ch in channels:
                store.append_channel(obj.from_config(ch, store))
        except Exception as e:
            Logger.Logger.debug('Error load config {}'.format(e))
