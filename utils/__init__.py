"""PRINT_PRETTY_FOrMAT function"""

"""
PRETTY PRINTING
"""
COL_SIZE = 25
SP = ': '


def pfp(desc, val):
    """Prints out a string and value in formatted columns. The left columnnwidth is determined
    by COL_SIZE module global"""
    print('{0}{1}{2}'.format(str(desc).ljust(COL_SIZE), SP, val))

"""
CONFIG PARSER
"""
from configparser import ConfigParser

CONF_FILE = 'config.ini'
cfg = ConfigParser()
cfg.read(CONF_FILE)
SCORE_FILENAME = cfg.get('scores', 'filename')
AUDIO_PATH = cfg.get('audio', 'path')
AUDIO_EXTENSION = cfg.get('audio', 'format')
