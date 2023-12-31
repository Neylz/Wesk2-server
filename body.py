from enum import Enum
import datetime
import time
from typing import List




# try:
#     self.apiOutput = json.loads(apiOutput)
# except json.decoder.JSONDecodeError as e:
#     breakpoint("Failed to parse API output to json \n [{}]\n{}".format(apiOutput, e))


class BodyType(Enum):
    FIXED_MARKER = 0  # fixed markers on the border of the arena, reference points
    TARGET = 1  # targets, special type of MOVABLE_BODY
    MOVABLE_BODY = 2  # bodies that can move
    CONNECTED_BODY = 3  # bodies connected to this server


class Body:
    def __init__(self, id: int, Pos: list, Rot: int, type: BodyType, lastSeen=time.time()):
        self.id = id
        self.Pos = Pos
        self.Rot = Rot
        self.type = type
        self.seen = False
        self.lastSeen = lastSeen

    def update(self, Pos: list, Rot: int):
        if self.type == BodyType.FIXED_MARKER:
            print("Can't update fixed marker")
            return -1

        self.Pos = Pos
        self.Rot = Rot
        self.seen = True
        self.lastSeen = time.time()

    def getPos(self):
        return self.Pos

    def get2DPos(self):
        return [self.Pos[0], self.Pos[2]]

    def getRot(self):
        return self.Rot

    def getID(self):
        return self.id

    def getType(self):
        return self.type




def initBodies():
    out = [
        Body(21, [57.5, 0, 125], 180, BodyType.FIXED_MARKER, lastSeen=0),
        Body(22, [112.5, 0, 125], 180, BodyType.FIXED_MARKER, lastSeen=0),
        Body(23, [167.5, 0, 125], 180, BodyType.FIXED_MARKER, lastSeen=0),
        Body(24, [222.5, 0, 125], 180, BodyType.FIXED_MARKER, lastSeen=0),
        Body(25, [277.5, 0, 125], 180, BodyType.FIXED_MARKER, lastSeen=0),

        Body(26, [277.5, 0, 0], 0, BodyType.FIXED_MARKER, lastSeen=0),
        Body(27, [222.5, 0, 0], 0, BodyType.FIXED_MARKER, lastSeen=0),
        Body(28, [167.5, 0, 0], 0, BodyType.FIXED_MARKER, lastSeen=0),
        Body(29, [112.5, 0, 0], 0, BodyType.FIXED_MARKER, lastSeen=0),
        Body(30, [57.5, 0, 0], 0, BodyType.FIXED_MARKER, lastSeen=0),

        Body(31, [335, 0, 62.5], -90, BodyType.FIXED_MARKER, lastSeen=0),
        Body(32, [335, 0, 26], -90, BodyType.FIXED_MARKER, lastSeen=0),
        Body(33, [335, 0, 99], -90, BodyType.FIXED_MARKER, lastSeen=0),

        Body(34, [0, 0, 62.5], 90, BodyType.FIXED_MARKER, lastSeen=0),
        Body(35, [0, 0, 99], 90, BodyType.FIXED_MARKER, lastSeen=0),
        Body(36, [0, 0, 26], 90, BodyType.FIXED_MARKER, lastSeen=0)
    ]

    return out

