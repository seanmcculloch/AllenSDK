import warnings
from typing import Optional

from pynwb import NWBFile

from allensdk.brain_observatory.behavior.data_objects import DataObject
from allensdk.brain_observatory.behavior.data_objects._base.readable_mixins\
    .lims_readable_mixin import \
    LimsReadableMixin
from allensdk.internal.api import PostgresQueryMixin


class FullGenotype(DataObject, LimsReadableMixin):
    """the name of the subject's genotype"""
    def __init__(self, full_genotype: str):
        super().__init__(name="full_genotype", value=full_genotype)

    @classmethod
    def from_json(cls, dict_repr: dict) -> "FullGenotype":
        pass

    def to_json(self) -> dict:
        return {"sex": self.value}

    @classmethod
    def from_lims(cls, behavior_session_id: int,
                  lims_db: PostgresQueryMixin) -> "FullGenotype":
        query = f"""
                SELECT d.full_genotype
                FROM behavior_sessions bs
                JOIN donors d ON d.id=bs.donor_id
                WHERE bs.id= {behavior_session_id};
                """
        genotype = lims_db.fetchone(query, strict=True)
        return cls(full_genotype=genotype)

    @classmethod
    def from_nwb(cls, nwbfile: NWBFile) -> "FullGenotype":
        return cls(full_genotype=nwbfile.subject.genotype)

    def parse_cre_line(self, warn=False) -> Optional[str]:
        """
        Parameters
        ----------
        warn
            Whether to output warning if parsing fails

        Returns
        ----------
        cre_line
            just the Cre line, e.g. Vip-IRES-Cre, or None if not possible to
            parse
        """
        full_genotype = self.value
        if ';' not in full_genotype:
            if warn:
                warnings.warn('Unable to parse cre_line from full_genotype')
            return None
        return full_genotype.split(';')[0].replace('/wt', '')