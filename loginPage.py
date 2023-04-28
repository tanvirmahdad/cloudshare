
#import sys
#raise RuntimeError(sys.path)

from Tkinter import *
#from Tkinter import ttk
import ttk
import thread
import threading
import requests
import json
from mainWindow import *
from subprocess import call
from subprocess import Popen
import watchDog



loginURL='https://fgr67xyl7d.execute-api.us-east-2.amazonaws.com/default/login_auth'


class login:


    def __init__(self,root):

        self.root = root
        self.root.title('CloudShare')

        self.photo = ImageTk.PhotoImage(Image.open("cloudshare.gif"))
        self.label = Label(image=self.photo)
        self.label.photo = self.photo  # Just creating a reference
        self.label.grid(row=0, column=0)

        self.label1 = Label(font=('arial', 15, 'bold'), text='CloudShare File Sharing', fg='dark blue')
        self.label1.grid(row=4, column=0)

        # Frame
        frame = LabelFrame(self.root, text='Log in:')
        frame.grid(row=0, column=1)
        #ttk.Button(frame, text='Start Syncing Folder').grid(row=6, column=2)

        Label(frame, text = ' Username ',font='Times 15').grid(row=1,column=6)
        self.username = Entry(frame)
        self.username.grid(row=1,column=7,columnspan=10)

        Label(frame, text = ' Password ',font='Times 15').grid(row=2,column=6)
        self.password = Entry(frame,show='*')
        self.password.grid(row=2,column=7,columnspan=10)

        ttk.Button(frame,text='LOGIN',command=self.login_user).grid(row=3,column=10)


    def login_user(self):

        raw_data = '{"username": "' + str(self.username.get()) + '","password": "' + str(self.password.get()) + '"}'
        #print(raw_data)
        response = requests.post(loginURL, data=raw_data)
        body = json.loads(response.content)

        message=body['message']
        print(body)

        if(message=='success'):
            #print("Yahoo")
            # Destroy the current window
            #watchDog.main()



            root.destroy()

            newroot = Tk()
            application = cloudShare(newroot)
            newroot.mainloop()

        else:
            self.message = Label(text = message,fg = 'Red')
            self.message.grid(row=6,column=1)



        #else:
            #self.message = Label(text = 'Username or Password incorrect. Try again!',fg = 'Red')
            #self.message.grid(row=6,column=2)


if __name__ == '__main__':

    root = Tk()
    root.geometry('655x325+600+200')
    application = login(root)

    root.mainloop()

