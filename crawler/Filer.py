from os import listdir, remove
from os.path import isfile, join
import logging

log = logging.getLogger("main")


class Filer:
    def __init__(self, download_path):
        self._download_path = download_path

    def get_all_files(self):
        all_files = [f for f in listdir(self._download_path) if isfile(join(self._download_path, f))]
        log.info("Files found:\t{}".format(len(all_files)))
        return all_files

    def empty_dir(self):
        log.warning("Removing files from:\t{}".format(self._download_path))
        for file in self.get_all_files():
            filename = "{}/{}".format(self._download_path, file)
            remove(filename)
            log.debug("Removed:\t{}".format(filename))
