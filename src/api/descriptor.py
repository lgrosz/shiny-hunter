from __future__ import annotations
from dataclasses import dataclass, asdict
from json import dumps, loads, JSONEncoder
from sys import stderr


# TODO SemVer
DESCRIPTOR_VERSION = '0.1.1'

class DescriptorJSONEncoder(JSONEncoder):
    def default(self, o):
        if type(o) is Descriptor:
            return asdict(o)
        return super().default(o)

@dataclass
class Descriptor():
    '''
    A dataclass which has the following members:

    resolvers :: a list of ((x, y), (r, g, b)) values which should be resolved
                 before the shiny pick
    pick_delay :: seconds between the last resovler and when the shiny should
                  be picked
    expected_pick :: ((x, y), (r, g, b)) value which is expected when not shiny
    '''
    resolvers: list[tuple[tuple[int, int], tuple[int, int]]]
    pick_delay: float
    expected_pick: tuple[tuple[int, int], tuple[int, int]]
    colormodel: str
    scalars: [str]
    variance: float
    version: str = DESCRIPTOR_VERSION

    @staticmethod
    def from_json(json: str) -> Descriptor:
        # TODO Somehow losing the tuples. I figured the type annotations would
        # cast it. I guess it's only something to help the language server
        # out.. How can i go about casting these without doing it explicitly to the respective
        d = loads(json, object_hook=lambda d: Descriptor(**d))
        if (d.version != DESCRIPTOR_VERSION):
            print('Descriptor version mismatch. Things may be behave as expected', file=stderr)
        return d

    def to_json(self) -> str:
        return dumps(self, cls=DescriptorJSONEncoder)

