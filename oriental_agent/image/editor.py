"""
智能体形象编辑器 - 核心模块
包含维密亚洲面孔预设模板
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from image.types import (
    Avatar, AvatarPreset, FacialFeatures, HairFeatures,
    MakeupFeatures, Accessories, Outfit,
    FaceShape, EyeShape, HairStyle, SkinTone, MakeupStyle
)


class VictoriaSecretPresets:
    """维密亚洲面孔预设模板"""
    
    # 维密风格亚洲面孔特点：
    # - 鹅蛋脸或心形脸为主
    # - 杏仁眼或单眼皮
    # - 精致五官
    # - 健康肤色
    # - 时尚发型
    
    PRESETS = {
        "model_a": {
            "name": "优雅东方",
            "description": "灵感来自维密舞台上的东方优雅气质",
            "facial_features": FacialFeatures(
                face_shape=FaceShape.OVAL,
                face_width=0.45,
                face_length=0.55,
                eye_shape=EyeShape.ALMOND,
                eye_size=0.55,
                eye_spacing=0.48,
                eye_height=0.52,
                nose_width=0.45,
                nose_length=0.52,
                nose_tip=0.6,
                lip_thickness=0.45,
                lip_width=0.52,
                lip_curve=0.65,
                cheekbones=0.55,
                jawline=0.5,
                forehead=0.48
            ),
            "hair_features": HairFeatures(
                style=HairStyle.STRAIGHT_LONG,
                length=0.85,
                volume=0.45,
                wave_intensity=0.15,
                color="#1a1a1a",
                highlights="#3d3d3d",
                bangs=False
            ),
            "makeup_features": MakeupFeatures(
                style=MakeupStyle.NATURAL,
                foundation_shade="#f2e6d8",
                foundation_coverage=0.6,
                eyeshadow_color="#c9b896",
                eyeshadow_intensity=0.35,
                eyeliner=True,
                eyeliner_thickness=0.25,
                mascara=True,
                mascara_intensity=0.6,
                blush_color="#ffc0cb",
                blush_intensity=0.3,
                lipstick_color="#d47575",
                lipstick_gloss=0.6,
                eyebrow_color="#4a3728",
                eyebrow_thickness=0.45,
                eyebrow_arch=0.55
            ),
            "accessories": Accessories(
                earrings=True,
                earring_style="drop",
                necklace=True,
                necklace_style="simple"
            ),
            "outfit": Outfit(
                type="elegant",
                color="#f8f9fa",
                pattern="solid",
                neckline="off-shoulder",
                sleeves="sleeveless"
            ),
            "skin_tone": SkinTone.LIGHT
        },
        "model_b": {
            "name": "自信光芒",
            "description": "展现亚洲女性的自信与魅力",
            "facial_features": FacialFeatures(
                face_shape=FaceShape.HEART,
                face_width=0.48,
                face_length=0.58,
                eye_shape=EyeShape.MONOLID,
                eye_size=0.52,
                eye_spacing=0.5,
                eye_height=0.48,
                nose_width=0.48,
                nose_length=0.5,
                nose_tip=0.55,
                lip_thickness=0.52,
                lip_width=0.55,
                lip_curve=0.55,
                cheekbones=0.6,
                jawline=0.45,
                forehead=0.52
            ),
            "hair_features": HairFeatures(
                style=HairStyle.WAVY_LONG,
                length=0.8,
                volume=0.6,
                wave_intensity=0.5,
                color="#2d2d2d",
                highlights="#5a4a42",
                bangs=True,
                bangs_length=0.35
            ),
            "makeup_features": MakeupFeatures(
                style=MakeupStyle.GLAM,
                foundation_shade="#ede0d4",
                foundation_coverage=0.7,
                eyeshadow_color="#a0826d",
                eyeshadow_intensity=0.5,
                eyeliner=True,
                eyeliner_thickness=0.4,
                mascara=True,
                mascara_intensity=0.75,
                blush_color="#ffb6c1",
                blush_intensity=0.45,
                lipstick_color="#c75b7a",
                lipstick_gloss=0.75,
                eyebrow_color="#3d2914",
                eyebrow_thickness=0.5,
                eyebrow_arch=0.6
            ),
            "accessories": Accessories(
                earrings=True,
                earring_style="hoop",
                necklace=True,
                necklace_style="pendant",
                bracelet=True,
                bracelet_style="chain"
            ),
            "outfit": Outfit(
                type="formal",
                color="#000000",
                pattern="solid",
                neckline="v-neck",
                sleeves="long"
            ),
            "skin_tone": SkinTone.MEDIUM
        },
        "model_c": {
            "name": "清新自然",
            "description": "邻家女孩般的清新自然美",
            "facial_features": FacialFeatures(
                face_shape=FaceShape.ROUND,
                face_width=0.55,
                face_length=0.48,
                eye_shape=EyeShape.ALMOND,
                eye_size=0.58,
                eye_spacing=0.52,
                eye_height=0.55,
                nose_width=0.5,
                nose_length=0.48,
                nose_tip=0.65,
                lip_thickness=0.55,
                lip_width=0.58,
                lip_curve=0.7,
                cheekbones=0.45,
                jawline=0.4,
                forehead=0.45
            ),
            "hair_features": HairFeatures(
                style=HairStyle.BOB,
                length=0.4,
                volume=0.5,
                wave_intensity=0.2,
                color="#353535",
                highlights=None,
                bangs=True,
                bangs_length=0.4
            ),
            "makeup_features": MakeupFeatures(
                style=MakeupStyle.MINIMAL,
                foundation_shade="#f5ebe0",
                foundation_coverage=0.4,
                eyeshadow_color="#e8dcc8",
                eyeshadow_intensity=0.2,
                eyeliner=False,
                eyeliner_thickness=0.1,
                mascara=True,
                mascara_intensity=0.4,
                blush_color="#ffe4e9",
                blush_intensity=0.25,
                lipstick_color="#f0b4b4",
                lipstick_gloss=0.5,
                eyebrow_color="#5a4a42",
                eyebrow_thickness=0.4,
                eyebrow_arch=0.45
            ),
            "accessories": Accessories(
                earrings=True,
                earring_style="stud"
            ),
            "outfit": Outfit(
                type="casual",
                color="#ffffff",
                pattern="solid",
                neckline="round",
                sleeves="short"
            ),
            "skin_tone": SkinTone.FAIR
        },
        "model_d": {
            "name": "时尚前卫",
            "description": "大胆前卫的时尚风格",
            "facial_features": FacialFeatures(
                face_shape=FaceShape.DIAMOND,
                face_width=0.42,
                face_length=0.55,
                eye_shape=EyeShape.HOODDED,
                eye_size=0.5,
                eye_spacing=0.45,
                eye_height=0.5,
                nose_width=0.42,
                nose_length=0.55,
                nose_tip=0.5,
                lip_thickness=0.48,
                lip_width=0.5,
                lip_curve=0.5,
                cheekbones=0.7,
                jawline=0.55,
                forehead=0.5
            ),
            "hair_features": HairFeatures(
                style=HairStyle.WAVY_SHORT,
                length=0.35,
                volume=0.7,
                wave_intensity=0.6,
                color="#1a1a1a",
                highlights="#8b7355",
                bangs=False
            ),
            "makeup_features": MakeupFeatures(
                style=MakeupStyle.SMOKEY,
                foundation_shade="#eddcd2",
                foundation_coverage=0.75,
                eyeshadow_color="#4a4a4a",
                eyeshadow_intensity=0.7,
                eyeliner=True,
                eyeliner_thickness=0.5,
                mascara=True,
                mascara_intensity=0.85,
                blush_color="#ffb4c4",
                blush_intensity=0.35,
                lipstick_color="#9b4dca",
                lipstick_gloss=0.3,
                eyebrow_color="#2d2d2d",
                eyebrow_thickness=0.6,
                eyebrow_arch=0.65
            ),
            "accessories": Accessories(
                earrings=True,
                earring_style="hoop",
                glasses=True,
                glasses_style="cat_eye"
            ),
            "outfit": Outfit(
                type="formal",
                color="#1a1a1a",
                pattern="solid",
                neckline="v-neck",
                sleeves="sleeveless"
            ),
            "skin_tone": SkinTone.OLIVE
        },
        "model_e": {
            "name": "活力四射",
            "description": "充满青春活力的运动风格",
            "facial_features": FacialFeatures(
                face_shape=FaceShape.LONG,
                face_width=0.45,
                face_length=0.62,
                eye_shape=EyeShape.ROUND,
                eye_size=0.6,
                eye_spacing=0.52,
                eye_height=0.58,
                nose_width=0.48,
                nose_length=0.52,
                nose_tip=0.6,
                lip_thickness=0.5,
                lip_width=0.55,
                lip_curve=0.6,
                cheekbones=0.5,
                jawline=0.48,
                forehead=0.52
            ),
            "hair_features": HairFeatures(
                style=HairStyle.PONYTAIL,
                length=0.75,
                volume=0.55,
                wave_intensity=0.2,
                color="#252525",
                highlights=None,
                bangs=False
            ),
            "makeup_features": MakeupFeatures(
                style=MakeupStyle.BRIGHT,
                foundation_shade="#f0e6d8",
                foundation_coverage=0.5,
                eyeshadow_color="#ffb347",
                eyeshadow_intensity=0.45,
                eyeliner=True,
                eyeliner_thickness=0.2,
                mascara=True,
                mascara_intensity=0.65,
                blush_color="#ff69b4",
                blush_intensity=0.4,
                lipstick_color="#ff6b6b",
                lipstick_gloss=0.8,
                eyebrow_color="#4a3728",
                eyebrow_thickness=0.45,
                eyebrow_arch=0.5
            ),
            "accessories": Accessories(
                earrings=True,
                earring_style="stud",
                bracelet=True,
                bracelet_style="bangle"
            ),
            "outfit": Outfit(
                type="sporty",
                color="#4ecdc4",
                pattern="solid",
                neckline="scoop",
                sleeves="short"
            ),
            "skin_tone": SkinTone.TAN
        }
    }
    
    @classmethod
    def get_preset(cls, preset_id: str) -> Optional[Dict[str, Any]]:
        """获取预设"""
        return cls.PRESETS.get(preset_id)
    
    @classmethod
    def list_presets(cls) -> List[Dict[str, str]]:
        """列出所有预设"""
        return [
            {"id": key, "name": value["name"], "description": value["description"]}
            for key, value in cls.PRESETS.items()
        ]


class AvatarEditor:
    """形象编辑器"""
    
    def __init__(self):
        self._avatars: Dict[str, Avatar] = {}
        self._presets: Dict[str, AvatarPreset] = {}
        
        # 加载预设
        self._load_presets()
    
    def _load_presets(self):
        """加载维密预设"""
        for preset_id, data in VictoriaSecretPresets.PRESETS.items():
            preset = AvatarPreset(
                preset_id=preset_id,
                name=data["name"],
                description=data["description"],
                category="celebrity",
                facial_features=data["facial_features"],
                hair_features=data["hair_features"],
                makeup_features=data["makeup_features"],
                accessories=data["accessories"],
                outfit=data["outfit"]
            )
            self._presets[preset_id] = preset
    
    def create_from_preset(self, preset_id: str, name: str = "") -> Avatar:
        """
        从预设创建形象
        
        Args:
            preset_id: 预设ID
            name: 形象名称
            
        Returns:
            创建的形象
        """
        preset = self._presets.get(preset_id)
        if not preset:
            raise ValueError(f"预设 {preset_id} 不存在")
        
        avatar = Avatar(
            name=name if name else preset.name,
            display_name=preset.name,
            facial_features=preset.facial_features,
            hair_features=preset.hair_features,
            makeup_features=preset.makeup_features,
            accessories=preset.accessories,
            outfit=preset.outfit,
            preset_source=preset_id
        )
        
        self._avatars[avatar.avatar_id] = avatar
        return avatar
    
    def create_empty(self, name: str = "东方智慧") -> Avatar:
        """创建空形象"""
        avatar = Avatar(name=name)
        self._avatars[avatar.avatar_id] = avatar
        return avatar
    
    def get_avatar(self, avatar_id: str) -> Optional[Avatar]:
        """获取形象"""
        return self._avatars.get(avatar_id)
    
    def update_avatar(self, avatar_id: str, updates: Dict[str, Any]) -> Avatar:
        """
        更新形象
        
        Args:
            avatar_id: 形象ID
            updates: 更新数据
            
        Returns:
            更新后的形象
        """
        avatar = self._avatars.get(avatar_id)
        if not avatar:
            raise ValueError(f"形象 {avatar_id} 不存在")
        
        # 更新面部特征
        if "facial_features" in updates:
            for key, value in updates["facial_features"].items():
                if hasattr(avatar.facial_features, key):
                    setattr(avatar.facial_features, key, value)
        
        # 更新发型特征
        if "hair_features" in updates:
            for key, value in updates["hair_features"].items():
                if hasattr(avatar.hair_features, key):
                    setattr(avatar.hair_features, key, value)
        
        # 更新妆容特征
        if "makeup_features" in updates:
            for key, value in updates["makeup_features"].items():
                if hasattr(avatar.makeup_features, key):
                    setattr(avatar.makeup_features, key, value)
        
        # 更新配饰
        if "accessories" in updates:
            for key, value in updates["accessories"].items():
                if hasattr(avatar.accessories, key):
                    setattr(avatar.accessories, key, value)
        
        # 更新服装
        if "outfit" in updates:
            for key, value in updates["outfit"].items():
                if hasattr(avatar.outfit, key):
                    setattr(avatar.outfit, key, value)
        
        # 更新其他属性
        if "name" in updates:
            avatar.name = updates["name"]
        if "display_name" in updates:
            avatar.display_name = updates["display_name"]
        if "skin_tone" in updates:
            avatar.skin_tone = SkinTone(updates["skin_tone"])
        if "emotion" in updates:
            avatar.emotion = updates["emotion"]
        if "pose" in updates:
            avatar.pose = updates["pose"]
        
        avatar.last_modified = datetime.now()
        return avatar
    
    def adjust_feature(self, avatar_id: str, feature_path: str, value: float):
        """
        微调特征值
        
        Args:
            avatar_id: 形象ID
            feature_path: 特征路径，如 "facial_features.eye_size"
            value: 新的特征值 (0-1)
        """
        avatar = self._avatars.get(avatar_id)
        if not avatar:
            raise ValueError(f"形象 {avatar_id} 不存在")
        
        parts = feature_path.split('.')
        obj = avatar
        for part in parts[:-1]:
            obj = getattr(obj, part)
        
        # 如果是数值类型，限制在 0-1 范围内；否则直接设置
        if isinstance(value, (int, float)):
            setattr(obj, parts[-1], max(0.0, min(1.0, float(value))))
        else:
            setattr(obj, parts[-1], value)
        avatar.last_modified = datetime.now()
    
    def delete_avatar(self, avatar_id: str) -> bool:
        """删除形象"""
        if avatar_id in self._avatars:
            del self._avatars[avatar_id]
            return True
        return False
    
    def list_avatars(self) -> List[Dict[str, str]]:
        """列出所有形象"""
        return [
            {"avatar_id": aid, "name": avatar.name, "display_name": avatar.display_name}
            for aid, avatar in self._avatars.items()
        ]
    
    def list_presets(self) -> List[Dict[str, str]]:
        """列出所有预设"""
        return [
            {"preset_id": p.preset_id, "name": p.name, "description": p.description}
            for p in self._presets.values()
        ]
    
    def export_avatar(self, avatar_id: str) -> Dict[str, Any]:
        """导出形象数据"""
        avatar = self._avatars.get(avatar_id)
        if not avatar:
            raise ValueError(f"形象 {avatar_id} 不存在")
        return avatar.to_dict()
    
    def import_avatar(self, avatar_data: Dict[str, Any]) -> Avatar:
        """导入形象数据"""
        avatar = Avatar(
            avatar_id=avatar_data.get("avatar_id", str(datetime.now().timestamp())),
            name=avatar_data.get("name", "东方智慧"),
            display_name=avatar_data.get("display_name", "")
        )
        
        # 导入面部特征
        if "facial_features" in avatar_data:
            ff = avatar_data["facial_features"]
            avatar.facial_features.face_shape = FaceShape(ff.get("face_shape", "oval"))
            avatar.facial_features.face_width = ff.get("face_width", 0.5)
            avatar.facial_features.face_length = ff.get("face_length", 0.5)
            avatar.facial_features.eye_shape = EyeShape(ff.get("eye_shape", "almond"))
            avatar.facial_features.eye_size = ff.get("eye_size", 0.5)
            avatar.facial_features.eye_spacing = ff.get("eye_spacing", 0.5)
            avatar.facial_features.eye_height = ff.get("eye_height", 0.5)
            avatar.facial_features.nose_width = ff.get("nose_width", 0.5)
            avatar.facial_features.nose_length = ff.get("nose_length", 0.5)
            avatar.facial_features.nose_tip = ff.get("nose_tip", 0.5)
            avatar.facial_features.lip_thickness = ff.get("lip_thickness", 0.5)
            avatar.facial_features.lip_width = ff.get("lip_width", 0.5)
            avatar.facial_features.lip_curve = ff.get("lip_curve", 0.5)
            avatar.facial_features.cheekbones = ff.get("cheekbones", 0.5)
            avatar.facial_features.jawline = ff.get("jawline", 0.5)
            avatar.facial_features.forehead = ff.get("forehead", 0.5)
        
        # 导入发型特征
        if "hair_features" in avatar_data:
            hf = avatar_data["hair_features"]
            avatar.hair_features.style = HairStyle(hf.get("style", "straight_long"))
            avatar.hair_features.length = hf.get("length", 0.7)
            avatar.hair_features.volume = hf.get("volume", 0.5)
            avatar.hair_features.wave_intensity = hf.get("wave_intensity", 0.3)
            avatar.hair_features.color = hf.get("color", "#2c2c2c")
            avatar.hair_features.highlights = hf.get("highlights")
            avatar.hair_features.bangs = hf.get("bangs", False)
            avatar.hair_features.bangs_length = hf.get("bangs_length", 0.3)
        
        # 导入妆容特征
        if "makeup_features" in avatar_data:
            mf = avatar_data["makeup_features"]
            avatar.makeup_features.style = MakeupStyle(mf.get("style", "natural"))
            avatar.makeup_features.foundation_shade = mf.get("foundation_shade", "#f5e6d3")
            avatar.makeup_features.foundation_coverage = mf.get("foundation_coverage", 0.5)
            avatar.makeup_features.eyeshadow_color = mf.get("eyeshadow_color", "#d4c4b0")
            avatar.makeup_features.eyeshadow_intensity = mf.get("eyeshadow_intensity", 0.3)
            avatar.makeup_features.eyeliner = mf.get("eyeliner", True)
            avatar.makeup_features.eyeliner_thickness = mf.get("eyeliner_thickness", 0.3)
            avatar.makeup_features.mascara = mf.get("mascara", True)
            avatar.makeup_features.mascara_intensity = mf.get("mascara_intensity", 0.5)
            avatar.makeup_features.blush_color = mf.get("blush_color", "#ffb7c5")
            avatar.makeup_features.blush_intensity = mf.get("blush_intensity", 0.3)
            avatar.makeup_features.lipstick_color = mf.get("lipstick_color", "#e87a8a")
            avatar.makeup_features.lipstick_gloss = mf.get("lipstick_gloss", 0.5)
            avatar.makeup_features.eyebrow_color = mf.get("eyebrow_color", "#5a4a42")
            avatar.makeup_features.eyebrow_thickness = mf.get("eyebrow_thickness", 0.5)
            avatar.makeup_features.eyebrow_arch = mf.get("eyebrow_arch", 0.5)
        
        # 导入配饰
        if "accessories" in avatar_data:
            acc = avatar_data["accessories"]
            avatar.accessories.earrings = acc.get("earrings", False)
            avatar.accessories.earring_style = acc.get("earring_style", "stud")
            avatar.accessories.necklace = acc.get("necklace", False)
            avatar.accessories.necklace_style = acc.get("necklace_style", "simple")
            avatar.accessories.bracelet = acc.get("bracelet", False)
            avatar.accessories.bracelet_style = acc.get("bracelet_style", "bangle")
            avatar.accessories.glasses = acc.get("glasses", False)
            avatar.accessories.glasses_style = acc.get("glasses_style", "cat_eye")
        
        # 导入服装
        if "outfit" in avatar_data:
            out = avatar_data["outfit"]
            avatar.outfit.type = out.get("type", "casual")
            avatar.outfit.color = out.get("color", "#ffffff")
            avatar.outfit.pattern = out.get("pattern", "solid")
            avatar.outfit.neckline = out.get("neckline", "round")
            avatar.outfit.sleeves = out.get("sleeves", "long")
        
        # 导入其他属性
        if "skin_tone" in avatar_data:
            avatar.skin_tone = SkinTone(avatar_data["skin_tone"])
        if "emotion" in avatar_data:
            avatar.emotion = avatar_data["emotion"]
        if "pose" in avatar_data:
            avatar.pose = avatar_data["pose"]
        
        self._avatars[avatar.avatar_id] = avatar
        return avatar
