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
if SCORE_FILENAME == None: SCORE_FILENAME = 'infinity.xml'
logging.info("SCORE_FILENAME: {0}".format(SCORE_FILENAME))

SCHEMA_FILENAME = cfg.get('scores', 'schemaname')
logging.info("SCHEMA_FILENAME: {0}".format(SCHEMA_FILENAME))

AUDIO_EXTENSION = cfg.get('audio', 'format')
if AUDIO_EXTENSION == None: AUDIO_EXTENSION = 'wav'
logging.info("AUDIO_EXTENSION: {0}".format(AUDIO_EXTENSION))

AUDIO_PATH = cfg.get('audio', 'path')
AUDIO_PATH = os.path.abspath(os.path.join(os.getcwd(), AUDIO_PATH))
if AUDIO_PATH == None: AUDIO_PATH = '.'
logging.info("AUDIO_PATH: {0}".format(AUDIO_PATH))

DEFAULT_VOLUME = cfg.getfloat('audio', 'default_volume')
if DEFAULT_VOLUME == None: DEFAULT_VOLUME = 0.8
logging.info("DEFAULT_VOLUME: {0}".format(DEFAULT_VOLUME))

FADE_TIME = cfg.getint('player', 'default_fade_time_ms')
if FADE_TIME == None: FADE_TIME = 20
logging.info("FADE_TIME: {0}".format(FADE_TIME))

NUM_AUDIO_CHANNELS = cfg.getint('audio', 'num_channels')
if NUM_AUDIO_CHANNELS == None: NUM_AUDIO_CHANNELS = 8
logging.info("NUM_AUDIO_CHANNELS: {0}".format(NUM_AUDIO_CHANNELS))


