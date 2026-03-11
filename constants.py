# Traffic engineering constants for JUNC
# Change values here to affect all calculations system-wide.

# Saturation flow (vehicles per hour per lane, green phase)
DEFAULT_CAPACITY = 1800

# Default signal cycle time (seconds)
DEFAULT_CYCLE_TIME = 120

# Maximum number of lanes per direction (used in lane-combination filters)
MAX_LANES_PER_DIRECTION = 50

# Level of Service (LOS) thresholds based on V/C ratio
# V/C < LOS_C_THRESHOLD  → LOS C
# V/C < LOS_D_THRESHOLD  → LOS D
# V/C < 1.0              → LOS E
# V/C >= 1.0             → LOS F
LOS_C_THRESHOLD = 0.8
LOS_D_THRESHOLD = 0.9

# Table PNG crop geometry (fraction of full slide height per phase slot)
CROP_FULL_SLOTS = 27.5
CROP_SLOT_HEIGHT = 2.4
