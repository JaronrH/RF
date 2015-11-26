# RF - 433mhz Remote Application

A few months ago, I bought a set of "Etekcity ZAP 5LX Auto-Programmable Function Wireless Remote Control Outlet Light Switch with 2 Remotes, 5-Pack Outlet " (http://amzn.com/B00DQELHBS) which had a major problem: *the remote buttons 1 and 2 where using the same codes as buttons 3 and 4*!  As a result, I had to either use 2 receivers on the same code or just live without using the last two outlets!

I happened to have a Rasperry Pi 2 device so I went looking to see if I could use that to control it.  That is when I stumbled upon this amazing blog post by Sam Kear (https://www.samkear.com/hardware/control-power-outlets-wirelessly-raspberry-pi) about using the Pi to control the outlets!  *The resources he provided were instrumental in getting this project off the ground*!  You should go read his blog as it tells you how to hook up and test the hardware.

While the hardware setup guide was great, I wasn't a huge fan of the UI.  Since I was trying to learn python Flask at the time, I decided to use this opportunity to come up with my own.  That is where this project was born!

Demo:  https://www.youtube.com/watch?v=G9kaAmel5R4 (doesn't include longpress on command for timer)

**Features:**
 - Custom command creation
 - Scheduling commands (repeat or single use)
 - Restful API for control (I have a Tasker task on my phone to control all my lights)
 - All commands can be created/edited from the ui - no need to edit PHP files or config files directly.
 - Timer (press and hold command button)
 - AutoLight -- connects to a weather station I have to read the lux value and turn on lights based off of the current value.

**433Utils:**
https://github.com/ninjablocks/433Utils
I used this project for the actual communication.  However, I had to make 2 minor modifications.  First, I removed "received" from the RFSniffer.  Second, in order to get the values so I could read them from Python, I had to make if flush the buffer after each line was written.  This is done by add *<< flush* to the end of the *cout* statement.  The modded source can be found in RF\drivers\rf\433Utils\RPi_utils.

**Testing**
The drivers (IP address and RF) can be run directly for testing.  

Send code 12345

    [sudo] python drivers\rf\__init__.py 12345

Listen for codes

    [sudo] python drivers\rf\__init__.py

Please note that there is a mock python script that runs when on windows which feeds random values into the application!  This was for local development testing.

**Known Issues:**
 - Autolight requires a Weather Station service I setup at my house.  Therefore, this will not work in this release (would need to estimate sunset or talk to a weather service to get sunset information)
 - Some issues with Internet Explorer (I used Chrome so that's really all I care about!)
 - This is a personal pet project made for myself so I'm sure there are issues that others will have running it!

**Python Requirements:**

    [sudo] pip install [package]

 - apscheduler (Note: I had to install this manually from code on my PI2! https://bitbucket.org/agronholm/apscheduler/src/)
 - sqlalchemy 
 - flask
 - flask-classy
 - flask_apscheduler
 - flask_sqlalchemy 

Made to run on Python 2.7  You run the application by calling

    [sudo] python RF.py console

You can replace console with *status*, *start*, or *stop*.  This allows you to run in debug mode with console output or run as a damon on your pi (you can then use cron to start this at boottime).  You can then go to http://[ipaddress]:54321 to access the page (use the .conf file to change the port).

**3rd Party Components that made this project possible!**
 - BootBox - http://bootboxjs.com/
 - ClockPicker - https://weareoutman.github.io/clockpicker/
 - DataTables - https://www.datatables.net/
 - JQuery Longpress - https://github.com/vaidik/jquery-longpress
 - JQuery - https://jquery.com/
 - Modernizr - https://modernizr.com/
 - Animate - https://daneden.github.io/animate.css/
 - Boostrap - http://getbootstrap.com/
 - Paper Collapse - https://github.com/alexander-ruehle/paper-collapse
 - roundSlider - http://roundsliderui.com/
 - SB Admin2 - http://startbootstrap.com/template-overviews/sb-admin-2/
 - Font Awesome - https://fortawesome.github.io/Font-Awesome/
