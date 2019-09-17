import pygame

def play_one():

    pygame.init()
    soundpath = '/Users/wilsona/projects/development/infinity/static/audio/echo drone.wav'
    soundmixer = pygame.mixer
    soundmixer.init()
    mysound = soundmixer.Sound(soundpath)
    mysound.set_volume(1.0)
    mysound.play()
    # print(mysound.get_raw())

    # mysound.play(loops=0, maxtime=0, fade_ms=0) -> Channel
    # mysound.stop()
    # mysound.fadeout()
    # mysound.set_volume()
    # mysound.get_volume() -> value
    # mysound.num_channels() -> count
    # mysound.get_length() -> seconds
    # mysound.get_raw() -> bytes

    # eventually
    # soundmixer.init(frequency=22050, size=-16, channels=2, buffer=4096, devicename=None, allowedchanges=AUDIO_ALLOW_FREQUENCY_CHANGE | AUDIO_ALLOW_CHANNELS_CHANGE) -> None
    # soundmixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None) -> None
    # soundmixer.quit() -> None
    # soundmixer.get_init() -> (frequency, format, channels)
    # soundmixer.stop() -> None
    # soundmixer.pause() -> None
    # soundmixer.unpause() -> None
    # soundmixer.fadeout(time) -> None
    # soundmixer.set_num_channels(count) -> None
    # soundmixer.get_num_channels() -> count
    # soundmixer.set_reserved(count) -> None
    # soundmixer.find_channel(force=False) -> Channel
    # soundmixer.get_busy() -> bool
    # soundmixer.get_sdl_mixer_version() -> (major, minor, patch)
    # soundmixer.get_sdl_mixer_version(linked=True) -> (major, minor, patch)

    """
    CREATE SOUND
    """
    # soundmixer.Sound(filename) -> Sound
    # soundmixer.Sound(file=filename) -> Sound
    # soundmixer.Sound(buffer) -> Sound
    # soundmixer.Sound(buffer=buffer) -> Sound
    # soundmixer.Sound(object) -> Sound
    # soundmixer.Sound(file=object) -> Sound
    # soundmixer.Sound(array=object) -> Sound

    # soundmixer.quit()
    # pygame.quit()

play_one()