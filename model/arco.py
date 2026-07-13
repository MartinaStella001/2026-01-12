from dataclasses import dataclass

from model.Constructor import Constructor


@dataclass
class Arco:
    costruttore1: Constructor
    costruttore2: Constructor
    numPiloti: int