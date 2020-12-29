from keyboard import press_and_release, write

def Init(module_config):
    captured_keys = list(module_config["shortcuts"].keys()) + list(module_config["write"].keys())
    return True, captured_keys

def Update(module_config, key):
    if key in module_config["write"]:
        string = module_config["write"][key]
        write(string)
    else:
        combo = module_config["shortcuts"][key]
        press_and_release(combo)
    return True

def Finish(module_config):
    return True
