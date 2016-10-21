An IRC bot I wrote using python-twisted.

Features modular addons, command rate limiting, and addon reloading during runtime.

=========
# Dependencies (install through pip)
    pip install twisted simplejson GitPython
    
    pyOpenSSL (I recommend installing through distro package manager: python-openssl for Debian, pyOpenSSL for RHEL )

## Files
### pepperoni.py
Contains python-twisted Bot and BotFactory.  Loads initial settings from config.
### modules/
Contains the user-defined functionalities of the bot.  Each module contains an initialization function, and the main functionality of the module.  These classes inherit from `basemodules/botmodule`
### basemodules.py
Some core modules for the bot.
### settings.ini
Contains settings for the bot and various modules.  Read by ConfigParser

## Plans
- replace twisted-python with tulip for asynchronous functionality
- replace twisted-python's IRC interface with a custom built one in Go
- make `!reload pull` reload changes to basemodules.py
