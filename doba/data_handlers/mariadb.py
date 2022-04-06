import os
import subprocess
from typing import List

from doba.structures import Container
from .AbstractDataHandler import AbstractDataHandler


class MariadbHandler(AbstractDataHandler):

    @staticmethod
    def preflight():
        subprocess.run(["mysqldump", "--version"], capture_output=True, check=True)

    def __init__(self, container: Container):
        super().__init__(container)
        self.temp_backup_file = None

    def prepare_files_to_backup(self) -> List[str]:
        self.temp_backup_file = self.container.name + ".sql"
        subprocess.run([
            "mysqldump",
            "--host=" + self.container.ip_address,
            "--port=" + str(self.container.ports[0].port),
            "--user=root",
            "--password=" + self.container.env["MARIADB_ROOT_PASSWORD"],
            "--all-databases",
            "--add-drop-database",
            "--skip-comments",
            "--skip-dump-date",
            "--result-file=" + self.temp_backup_file
        ], capture_output=True, check=True)
        return [self.temp_backup_file]

    def after_backup(self):
        os.remove(self.temp_backup_file)
