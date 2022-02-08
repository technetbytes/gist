import yaml

def load_setting():
    # Read YAML configuration file
    with open("setting.yml","r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg
