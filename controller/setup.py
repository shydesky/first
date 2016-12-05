# setup.py

from distutils.core import setup
import py2exe
options = {"py2exe":{"compressed": 1,
                     "optimize": 2
                     }}
setup(console=['wxpython.py'],options=options,zipfile=None)