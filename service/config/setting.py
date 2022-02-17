import yaml


class Config(object):

    _cfg = None  
    def __init():
        # Read YAML configuration file
        with open("setting.yml","r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        Config._cfg = cfg

    @staticmethod
    def get_property(property_name):
        if Config._cfg is None:
            Config.__init()
        if property_name not in Config._cfg.keys(): # we don't want KeyError
            return None  # just return None if not found
        return Config._cfg[property_name]

    @staticmethod
    def get_complete_property(parent_property, child_property):
        if Config._cfg is None:
            Config.__init()
        if parent_property not in Config._cfg.keys():
            return None  # just return None if not found
        return Config._cfg[parent_property][child_property]
           

def load_setting():
    # Read YAML configuration file
    with open("setting.yml","r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg
