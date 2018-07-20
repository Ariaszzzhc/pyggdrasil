import sys
import os

sys.path.insert(0, os.getcwd())

from pyggdrasil import create_app

application = create_app('prod')
