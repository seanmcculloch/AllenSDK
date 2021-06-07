import warnings
from typing import Optional, List

from pynwb import NWBFile

from allensdk.brain_observatory.behavior.data_objects import DataObject
from allensdk.brain_observatory.behavior.data_objects._base.readable_mixins\
    .lims_readable_mixin import \
    LimsReadableMixin
from allensdk.internal.api import PostgresQueryMixin, \
    OneOrMoreResultExpectedError


class ReporterLine(DataObject, LimsReadableMixin):
    """the genotype name(s) of the reporter line(s)"""
    def __init__(self, reporter_line: Optional[str]):
        super().__init__(name="reporter_line", value=reporter_line)

    @classmethod
    def from_json(cls, dict_repr: dict) -> "ReporterLine":
        pass

    def to_json(self) -> dict:
        return {"sex": self.value}

    @classmethod
    def from_lims(cls, behavior_session_id: int,
                  lims_db: PostgresQueryMixin) -> "ReporterLine":
        query = f"""
            SELECT g.name AS reporter_line
            FROM behavior_sessions bs
            JOIN donors d ON bs.donor_id=d.id
            JOIN donors_genotypes dg ON dg.donor_id=d.id
            JOIN genotypes g ON g.id=dg.genotype_id
            JOIN genotype_types gt
                ON gt.id=g.genotype_type_id AND gt.name = 'reporter'
            WHERE bs.id={behavior_session_id};
        """
        result = lims_db.fetchall(query)
        if result is None or len(result) < 1:
            raise OneOrMoreResultExpectedError(
                f"Expected one or more, but received: '{result}' "
                f"from query:\n'{query}'")
        reporter_line = cls._parse(reporter_line=result, warn=True)
        return cls(reporter_line=reporter_line)

    @classmethod
    def from_nwb(cls, nwbfile: NWBFile) -> "ReporterLine":
        return cls(reporter_line=nwbfile.subject.reporter_line)

    def to_nwb(self, nwbfile: NWBFile) -> NWBFile:
        pass

    @staticmethod
    def _parse(reporter_line: Optional[List[str]],
                            warn=False) -> Optional[str]:
        """There can be multiple reporter lines, so it is returned from LIMS
        as a list. But there shouldn't be more than 1 for behavior. This
        tries to convert to str

        Parameters
        ----------
        reporter_line
            List of reporter line
        warn
            Whether to output warnings if parsing fails

        Returns
        ---------
        single reporter line, or None if not possible
        """
        if reporter_line is None:
            if warn:
                warnings.warn('Error parsing reporter line. It is null.')
            return None

        if len(reporter_line) == 0:
            if warn:
                warnings.warn('Error parsing reporter line. '
                              'The array is empty')
            return None

        if isinstance(reporter_line, str):
            return reporter_line

        if len(reporter_line) > 1:
            if warn:
                warnings.warn('More than 1 reporter line. Returning the first '
                              'one')

        return reporter_line[0]

    @property
    def indicator(self, warn=False) -> Optional[str]:
        """Parses indicator from reporter"""
        reporter_line = self.value
        reporter_substring_indicator_map = {
            'GCaMP6f': 'GCaMP6f',
            'GC6f': 'GCaMP6f',
            'GCaMP6s': 'GCaMP6s'
        }
        if reporter_line is None:
            if warn:
                warnings.warn(
                    'Could not parse indicator from reporter because '
                    'there is no reporter')
            return None

        for substr, indicator in reporter_substring_indicator_map.items():
            if substr in reporter_line:
                return indicator

        if warn:
            warnings.warn(
                'Could not parse indicator from reporter because none'
                'of the expected substrings were found in the reporter')
        return None