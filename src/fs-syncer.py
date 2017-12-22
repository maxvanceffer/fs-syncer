from sys import argv
import syncer

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

_STORE = None
_CONFIG = None


def main():
    app = QGuiApplication(argv)

    qmlRegisterType(syncer.Channel.Channel, 'Example', 1, 0, 'Channel')
    qmlRegisterType(syncer.Store.Store, 'Example', 1, 0, 'Store')
    qmlRegisterType(syncer.Watcher.Watcher, 'Example', 1, 0, 'Watcher')

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('store', _STORE)
    engine.load('qml/main.qml')

    exit(app.exec_())


if __name__ == '__main__':
    syncer.Logger.configure_logging()
    _STORE = syncer.Store.Store()

    _CONFIG = syncer.Configuration.Configuration()
    _CONFIG.load_config(_STORE)

    main()
