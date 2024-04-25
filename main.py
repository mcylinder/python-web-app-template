import os
import threading
from serve import run_server

import easygui
import subprocess

# Start server in a separate thread
threading.Thread(target=run_server).start()

# Check if the saved path exists and points to a valid file
chrome_path = ""
if os.path.isfile('chrome_path.txt'):
    with open('chrome_path.txt', 'r') as file:
        chrome_path = file.read().strip()

if not os.path.isfile(chrome_path):
    # If the saved path doesn't exist or doesn't point to a valid file, use easygui to show a file dialog
    chrome_path = os.path.abspath(easygui.fileopenbox(msg="Select Chrome executable", default='/Applications/*.app'))

    # Append the path to the actual executable inside the .app package
    chrome_path = os.path.join(chrome_path, 'Contents/MacOS/Google Chrome')

    # Save the selected path to a file for future use
    with open('chrome_path.txt', 'w') as file:
        file.write(chrome_path)


import subprocess

subprocess.Popen([chrome_path, '--app=http://127.0.0.1:9001/'])
