import sys
if sys.version_info.major < 3:
    from flufl.enum import Enum
else:
    from enum import Enum


class Connection(Enum):
    off = 0
    on = 1
