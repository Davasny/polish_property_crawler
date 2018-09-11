import logging
from os import listdir, remove, path, makedirs

log = logging.getLogger("main")


class Filer:
    def __init__(self, dir_path):
        self._dir_path = dir_path

    def get_all_files(self):
        all_files = [f for f in listdir(self._dir_path) if path.isfile(path.join(self._dir_path, f))]
        log.debug("Files found:\t{}".format(len(all_files)))
        return all_files

    def empty_dir(self):
        log.warning("Removing files from:\t{}".format(self._dir_path))
        for file in self.get_all_files():
            filename = "{}/{}".format(self._dir_path, file)
            remove(filename)
            log.debug("Removed:\t{}".format(filename))

        if len(listdir(self._dir_path)) != 0:
            log.warning("Dir was not cleared correctly!")
            return False
        return True

    def make_sure_if_path_exists(self):
        if path.isdir(self._dir_path):
            return True
        else:
            try:
                log.info("Creating directory:\t{}".format(self._dir_path))
                makedirs(self._dir_path, exist_ok=True)
                return True
            except Exception as ex:
                log.warning(ex)
                return False
