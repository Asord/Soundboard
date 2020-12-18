from keyboard import press_and_release

def Init(module_config):
    captured_keys = module_config["shortcuts"].keys()
    return True, captured_keys

def Update(module_config, key):
    combo = module_config["shortcuts"][key]
    press_and_release(combo)
    return True

def Finish(module_config):
    return True
