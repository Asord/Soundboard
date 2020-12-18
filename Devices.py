from ctypes import windll
from ctypes import Structure, c_ushort, c_uint, create_string_buffer, sizeof, byref

stringBuffer = create_string_buffer(b'\000' * 32)
class LPWAVEOUTCAPS(Structure):
    _fields_ = [
        ("wMid", c_ushort),
        ("wPid", c_ushort),
        ("vDriverVersion", c_uint),
        ("szPname", type(stringBuffer)),
        ("dwFormats", c_uint),
        ("wChannels", c_ushort),
        ("wReserved1", c_ushort),
    ]

class NoValidPlaybackDeviceException(Exception):
    pass

class NoValidOutputDeviceException(Exception):
    pass


def queryOutputDevicesList():
    deviceList = {}

    nbDevices = windll.winmm.waveOutGetNumDevs()
    structLP = LPWAVEOUTCAPS()

    for i in range(nbDevices):
        windll.winmm.waveOutGetDevCapsA(c_uint(i), byref(structLP), sizeof(structLP))
        deviceList[structLP.szPname.decode() ] = i

    return deviceList

def queryInputDevicesList():
    deviceList = {}

    nbDevices = windll.winmm.waveInGetNumDevs()
    structLP = LPWAVEOUTCAPS()

    for i in range(nbDevices):
        windll.winmm.waveInGetDevCapsA(c_uint(i), byref(structLP), sizeof(structLP))
        deviceList[structLP.szPname.decode()] = i

    return deviceList


def queryDevices(config):
    connectedOutputDevices = queryOutputDevicesList()

    playback_device = None
    playback_volume = 0
    for device in config["playback_devices"]:
        if device["name"] in connectedOutputDevices:
            playback_device = device["name"]
            playback_volume = device["volume"]
            break
    if playback_device is None:
        raise NoValidPlaybackDeviceException("None of the playback devices from the configuration file are connected.")


    feedback_device = None
    feedback_volume = 0
    for device in config["output_devices"]:
        if device["name"] in connectedOutputDevices:
            feedback_device = device["name"]
            feedback_volume = device["volume"]
            break
    if feedback_device is None:
        raise NoValidOutputDeviceException("None of the output devices from the configuration file are connected.")

    return playback_device, playback_volume, feedback_device, feedback_volume

