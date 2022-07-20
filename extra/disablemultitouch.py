import kivy;kivy.require('2.1.0')
from kivy.config import Config
Config.set('input','mouse','mouse,disable_multitouch')
Config.remove_option('input',r'%(name)s')
