from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtCore import QObject, QDir
from . import Logger


class Handler(FileSystemEventHandler):
    store = None

    def on_any_event(self, event):

        if event.is_directory:
            return None

        Logger.Logger.debug('Watcher event received {}'.format(event.event_type))

        try:
            for channel in self.store.raw_channels():

                if hasattr(event, 'dest_path') and channel.is_accept_file(filename=event.dest_path) and channel.has_event(event=event.event_type):
                    Logger.Logger.debug('Channel accepted sync')
                    channel.sync(event.dest_path)

                elif hasattr(event, 'src_path') and channel.is_accept_file(filename=event.src_path) and channel.has_event(event=event.event_type):
                    Logger.Logger.debug('Channel accepted sync')
                    channel.sync(event.src_path)
                else:
                    Logger.Logger.debug('dddddd')

        except Exception as e:
            Logger.Logger.debug('Exception happen during channel sync {}'.format(e))


class Watcher(QObject):
    path = None
    running = False

    def __init__(self, store, path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.observer = Observer()
        self.path = path
        self.store = store

    def run(self):
        watch_dir = QDir(self.path)
        if self.path and watch_dir.exists():
            self.running = True
            event_handler = Handler()
            event_handler.store = self.store
            self.observer.schedule(event_handler, self.path, recursive=True)
            self.observer.start()
        else:
            Logger.Logger().debug('Error no path set, or path is invalid {}'.format(self.path))

    def stop(self):
        self.running = False
        self.observer.stop()
