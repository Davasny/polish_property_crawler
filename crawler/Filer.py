import os
from os import listdir, remove, path
from os.path import isfile, join
import logging

log = logging.getLogger("main")


class Filer:
    def __init__(self, dir_path):
        self._dir_path = dir_path

    def get_all_files(self):
        all_files = [f for f in listdir(self._dir_path) if isfile(join(self._dir_path, f))]
        log.debug("Files found:\t{}".format(len(all_files)))
        return all_files

    def empty_dir(self):
        log.warning("Removing files from:\t{}".format(self._dir_path))
        for file in self.get_all_files():
            filename = "{}/{}".format(self._dir_path, file)
            remove(filename)
            log.debug("Removed:\t{}".format(filename))
    def make_sure_if_path_exists(self):
        if path.isdir(self._dir_path):
            return True
        else:
            try:
                log.info("Creating directory:\t{}".format(self._dir_path))
                os.makedirs(self._dir_path, exist_ok=True)
                return True
            except Exception as ex:
                log.warning(ex)
                return False
