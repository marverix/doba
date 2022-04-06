from doba.config import IS_INSIDE_DOCKER
from doba.structures import Volume
from .AbstractDataHandler import AbstractDataHandler


class VolumesHandler(AbstractDataHandler):

    @staticmethod
    def get_volume_path_to_backup(volume: Volume) -> str:
        """
        Get a volume's path that should be backup-ed
        :param volume:
        :return:
        """
        if IS_INSIDE_DOCKER:
            return volume.dst
        else:
            return volume.src

    def prepare_files_to_backup(self):
        return [self.get_volume_path_to_backup(volume) for volume in self.container.volumes]
