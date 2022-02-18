import os
import shutil
import json
import yaml


def update_front_end():
    # send the build folder to src
    copy_folders_to_front_end("../build", "../front-end/src/chain-info")

    # send brownie config to src
    with open("../brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("../front-end/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print("Front-end updated!")


def copy_folders_to_front_end(src, dest):
    # if the folder exists, delete the entire tree, otherwise copy the tree
    if os.path.exists(dest):
        shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(os.path.abspath(src), os.path.abspath(dest))

# TO BE USED WHEN NEWLY DEPLOYED CONTRACT NEEDS TO BE USED IN FRONT-END (see React-shelther-front-end)
# data => to be copied in corresponding repo folder
