
import os
from pathlib import Path
import logging


log_level = os.getenv("IRONING_GUI_LOG_LEVEL").upper()
log_file = os.getenv("IRONING_GUI_LOG_FILE")
logging.basicConfig( level=log_level)
LOGGER = logging.getLogger("")

#GLOBAL CONSTANTS
RATE_PV_MAPPINGS = {
    'SC_BSYD': 'TPG:SYS0:1:DST02:RATE_RBV',
    'SC_DIAG0': 'TPG:SYS0:1:DST01:RATE_RBV',
    'SC_HXR (GUNB-SLTH)': 'TPG:SYS0:1:DST03:RATE_RBV',
    'SC_HXR (BSYH-DMPH)': 'TPG:SYS0:1:DST03:RATE_RBV',
    'SC_SXR (GUNB-SLTS)': 'TPG:SYS0:1:DST04:RATE_RBV',
    'SC_SXR (SLTS-DMPS)': 'TPG:SYS0:1:DST04:RATE_RBV',
}
BEAMLINES = [
    'SC_BSYD', 'SC_DIAG0',
    'SC_HXR (GUNB-SLTH)', 'SC_HXR (BSYH-DMPH)',
    'SC_SXR (GUNB-SLTS)', 'SC_SXR (SLTS-DMPS)'
]
IRONING_MODE_LABELS = ['All', 'Area', 'Single']
RUN_MODE_LABELS = ["Inclusion", "Exclusion", "Disable"]

DEST_MASK = ['SC_BSYD']
REFERENCE_BPM = 'BPMS:GUNB:314'
TARGET_BPM = 'BPMS:GUNB:314'
TARGET_AREA = 'GUNB'

DATA_TABLE_HANDLERS  = {
        'Average TMIT From BSA': ('bsa_buffer.bpm_tmit_averages_dictionary', 'dict'),
        'Wrong Size Nord': ('wrong_size_nord_dictionary', 'dict'),
        'Counts of BPMs per Unique PID': ('bpm_pid_counts_by_meas', 'nested'),
        'Dev Names of PIDs by Measurement': ('bpm_pid_devs_by_meas', 'nested'),
        'Cleaned TMIT Averages': ('bpm_ave_tmits', 'dict'),
        'Cleaned FW QSCLS': ('bpm_fw_scl_pvs', 'dict'),
        'Cleaned SW QSCLS': ('bpm_sw_scl_pvs', 'dict'),
        'Cleaned TMIT Ratios': ('tmits_ratiod_to_ref', 'dict'),
        'Value of FW QSCL if Ironed': ('put_fwscl_vals', 'dict'),
        'Value of SW QSCL if Ironed': ('put_swscl_vals', 'dict'),
        'Total Failures': ('total_failures', 'nested'),
    }
