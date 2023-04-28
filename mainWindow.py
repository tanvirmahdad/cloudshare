from Tkinter import *
#from Tkinter import ttk
from PIL import ImageTk, Image

import ttk
import os


import requests
import json
import subprocess, os, platform
import watchDog
import thread
import threading

import sys
import time
import logging

from dirsync import sync

import requests
import Queue
import tkMessageBox




from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

url='https://m4couxpmz6.execute-api.us-east-2.amazonaws.com/default/fileUpload'
deleteURL='https://iq4mti3q80.execute-api.us-east-2.amazonaws.com/default/fileDelete'

filepath='/Users/tanvirmahdad/summer2020/cloudComputing/projects/'
sourceDir='/Users/tanvirmahdad/summer2020/cloudComputing/projects/'
destinationDir='/Users/tanvirmahdad/summer2020/cloudComputing/projectCloud'


#WatchDog Requests:




class cloudShare:
    def __init__(self, root):

        self.root = root
        self.root.geometry('455x325+600+200')
        self.root.title('CloudShare File Sharing')

        '''Logo and Title'''

        self.photo = ImageTk.PhotoImage(Image.open("cloudshare.gif"))
        self.label = Label(image=self.photo)
        self.label.photo = self.photo  # Just creating a reference
        self.label.grid(row=0, column=0)

        self.label1 = Label(font=('arial', 15, 'bold'), text='CloudShare File Sharing', fg='dark blue')
        self.label1.grid(row=8, column=0)

        #Frame
        frame = LabelFrame(self.root, text='CloudShare:')
        frame.grid(row=0, column=1)

        #Buttons
        ttk.Button(frame, text='Start Syncing Folder', command=self.start).grid(row=6, column=2)
        ttk.Button(frame, text='Show CloudShare Folder', command=self.add).grid(row=7, column=2)
        ttk.Button(frame, text='Exit', command=self.ex).grid(row=8, column=2)

        '''Message Display'''
        self.message = Label(text='', fg='Red')
        self.message.grid(row=8, column=1)
        #main()

    def add(self):
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(filepath)
        else:  # linux variants
            subprocess.call(('xdg-open', filepath))


    def start(self):
        self.queue = Queue.Queue()
        ThreadedTask(self.queue).start()
        self.root.after(100, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            # Show result of the task if needed
            #self.prog_bar.stop()
        except Queue.Empty:
            self.root.after(100, self.process_queue)

    def ex(self):
        exit = tkMessageBox.askquestion('Exit Application','Are you sure you want to close this application?')
        if exit == 'yes':
            self.root.destroy()


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        main()
        self.queue.put("Task finished")

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




def create_file(filename):
    raw_data = '{"Bucket": "tanvirmahdad2","key": "'+filename+'"}'
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
    raw_data = '{"Bucket": "tanvirmahdad2","key": "' + filename + '"}'
    response = requests.post(deleteURL, data=raw_data)

    body = json.loads(response.content)
    #print(body)

    demoURL = body['presigned_url']
    #print(demoURL)

    r = requests.delete(demoURL)
    print(r.status_code)






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


if __name__ == '__main__':
    print('hello')
    root = Tk()
    # root.geometry('585x515+500+200')
    application = cloudShare(root)
    root.mainloop()