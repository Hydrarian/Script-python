import pandas as pd
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path


class Watcher:
    DIRECTORY_TO_WATCH = "C:/Users/Mh2/Desktop/convertitoreCsv-Xlsx"

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
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            filepath_in = event.src_path                                    #path sorgente
            filepath_out=str(Path(event.src_path).parents[1])+'/'+Path(filepath_in).stem+'.xlsx'             #path destinazione (cartella superiore)
            pd.read_csv(filepath_in, delimiter=",").to_excel(filepath_out)
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)


if __name__ == '__main__':
    w = Watcher()
    w.run()

