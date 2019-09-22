"""infinity.py
Andy Wilson, 2019
Imports the scores.xml file and parses it into memory
This is not invoked explicitly but happens automatically when the modules are imported
The score is read when importscore.components is loaded
The components are loaded when importscore is loaded
"""
from importscore.scores import Score
from interpret.concert_events import *
from schedule import schedule_command_events, schedule_run
from random import randint
from play.mixer import mixer

# print(score_is_valid())

class Player():
    def __init__(self):
        self.numscores = Score.get_num_scores()
        self.currentscorenum = randint(0, self.numscores)

    def play_next_score(self):
        if not self.numscores: return None
        self.currentscorenum = (self.currentscorenum + 1)
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

mixer.callback = score_done
print(mixer.callback)

player = Player()
player.play_next_score()


