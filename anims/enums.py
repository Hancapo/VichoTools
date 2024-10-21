from enum import Enum

class GroupType(Enum):
    ANIMATIONS = 0
    CLIPS = 1

class ChildType(Enum):
    ANIMATION = 0
    CLIP = 1

class AnimationType(Enum):
    ARMATURE = "ARMATURE"
    MATERIAL = "MATERIAL"
    CAMERA = "CAMERA"