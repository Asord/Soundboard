import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from threading import Thread
from os.path import join

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def getAudiofileData(file, playback_vol_mod=0, feedback_vol_mod=0):
    sound = AudioSegment.from_mp3(file=file)

    pb_sound_vol = sound + playback_vol_mod
    pb_samples = pb_sound_vol.get_array_of_samples()
    fb_sound_vol = sound + feedback_vol_mod
    fb_samples = fb_sound_vol.get_array_of_samples()

    return np.array(pb_samples, dtype="int16"), np.array(fb_samples, dtype="int16")

def PreloadSounds(config, playback_vol_mod=0, feedback_vol_mod=0):
    ret = {}

    for key, file in config["sounds"].items():
        filePath = join(config["sound_directory"], file)
        ret[key] = getAudiofileData(filePath, playback_vol_mod, feedback_vol_mod)

    return ret

class Sound(Thread):
    def __init__(self, samplerate=44100, dtype="int16", device=None):
        super().__init__()
        self._stopped = False
        self.finished = False

        self._samplerate = samplerate
        self._dtype = dtype
        self._device = device

        self._file = ""

        self._data = None
        self._outputStream = None

        self._createSoundDevice()

    def _createSoundDevice(self):
        self._outputStream = sd.OutputStream(
            samplerate=self._samplerate,
            device=self._device,
            dtype=self._dtype,
        )

    def play(self, data):
        self._data = data
        self.start()
        return self

    def stop(self):
        self._stopped = True

    def run(self):
        self._outputStream.start()

        for chunk in list(chunks(self._data, 2048)):
            if self._stopped: break
            self._outputStream.write(chunk)

        self._outputStream.stop()
        self.finished = True


