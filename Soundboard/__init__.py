from .Sound import Sound, PreloadSounds
from .Devices import queryDevices

Players = []
preload = {}
playback_device, feedback_device = ("", "")

def _delete_finished_players():
    for player in Players:
        if player.finished:
            Players.remove(player)

def _stop_players():
    for player in Players:
        player.stop()


def Init(module_config):
    global preload, playback_device, feedback_device

    print("Soundboard: Retreiving playback & feedback config...")
    playback_device, playback_volume, feedback_device, feedback_volume = queryDevices(module_config)
    print("Soundboard: Playback on %s with volume %d" % (playback_device, playback_volume))
    print("Soundboard: Feedback on %s with volume %d" % (feedback_device, feedback_volume))

    print("Soundboard: Preloading...")
    preload = PreloadSounds(module_config, playback_volume, feedback_volume)
    print("Soundboard: Preload ok.")

    captured_keys = list(module_config["sounds"].keys()) + list(module_config["actions"].keys())

    return True, captured_keys

def Update(module_config, key):

    _delete_finished_players()

    if key in module_config["sounds"]:
        Players.append(Sound(samplerate=44100, device=playback_device).play(preload[key][0]))
        Players.append(Sound(samplerate=44100, device=feedback_device).play(preload[key][1]))
        return True

    elif key in module_config["actions"]:
        if module_config["actions"][key] == "<key.stop>":
            _stop_players()
            return True

    return False

def Finish(module_config):
    _stop_players()
    _delete_finished_players()
    return True
