import tarfile
from pathlib import Path
from tempfile import gettempdir
from typing import List

from doba.lib.time import time_str
from doba.structures import BackupPath, Container


class AbstractDataHandler:

    @staticmethod
    def preflight():
        """
        Preflight method may be used by a Data Handler to verify if environment conditions required by a Data Handler
        have been meet. E.g. it may be used to check if required application is installed on a host.
        :return:
        """
        pass

    def __init__(self, container: Container):
        self.container = container

    @property
    def name(self) -> str:
        return self.__class__.__name__[:-7].lower()

    @property
    def backup_path(self) -> str:
        return str(Path("doba").joinpath(self.container.name, self.name))

    @property
    def file_name(self) -> str:
        return time_str() + ".tar.bz2"

    def before_backup(self):
        """
        Before backup
        Use this method to do something before calling backup method
        :return:
        """
        pass

    def after_backup(self):
        """
        After backup
        Use this method to do something after calling backup method
        :return:
        """
        pass

    def backup(self):
        """
        Create backup
        :return:
        """
        temp_backup_file = self.create_temp_backup_file()
        backup_archive = tarfile.open(temp_backup_file.path, "w:bz2")

        files = self.prepare_files_to_backup()
        for file_path in files:
            backup_archive.add(file_path)

        backup_archive.close()

    def prepare_files_to_backup(self) -> List[str]:
        """
        Each Data Handler class must define method to prepare list of files to backup.
        This is method must return list of files paths.
        :return: List of paths to be added to archive
        """
        raise NotImplementedError()

    def create_temp_backup_file(self) -> BackupPath:
        """
        Create temporary backup file
        :return:
        """
        backup_path = self.backup_path
        file_name = self.file_name

        temp_backup_path = Path(gettempdir()).joinpath(backup_path)
        temp_backup_path.mkdir(mode=0o740, parents=True, exist_ok=True)

        temp_backup_file = temp_backup_path.joinpath(file_name)
        temp_backup_file.touch(mode=0o740, exist_ok=True)

        return BackupPath(str(temp_backup_file), backup_path, file_name)
