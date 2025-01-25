from collections.abc import Mapping

from .shapes import *

type KeySetType = Mapping[Shape2D, Shape3D]

KS_MIXED: KeySetType = {
    circle:   prism,
    triangle: cylinder,
    square:   cone,
    }
KS_DOUBLE_1: KeySetType = {
    circle:   cube,
    triangle: sphere,
    square:   pyramid,
    }
KS_DOUBLE_2: KeySetType = {
    circle:   pyramid,
    triangle: cube,
    square:   sphere,
    }

__all__ = 'KeySetType', 'KS_MIXED', 'KS_DOUBLE_1', 'KS_DOUBLE_2'
