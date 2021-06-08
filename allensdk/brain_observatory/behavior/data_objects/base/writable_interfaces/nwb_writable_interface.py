import abc

from pynwb import NWBFile

from allensdk.brain_observatory.behavior.data_objects import DataObject


class NwbWritableInterface(abc.ABC):
    """Marks a data object as writable to NWB"""
    @classmethod
    @abc.abstractmethod
    def to_nwb(self, nwbfile: NWBFile) -> NWBFile:  # pragma: no cover
        """Given an already populated DataObject, return an pyNWB file object
        that had had DataObject data added.

        Parameters
        ----------
        nwbfile : NWBFile
            An NWB file object

        Returns
        -------
        NWBFile
            An NWB file object that has had data from the DataObject added
            to it.
        """
        raise NotImplementedError()