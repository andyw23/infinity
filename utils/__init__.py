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
import os, logging

CONF_FILE = 'config.ini'
cfg = ConfigParser()
cfg.read(CONF_FILE)

SCORE_FILENAME = cfg.get('scores', 'filename')
logging.info("SCORE_FILENAME: {0}".format(SCORE_FILENAME))

SCHEMA_FILENAME = cfg.get('scores', 'schemaname')
logging.info("SCHEMA_FILENAME: {0}".format(SCHEMA_FILENAME))

AUDIO_PATH = cfg.get('audio', 'path')

AUDIO_EXTENSION = cfg.get('audio', 'format')
logging.info("AUDIO_EXTENSION: {0}".format(AUDIO_EXTENSION))

AUDIO_PATH = os.path.abspath(os.path.join(os.getcwd(), AUDIO_PATH))
logging.info("AUDIO_PATH: {0}".format(AUDIO_PATH))
