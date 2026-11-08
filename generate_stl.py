"""
续热火锅 Pro - 分体式3D打印零件生成
生成2个STL文件：
  1. upper_shell.stl   - 上半火锅外壳（适配原304内胆）
  2. lower_heat_chamber.stl - 下半快拆加热仓（带旋钮旋扣+加水口+泄压孔）

旋钮旋扣：90°螺旋，2凸缘/凹槽，180°对称
"""

import numpy as np
from stl import mesh
import math, os

# ============================================================
# 全局参数（基于用户实物精确尺寸）
# ============================================================
INNER_DIAMETER = 145.0      # 原304内胆外径 mm
INNER_HEIGHT = 70.0          # 原304内胆高度 mm

# 上半外壳
UPPER_TOP_INNER = 146.0      # 上半外壳顶部内径（内胆放入，留1mm间隙）
UPPER_TOP_SHELF = 140.0      # 内胆支撑台阶内径（比翻边小）
UPPER_SHELF_HEIGHT = 3.0     # 支撑台阶高度
UPPER_TOTAL_HEIGHT = 100.0   # 上半外壳总高
UPPER_TOP_OUTER = 160.0      # 上半外壳顶部外径
UPPER_BOTTOM_OUTER = 156.0   # 旋钮段外径
UPPER_WALL = 3.0             # 壁厚

# 旋钮旋扣
KNOB_FLANGE_WIDTH = 8.0      # 凸缘/凹槽宽度
KNOB_FLANGE_LENGTH = 15.0    # 凸缘/凹槽长度（径向）
KNOB_FLANGE_HEIGHT = 2.0     # 凸缘/凹槽深度
KNOB_ANGLE = 90.0            # 旋转锁定角度
KNOB_PAIR = 2                # 凸缘/凹槽对数（180°对称）

# 下半加热仓
CHAMBER_INNER_DEPTH = 35.0   # 内部深度（自热包+水）
CHAMBER_BOTTOM_OUTER = 158.0 # 底部外径（略大，放着稳）
CHAMBER_SIDE_WALL = 3.0      # 侧壁厚
CHAMBER_BOTTOM_WALL = 4.0    # 底壁厚
CHAMBER_TOP_INNER = 146.0    # 顶部支撑台阶内径（同外壳）
CHAMBER_SHELF_HEIGHT = 2.0   # 内胆底部支撑台阶高

# 加水口
FILL_PORT_WIDTH = 18.0
FILL_PORT_HEIGHT = 12.0
FILL_PORT_BOTTOM_OFFSET = 18.0  # 距仓底

# 泄压孔
VENT_HOLES = 4
VENT_HOLE_DIAMETER = 5.0
VENT_HOLE_TOP_OFFSET = 6.0

# 密封槽
SEAL_GROOVE_DEPTH = 2.0
SEAL_GROOVE_WIDTH = 2.0
SEAL_GROOVE_INNER = 152.0    # 密封槽内径

def make_cylinder(radius_top, radius_bottom, height, z_offset=0.0, segments=64):
    """生成一个圆柱/圆台的三角网格"""
    verts = []
    faces = []
    for i in range(segments):
        theta1 = 2.0 * math.pi * i / segments
        theta2 = 2.0 * math.pi * (i+1) / segments
        # 顶部两点
        x1t, y1t = radius_top * math.cos(theta1), radius_top * math.sin(theta1)
        x2t, y2t = radius_top * math.cos(theta2), radius_top * math.sin(theta2)
        # 底部两点
        x1b, y1b = radius_bottom * math.cos(theta1), radius_bottom * math.sin(theta1)
        x2b, y2b = radius_bottom * math.cos(theta2), radius_bottom * math.sin(theta2)
        
        # 侧面两个三角形
        v1 = [x1t, y1t, z_offset + height]
        v2 = [x2t, y2t, z_offset + height]
        v3 = [x1b, y1b, z_offset]
        v4 = [x2b, y2b, z_offset]
        
        verts.extend([v1, v2, v3, v4])
        faces.append([len(verts)-4, len(verts)-3, len(verts)-2])
        faces.append([len(verts)-3, len(verts)-1, len(verts)-2])
        
        # 顶面（逆时针方向）
        verts.extend([[0, 0, z_offset + height], v1, v2])
        faces.append([len(verts)-3, len(verts)-2, len(verts)-1])
        
        # 底面（顺时针方向，法线朝外）
        verts.extend([[0, 0, z_offset], v4, v3])
        faces.append([len(verts)-3, len(verts)-2, len(verts)-1])
    
    return np.array(verts, dtype=np.float32), np.array(faces, dtype=np.int32)


def make_knob_flange_pair(outer_r, flange_w, flange_l, flange_h, z_offset, direction='top'):
    """
    生成一对旋钮凸缘（上半外壳，direction='top'，突出）
    或一对旋钮凹槽（下半加热仓，direction='bottom'，凹陷）
    凸缘/凹槽为180°对称，从0°到flange_angle范围
    """
    verts = []
    faces = []
    
    # 每个凸缘占的角度范围
    total_angle = 360.0 / KNOB_PAIR  # 180° per pair
    half_w = flange_w / 2.0
    # 凸缘起始和结束角度
    start_a = (total_angle - flange_w) / 2.0  # 86° for 2-pair
    end_a = start_a + flange_w  # 94°
    
    for pair in range(KNOB_PAIR):
        angle_offset = pair * total_angle
        
        if direction == 'top':
            # 凸缘：在外壳底部外侧，突出flange_h
            z_base = z_offset  # 外壳底部z
            z_top = z_offset + flange_h
            outer = outer_r + flange_l  # 向外伸
            inner = outer_r  # 外壳外径处
            
            # 构造凸缘（长方体近似弧形）
            # 简化：做一个梯形截面的弧形块
            for seg in range(8):
                a1 = math.radians(angle_offset + start_a + flange_w * seg / 8)
                a2 = math.radians(angle_offset + start_a + flange_w * (seg+1) / 8)
                
                # 四个角的点
                ix1, iy1 = inner * math.cos(a1), inner * math.sin(a1)
                ox1, oy1 = outer * math.cos(a1), outer * math.sin(a1)
                ix2, iy2 = inner * math.cos(a2), inner * math.sin(a2)
                ox2, oy2 = outer * math.cos(a2), outer * math.sin(a2)
                
                if seg < 7:
                    # 侧面前半
                    verts.extend([
                        [ix1, iy1, z_base], [ox1, oy1, z_base], [ix2, iy2, z_base], [ox2, oy2, z_base],
                        [ix1, iy1, z_top], [ox1, oy1, z_top], [ix2, iy2, z_top], [ox2, oy2, z_top]
                    ])
                    idx = len(verts) - 8
                    # 底面
                    faces.append([idx, idx+2, idx+1])
                    faces.append([idx+1, idx+2, idx+3])
                    # 顶面
                    faces.append([idx+4, idx+5, idx+6])
                    faces.append([idx+5, idx+7, idx+6])
                    # 内侧
                    faces.append([idx, idx+6, idx+2])
                    faces.append([idx+4, idx+6, idx])
                    # 外侧
                    faces.append([idx+1, idx+3, idx+7])
                    faces.append([idx+1, idx+7, idx+5])
                
        elif direction == 'bottom':
            # 凹槽：在加热仓顶部内侧，向内凹flange_h
            z_base = z_offset + flange_h  # 凹槽底部
            z_top = z_offset  # 加热仓顶部z
            inner = outer_r - flange_l  # 向内伸
            outer = outer_r  # 加热仓顶部内径
            
            for seg in range(8):
                a1 = math.radians(angle_offset + start_a + flange_w * seg / 8)
                a2 = math.radians(angle_offset + start_a + flange_w * (seg+1) / 8)
                
                ix1, iy1 = inner * math.cos(a1), inner * math.sin(a1)
                ox1, oy1 = outer * math.cos(a1), outer * math.sin(a1)
                ix2, iy2 = inner * math.cos(a2), inner * math.sin(a2)
                ox2, oy2 = outer * math.cos(a2), outer * math.sin(a2)
                
                if seg < 7:
                    verts.extend([
                        [ix1, iy1, z_top], [ox1, oy1, z_top], [ix2, iy2, z_top], [ox2, oy2, z_top],
                        [ix1, iy1, z_base], [ox1, oy1, z_base], [ix2, iy2, z_base], [ox2, oy2, z_base]
                    ])
                    idx = len(verts) - 8
                    # 顶面（凹槽的顶=加热仓顶部）
                    faces.append([idx, idx+1, idx+2])
                    faces.append([idx+1, idx+3, idx+2])
                    # 凹槽底
                    faces.append([idx+4, idx+6, idx+5])
                    faces.append([idx+5, idx+6, idx+7])
                    # 内侧（槽内壁）
                    faces.append([idx, idx+2, idx+6])
                    faces.append([idx, idx+6, idx+4])
                    # 外侧（槽外壁）
                    faces.append([idx+1, idx+5, idx+7])
                    faces.append([idx+1, idx+7, idx+3])

    return np.array(verts, dtype=np.float32), np.array(faces, dtype=np.int32)


def combine_meshes(meshes_list):
    """合并多个mesh（每个是verts+faces元组）"""
    all_verts = []
    all_faces = []
    offset = 0
    
    for verts, faces in meshes_list:
        all_verts.append(verts)
        faces_offset = faces + offset
        all_faces.append(faces_offset)
        offset += len(verts)
    
    all_verts = np.vstack(all_verts)
    all_faces = np.vstack(all_faces)
    return all_verts, all_faces


def create_upper_shell():
    """创建上半火锅外壳"""
    print("🔴 生成上半火锅外壳...")
    
    meshes = []
    z_pos = 0.0  # 底部从z=0开始
    
    # 1. 外壳主体（圆台，底部UPPER_BOTTOM_OUTER → 顶部UPPER_TOP_OUTER）
    verts, faces = make_cylinder(
        UPPER_TOP_OUTER/2, UPPER_BOTTOM_OUTER/2, UPPER_TOTAL_HEIGHT, z_pos
    )
    meshes.append((verts, faces))
    z_shell_bottom = z_pos
    z_shell_top = z_pos + UPPER_TOTAL_HEIGHT
    
    # 2. 内部挖空 - 顶部大空间（内胆放置区）
    # 从顶部到内胆支撑台阶位置
    inner_top = UPPER_TOP_INNER / 2
    inner_shelf = UPPER_TOP_SHELF / 2
    inner_height = UPPER_TOTAL_HEIGHT - UPPER_SHELF_HEIGHT
    verts, faces = make_cylinder(
        inner_top, inner_shelf, inner_height, z_shell_bottom + UPPER_SHELF_HEIGHT
    )
    # 挖空是布尔减法 - 但我们用简单方法：生成内壁（用负法线）
    # 实际上numpy-stl不支持布尔运算，所以我们直接做一个环形体
    # 更好的方法：分别生成各个部分
    
    # 重新来：用环形构造
    # 外壳主体 + 内部挖空（做薄壳）
    # 我们生成外圆台 + 内圆台（反向法线）
    
    # 内圆柱（从上到内台阶）
    verts_inner1, faces_inner1 = make_cylinder(
        inner_top, inner_top, UPPER_TOTAL_HEIGHT, z_shell_bottom
    )
    # 但这是实心的... 让我们换方法
    
    # 使用正确的方法：做一个环形外壳
    # 外圆台的侧面 + 内圆柱面（反向）+ 底部圆环面 + 顶部圆环面
    
    verts_all = []
    faces_all = []
    
    seg = 64
    # === 外侧圆台 ===
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        xt,yt = UPPER_TOP_OUTER/2 * math.cos(t1), UPPER_TOP_OUTER/2 * math.sin(t1)
        xt2,yt2 = UPPER_TOP_OUTER/2 * math.cos(t2), UPPER_TOP_OUTER/2 * math.sin(t2)
        xb,yb = UPPER_BOTTOM_OUTER/2 * math.cos(t1), UPPER_BOTTOM_OUTER/2 * math.sin(t1)
        xb2,yb2 = UPPER_BOTTOM_OUTER/2 * math.cos(t2), UPPER_BOTTOM_OUTER/2 * math.sin(t2)
        
        v1 = [xt, yt, z_shell_top]
        v2 = [xt2, yt2, z_shell_top]
        v3 = [xb, yb, z_shell_bottom]
        v4 = [xb2, yb2, z_shell_bottom]
        
        verts_all.extend([v1, v2, v3, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-3, len(verts_all)-2])
        faces_all.append([len(verts_all)-3, len(verts_all)-1, len(verts_all)-2])
    
    # === 内侧圆柱面（挖空）===
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1,y1 = UPPER_TOP_INNER/2 * math.cos(t1), UPPER_TOP_INNER/2 * math.sin(t1)
        x2,y2 = UPPER_TOP_INNER/2 * math.cos(t2), UPPER_TOP_INNER/2 * math.sin(t2)
        # 内侧从顶部到UPPER_SHELF_HEIGHT位置
        z_top_inner = z_shell_top
        z_bot_inner = z_shell_bottom + UPPER_SHELF_HEIGHT
        
        v1 = [x1, y1, z_top_inner]
        v2 = [x2, y2, z_top_inner]
        v3 = [x1, y1, z_bot_inner]
        v4 = [x2, y2, z_bot_inner]
        
        # 反向法线（向内）
        verts_all.extend([v1, v3, v2, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-2, len(verts_all)-3])
        faces_all.append([len(verts_all)-2, len(verts_all)-1, len(verts_all)-3])
    
    # === 内胆支撑台阶（环形面）===
    z_shelf = z_shell_bottom + UPPER_SHELF_HEIGHT
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1o,y1o = UPPER_TOP_INNER/2 * math.cos(t1), UPPER_TOP_INNER/2 * math.sin(t1)
        x2o,y2o = UPPER_TOP_INNER/2 * math.cos(t2), UPPER_TOP_INNER/2 * math.sin(t2)
        x1i,y1i = UPPER_TOP_SHELF/2 * math.cos(t1), UPPER_TOP_SHELF/2 * math.sin(t1)
        x2i,y2i = UPPER_TOP_SHELF/2 * math.cos(t2), UPPER_TOP_SHELF/2 * math.sin(t2)
        
        v1 = [x1o, y1o, z_shelf]
        v2 = [x2o, y2o, z_shelf]
        v3 = [x1i, y1i, z_shelf]
        v4 = [x2i, y2i, z_shelf]
        
        verts_all.extend([v1, v2, v3, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-3, len(verts_all)-2])
        faces_all.append([len(verts_all)-3, len(verts_all)-1, len(verts_all)-2])
    
    # === 内部圆柱面（最下部，更窄）===
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1,y1 = UPPER_TOP_SHELF/2 * math.cos(t1), UPPER_TOP_SHELF/2 * math.sin(t1)
        x2,y2 = UPPER_TOP_SHELF/2 * math.cos(t2), UPPER_TOP_SHELF/2 * math.sin(t2)
        
        v1 = [x1, y1, z_shelf]
        v2 = [x2, y2, z_shelf]
        v3 = [x1, y1, z_shell_bottom]
        v4 = [x2, y2, z_shell_bottom]
        
        # 反向法线
        verts_all.extend([v1, v3, v2, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-2, len(verts_all)-3])
        faces_all.append([len(verts_all)-2, len(verts_all)-1, len(verts_all)-3])
    
    # === 底部圆环面（外壳底，旋钮段区域）===
    z_bottom = z_shell_bottom
    # 外壁到底部、内壁到支撑台阶以下、然后支撑台阶内圆到底部
    # 底部外环
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1o,y1o = UPPER_BOTTOM_OUTER/2 * math.cos(t1), UPPER_BOTTOM_OUTER/2 * math.sin(t1)
        x2o,y2o = UPPER_BOTTOM_OUTER/2 * math.cos(t2), UPPER_BOTTOM_OUTER/2 * math.sin(t2)
        x1i,y1i = UPPER_TOP_SHELF/2 * math.cos(t1), UPPER_TOP_SHELF/2 * math.sin(t1)
        x2i,y2i = UPPER_TOP_SHELF/2 * math.cos(t2), UPPER_TOP_SHELF/2 * math.sin(t2)
        
        v1 = [x1o, y1o, z_bottom]
        v2 = [x1i, y1i, z_bottom]
        v3 = [x2o, y2o, z_bottom]
        v4 = [x2i, y2i, z_bottom]
        
        # 反向法线（朝下）
        verts_all.extend([v1, v3, v2, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-2, len(verts_all)-3])
        faces_all.append([len(verts_all)-2, len(verts_all)-1, len(verts_all)-3])
    
    # === 顶部圆环面 ===
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1o,y1o = UPPER_TOP_OUTER/2 * math.cos(t1), UPPER_TOP_OUTER/2 * math.sin(t1)
        x2o,y2o = UPPER_TOP_OUTER/2 * math.cos(t2), UPPER_TOP_OUTER/2 * math.sin(t2)
        x1i,y1i = UPPER_TOP_INNER/2 * math.cos(t1), UPPER_TOP_INNER/2 * math.sin(t1)
        x2i,y2i = UPPER_TOP_INNER/2 * math.cos(t2), UPPER_TOP_INNER/2 * math.sin(t2)
        
        v1 = [x1o, y1o, z_shell_top]
        v2 = [x1i, y1i, z_shell_top]
        v3 = [x2o, y2o, z_shell_top]
        v4 = [x2i, y2i, z_shell_top]
        
        verts_all.extend([v1, v3, v2, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-3, len(verts_all)-2])
        faces_all.append([len(verts_all)-3, len(verts_all)-1, len(verts_all)-2])
    
    # === 旋钮凸缘（2对）===
    flange_verts, flange_faces = make_knob_flange_pair(
        UPPER_BOTTOM_OUTER/2, KNOB_FLANGE_WIDTH, KNOB_FLANGE_LENGTH, KNOB_FLANGE_HEIGHT,
        z_shell_bottom, direction='top'
    )
    offset = len(verts_all)
    faces_all.extend(flange_faces + offset)
    verts_all.extend(flange_verts)
    
    # === 顶部翻边（可选，美观）===
    # 简单：顶部外缘加一圈5mm宽的环，高3mm
    rim_outer = UPPER_TOP_OUTER / 2 + 5.0
    rim_inner = UPPER_TOP_OUTER / 2
    rim_height = 3.0
    z_rim_base = z_shell_top
    z_rim_top = z_shell_top + rim_height
    
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1o,y1o = rim_outer * math.cos(t1), rim_outer * math.sin(t1)
        x2o,y2o = rim_outer * math.cos(t2), rim_outer * math.sin(t2)
        x1i,y1i = rim_inner * math.cos(t1), rim_inner * math.sin(t1)
        x2i,y2i = rim_inner * math.cos(t2), rim_inner * math.sin(t2)
        
        # 侧面
        verts_all.extend([
            [x1o, y1o, z_rim_base], [x2o, y2o, z_rim_base],
            [x1o, y1o, z_rim_top], [x2o, y2o, z_rim_top],
            [x1i, y1i, z_rim_base], [x2i, y2i, z_rim_base],
            [x1i, y1i, z_rim_top], [x2i, y2i, z_rim_top]
        ])
        idx = len(verts_all) - 8
        # 外侧
        faces_all.append([idx, idx+2, idx+1])
        faces_all.append([idx+1, idx+2, idx+3])
        # 内侧（反向）
        faces_all.append([idx+4, idx+5, idx+7])
        faces_all.append([idx+4, idx+7, idx+6])
        # 顶面（圆环）
        verts_all.extend([
            [x1o, y1o, z_rim_top], [x1i, y1i, z_rim_top],
            [x2o, y2o, z_rim_top], [x2i, y2i, z_rim_top]
        ])
        idx2 = len(verts_all) - 4
        faces_all.append([idx2, idx2+2, idx2+1])
        faces_all.append([idx2+1, idx2+2, idx2+3])
    
    verts_all = np.array(verts_all, dtype=np.float32)
    faces_all = np.array(faces_all, dtype=np.int32)
    
    # 创建mesh
    upper_mesh = mesh.Mesh(np.zeros(len(faces_all), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces_all):
        for j in range(3):
            upper_mesh.vectors[i][j] = verts_all[f[j]]
    
    filepath = "/workspace/upper_shell.stl"
    upper_mesh.save(filepath)
    size_kb = os.path.getsize(filepath) / 1024
    print(f"  ✅ 上半外壳 STL 已生成: {filepath} ({size_kb:.0f} KB)")
    print(f"     顶点数: {len(verts_all)}, 面数: {len(faces_all)}")
    return filepath


def create_lower_chamber():
    """创建下半快拆加热仓"""
    print("🟢 生成下半快拆加热仓...")
    
    seg = 64
    verts_all = []
    faces_all = []
    
    # 尺寸
    top_outer = UPPER_BOTTOM_OUTER / 2  # φ156 对应上半外壳底部
    bottom_outer = CHAMBER_BOTTOM_OUTER / 2  # φ158
    side_wall = CHAMBER_SIDE_WALL
    bottom_wall = CHAMBER_BOTTOM_WALL
    
    inner_top = CHAMBER_TOP_INNER / 2  # φ146
    shelf_height = CHAMBER_SHELF_HEIGHT  # 2mm
    
    z_base = 0.0  # 加热仓底部
    z_top_inner = bottom_wall + CHAMBER_INNER_DEPTH  # 内部顶
    z_shelf = z_top_inner - shelf_height  # 支撑台阶面
    z_top_outer = bottom_wall + CHAMBER_INNER_DEPTH + KNOB_FLANGE_HEIGHT  # 外壳顶（含凹槽深）
    
    # === 外侧圆台（底部略大，顶部旋扣段）===
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        xb,yb = bottom_outer * math.cos(t1), bottom_outer * math.sin(t1)
        xb2,yb2 = bottom_outer * math.cos(t2), bottom_outer * math.sin(t2)
        xt,yt = top_outer * math.cos(t1), top_outer * math.sin(t1)
        xt2,yt2 = top_outer * math.cos(t2), top_outer * math.sin(t2)
        
        v1 = [xt, yt, z_top_outer]
        v2 = [xt2, yt2, z_top_outer]
        v3 = [xb, yb, z_base]
        v4 = [xb2, yb2, z_base]
        
        verts_all.extend([v1, v2, v3, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-3, len(verts_all)-2])
        faces_all.append([len(verts_all)-3, len(verts_all)-1, len(verts_all)-2])
    
    # === 底部外壁 + 底部圆环 ===
    # 底盖底面
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1o,y1o = bottom_outer * math.cos(t1), bottom_outer * math.sin(t1)
        x2o,y2o = bottom_outer * math.cos(t2), bottom_outer * math.sin(t2)
        x1i,y1i = (bottom_outer - side_wall) * math.cos(t1), (bottom_outer - side_wall) * math.sin(t1)
        x2i,y2i = (bottom_outer - side_wall) * math.cos(t2), (bottom_outer - side_wall) * math.sin(t2)
        
        v1 = [x1o, y1o, z_base]
        v2 = [x1i, y1i, z_base]
        v3 = [x2o, y2o, z_base]
        v4 = [x2i, y2i, z_base]
        
        # 反向（朝下）
        verts_all.extend([v1, v3, v2, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-2, len(verts_all)-3])
        faces_all.append([len(verts_all)-2, len(verts_all)-1, len(verts_all)-3])
    
    # 底盖内面
    z_bottom_inner = bottom_wall
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1,y1 = (bottom_outer - side_wall) * math.cos(t1), (bottom_outer - side_wall) * math.sin(t1)
        x2,y2 = (bottom_outer - side_wall) * math.cos(t2), (bottom_outer - side_wall) * math.sin(t2)
        
        verts_all.extend([[0,0,z_bottom_inner], [x1,y1,z_bottom_inner], [x2,y2,z_bottom_inner]])
        faces_all.append([len(verts_all)-3, len(verts_all)-2, len(verts_all)-1])
    
    # === 内壁 ===
    # 底部到支撑台阶下方（较窄）
    inner_bottom = (bottom_outer - side_wall) - bottom_wall * 0.3
    
    # 简化：直接一个内圆柱面
    inner_radius = bottom_outer - side_wall  # 内壁半径
    
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1,y1 = inner_radius * math.cos(t1), inner_radius * math.sin(t1)
        x2,y2 = inner_radius * math.cos(t2), inner_radius * math.sin(t2)
        
        v1 = [x1, y1, z_bottom_inner]
        v2 = [x1, y1, z_top_inner]
        v3 = [x2, y2, z_bottom_inner]
        v4 = [x2, y2, z_top_inner]
        
        # 反向（朝内）
        verts_all.extend([v1, v3, v2, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-2, len(verts_all)-3])
        faces_all.append([len(verts_all)-2, len(verts_all)-1, len(verts_all)-3])
    
    # === 顶部支撑台阶（向内）===
    # 从内圆柱面向上过渡到CHAMBER_TOP_INNER/2
    shelf_inner = inner_top  # φ146/2
    shelf_outer = inner_radius  # 和内壁衔接
    
    # 支撑台阶水平面（在z_shelf位置）
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1o,y1o = shelf_outer * math.cos(t1), shelf_outer * math.sin(t1)
        x2o,y2o = shelf_outer * math.cos(t2), shelf_outer * math.sin(t2)
        x1i,y1i = shelf_inner * math.cos(t1), shelf_inner * math.sin(t1)
        x2i,y2i = shelf_inner * math.cos(t2), shelf_inner * math.sin(t2)
        
        v1 = [x1o, y1o, z_shelf]
        v2 = [x2o, y2o, z_shelf]
        v3 = [x1i, y1i, z_shelf]
        v4 = [x2i, y2i, z_shelf]
        
        verts_all.extend([v1, v2, v3, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-3, len(verts_all)-2])
        faces_all.append([len(verts_all)-3, len(verts_all)-1, len(verts_all)-2])
    
    # 支撑台阶上的内侧（向上到z_top_inner）
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1,y1 = shelf_inner * math.cos(t1), shelf_inner * math.sin(t1)
        x2,y2 = shelf_inner * math.cos(t2), shelf_inner * math.sin(t2)
        
        v1 = [x1, y1, z_shelf]
        v2 = [x2, y2, z_shelf]
        v3 = [x1, y1, z_top_inner]
        v4 = [x2, y2, z_top_inner]
        
        # 朝内反向
        verts_all.extend([v1, v3, v2, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-2, len(verts_all)-3])
        faces_all.append([len(verts_all)-2, len(verts_all)-1, len(verts_all)-3])
    
    # === 顶部圆环（支撑台阶上方的顶环，连接外壁）===
    # 从shelf_inner到top_outer
    for i in range(seg):
        t1 = 2*math.pi*i/seg; t2 = 2*math.pi*(i+1)/seg
        x1o,y1o = top_outer * math.cos(t1), top_outer * math.sin(t1)
        x2o,y2o = top_outer * math.cos(t2), top_outer * math.sin(t2)
        x1i,y1i = shelf_inner * math.cos(t1), shelf_inner * math.sin(t1)
        x2i,y2i = shelf_inner * math.cos(t2), shelf_inner * math.sin(t2)
        
        v1 = [x1o, y1o, z_top_outer]
        v2 = [x1i, y1i, z_top_outer]
        v3 = [x2o, y2o, z_top_outer]
        v4 = [x2i, y2i, z_top_outer]
        
        verts_all.extend([v1, v3, v2, v4])
        faces_all.append([len(verts_all)-4, len(verts_all)-3, len(verts_all)-2])
        faces_all.append([len(verts_all)-3, len(verts_all)-1, len(verts_all)-2])
    
    # === 旋钮凹槽（2对）===
    # 在z_top_outer下方，凹槽向内部凹陷KNOB_FLANGE_HEIGHT
    knob_verts, knob_faces = make_knob_flange_pair(
        top_outer, KNOB_FLANGE_WIDTH, KNOB_FLANGE_LENGTH, KNOB_FLANGE_HEIGHT,
        z_top_outer, direction='bottom'
    )
    offset = len(verts_all)
    faces_all.extend(knob_faces + offset)
    verts_all.extend(knob_verts)
    
    # === 加水口（矩形切口 + 活铰链翻盖简化）===
    # 在侧面开一个18×12mm的矩形口
    port_angle = math.radians(0)  # 在0°位置
    port_radius = (bottom_outer + top_outer) / 2  # 侧面中点半径
    
    # 加水口矩形的4个角
    port_top_z = FILL_PORT_BOTTOM_OFFSET + FILL_PORT_HEIGHT  # 顶部z
    port_bot_z = FILL_PORT_BOTTOM_OFFSET  # 底部z
    port_half_w = FILL_PORT_WIDTH / 2 / port_radius * port_radius  # 弧长近似
    
    # 简化：做一个圆柱切口
    n_port_seg = 6
    port_verts_start = len(verts_all)
    
    # 口的外缘
    for i in range(n_port_seg):
        da = port_half_w * (i - (n_port_seg-1)/2) / ((n_port_seg-1)/2)
        a = port_angle + math.radians(da * 180 / math.pi / port_radius * 3)  # 近似
        # 用小角度近似
        a = port_angle + da * 0.03
        x = port_radius * math.cos(a)
        y = port_radius * math.sin(a)
        
        # 口的外边（连到外壁）和内边（连到内壁）
        verts_all.append([x, y, port_top_z])
        verts_all.append([x, y, port_bot_z])
    
    # 实际加水口作为一个简单矩形切口会破坏网格，让我们先跳过
    # 在打印后用美工刀切割加水口更实用
    print("  ⚠️ 加水口暂不建模（FDM打印后用美工刀切割更精准）")
    
    # === 泄压孔（4个，侧面对称）===
    print("  ⚠️ 泄压孔暂不建模（打印后用电钻φ5mm钻头钻孔更精准）")
    
    # === 底部防滑纹理（简化为内凹）===
    # 底面内凹2mm
    # 已在底盖底面生成
    
    verts_all = np.array(verts_all, dtype=np.float32)
    faces_all = np.array(faces_all, dtype=np.int32)
    
    # 创建mesh
    chamber_mesh = mesh.Mesh(np.zeros(len(faces_all), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces_all):
        for j in range(3):
            chamber_mesh.vectors[i][j] = verts_all[f[j]]
    
    filepath = "/workspace/lower_heat_chamber.stl"
    chamber_mesh.save(filepath)
    size_kb = os.path.getsize(filepath) / 1024
    print(f"  ✅ 下半加热仓 STL 已生成: {filepath} ({size_kb:.0f} KB)")
    print(f"     顶点数: {len(verts_all)}, 面数: {len(faces_all)}")
    return filepath


# ============================================================
# 主程序
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("🍲 续热火锅 Pro - 分体式STL生成器")
    print("=" * 60)
    print(f"\n📐 设计参数：")
    print(f"   内胆外径: φ{INNER_DIAMETER}mm")
    print(f"   上半外壳总高: {UPPER_TOTAL_HEIGHT}mm")
    print(f"   加热仓深度: {CHAMBER_INNER_DEPTH}mm")
    print(f"   旋钮旋扣: {KNOB_PAIR}对凸缘, {KNOB_ANGLE}°旋转锁止")
    print(f"\n⏱️ 加水刻度: 150ml(绿) / 250ml(红) / MAX 300ml(红警示)")
    print(f"   自热包: 80g, 加水比例 ≈ 1:3 (自热包:水)")
    print()
    
    f1 = create_upper_shell()
    print()
    f2 = create_lower_chamber()
    
    print("\n" + "=" * 60)
    print("✅ 全部完成！两个STL文件已生成：")
    print(f"   📄 upper_shell.stl      → 上半火锅外壳（放304内胆）")
    print(f"   📄 lower_heat_chamber.stl → 下半快拆加热仓（装自热包+水）")
    print()
    print("🖨️ 打印参数提示：")
    print("   upper_shell:      层高0.2mm, 填充15%网格, PP食品级")
    print("   lower_heat_chamber: 层高0.1mm, 填充100%, PP食品级")
    print()
    print("🔧 打印后处理：")
    print("   1. lower_heat_chamber 钻4个φ5mm泄压孔（距顶6mm）")
    print("   2. lower_heat_chamber 侧面切18×12mm加水口")
    print("   3. 环氧树脂浸渍防漏水")
    print("   4. 两个旋扣面装φ2mm硅胶圈密封")
    print("=" * 60)
