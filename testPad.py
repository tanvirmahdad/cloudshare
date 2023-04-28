#import sys
#raise RuntimeError(sys.path)

from Tkinter import *
#from Tkinter import ttk
import tkFileDialog
import ttk
import subprocess, os, platform

#root = Tk()
#root.withdraw()
#root.focus_force()

#folder = tkFileDialog.askdirectory(initialdir="//Users/tanvirmahdad/summer2020/cloudComputing/projects/")

filepath='/Users/tanvirmahdad/summer2020/cloudComputing/projects/'

if platform.system() == 'Darwin':       # macOS
    subprocess.call(('open', filepath))
elif platform.system() == 'Windows':    # Windows
    os.startfile(filepath)
else:                                   # linux variants
    subprocess.call(('xdg-open', filepath))