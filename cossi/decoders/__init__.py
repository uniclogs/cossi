import enum
from .csim import Csim
from .oreflat0 import Oreflat0
from .oresat0 import Oresat0


class Decoder(enum.Enum):
    CSIM = Csim
    OREFLAT0 = Oreflat0
    ORESAT0 = Oresat0


__all__ = [
    "Csim",
    "Decoder",
    "Oreflat0",
    "Oresat0",
]
