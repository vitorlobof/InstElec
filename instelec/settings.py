import sys
import os


if os.path.exists('settings.py'):
    sys.path.insert(0, 'settings.py')

    from settings import *
else:
    from .default.settings import *
