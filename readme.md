**Soundboard Python** is intented to use a second keyboard as soundboard but also macro key using Python.

To create a new module, you only need to create a folder including a "module.json" file which will contain at least the module `name`, `version`,  `author` AND `config`.

```
{
  "name": "module-name",
  "author": "module-author",
  "version": "1.0.0",
  "config": {
    "config-1": "value-1", 
    "config-2": "value-2", 
	.
	.
  }
}
```

This file can also contain module-wild configs.

Next you need to create a **\_\_init\_\_.py** file which will contain at least the three functions "Init", "Update" and "Finish" with this signature:

`Init(module_config: dict): tuple[bool, list[str]]`

* *@type module_config:* dict
* *@arg module_config:* the "config" dict from the config.json file
* 
* *@ret tuple[bool, list[str]]*: return a tuple containing a bool "True" if init succeed, and the list of keys triggered/listened by this module. If the init failed, then return False and an empty list

`Update(module_config: dict, key: str): bool`

* *@type module_config:* dict
* *@arg module_config:* the "config" dict from the config.json file
* *@type key:* str
* *@arg key:* the key triggered
* 
* *@ret bool:* True if succeed, False if any error occured

`Finish(module_config: dict): bool`

* *@type module_config:* dict
* *@arg module_config:* the "config" dict from the config.json file
* 
* *@ret bool:* True if succeed, False if any error occured

