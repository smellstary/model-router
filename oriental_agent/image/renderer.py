"""
SVG形象渲染器
将形象数据渲染为SVG矢量图形
"""

from typing import Dict, Any, Optional
from image.types import Avatar, SkinTone


class SVGRenderer:
    """SVG形象渲染器"""
    
    def __init__(self, width: int = 400, height: int = 500):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 3
        self.scale = min(width, height) / 2.5
    
    def _get_skin_color(self, skin_tone: SkinTone) -> str:
        """获取肤色"""
        colors = {
            SkinTone.FAIR: "#f8f0e8",
            SkinTone.LIGHT: "#f2e6d8",
            SkinTone.MEDIUM: "#e8d4c4",
            SkinTone.OLIVE: "#d4c4a8",
            SkinTone.TAN: "#c9a96e"
        }
        return colors.get(skin_tone, "#f2e6d8")
    
    def _render_face(self, avatar: Avatar) -> str:
        """渲染脸部"""
        ff = avatar.facial_features
        skin_color = self._get_skin_color(avatar.skin_tone)
        
        # 根据脸型计算尺寸
        face_width = self.scale * (0.4 + ff.face_width * 0.3)
        face_height = self.scale * (0.5 + ff.face_length * 0.3)
        
        face_shapes = {
            "oval": f"""
                <ellipse cx="{self.center_x}" cy="{self.center_y}" 
                         rx="{face_width}" ry="{face_height}" 
                         fill="{skin_color}" stroke="#c9b8a0" stroke-width="1"/>
            """,
            "round": f"""
                <ellipse cx="{self.center_x}" cy="{self.center_y}" 
                         rx="{face_width}" ry="{face_width * 0.9}" 
                         fill="{skin_color}" stroke="#c9b8a0" stroke-width="1"/>
            """,
            "heart": f"""
                <path d="M {self.center_x} {self.center_y - face_height * 0.8}
                        Q {self.center_x + face_width} {self.center_y - face_height * 0.3}
                          {self.center_x + face_width * 0.8} {self.center_y + face_height * 0.2}
                        Q {self.center_x} {self.center_y + face_height * 0.6}
                          {self.center_x - face_width * 0.8} {self.center_y + face_height * 0.2}
                        Q {self.center_x - face_width} {self.center_y - face_height * 0.3}
                          {self.center_x} {self.center_y - face_height * 0.8} Z"
                      fill="{skin_color}" stroke="#c9b8a0" stroke-width="1"/>
            """,
            "square": f"""
                <rect x="{self.center_x - face_width}" y="{self.center_y - face_height}"
                      width="{face_width * 2}" height="{face_height * 2}"
                      rx="{face_width * 0.15}" fill="{skin_color}" 
                      stroke="#c9b8a0" stroke-width="1"/>
            """,
            "long": f"""
                <ellipse cx="{self.center_x}" cy="{self.center_y}" 
                         rx="{face_width * 0.85}" ry="{face_height * 1.1}" 
                         fill="{skin_color}" stroke="#c9b8a0" stroke-width="1"/>
            """,
            "diamond": f"""
                <polygon points="
                    {self.center_x},{self.center_y - face_height * 0.9}
                    {self.center_x + face_width * 0.9},{self.center_y}
                    {self.center_x},{self.center_y + face_height * 0.9}
                    {self.center_x - face_width * 0.9},{self.center_y}"
                    fill="{skin_color}" stroke="#c9b8a0" stroke-width="1"/>
            """
        }
        
        return face_shapes.get(ff.face_shape.value, face_shapes["oval"])
    
    def _render_eyes(self, avatar: Avatar) -> str:
        """渲染眼睛"""
        ff = avatar.facial_features
        mf = avatar.makeup_features
        
        eye_width = self.scale * (0.12 + ff.eye_size * 0.08)
        eye_height = self.scale * (0.08 + ff.eye_size * 0.06)
        eye_spacing = self.scale * (0.15 + ff.eye_spacing * 0.1)
        eye_y = self.center_y - self.scale * (0.15 - ff.eye_height * 0.1)
        
        # 眼白
        eyes = f"""
            <ellipse cx="{self.center_x - eye_spacing}" cy="{eye_y}" 
                     rx="{eye_width}" ry="{eye_height}" 
                     fill="white" stroke="#d4c4b0" stroke-width="1"/>
            <ellipse cx="{self.center_x + eye_spacing}" cy="{eye_y}" 
                     rx="{eye_width}" ry="{eye_height}" 
                     fill="white" stroke="#d4c4b0" stroke-width="1"/>
        """
        
        # 瞳孔
        pupil_size = eye_width * 0.55
        eyes += f"""
            <circle cx="{self.center_x - eye_spacing}" cy="{eye_y}" 
                    r="{pupil_size}" fill="#2c2c2c"/>
            <circle cx="{self.center_x + eye_spacing}" cy="{eye_y}" 
                    r="{pupil_size}" fill="#2c2c2c"/>
            <circle cx="{self.center_x - eye_spacing - pupil_size * 0.3}" cy="{eye_y - pupil_size * 0.3}" 
                    r="{pupil_size * 0.2}" fill="white"/>
            <circle cx="{self.center_x + eye_spacing - pupil_size * 0.3}" cy="{eye_y - pupil_size * 0.3}" 
                    r="{pupil_size * 0.2}" fill="white"/>
        """
        
        # 眼线
        if mf.eyeliner:
            line_thickness = 1 + mf.eyeliner_thickness * 2
            eyes += f"""
                <path d="M {self.center_x - eye_spacing - eye_width} {eye_y}
                        Q {self.center_x - eye_spacing - eye_width * 0.8} {eye_y - eye_height * 0.3}
                          {self.center_x - eye_spacing} {eye_y - eye_height * 0.2}
                        Q {self.center_x - eye_spacing + eye_width * 0.8} {eye_y - eye_height * 0.3}
                          {self.center_x - eye_spacing + eye_width} {eye_y}"
                      stroke="#1a1a1a" stroke-width="{line_thickness}" fill="none"/>
                <path d="M {self.center_x + eye_spacing - eye_width} {eye_y}
                        Q {self.center_x + eye_spacing - eye_width * 0.8} {eye_y - eye_height * 0.3}
                          {self.center_x + eye_spacing} {eye_y - eye_height * 0.2}
                        Q {self.center_x + eye_spacing + eye_width * 0.8} {eye_y - eye_height * 0.3}
                          {self.center_x + eye_spacing + eye_width} {eye_y}"
                      stroke="#1a1a1a" stroke-width="{line_thickness}" fill="none"/>
            """
        
        # 眼影
        if mf.eyeshadow_intensity > 0:
            opacity = 0.3 + mf.eyeshadow_intensity * 0.4
            eyes += f"""
                <ellipse cx="{self.center_x - eye_spacing}" cy="{eye_y - eye_height * 0.5}" 
                         rx="{eye_width * 1.2}" ry="{eye_height * 0.6}" 
                         fill="{mf.eyeshadow_color}" opacity="{opacity}"/>
                <ellipse cx="{self.center_x + eye_spacing}" cy="{eye_y - eye_height * 0.5}" 
                         rx="{eye_width * 1.2}" ry="{eye_height * 0.6}" 
                         fill="{mf.eyeshadow_color}" opacity="{opacity}"/>
            """
        
        return eyes
    
    def _render_nose(self, avatar: Avatar) -> str:
        """渲染鼻子"""
        ff = avatar.facial_features
        
        nose_length = self.scale * (0.25 + ff.nose_length * 0.15)
        nose_width = self.scale * (0.08 + ff.nose_width * 0.06)
        nose_tip_width = self.scale * (0.06 + ff.nose_tip * 0.06)
        
        start_y = self.center_y - self.scale * 0.05
        
        nose = f"""
            <path d="M {self.center_x} {start_y}
                    L {self.center_x} {start_y + nose_length * 0.7}
                    Q {self.center_x + nose_width} {start_y + nose_length * 0.85}
                      {self.center_x + nose_tip_width} {start_y + nose_length}
                    Q {self.center_x} {start_y + nose_length * 0.95}
                      {self.center_x - nose_tip_width} {start_y + nose_length}
                    Q {self.center_x - nose_width} {start_y + nose_length * 0.85}
                      {self.center_x} {start_y + nose_length * 0.7} Z"
                  fill="#e8d4c4" stroke="#d4c4a8" stroke-width="0.5"/>
        """
        
        return nose
    
    def _render_mouth(self, avatar: Avatar) -> str:
        """渲染嘴巴"""
        ff = avatar.facial_features
        mf = avatar.makeup_features
        
        mouth_y = self.center_y + self.scale * 0.15
        mouth_width = self.scale * (0.2 + ff.lip_width * 0.15)
        mouth_height = self.scale * (0.06 + ff.lip_thickness * 0.06)
        curve = ff.lip_curve * 0.5
        
        # 嘴唇
        mouth = f"""
            <path d="M {self.center_x - mouth_width} {mouth_y}
                    Q {self.center_x - mouth_width * 0.5} {mouth_y + mouth_height * (1 + curve)}
                      {self.center_x} {mouth_y + mouth_height * (1 + curve * 0.8)}
                    Q {self.center_x + mouth_width * 0.5} {mouth_y + mouth_height * (1 + curve)}
                      {self.center_x + mouth_width} {mouth_y}"
                  fill="{mf.lipstick_color}" stroke="#c75b7a" stroke-width="1"/>
            <ellipse cx="{self.center_x}" cy="{mouth_y + mouth_height * 0.5}" 
                     rx="{mouth_width * 0.8}" ry="{mouth_height * 0.6}" 
                     fill="white" opacity="{mf.lipstick_gloss * 0.5}"/>
        """
        
        return mouth
    
    def _render_eyebrows(self, avatar: Avatar) -> str:
        """渲染眉毛"""
        ff = avatar.facial_features
        mf = avatar.makeup_features
        
        brow_y = self.center_y - self.scale * (0.28 - ff.eye_height * 0.05)
        brow_spacing = self.scale * (0.15 + ff.eye_spacing * 0.1)
        brow_length = self.scale * (0.18 + ff.eye_spacing * 0.05)
        brow_thickness = 2 + mf.eyebrow_thickness * 3
        brow_arch = mf.eyebrow_arch * 0.3
        
        brow = f"""
            <path d="M {self.center_x - brow_spacing - brow_length * 0.5} {brow_y}
                    Q {self.center_x - brow_spacing} {brow_y - brow_length * brow_arch}
                      {self.center_x - brow_spacing + brow_length * 0.5} {brow_y}"
                  stroke="{mf.eyebrow_color}" stroke-width="{brow_thickness}" 
                  stroke-linecap="round"/>
            <path d="M {self.center_x + brow_spacing - brow_length * 0.5} {brow_y}
                    Q {self.center_x + brow_spacing} {brow_y - brow_length * brow_arch}
                      {self.center_x + brow_spacing + brow_length * 0.5} {brow_y}"
                  stroke="{mf.eyebrow_color}" stroke-width="{brow_thickness}" 
                  stroke-linecap="round"/>
        """
        
        return brow
    
    def _render_blush(self, avatar: Avatar) -> str:
        """渲染腮红"""
        mf = avatar.makeup_features
        
        if mf.blush_intensity <= 0:
            return ""
        
        cheek_y = self.center_y + self.scale * 0.05
        cheek_spacing = self.scale * 0.25
        cheek_radius = self.scale * 0.15
        
        opacity = 0.2 + mf.blush_intensity * 0.4
        
        return f"""
            <ellipse cx="{self.center_x - cheek_spacing}" cy="{cheek_y}" 
                     rx="{cheek_radius}" ry="{cheek_radius * 0.6}" 
                     fill="{mf.blush_color}" opacity="{opacity}"/>
            <ellipse cx="{self.center_x + cheek_spacing}" cy="{cheek_y}" 
                     rx="{cheek_radius}" ry="{cheek_radius * 0.6}" 
                     fill="{mf.blush_color}" opacity="{opacity}"/>
        """
    
    def _render_hair(self, avatar: Avatar) -> str:
        """渲染头发"""
        hf = avatar.hair_features
        
        hair_length = self.scale * (0.4 + hf.length * 0.4)
        hair_volume = 1 + hf.volume * 0.3
        
        hair_styles = {
            "straight_long": f"""
                <ellipse cx="{self.center_x}" cy="{self.center_y - hair_length * 0.2}" 
                         rx="{self.scale * 0.4 * hair_volume}" ry="{hair_length}" 
                         fill="{hf.color}"/>
                <ellipse cx="{self.center_x}" cy="{self.center_y - hair_length * 0.2}" 
                         rx="{self.scale * 0.35 * hair_volume}" ry="{hair_length}" 
                         fill="{hf.highlights if hf.highlights else hf.color}" opacity="0.3"/>
            """,
            "straight_short": f"""
                <ellipse cx="{self.center_x}" cy="{self.center_y - hair_length * 0.1}" 
                         rx="{self.scale * 0.4 * hair_volume}" ry="{hair_length * 0.5}" 
                         fill="{hf.color}"/>
            """,
            "wavy_long": f"""
                <path d="M {self.center_x - self.scale * 0.4 * hair_volume} {self.center_y - hair_length * 0.3}
                        Q {self.center_x - self.scale * 0.3} {self.center_y}
                          {self.center_x - self.scale * 0.35} {self.center_y + hair_length * 0.5}
                        Q {self.center_x - self.scale * 0.2} {self.center_y + hair_length}
                          {self.center_x} {self.center_y + hair_length * 0.9}
                        Q {self.center_x + self.scale * 0.2} {self.center_y + hair_length}
                          {self.center_x + self.scale * 0.35} {self.center_y + hair_length * 0.5}
                        Q {self.center_x + self.scale * 0.3} {self.center_y}
                          {self.center_x + self.scale * 0.4 * hair_volume} {self.center_y - hair_length * 0.3} Z"
                      fill="{hf.color}"/>
            """,
            "wavy_short": f"""
                <path d="M {self.center_x - self.scale * 0.4 * hair_volume} {self.center_y - hair_length * 0.2}
                        Q {self.center_x - self.scale * 0.25} {self.center_y + hair_length * 0.1}
                          {self.center_x} {self.center_y + hair_length * 0.2}
                        Q {self.center_x + self.scale * 0.25} {self.center_y + hair_length * 0.1}
                          {self.center_x + self.scale * 0.4 * hair_volume} {self.center_y - hair_length * 0.2} Z"
                      fill="{hf.color}"/>
            """,
            "bob": f"""
                <rect x="{self.center_x - self.scale * 0.4 * hair_volume}" 
                      y="{self.center_y - hair_length * 0.3}"
                      width="{self.scale * 0.8 * hair_volume}" 
                      height="{hair_length}"
                      rx="{self.scale * 0.1}" fill="{hf.color}"/>
            """,
            "ponytail": f"""
                <ellipse cx="{self.center_x}" cy="{self.center_y - self.scale * 0.3}" 
                         rx="{self.scale * 0.35}" ry="{self.scale * 0.25}" 
                         fill="{hf.color}"/>
                <ellipse cx="{self.center_x}" cy="{self.center_y + hair_length * 0.3}" 
                         rx="{self.scale * 0.15}" ry="{hair_length * 0.7}" 
                         fill="{hf.color}"/>
            """,
            "bun": f"""
                <ellipse cx="{self.center_x}" cy="{self.center_y - self.scale * 0.4}" 
                         rx="{self.scale * 0.35}" ry="{self.scale * 0.25}" 
                         fill="{hf.color}"/>
                <circle cx="{self.center_x}" cy="{self.center_y - self.scale * 0.55}" 
                        r="{self.scale * 0.2}" fill="{hf.color}"/>
            """,
            "shaved": f"""
                <ellipse cx="{self.center_x}" cy="{self.center_y - self.scale * 0.15}" 
                         rx="{self.scale * 0.32}" ry="{self.scale * 0.18}" 
                         fill="{hf.color}"/>
            """
        }
        
        hair = hair_styles.get(hf.style.value, hair_styles["straight_long"])
        
        # 添加刘海
        if hf.bangs:
            bang_length = self.scale * (0.2 + hf.bangs_length * 0.2)
            hair += f"""
                <rect x="{self.center_x - self.scale * 0.45}" 
                      y="{self.center_y - self.scale * 0.3}"
                      width="{self.scale * 0.9}" 
                      height="{bang_length}"
                      rx="{self.scale * 0.05}" fill="{hf.color}"/>
            """
        
        return hair
    
    def _render_accessories(self, avatar: Avatar) -> str:
        """渲染配饰"""
        acc = avatar.accessories
        skin_color = self._get_skin_color(avatar.skin_tone)
        
        accessories = ""
        
        # 耳环
        if acc.earrings:
            ear_y = self.center_y
            ear_x_left = self.center_x - self.scale * 0.4
            ear_x_right = self.center_x + self.scale * 0.4
            
            if acc.earring_style == "stud":
                accessories += f"""
                    <circle cx="{ear_x_left}" cy="{ear_y}" r="{self.scale * 0.04}" fill="#d4af37"/>
                    <circle cx="{ear_x_right}" cy="{ear_y}" r="{self.scale * 0.04}" fill="#d4af37"/>
                """
            elif acc.earring_style == "hoop":
                accessories += f"""
                    <ellipse cx="{ear_x_left}" cy="{ear_y + self.scale * 0.1}" 
                             rx="{self.scale * 0.08}" ry="{self.scale * 0.12}" 
                             fill="none" stroke="#d4af37" stroke-width="2"/>
                    <ellipse cx="{ear_x_right}" cy="{ear_y + self.scale * 0.1}" 
                             rx="{self.scale * 0.08}" ry="{self.scale * 0.12}" 
                             fill="none" stroke="#d4af37" stroke-width="2"/>
                """
            elif acc.earring_style == "drop":
                accessories += f"""
                    <circle cx="{ear_x_left}" cy="{ear_y}" r="{self.scale * 0.03}" fill="#d4af37"/>
                    <path d="M {ear_x_left} {ear_y + self.scale * 0.03}
                            L {ear_x_left} {ear_y + self.scale * 0.2}"
                          stroke="#d4af37" stroke-width="2"/>
                    <diamond cx="{ear_x_left}" cy="{ear_y + self.scale * 0.25}" 
                             rx="{self.scale * 0.05}" ry="{self.scale * 0.07}" 
                             fill="#d4af37"/>
                    <circle cx="{ear_x_right}" cy="{ear_y}" r="{self.scale * 0.03}" fill="#d4af37"/>
                    <path d="M {ear_x_right} {ear_y + self.scale * 0.03}
                            L {ear_x_right} {ear_y + self.scale * 0.2}"
                          stroke="#d4af37" stroke-width="2"/>
                    <diamond cx="{ear_x_right}" cy="{ear_y + self.scale * 0.25}" 
                             rx="{self.scale * 0.05}" ry="{self.scale * 0.07}" 
                             fill="#d4af37"/>
                """
        
        # 项链
        if acc.necklace:
            if acc.necklace_style == "simple":
                accessories += f"""
                    <ellipse cx="{self.center_x}" cy="{self.center_y + self.scale * 0.5}" 
                             rx="{self.scale * 0.25}" ry="{self.scale * 0.15}" 
                             fill="none" stroke="#d4af37" stroke-width="2"/>
                """
            elif acc.necklace_style == "pendant":
                accessories += f"""
                    <path d="M {self.center_x - self.scale * 0.25} {self.center_y + self.scale * 0.35}
                            Q {self.center_x} {self.center_y + self.scale * 0.5}
                              {self.center_x + self.scale * 0.25} {self.center_y + self.scale * 0.35}"
                          stroke="#d4af37" stroke-width="2"/>
                    <circle cx="{self.center_x}" cy="{self.center_y + self.scale * 0.5}" 
                            r="{self.scale * 0.05}" fill="#d4af37"/>
                """
        
        # 眼镜
        if acc.glasses:
            if acc.glasses_style == "cat_eye":
                accessories += f"""
                    <path d="M {self.center_x - self.scale * 0.3} {self.center_y - self.scale * 0.12}
                            Q {self.center_x - self.scale * 0.35} {self.center_y - self.scale * 0.22}
                              {self.center_x - self.scale * 0.25} {self.center_y - self.scale * 0.25}"
                          stroke="#2c2c2c" stroke-width="2" fill="none"/>
                    <ellipse cx="{self.center_x - self.scale * 0.15}" cy="{self.center_y - self.scale * 0.1}" 
                             rx="{self.scale * 0.12}" ry="{self.scale * 0.08}" 
                             fill="rgba(200, 220, 255, 0.3)" stroke="#2c2c2c" stroke-width="2"/>
                    <path d="M {self.center_x + self.scale * 0.3} {self.center_y - self.scale * 0.12}
                            Q {self.center_x + self.scale * 0.35} {self.center_y - self.scale * 0.22}
                              {self.center_x + self.scale * 0.25} {self.center_y - self.scale * 0.25}"
                          stroke="#2c2c2c" stroke-width="2" fill="none"/>
                    <ellipse cx="{self.center_x + self.scale * 0.15}" cy="{self.center_y - self.scale * 0.1}" 
                             rx="{self.scale * 0.12}" ry="{self.scale * 0.08}" 
                             fill="rgba(200, 220, 255, 0.3)" stroke="#2c2c2c" stroke-width="2"/>
                    <path d="M {self.center_x - self.scale * 0.03} {self.center_y - self.scale * 0.1}
                            L {self.center_x + self.scale * 0.03} {self.center_y - self.scale * 0.1}"
                          stroke="#2c2c2c" stroke-width="2"/>
                """
        
        return accessories
    
    def _render_outfit(self, avatar: Avatar) -> str:
        """渲染服装"""
        outfit = avatar.outfit
        
        top_y = self.center_y + self.scale * 0.4
        top_width = self.scale * 0.6
        top_height = self.scale * 0.7
        
        necklines = {
            "round": f"""
                <ellipse cx="{self.center_x}" cy="{top_y}" 
                         rx="{self.scale * 0.12}" ry="{self.scale * 0.1}" 
                         fill="{outfit.color}"/>
            """,
            "v-neck": f"""
                <path d="M {self.center_x - self.scale * 0.12} {top_y}
                        L {self.center_x} {top_y + self.scale * 0.2}
                        L {self.center_x + self.scale * 0.12} {top_y} Z"
                      fill="{outfit.color}"/>
            """,
            "scoop": f"""
                <ellipse cx="{self.center_x}" cy="{top_y + self.scale * 0.05}" 
                         rx="{self.scale * 0.15}" ry="{self.scale * 0.12}" 
                         fill="{outfit.color}"/>
            """,
            "off-shoulder": f"""
                <path d="M {self.center_x - top_width * 0.7} {top_y - self.scale * 0.1}
                        Q {self.center_x} {top_y + self.scale * 0.05}
                          {self.center_x + top_width * 0.7} {top_y - self.scale * 0.1}"
                      stroke="{outfit.color}" stroke-width="{self.scale * 0.15}" 
                      stroke-linecap="round"/>
            """
        }
        
        clothing = f"""
            <rect x="{self.center_x - top_width}" y="{top_y}"
                  width="{top_width * 2}" height="{top_height}"
                  fill="{outfit.color}"/>
        """
        
        clothing += necklines.get(outfit.neckline, necklines["round"])
        
        # 袖子
        if outfit.sleeves == "long":
            clothing += f"""
                <rect x="{self.center_x - top_width - self.scale * 0.15}" 
                      y="{top_y}"
                      width="{self.scale * 0.15}" height="{top_height * 0.8}"
                      fill="{outfit.color}"/>
                <rect x="{self.center_x + top_width}" 
                      y="{top_y}"
                      width="{self.scale * 0.15}" height="{top_height * 0.8}"
                      fill="{outfit.color}"/>
            """
        elif outfit.sleeves == "short":
            clothing += f"""
                <rect x="{self.center_x - top_width - self.scale * 0.12}" 
                      y="{top_y}"
                      width="{self.scale * 0.12}" height="{top_height * 0.3}"
                      fill="{outfit.color}"/>
                <rect x="{self.center_x + top_width}" 
                      y="{top_y}"
                      width="{self.scale * 0.12}" height="{top_height * 0.3}"
                      fill="{outfit.color}"/>
            """
        
        return clothing
    
    def render(self, avatar: Avatar) -> str:
        """渲染完整形象"""
        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="{self.width}" height="{self.height}" fill="#f8f9fa"/>
    
    <!-- 服装 -->
    {self._render_outfit(avatar)}
    
    <!-- 头发 -->
    {self._render_hair(avatar)}
    
    <!-- 脸部 -->
    {self._render_face(avatar)}
    
    <!-- 腮红 -->
    {self._render_blush(avatar)}
    
    <!-- 眉毛 -->
    {self._render_eyebrows(avatar)}
    
    <!-- 眼睛 -->
    {self._render_eyes(avatar)}
    
    <!-- 鼻子 -->
    {self._render_nose(avatar)}
    
    <!-- 嘴巴 -->
    {self._render_mouth(avatar)}
    
    <!-- 配饰 -->
    {self._render_accessories(avatar)}
</svg>
"""
        return svg
    
    def render_to_file(self, avatar: Avatar, file_path: str) -> None:
        """渲染到文件"""
        svg = self.render(avatar)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(svg)
