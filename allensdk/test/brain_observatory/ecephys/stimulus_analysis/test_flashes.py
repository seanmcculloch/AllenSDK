import pytest
import os
import pandas as pd
import numpy as np

from allensdk.brain_observatory.ecephys.stimulus_analysis import flashes


data_dir = '/allen/aibs/informatics/module_test_data/ecephys/stimulus_analysis_fh'


@pytest.mark.parametrize('spikes_nwb,expected_csv,analysis_params,units_filter',
                         [
                             #(os.path.join(data_dir, 'data', 'mouse406807_integration_test.spikes.nwb2'),
                             # os.path.join(data_dir, 'expected', 'mouse406807_integration_test.flashes.csv'),
                             # {})
                             (os.path.join(data_dir, 'data', 'ecephys_session_773418906.nwb'),
                              os.path.join(data_dir, 'expected', 'ecephys_session_773418906.flashes.csv'),
                              {},
                              [914580630, 914580280, 914580278, 914580634, 914580610, 914580290, 914580288, 914580286,
                               914580284, 914580282, 914580294, 914580330, 914580304, 914580292, 914580300, 914580298,
                               914580308, 914580306, 914580302, 914580316, 914580314, 914580312, 914580310, 914580318,
                               914580324, 914580322, 914580320, 914580328, 914580326, 914580334])
                         ])
def test_metrics(spikes_nwb, expected_csv, analysis_params, units_filter, skip_cols=[]):
    """Full intergration tests of metrics table"""
    # TODO: Not completed, some values still None
    if not os.path.exists(spikes_nwb):
        pytest.skip('No input spikes file {}.'.format(spikes_nwb))

    analysis_params = analysis_params or {}
    analysis = flashes.Flashes(spikes_nwb, filter=units_filter, **analysis_params)
    actual_data = analysis.metrics.sort_index()

    expected_data = pd.read_csv(expected_csv)
    expected_data = expected_data.set_index('unit_id')
    expected_data = expected_data.sort_index()  # in theory this should be sorted in the csv, no point in risking it.

    assert (np.all(actual_data.index.values == expected_data.index.values))
    assert (set(actual_data.columns) == (set(expected_data.columns) - set(skip_cols)))

    assert(np.allclose(actual_data['on_off_ratio_fl'].astype(np.float), expected_data['on_off_ratio_fl'], equal_nan=True))
    assert(np.allclose(actual_data['sustained_idx_fl'].astype(np.float), expected_data['sustained_idx_fl'], equal_nan=True))
    assert(np.allclose(actual_data['firing_rate_fl'].astype(np.float), expected_data['firing_rate_fl'], equal_nan=True))
    assert(np.allclose(actual_data['reliability_fl'].astype(np.float), expected_data['reliability_fl'], equal_nan=True))
    assert(np.allclose(actual_data['fano_fl'].astype(np.float), expected_data['fano_fl'], equal_nan=True))
    assert(np.allclose(actual_data['lifetime_sparseness_fl'].astype(np.float), expected_data['lifetime_sparseness_fl'],
                       equal_nan=True))
    assert(np.allclose(actual_data['run_pval_fl'].astype(np.float), expected_data['run_pval_fl'], equal_nan=True))
    assert(np.allclose(actual_data['run_mod_fl'].astype(np.float), expected_data['run_mod_fl'], equal_nan=True))
