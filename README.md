An IRC bot I wrote using python-twisted.

Features a settings file, modular addons, command rate limiting, and addon reloading during runtime.

=========

##Files
###pepperoni.py
Contains python-twisted Bot and BotFactory.  Loads initial settings from config.
###modules/
Contains the user-defined functionalities of the bot.  Each module contains an initialization function, and the main functionality of the module.  These classes inherit from `basemodules/botmodule`
###basemodules.py
Some core modules for the bot.
###settings.ini
Contains settings for the bot and various modules.  Read by ConfigParser

##Plans
- replace twisted-python with tulip for asynchronous functionality
- replace twisted-python's IRC interface with a custom built one in Go
