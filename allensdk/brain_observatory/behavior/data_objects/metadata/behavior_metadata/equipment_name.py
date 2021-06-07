from pynwb import NWBFile

from allensdk.brain_observatory.behavior.data_objects import DataObject
from allensdk.internal.api import PostgresQueryMixin


class EquipmentName(DataObject):
    """the name of the experimental rig."""
    def __init__(self, equipment_name: str):
        super().__init__(name="equipment_name", value=equipment_name)

    @classmethod
    def from_json(cls, dict_repr: dict) -> "EquipmentName":
        return cls(equipment_name=dict_repr["equipment_name"])

    def to_json(self) -> dict:
        return {"eqipment_name": self.value}

    @classmethod
    def from_lims(cls, behavior_session_id: int,
                  lims_db: PostgresQueryMixin) -> "EquipmentName":
        query = f"""
            SELECT e.name AS device_name
            FROM behavior_sessions bs
            JOIN equipment e ON e.id = bs.equipment_id
            WHERE bs.id = {behavior_session_id};
        """
        equipment_name = lims_db.fetchone(query, strict=True)
        return cls(equipment_name=equipment_name)

    @classmethod
    def from_nwb(cls, nwbfile: NWBFile) -> "EquipmentName":
        metadata = nwbfile.lab_meta_data['metadata']
        return cls(equipment_name=metadata.equipment_name)