"""
智能体形象系统
基于SVG的可自定义虚拟形象编辑器
"""

from image.types import (
    Avatar, AvatarPreset, FacialFeatures, HairFeatures,
    MakeupFeatures, Accessories, Outfit,
    FaceShape, EyeShape, HairStyle, SkinTone, MakeupStyle
)

from image.editor import AvatarEditor, VictoriaSecretPresets
from image.renderer import SVGRenderer

__all__ = [
    "Avatar",
    "AvatarPreset",
    "FacialFeatures",
    "HairFeatures",
    "MakeupFeatures",
    "Accessories",
    "Outfit",
    "FaceShape",
    "EyeShape",
    "HairStyle",
    "SkinTone",
    "MakeupStyle",
    "AvatarEditor",
    "VictoriaSecretPresets",
    "SVGRenderer"
]
