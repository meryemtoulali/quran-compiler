import settings
from interface import start
from logger import logevent

# main, start here
logevent('Starting app\n')
settings.init()
start()