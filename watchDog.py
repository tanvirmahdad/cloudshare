import sys
import time
import logging

from dirsync import sync

import requests
import json

url='https://c5plwiyi3e.execute-api.us-east-1.amazonaws.com/Beta/fileUpload'
deleteURL='https://ymxir7gwg7.execute-api.us-east-1.amazonaws.com/beta/fileDelete'

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

sourceDir='/Users/tanvirmahdad/summer2020/cloudComputing/projects/'
destinationDir='/Users/tanvirmahdad/summer2020/cloudComputing/projectCloud'

def create_file(filename):
    raw_data = '{"Bucket": "tanvirmahdad1","key": "'+filename+'"}'
    response = requests.post(url, data=raw_data)

    body = json.loads(response.content)

    # print(body['presigned_url']['fields'])

    demoURL = body['presigned_url']['url']
    demoField = body['presigned_url']['fields']

    print(body)

    fullpath=sourceDir+filename
    print(fullpath)

    fin = open(fullpath, 'rb')
    files = {'file': fin}

    try:

        r = requests.post(demoURL, data=demoField, files=files)
        print(r.content)

    finally:
        fin.close()


def delete_file(filename):
    raw_data = '{"Bucket": "tanvirmahdad1","key": "' + filename + '"}'
    response = requests.post(deleteURL, data=raw_data)

    body = json.loads(response.content)
    #print(body)

    demoURL = body['presigned_url']
    #print(demoURL)

    r = requests.delete(demoURL)
    print(r.status_code)




class Event(FileSystemEventHandler):

    @staticmethod
    def on_any_event(changeEvent):

       # print(changeEvent.event_type)
        path=changeEvent.src_path
        filename=path.replace(sourceDir,'')
        #print(path)
        print(filename)
        if (changeEvent.is_directory):
            return None

        elif changeEvent.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % changeEvent.src_path)
            create_file(filename)
        elif changeEvent.event_type == 'deleted':
            # Event is modified, you can process it now
            print("Watchdog received deleted event - % s." % changeEvent.src_path)
            delete_file(filename)






def main():
    print("I am started")
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

if __name__ == "__main__":
    main()