import os
import pathlib
from shutil import rmtree

import yaml


class IOHandler(dict):
    """Class of Input & Output Handlers

    This will need either a dictioanry or a YAML filepath to be setup.

    Custom methods:
        read_yaml (file_path)
            Way of initialising with a YAML filepath
        list_files(key)
            List files in 'key' element
        create_dir(key)
            Create a directory from key element
        delete_path(key)
            Delete an object in a specified path
        dump(file_path)
            Dump the handler/config file into a YAML file
    """

    def __init__(self, *args, **kwargs):
        """Init"""
        super(IOHandler, self).__init__(*args, **kwargs)

    @classmethod
    def read_yaml(cls, file_path: str):
        """Way of initialising with a YAML filepath

        Args:
            file_path (str): Path to a YAML file
        """
        return cls(yaml.safe_load(file_path))

    def list_files(self, key: str) -> list:
        """List files in 'key' element

        Args:
            key (str): key name containing path of interest

        Returns:
            list: files and subfolders in this directory
        """
        return os.listdir(self[key])

    def create_dir(self, key: str):
        """Create a directory from key element, with all necessary parents if necessary

        Args:
            key (str): key name containing path of interest
        """
        pathlib.Path(self[key]).mkdir(mode=0o775, exist_ok=True, parents=True)

    def delete_path(self, key: str):
        """Delete an object in a specified path, either for a file or directory.

        From key element

        Args:
            key (str): key name containing path of interest
        """
        if os.path.isfile(self[key]):
            os.remove(self[key])
        elif os.path.isdir(self[key]):
            rmtree(self[key])
        else:
            raise ValueError(f"the path {self[key]} doesn't exist")

    def dump(self, file_path: str):
        """Dump the handler/config file into a YAML file

        Args:
            file_path (str): path where to dump file
        """
        with open(file_path, "w") as f:
            yaml.dump(dict(self), f, default_flow_style=False)
