from keyboard import wait as keyboard_interupt
from json import load as load_json
from os import listdir
from os.path import isdir, join
from importlib import import_module
from atexit import register as register_atexit

with open("config.json", "r") as cfg: global_cfg = load_json(cfg)

def _clear_before_exit(modules):
    for module in modules:
        module_config = module["infos"]["config"]
        print("Safely finishing module %s" % module["infos"]["name"])
        module["functions"].Finish(module_config)
    print("All modules finished. Closing.")
    print("============== Closed ==============")

def _restart(modules):
    _clear_before_exit(modules)
    exit(1)


def get_modules_dir():
    modules = []
    for elem in listdir("."):
        if isdir(elem) and not (elem.startswith(".") or elem.startswith("_")):
            modules.append(elem)
    return modules

def load_modules():
    modules = []

    modules_dirs = get_modules_dir()
    for module_dir in modules_dirs:
        try:
            with open(join(module_dir, "module.json")) as module_file:
                module_infos = load_json(module_file)
                modules_funcs = import_module(module_dir)

                modules.append({"infos": module_infos, "functions" : modules_funcs, "keys":[]})

                print("Registred: %s v%s by %s" % (
                    module_infos["name"],
                    module_infos["version"],
                    module_infos["author"]
                ))

        except ModuleNotFoundError as mnfe:
            print("An issue has been encounted while trying to import a module.")
            print("Did the __init__.py file exists in the module %s ?" % module_dir)
            print(mnfe)

        except FileNotFoundError as fnfe:
            print("The config file of %s was not found while trying to initialize." % module_dir)
            print(fnfe)

    return modules

if __name__ == '__main__':
    modules = load_modules()

    for module in modules:
        config = module["infos"]["config"]

        print("===========Initializing %s==========="% module["infos"]["name"])
        success, captured_keys = module["functions"].Init(config)
        if success:
            module["keys"] = captured_keys
            print("=============Initialized=============")
        else:
            print("===========Not initialized===========")

    print("Register exit event")
    register_atexit(lambda: _clear_before_exit(modules))

    print("Starting keyboard interupt... Waiting for F24...")
    while True:
        keyboard_interupt(global_cfg["key_trigger"])

        with open(global_cfg["key_exchange_file"], "r") as kef: key = kef.readline()

        if key == global_cfg["key_stop"]:
            _clear_before_exit(modules)
            exit(0)

        elif key == global_cfg["key_restart"]:
            _restart(modules)

        for module in modules:
            if key in module["keys"]:
                config = module["infos"]["config"]

                module["functions"].Update(config, key)
