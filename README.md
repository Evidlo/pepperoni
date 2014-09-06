An IRC bot I wrote using python-twisted.

Features a settings file, modular addons, command rate limiting, and addon reloading during runtime.

=========

Everyone's favorite sausagebot.

##Files
###pepperoni.py
Contains python twisted objects.  Loads classes from modules.py, settings for each module and handles triggering of each module.
###modules/
Contains the functionalities of the bot.  Each module is a class that contains an initialization function called at startup file (see basemodules.py), a function for reanabling the module after a timeout period (enable), and the main functionality of the module (run).
###basemodules.py
Some core modules for the bot.  These could be deleted and the bot should still run.
###settings.py
A settings file which contains information about the server to join and some basic configuration settings for each module.  This file is read by ConfigParser.
