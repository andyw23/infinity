from pydub import AudioSegment

soundpath = '/Users/wilsona/projects/development/infinity/static/audio/echo drone.wav'

newsound = AudioSegment.from_file(soundpath, format="raw", frame_rate=44100, channels=2, sample_width=2)
trimsound = newsound[1000:5000]
trimsoundraw = trimsound.raw_data