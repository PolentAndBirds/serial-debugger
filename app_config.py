import json
import os

def load_config(config_file="config.json"):
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except: pass
    return {}

def save_config(config_data, config_file="config.json"):
    try:
        with open(config_file, "w") as f:
            json.dump(config_data, f)
    except: pass
