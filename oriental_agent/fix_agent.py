"""一次性修复脚本 —— 修复 core/agent.py 的缩进问题"""
import os, re, sys

TARGET = r"D:\ai\ai-girlfriend\oriental_agent\core\agent.py"

if not os.path.exists(TARGET):
    # 也许嵌套了一层？搜一下
    for root, dirs, files in os.walk(r"D:\ai\ai-girlfriend\oriental_agent"):
        if 'agent.py' in files and 'core' in root:
            TARGET = os.path.join(root, 'agent.py')
            print(f"[找到文件] {TARGET}")
            break
    else:
        print("[错误] 找不到 agent.py，请告诉我你解压后的实际路径")
        sys.exit(1)

with open(TARGET, 'r', encoding='utf-8') as f:
    src = f.read()

# 目标替换内容（正确的 4 空格缩进版本）
NEW_CHECKS = """    checks = [
        ('commercial_opportunity', 0.85, ['商机', '创业', '创业机会', '创业项目', '市场机会', '好项目', '开店', '做生意', '时机好', '能做吗', '赚钱', '能赚钱']),
        ('investment',            0.85, ['投资', '融资', '回报', '收益', '回报', '投什么', '入股', '风险大']),
        ('strategy',              0.80, ['战略', '策略', '布局', '方向', '怎么做大', '发展']),
        ('competition',           0.80, ['竞争', '对手', '格局', '打败', '脱颖而出', '价格战']),
        ('prediction',            0.75, ['预测', '卜', '卦', '易经', '吉凶', '会怎样', '会成功吗', '起卦', '占卜']),
        ('body_health',           0.70, ['身体', '健康', '养生', '经络', '气血', '精气神', '失眠', '精力']),
        ('cultivation',           0.70, ['修炼', '修真', '打坐', '冥想', '境界', '修行']),
        ('emotion_support',       0.65, ['焦虑', '压力', '心情不好', '抑郁', '痛苦', '难受', '崩溃', '不开心', '难受']),
        ('relationship',          0.65, ['关系', '合作', '人际', '矛盾', '怎么相处', '合伙']),
        ('wisdom_advice',         0.50, ['怎么办', '怎么看', '如何', '该不该', '应该', '建议']),
        ('introduce_self',        0.80, ['介绍', '你是谁', '你能做', '你是干什么']),
        ('hello',                 0.60, ['你好', 'hi', 'hello', '您好', '在吗', '小缘你好']),
    ]"""

# 用正则找到 checks 块（不管原来缩进化），整体替换
pattern = r'[ \t]*checks\s*=\s*\[(?:.|\r?\n)*?[ \t]*\]'

new_src, count = re.subn(pattern, NEW_CHECKS, src)

if count == 0:
    print("[错误] 没找到 checks 块，请手动打开文件检查")
    sys.exit(1)

# 备份 + 写入
import shutil
shutil.copy2(TARGET, TARGET + '.bak')
with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(new_src)

print(f"[成功] 已修复 {TARGET}")
print(f"[备份] 旧版本存为 {TARGET}.bak")
print("\n现在重启后端:")
print("  cd D:\\ai\\ai-girlfriend\\oriental_agent")
print("  python integration\\api_server_secure.py")
