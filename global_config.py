
import os
from pathlib import Path
import logging
from typing import Optional, List, Dict, Any
from enum import Enum, IntEnum

log_level = os.getenv("IRONING_GUI_LOG_LEVEL").upper()
log_file = os.getenv("IRONING_GUI_LOG_FILE")
logging.basicConfig(filename=log_file, level=log_level)
logger = logging.getLogger("BpmOnyx")

# ENUMS FOR IRONING MODES AND RUN MODES
class IRONING_MODE(IntEnum):
    ALL = 0
    AREA = 1
    SINGLE = 2

class RUN_MODE(Enum):
    INCLUSION = "Inclusion"
    EXCLUSION = "Exclusion"
    DISABLE = "Disable"
# ENUMS FOR IRONING MODES AND RUN MODES

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
RUN_MODE_LABELS = [m.value for m in (RUN_MODE.INCLUSION, RUN_MODE.EXCLUSION, RUN_MODE.DISABLE)]

DEST_MASK = ['SC_BSYD']
REFERENCE_BPM = 'BPMS:GUNB:314'
TARGET_BPM = 'BPMS:GUNB:314'
TARGET_AREA = 'GUNB'
