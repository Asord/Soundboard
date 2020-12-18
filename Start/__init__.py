from subprocess import Popen

procs = []

def _clear_dead_procs():
    for proc in procs:
        poll = proc.poll()
        if poll is not None:
            procs.remove(proc)

def Init(module_config):
    captured_keys = module_config["shortcuts"].keys()
    return True, captured_keys

def Update(module_config, key):
    app = module_config["shortcuts"][key]
    _clear_dead_procs()

    procs.append(Popen([app]))
    return True

def Finish(module_config):
    _clear_dead_procs()
    for proc in procs:
        proc.kill()
    return True
