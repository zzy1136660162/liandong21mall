import subprocess
import sys
import os

os.chdir(r"d:\选品\liandong21mall\flask-datta-able-master")
subprocess.Popen([sys.executable, "run.py"], 
                 stdout=subprocess.DEVNULL, 
                 stderr=subprocess.DEVNULL,
                 creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0)
print("Server started")
