import abc

from allensdk.brain_observatory.behavior.data_objects import DataObject


class SyncFileReadableInterface(abc.ABC):
    """Marks a data object as readable from sync file"""
    @classmethod
    @abc.abstractmethod
    def from_sync_file(cls, *args) -> "DataObject":
        """Populate a DataObject from the sync file

        Returns
        -------
        DataObject:
            An instantiated DataObject which has `name` and `value` properties
        """
        raise NotImplementedError()