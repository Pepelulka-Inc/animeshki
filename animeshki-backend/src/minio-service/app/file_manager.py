from enum import Enum
from attr import dataclass


class FileStatus(Enum):
    PENDING_UPLOAD = "PendingUpload"
    IN_PROGRESS = "InProgress"
    SUCCESS = "Success"
    LOADED = "Loaded"
    FAILED = "Failed"


@dataclass(slots=True)
class File:
    name: str
    _status: FileStatus = None

    @property
    def status(self) -> FileStatus:
        return self._status

    def pending_upload(self):
        self._status = FileStatus.PENDING_UPLOAD

    def in_progress(self):
        self._status = FileStatus.IN_PROGRESS

    def loaded(self):
        self._status = FileStatus.LOADED

    def success(self):
        self._status = FileStatus.SUCCESS

    def failed(self):
        self._status = FileStatus.FAILED
