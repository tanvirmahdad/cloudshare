import sys
import time
import logging

from dirsync import sync


from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

sourceDir='/Users/tanvirmahdad/summer2020/cloudComputing/projects'
destinationDir='/Users/tanvirmahdad/summer2020/cloudComputing/projectCloud'

class Event(LoggingEventHandler):
    #def dispatch(self, event):
       # print("Foobar")


    def on_modified(self, event):
        #sync(sourceDir, destinationDir, "sync", purge = True)
        print("modified")




if __name__ == "__main__":
    path = sourceDir
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()