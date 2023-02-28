import os
import yaml

with open("config.yml") as config:
    conf = yaml.safe_load(config)

print(conf["database"]["password"])
