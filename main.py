from Sound import Sound, PreloadSounds
from Devices import queryDevices
from keyboard import wait
from json import load

with open("config.json") as config_raw:
    config = load(config_raw)

print("Retreiving playback & feedback config...")
playback_device, playback_volume, feedback_device, feedback_volume = queryDevices(config)
print("Playback on %s with volume %d" % (playback_device, playback_volume))
print("Feedback on %s with volume %d" % (feedback_device, feedback_volume))

print("Preloading...")
preload = PreloadSounds(config, playback_volume, feedback_volume)
print("Preload ok.")

Players = []
while True:
    wait(config["key_trigger"])

    # garbage collection
    for player in Players:
        if player.finished:
            Players.remove(player)

    with open(config["key_exchange_file"], "r") as kef:
        key = kef.readline()

        if key in preload:
            Players.append(Sound(samplerate=44100, device=playback_device).play(preload[key][0]))
            Players.append(Sound(samplerate=44100, device=feedback_device).play(preload[key][1]))

        elif key == config["key_stop_id"]: # del
            for player in Players:
                player.stop()

