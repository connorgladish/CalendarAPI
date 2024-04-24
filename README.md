# CalendarAPI

_Needs_:
 -  Python installed.
 -  import requests.
 -  import datetime.
 -  import json.
 -  import pytz.
 -  import random.
 -  from PIL import Image, ImageTk.

   
Currently runs on Python 3.12.3.

**Prototype for CalendarAPI.** Works to pull subject, date and time, and location for a selected amount of time. Start and end time are fixed.
--------------
**Update** Now there is a GUI for this program.
 - Main GUI is under main.py - this one is the main one not to mess with until we know for sure.
 - guiTest.py is a test file for testing the possible scrolling, and body text functions for the event handling.
---------------

**Main problem that needs to be fixed before front-end development:
**
 -  Access token is a one-off and needs to be a static variable, not one that is constantly needing updating.
 -  Also, sometimes there shows an event from the day prior. Not sure why yet.
----------------

**Main problems in front-end development:
**
 - Scrolling back up in guiTest.py is just not working. I have tried many things and just can't figure out a proper solution.

----------
If it shows in the terminal "Failed to fetch data," it most likely is because of the Access Token. 
 - Go to Postman
 - Under Auth, Click Get New Access Token
 - Proceed
