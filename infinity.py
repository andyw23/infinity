# ##############################################################################
#  Infinity. Copyright (c) 2019 Oliver Wyman Digital and Andy Wilson. This     #
#  file is subject to the terms and conditions defined in the file 'LICENSE',  #
#  which is part of this source code package.                                  #
# ##############################################################################

from importscore.scores import Score
from interpret.concert_events import *
from schedule import schedule_command_events, schedule_run
from random import randint
from play.mixer import mixer

# print(score_is_valid())

class Player():
    def __init__(self):
        # pick a score at random as the first to play
        self.numscores = Score.get_num_scores()
        self.currentscorenum = randint(0, self.numscores)

    def play_next_score(self):
        if not self.numscores:
            logging.error("No scores were found")
        else:
            # increment the current score number
            self.currentscorenum = (self.currentscorenum + 1)
            # wraparound
            if self.currentscorenum > self.numscores: self.currentscorenum = 1

            self.score = Score.get_score(self.currentscorenum)
            if self.score != None:
                print("SCORE '{0}' RETRIEVED".format(self.score.id))
                sample_events = self.score.get_sample_components()
                # Sample.log_sample_events(sample_events)
                timeends, command_events = unpack_sample_events(sample_events)
                # log_command_events(command_events)
                schedule_command_events(timeends, command_events)
                schedule_run()

def score_done():
    # called by the schedule._score_end()
    # insert commands here as to what to do when a score ends
    player.play_next_score()
# tell the mixer to call the above function when a score is finished playing
mixer.callback = score_done

player = Player()
player.play_next_score()


