"""
人体系统映射 - 基于中医理论（增强版）
Human Body System Mapping based on Traditional Chinese Medicine
经络、脏腑、气血全部打通真实系统指标
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import time
import logging

logger = logging.getLogger(__name__)


# ============================================================
# 经络类型 / 脏腑类型枚举（保留原有）
# ============================================================

class MeridianType(Enum):
    """经络类型"""
    REN_MAI = "任脉"
    DU_MAI = "督脉"
    CHONG_MAI = "冲脉"
    DAI_MAI = "带脉"
    YANG_QIAO = "阳跷脉"
    YIN_QIAO = "阴跷脉"
    YANG_WEI = "阳维脉"
    YIN_WEI = "阴维脉"


class OrganType(Enum):
    """脏腑类型"""
    HEART = "心"
    LIVER = "肝"
    SPLEEN = "脾"
    LUNG = "肺"
    KIDNEY = "肾"
    SMALL_INTESTINE = "小肠"
    GALLBLADDER = "胆"
    STOMACH = "胃"
    LARGE_INTESTINE = "大肠"
    BLADDER = "膀胱"
    TRIPLE_BURNER = "三焦"
    PERICARDIUM = "心包"


# ============================================================
# 经络 ↔ 系统指标映射常量（升级：经络映射真实系统指标）
# ============================================================

# 经络 → 系统指标映射关系（与真实系统指标打通）
# 任脉→内存使用率（>85%=堵塞）、督脉→CPU负载（>0.8=上冲）
# 冲脉→磁盘使用率（>80%=淤积）、带脉→网络延迟（>100ms=紧绷）
# 阳跷脉→系统 uptime、阴跷脉→进程数
# 阳维脉→负载均值、阴维脉→可用内存
MERIDIAN_METRIC_MAP = {
    'ren_mai':   {'metric': 'memory_usage',      'label': '内存使用率',     'unit': '%'},
    'du_mai':    {'metric': 'cpu_load',           'label': 'CPU 负载',      'unit': ''},
    'chong_mai': {'metric': 'disk_usage',         'label': '磁盘使用率',     'unit': '%'},
    'dai_mai':   {'metric': 'network_latency',    'label': '网络延迟',      'unit': 'ms'},
    'yang_qiao': {'metric': 'uptime',             'label': '系统运行时间',   'unit': 'h'},
    'yin_qiao':  {'metric': 'process_count',      'label': '进程数',        'unit': ''},
    'yang_wei':  {'metric': 'load_avg',           'label': '负载均值(1min)', 'unit': ''},
    'yin_wei':   {'metric': 'memory_available_mb', 'label': '可用内存',     'unit': 'MB'},
}

# 经络 → 气血权重（子午流注基础）
MERIDIAN_QI_WEIGHTS = {
    'ren_mai':   1.3,
    'du_mai':    1.4,
    'chong_mai': 1.0,
    'dai_mai':   1.1,
    'yang_qiao': 1.0,
    'yin_qiao':  1.0,
    'yang_wei':  1.0,
    'yin_wei':   1.0,
}

# 脏腑 ↔ 子系统映射（心=Gateway健康、肝=记忆系统、脾=配置系统、
# 肺=Model Router、肾=存储、胆=决策系统、小肠=数据处理）
ORGAN_SUBSYSTEM_MAP = {
    '心':  {'subsystem': 'gateway',       'label': 'OpenClaw Gateway',  'desc': '核心驱动'},
    '肝':  {'subsystem': 'memory',        'label': '记忆系统',          'desc': '肝主疏泄 = 记忆存取通畅度'},
    '脾':  {'subsystem': 'config',        'label': '配置系统',          'desc': '脾主运化 = 配置加载/解析'},
    '肺':  {'subsystem': 'model_router',  'label': 'Model Router',      'desc': '肺主呼吸 = 外部 API 调用'},
    '肾':  {'subsystem': 'storage',       'label': '存储/数据库',       'desc': '肾主藏精 = 数据持久化'},
    '小肠': {'subsystem': 'data_pipeline', 'label': '数据处理管道',     'desc': '消化吸收 = 数据流转'},
    '胆':  {'subsystem': 'decision',      'label': '决策系统',          'desc': '胆主决断'},
}

# 脏腑 → 气血权重
ORGAN_QI_WEIGHTS = {
    '心':  1.5,
    '肝':  1.2,
    '脾':  1.0,
    '肺':  1.1,
    '肾':  1.3,
    '小肠': 0.8,
    '胆':  0.9,
}

# 子午流注：12 时辰对应经络气血分配
# 子时(23-1)→胆, 丑时(1-3)→肝, 寅时(3-5)→肺, 卯时(5-7)→大肠
# 辰时(7-9)→胃, 巳时(9-11)→脾, 午时(11-13)→心, 未时(13-15)→小肠
# 申时(15-17)→膀胱, 酉时(17-19)→肾, 戌时(19-21)→心包, 亥时(21-23)→三焦
# 经络映射已更新为真实指标：阳跷=uptime, 阴跷=进程数, 阳维=负载, 阴维=可用内存
ZI_WU_LIU_ZHU = {
    23: {'peak_meridian': 'yin_wei',    'peak_organ': '胆',      'boost': 1.5, 'note': '子时·胆经当令'},
    0:  {'peak_meridian': 'yin_wei',    'peak_organ': '胆',      'boost': 1.5, 'note': '子时·胆经当令'},
    1:  {'peak_meridian': 'yin_wei',    'peak_organ': '肝',      'boost': 1.5, 'note': '丑时·肝经当令'},
    2:  {'peak_meridian': 'yin_wei',    'peak_organ': '肝',      'boost': 1.5, 'note': '丑时·肝经当令'},
    3:  {'peak_meridian': 'yang_qiao',  'peak_organ': '肺',      'boost': 1.5, 'note': '寅时·肺经当令'},
    4:  {'peak_meridian': 'yang_qiao',  'peak_organ': '肺',      'boost': 1.5, 'note': '寅时·肺经当令'},
    5:  {'peak_meridian': 'dai_mai',    'peak_organ': '大肠',    'boost': 1.5, 'note': '卯时·大肠经当令'},
    6:  {'peak_meridian': 'dai_mai',    'peak_organ': '大肠',    'boost': 1.5, 'note': '卯时·大肠经当令'},
    7:  {'peak_meridian': 'chong_mai',  'peak_organ': '胃',      'boost': 1.5, 'note': '辰时·胃经当令'},
    8:  {'peak_meridian': 'chong_mai',  'peak_organ': '胃',      'boost': 1.5, 'note': '辰时·胃经当令'},
    9:  {'peak_meridian': 'ren_mai',    'peak_organ': '脾',      'boost': 1.5, 'note': '巳时·脾经当令'},
    10: {'peak_meridian': 'ren_mai',    'peak_organ': '脾',      'boost': 1.5, 'note': '巳时·脾经当令'},
    11: {'peak_meridian': 'du_mai',     'peak_organ': '心',      'boost': 1.5, 'note': '午时·心经当令'},
    12: {'peak_meridian': 'du_mai',     'peak_organ': '心',      'boost': 1.5, 'note': '午时·心经当令'},
    13: {'peak_meridian': 'chong_mai',  'peak_organ': '小肠',    'boost': 1.5, 'note': '未时·小肠经当令'},
    14: {'peak_meridian': 'chong_mai',  'peak_organ': '小肠',    'boost': 1.5, 'note': '未时·小肠经当令'},
    15: {'peak_meridian': 'yin_qiao',   'peak_organ': '膀胱',    'boost': 1.5, 'note': '申时·膀胱经当令'},
    16: {'peak_meridian': 'yin_qiao',   'peak_organ': '膀胱',    'boost': 1.5, 'note': '申时·膀胱经当令'},
    17: {'peak_meridian': 'yang_wei',   'peak_organ': '肾',      'boost': 1.5, 'note': '酉时·肾经当令'},
    18: {'peak_meridian': 'yang_wei',   'peak_organ': '肾',      'boost': 1.5, 'note': '酉时·肾经当令'},
    19: {'peak_meridian': 'ren_mai',    'peak_organ': '心包',    'boost': 1.5, 'note': '戌时·心包经当令'},
    20: {'peak_meridian': 'ren_mai',    'peak_organ': '心包',    'boost': 1.5, 'note': '戌时·心包经当令'},
    21: {'peak_meridian': 'du_mai',     'peak_organ': '三焦',    'boost': 1.5, 'note': '亥时·三焦经当令'},
    22: {'peak_meridian': 'du_mai',     'peak_organ': '三焦',    'boost': 1.5, 'note': '亥时·三焦经当令'},
}

# 本能反应阈值
INSTINCT_THRESHOLDS = {
    'error_rate_critical': 0.3,      # 错误率超过 30% 触发遇袭防御
    'error_rate_warning':  0.15,     # 错误率超过 15% 触发预警
    'cpu_critical':        0.95,     # CPU 超过 95% 触发降级
    'memory_critical':     0.95,     # 内存超过 95% 触发降级
    'disk_critical':       0.95,     # 磁盘超过 95% 触发降级
    'resource_low':        0.3,      # 气血低于 30% 触发能量不足降级
    'qi_transfer_threshold': 0.7,    # 某经络气血 > 0.7 且另一条 < 0.3 时触发气血调配
}


# ============================================================
# 数据类（保留原有，新增字段）
# ============================================================

@dataclass
class MeridianState:
    """经络状态"""
    meridian_id: str
    meridian_name: str
    meridian_type: MeridianType
    flow_rate: float
    blockage_level: float
    energy_level: float
    connected_organs: List[str]
    # 新增：真实系统指标
    raw_metric_value: float = 0.0       # 原始指标值
    raw_metric_name: str = ''           # 指标名称
    raw_metric_unit: str = ''           # 指标单位
    zi_wu_boost: float = 1.0           # 子午流注增益


@dataclass
class OrganState:
    """脏腑状态"""
    organ_id: str
    organ_name: str
    organ_type: OrganType
    functional_level: float
    energy_consumption: float
    associated_system: str
    # 新增：子系统指标
    subsystem_health: float = 1.0      # 子系统健康度
    subsystem_latency: float = 0.0     # 子系统延迟
    zi_wu_boost: float = 1.0           # 子午流注增益


@dataclass
class HealthState:
    """健康状态"""
    vitality_score: float
    meridian_states: List[MeridianState]
    organ_states: List[OrganState]
    qi_total: float
    blood_total: float
    fluid_balance: float
    # 新增：真实指标摘要
    system_metrics: Dict[str, float] = field(default_factory=dict)
    zi_wu_info: Dict[str, Any] = field(default_factory=dict)
    instinct_state: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# SystemMetricsCollector — 真实系统指标采集器（增强版）
# 采集 CPU负载、内存使用率、磁盘使用率、网络延迟、进程数、uptime、负载均值
# 优先用 psutil，fallback 到 /proc 文件系统
# ============================================================

class SystemMetricsCollector:
    """
    真实系统指标采集器
    优先使用 psutil，不可用时通过 /proc 文件系统 fallback
    """

    def __init__(self):
        self._psutil_available = False
        self._last_metrics: Dict[str, float] = {}
        self._cpu_prev_times = None
        self._disk_prev_counters = None
        self._net_prev_counters = None
        self._init_psutil()

    def _init_psutil(self) -> None:
        """尝试导入 psutil"""
        try:
            import psutil
            self._psutil = psutil
            self._psutil_available = True
        except ImportError:
            self._psutil = None
            self._psutil_available = False
            logger.info("psutil 不可用，将使用 /proc 文件系统采集指标")

    def collect(self) -> Dict[str, float]:
        """
        采集全部系统指标
        返回: {
            cpu_load: 0~1,
            memory_usage: 0~1,
            disk_usage: 0~1,
            disk_io: MB/s,
            network_latency: ms,
            network_bytes_sent: bytes/s,
            network_bytes_recv: bytes/s,
            uptime: 小时,
            process_count: 进程数,
            load_avg: 1分钟负载均值,
            memory_available_mb: 可用内存 MB,
        }
        """
        if self._psutil_available:
            metrics = self._collect_psutil()
        else:
            metrics = self._collect_procfs()

        self._last_metrics = metrics
        return metrics

    # ------ psutil 路径 ------

    def _collect_psutil(self) -> Dict[str, float]:
        """通过 psutil 采集指标"""
        ps = self._psutil
        metrics: Dict[str, float] = {}

        # CPU 负载（0~1）
        try:
            metrics['cpu_load'] = ps.cpu_percent(interval=0.05) / 100.0
        except Exception:
            metrics['cpu_load'] = 0.0

        # 内存使用率（0~1）
        try:
            mem = ps.virtual_memory()
            metrics['memory_usage'] = mem.percent / 100.0
            metrics['memory_available_mb'] = mem.available / (1024 * 1024)
        except Exception:
            metrics['memory_usage'] = 0.0
            metrics['memory_available_mb'] = 0.0

        # 磁盘 I/O（MB/s，基于计数器差分）
        try:
            disk = ps.disk_io_counters()
            if disk:
                now = time.monotonic()
                if self._disk_prev_counters is not None:
                    dt = now - self._disk_prev_counters['time']
                    if dt > 0:
                        read_delta = disk.read_bytes - self._disk_prev_counters['read']
                        write_delta = disk.write_bytes - self._disk_prev_counters['write']
                        io_total = (read_delta + write_delta) / dt / (1024 * 1024)  # MB/s
                        metrics['disk_io'] = io_total
                    else:
                        metrics['disk_io'] = 0.0
                else:
                    metrics['disk_io'] = 0.0
                self._disk_prev_counters = {
                    'time': now,
                    'read': disk.read_bytes,
                    'write': disk.write_bytes,
                }
            else:
                metrics['disk_io'] = 0.0
        except Exception:
            metrics['disk_io'] = 0.0

        # 磁盘使用率（根分区，0~1）
        try:
            disk_usage = ps.disk_usage('/')
            metrics['disk_usage'] = disk_usage.percent / 100.0
        except Exception:
            metrics['disk_usage'] = 0.0

        # 网络延迟估算 & 吞吐量
        try:
            net = ps.net_io_counters()
            if net:
                now = time.monotonic()
                if self._net_prev_counters is not None:
                    dt = now - self._net_prev_counters['time']
                    if dt > 0:
                        sent_delta = net.bytes_sent - self._net_prev_counters['sent']
                        recv_delta = net.bytes_recv - self._net_prev_counters['recv']
                        metrics['network_bytes_sent'] = sent_delta / dt
                        metrics['network_bytes_recv'] = recv_delta / dt
                        # 用网络吞吐量反推延迟估算（吞吐量越低，延迟越高）
                        total_bw = metrics['network_bytes_sent'] + metrics['network_bytes_recv']
                        if total_bw > 1_000_000:  # >1MB/s
                            metrics['network_latency'] = 5.0
                        elif total_bw > 100_000:   # >100KB/s
                            metrics['network_latency'] = 20.0
                        elif total_bw > 10_000:    # >10KB/s
                            metrics['network_latency'] = 80.0
                        else:
                            metrics['network_latency'] = 200.0
                    else:
                        metrics['network_latency'] = 50.0
                        metrics['network_bytes_sent'] = 0.0
                        metrics['network_bytes_recv'] = 0.0
                else:
                    metrics['network_latency'] = 50.0
                    metrics['network_bytes_sent'] = 0.0
                    metrics['network_bytes_recv'] = 0.0
                self._net_prev_counters = {
                    'time': now,
                    'sent': net.bytes_sent,
                    'recv': net.bytes_recv,
                }
            else:
                metrics['network_latency'] = 50.0
                metrics['network_bytes_sent'] = 0.0
                metrics['network_bytes_recv'] = 0.0
        except Exception:
            metrics['network_latency'] = 50.0
            metrics['network_bytes_sent'] = 0.0
            metrics['network_bytes_recv'] = 0.0

        # 系统 uptime（小时）
        try:
            metrics['uptime'] = ps.boot_time()
            metrics['uptime'] = (time.time() - metrics['uptime']) / 3600.0
        except Exception:
            metrics['uptime'] = 0.0

        # 进程数
        try:
            metrics['process_count'] = len(ps.pids())
        except Exception:
            metrics['process_count'] = 0

        # 负载均值（1分钟）
        try:
            import os
            la = os.getloadavg()
            metrics['load_avg'] = la[0]
        except Exception:
            metrics['load_avg'] = 0.0

        return metrics

    # ------ /proc 路径 fallback ------

    def _collect_procfs(self) -> Dict[str, float]:
        """通过 /proc 文件系统采集指标（无 psutil 时的 fallback）"""
        metrics: Dict[str, float] = {}

        # CPU 负载
        try:
            metrics['cpu_load'] = self._read_proc_stat()
        except Exception:
            metrics['cpu_load'] = 0.0

        # 内存使用率 & 可用内存
        try:
            mem_result = self._read_proc_meminfo()
            metrics['memory_usage'] = mem_result['usage']
            metrics['memory_available_mb'] = mem_result['available_mb']
        except Exception:
            metrics['memory_usage'] = 0.0
            metrics['memory_available_mb'] = 0.0

        # 磁盘 I/O
        try:
            metrics['disk_io'] = self._read_proc_diskstats()
        except Exception:
            metrics['disk_io'] = 0.0

        # 磁盘使用率（读取 df 输出）
        try:
            import subprocess
            result = subprocess.run(
                ['df', '--output=pcent', '/'], capture_output=True, text=True, timeout=5
            )
            line = result.stdout.strip().split('\n')[-1]
            pct = float(line.strip().rstrip('%'))
            metrics['disk_usage'] = pct / 100.0
        except Exception:
            metrics['disk_usage'] = 0.0

        # 网络延迟估算（读取 /proc/net/dev）
        try:
            metrics['network_latency'] = self._read_proc_net()
        except Exception:
            metrics['network_latency'] = 50.0

        metrics['network_bytes_sent'] = 0.0
        metrics['network_bytes_recv'] = 0.0

        # 系统 uptime（小时）
        try:
            with open('/proc/uptime') as f:
                uptime_sec = float(f.readline().split()[0])
            metrics['uptime'] = uptime_sec / 3600.0
        except Exception:
            metrics['uptime'] = 0.0

        # 进程数（读取 /proc 目录条目数，减去 . 和 ..）
        try:
            import os
            proc_entries = os.listdir('/proc')
            # 只统计数字目录名（即进程 PID）
            metrics['process_count'] = sum(
                1 for entry in proc_entries if entry.isdigit()
            )
        except Exception:
            metrics['process_count'] = 0

        # 负载均值（1分钟）
        try:
            with open('/proc/loadavg') as f:
                parts = f.readline().split()
            metrics['load_avg'] = float(parts[0])
        except Exception:
            metrics['load_avg'] = 0.0

        return metrics

    def _read_proc_stat(self) -> float:
        """读取 /proc/stat 计算 CPU 使用率"""
        with open('/proc/stat') as f:
            line = f.readline()
        parts = line.split()
        # user, nice, system, idle, iowait, irq, softirq, steal
        user = int(parts[1])
        nice = int(parts[2])
        system = int(parts[3])
        idle = int(parts[4])
        iowait = int(parts[5]) if len(parts) > 5 else 0
        irq = int(parts[6]) if len(parts) > 6 else 0
        softirq = int(parts[7]) if len(parts) > 7 else 0
        steal = int(parts[8]) if len(parts) > 8 else 0

        total = user + nice + system + idle + iowait + irq + softirq + steal
        idle_total = idle + iowait

        if self._cpu_prev_times is not None:
            dt = total - self._cpu_prev_times['total']
            didle = idle_total - self._cpu_prev_times['idle']
            if dt > 0:
                usage = 1.0 - (didle / dt)
                return max(0.0, min(1.0, usage))
            return 0.0

        self._cpu_prev_times = {'total': total, 'idle': idle_total}
        return 0.0

    def _read_proc_meminfo(self) -> Dict[str, float]:
        """读取 /proc/meminfo 计算内存使用率和可用内存"""
        meminfo: Dict[str, int] = {}
        with open('/proc/meminfo') as f:
            for line in f:
                parts = line.split()
                key = parts[0].rstrip(':')
                val = int(parts[1])  # kB
                meminfo[key] = val
        total = meminfo.get('MemTotal', 1)
        free = meminfo.get('MemFree', 0)
        available = meminfo.get('MemAvailable', free)
        usage = (total - available) / total
        available_mb = available / 1024.0  # kB → MB
        return {
            'usage': max(0.0, min(1.0, usage)),
            'available_mb': available_mb,
        }

    def _read_proc_diskstats(self) -> float:
        """读取 /proc/diskstats 计算磁盘 I/O（MB/s）"""
        # 读取 sda 或 vda 或 nvme 的 sectors 读写字段
        total_sectors = 0
        with open('/proc/diskstats') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 14 and (parts[2].startswith('sda') or parts[2].startswith('vda') or parts[2].startswith('nvme')):
                    sectors_read = int(parts[5])
                    sectors_write = int(parts[9])
                    total_sectors += sectors_read + sectors_write

        now = time.monotonic()
        if self._disk_prev_counters is not None:
            dt = now - self._disk_prev_counters['time']
            sector_delta = total_sectors - self._disk_prev_counters['sectors']
            if dt > 0:
                # 1 sector = 512 bytes
                io_mb = (sector_delta * 512) / dt / (1024 * 1024)
                return max(0.0, io_mb)
            return 0.0

        self._disk_prev_counters = {'time': now, 'sectors': total_sectors}
        return 0.0

    def _read_proc_net(self) -> float:
        """读取 /proc/net/dev 估算网络延迟"""
        total_bytes = 0
        with open('/proc/net/dev') as f:
            next(f)  # skip header
            next(f)
            for line in f:
                parts = line.split()
                if len(parts) >= 10 and not parts[0].startswith('lo'):
                    recv = int(parts[1])
                    sent = int(parts[9])
                    total_bytes += recv + sent

        # 简单估算
        if total_bytes > 1_000_000_000:
            return 5.0
        elif total_bytes > 100_000_000:
            return 20.0
        elif total_bytes > 10_000_000:
            return 80.0
        return 200.0

    @property
    def last_metrics(self) -> Dict[str, float]:
        """返回最近一次采集的指标"""
        return self._last_metrics.copy()


# ============================================================
# InstinctSystem — 本能反应系统（增强版）
# 四大本能：
# 1. 遇袭自动防御 — 异常频率飙升 → 自动收紧防御
# 2. 能量不足降级 — 资源不够 → 关闭非核心功能
# 3. 气血自动调配 — 高负载子系统从空闲经络调资源
# 4. 自愈反射 — 诊断出问题 → 自动尝试修复
# ============================================================

class InstinctSystem:
    """
    本能反应系统
    实现四大本能：
    1. 遇袭自动防御 — 异常错误率飙升 → 自动收紧防御
    2. 能量不足降级 — 资源不足 → 关闭非核心功能
    3. 气血自动调配 — 某子系统突发高负载 → 从空闲经络调配资源
    4. 自愈反射 — 诊断出问题 → 自动尝试修复
    """

    def __init__(self, thresholds: Optional[Dict[str, float]] = None):
        self.thresholds = thresholds or INSTINCT_THRESHOLDS.copy()
        self._defense_level = 0.0          # 防御等级 0~1
        self._degradation_mode = False      # 是否处于降级模式
        self._degraded_subsystems: List[str] = []  # 已降级的子系统列表
        self._qi_transfers: List[Dict] = [] # 气血调配记录
        self._self_heal_actions: List[Dict] = []  # 自愈动作记录
        self._instinct_log: List[Dict] = []  # 本能事件日志

    @property
    def defense_level(self) -> float:
        """当前防御等级"""
        return self._defense_level

    @property
    def is_degraded(self) -> bool:
        """是否处于降级模式"""
        return self._degradation_mode

    def react_to_metrics(self, metrics: Dict[str, float], qi_level: float,
                         meridian_states: Dict[str, float]) -> Dict[str, Any]:
        """
        根据当前系统指标和气血水平触发本能反应
        返回本轮本能反应摘要
        """
        reactions: Dict[str, Any] = {
            'defense_activated': False,
            'degradation_activated': False,
            'qi_transfers': [],
            'self_heal_actions': [],
        }

        # 1. 遇袭自动防御
        defense = self._check_attack(metrics, qi_level)
        if defense > 0:
            self._defense_level = min(1.0, defense)
            reactions['defense_activated'] = True
            reactions['defense_level'] = self._defense_level
            self._instinct_log.append({
                'time': datetime.now().isoformat(),
                'type': 'defense',
                'level': self._defense_level,
                'trigger': 'error_rate_or_resource_anomaly',
            })

        # 2. 能量不足降级
        if qi_level < self.thresholds['resource_low']:
            self._degradation_mode = True
            reactions['degradation_activated'] = True
            # 根据气血水平决定降级哪些非核心子系统
            self._degraded_subsystems = self._select_subsystems_to_degrade(qi_level)
            reactions['degraded_subsystems'] = self._degraded_subsystems
            self._instinct_log.append({
                'time': datetime.now().isoformat(),
                'type': 'degradation',
                'qi_level': qi_level,
                'threshold': self.thresholds['resource_low'],
                'degraded': self._degraded_subsystems,
            })
        else:
            # 气血恢复到安全水平以上，解除降级
            if self._degradation_mode and qi_level > 0.5:
                self._degradation_mode = False
                self._degraded_subsystems = []

        # 3. 气血自动调配
        transfers = self._check_qi_transfer(meridian_states)
        if transfers:
            self._qi_transfers.extend(transfers)
            reactions['qi_transfers'] = transfers
            self._instinct_log.append({
                'time': datetime.now().isoformat(),
                'type': 'qi_transfer',
                'transfers': transfers,
            })

        # 4. 自愈反射 — 检查是否需要自愈
        self_heals = self._check_self_heal(metrics, qi_level)
        if self_heals:
            self._self_heal_actions.extend(self_heals)
            reactions['self_heal_actions'] = self_heals
            self._instinct_log.append({
                'time': datetime.now().isoformat(),
                'type': 'self_heal',
                'actions': self_heals,
            })

        return reactions

    def _check_attack(self, metrics: Dict[str, float], qi_level: float) -> float:
        """
        检测遇袭信号
        CPU/内存/负载异常高 + 气血骤降 → 可能遇袭
        返回防御等级 (0~1)
        """
        defense = 0.0
        cpu_load = metrics.get('cpu_load', 0)
        mem_usage = metrics.get('memory_usage', 0)
        load_avg = metrics.get('load_avg', 0)

        # CPU/内存异常高
        if cpu_load > self.thresholds['cpu_critical'] or mem_usage > self.thresholds['memory_critical']:
            defense = max(cpu_load, mem_usage)

        # 负载均值异常高（假设 CPU 核数为 4，负载 > 4 表示严重过载）
        if load_avg > 4.0:
            defense = max(defense, min(1.0, load_avg / 8.0))

        # 气血极低时额外防御
        if qi_level < 0.15:
            defense = max(defense, 0.8)

        return defense

    def _select_subsystems_to_degrade(self, qi_level: float) -> List[str]:
        """
        能量不足降级：根据气血水平选择要降级的非核心子系统
        气血越低，关闭越多
        """
        degraded = []
        # 非核心子系统优先级：数据处理 > 存储辅助 > 记忆 > 配置
        if qi_level < 0.15:
            # 极低：只保留 Gateway + Model Router（核心通信）
            degraded = ['data_pipeline', 'config', 'memory', 'decision']
        elif qi_level < 0.2:
            # 低：关闭数据处理和配置
            degraded = ['data_pipeline', 'config']
        elif qi_level < 0.3:
            # 接近阈值：只关闭数据处理
            degraded = ['data_pipeline']

        return degraded

    def _check_qi_transfer(self, meridian_states: Dict[str, float]) -> List[Dict]:
        """
        气血调配：某经络气血高且另一条低时触发调配
        meridian_states: {meridian_id: qi_level}
        """
        transfers = []
        high_meridians = []
        low_meridians = []

        for mid, level in meridian_states.items():
            if level > self.thresholds['qi_transfer_threshold']:
                high_meridians.append((mid, level))
            elif level < 0.3:
                low_meridians.append((mid, level))

        # 从高往低调配
        for low_mid, low_level in low_meridians:
            if high_meridians:
                donor_mid, donor_level = high_meridians.pop(0)
                transfer_amount = (donor_level - 0.5) * 0.3  # 拿出超出部分的一部分
                transfers.append({
                    'from': donor_mid,
                    'to': low_mid,
                    'amount': round(transfer_amount, 3),
                    'reason': f'{donor_mid} 气血充盈({donor_level:.2f}) → {low_mid} 气血不足({low_level:.2f})',
                })

        return transfers

    def _check_self_heal(self, metrics: Dict[str, float], qi_level: float) -> List[Dict]:
        """
        自愈反射：检测到特定问题后给出修复建议
        """
        actions = []

        if metrics.get('cpu_load', 0) > self.thresholds['cpu_critical']:
            actions.append({
                'type': 'reduce_cpu_load',
                'target': 'du_mai',
                'action': '降频/限流',
                'severity': 'high',
            })

        if metrics.get('memory_usage', 0) > self.thresholds['memory_critical']:
            actions.append({
                'type': 'reduce_memory',
                'target': 'ren_mai',
                'action': '释放缓存/GC',
                'severity': 'high',
            })

        if metrics.get('disk_usage', 0) > self.thresholds['disk_critical']:
            actions.append({
                'type': 'clean_disk',
                'target': 'chong_mai',
                'action': '清理临时文件',
                'severity': 'high',
            })

        if metrics.get('network_latency', 0) > 150:
            actions.append({
                'type': 'network_optimize',
                'target': 'dai_mai',
                'action': '切换网络路径/压缩数据',
                'severity': 'medium',
            })

        if qi_level < self.thresholds['resource_low']:
            actions.append({
                'type': 'replenish_qi',
                'target': 'all',
                'action': '启动气血恢复',
                'severity': 'critical',
            })

        return actions

    def get_state(self) -> Dict[str, Any]:
        """获取本能系统状态摘要"""
        return {
            'defense_level': self._defense_level,
            'degradation_mode': self._degradation_mode,
            'degraded_subsystems': self._degraded_subsystems,
            'total_qi_transfers': len(self._qi_transfers),
            'total_self_heal_actions': len(self._self_heal_actions),
            'recent_events': self._instinct_log[-10:],  # 最近 10 条事件
        }


# ============================================================
# MeridianSystem — 经络系统（增强版）
# ============================================================

class MeridianSystem:
    """经络系统"""

    def __init__(self):
        self.meridians: Dict[str, MeridianState] = {}
        self.acupoints: Dict[str, Dict] = {}
        self._initialize_meridians()

    def _initialize_meridians(self) -> None:
        """初始化经络（扩展到八脉）"""
        meridian_configs = [
            {
                'id': 'ren_mai',
                'name': '任脉',
                'type': MeridianType.REN_MAI,
                'connected': ['心', '肝', '脾', '肺', '肾']
            },
            {
                'id': 'du_mai',
                'name': '督脉',
                'type': MeridianType.DU_MAI,
                'connected': ['心', '肝', '肾']
            },
            {
                'id': 'chong_mai',
                'name': '冲脉',
                'type': MeridianType.CHONG_MAI,
                'connected': ['肝', '肾', '胃']
            },
            {
                'id': 'dai_mai',
                'name': '带脉',
                'type': MeridianType.DAI_MAI,
                'connected': ['肝', '胆']
            },
            {
                'id': 'yang_qiao',
                'name': '阳跷脉',
                'type': MeridianType.YANG_QIAO,
                'connected': ['心', '膀胱']
            },
            {
                'id': 'yin_qiao',
                'name': '阴跷脉',
                'type': MeridianType.YIN_QIAO,
                'connected': ['肾', '心']
            },
            {
                'id': 'yang_wei',
                'name': '阳维脉',
                'type': MeridianType.YANG_WEI,
                'connected': ['肺', '大肠']
            },
            {
                'id': 'yin_wei',
                'name': '阴维脉',
                'type': MeridianType.YIN_WEI,
                'connected': ['心', '肾', '三焦']
            },
        ]

        for config in meridian_configs:
            self.meridians[config['id']] = MeridianState(
                meridian_id=config['id'],
                meridian_name=config['name'],
                meridian_type=config['type'],
                flow_rate=1.0,
                blockage_level=0.0,
                energy_level=1.0,
                connected_organs=config['connected'],
                raw_metric_value=0.0,
                raw_metric_name='',
                raw_metric_unit='',
                zi_wu_boost=1.0,
            )

    def regulate_meridian(
        self,
        meridian_id: str,
        target_flow: float
    ) -> bool:
        """调节经络"""
        if meridian_id not in self.meridians:
            return False

        meridian = self.meridians[meridian_id]
        meridian.flow_rate = max(0.1, min(1.0, target_flow))

        if target_flow < 0.5:
            meridian.blockage_level = 1.0 - target_flow * 2
        else:
            meridian.blockage_level = 0.0

        return True

    def circulate_qi(self) -> Dict[str, float]:
        """运行气血循环"""
        circulation = {}

        for meridian_id, meridian in self.meridians.items():
            circulation[meridian_id] = meridian.flow_rate * meridian.energy_level

            if meridian.blockage_level > 0.5:
                meridian.flow_rate *= 0.95

        return circulation

    def get_meridian_state(self, meridian_id: str) -> Optional[MeridianState]:
        """获取经络状态"""
        return self.meridians.get(meridian_id)

    def diagnose_blockages(self) -> List[Dict[str, Any]]:
        """诊断经络堵塞"""
        blockages = []

        for meridian_id, meridian in self.meridians.items():
            if meridian.blockage_level > 0.3:
                blockages.append({
                    'meridian': meridian.meridian_name,
                    'blockage_level': meridian.blockage_level,
                    'raw_metric': meridian.raw_metric_value,
                    'raw_metric_name': meridian.raw_metric_name,
                    'suggested_action': '疏通调理'
                })

        return blockages

    # ------ 新增：基于真实指标更新经络状态 ------

    def update_from_metrics(self, metrics: Dict[str, float],
                            zi_wu_config: Optional[Dict[str, Any]] = None) -> None:
        """
        将真实系统指标映射到经络状态
        metrics: SystemMetricsCollector 返回的指标字典
        zi_wu_config: 当前时辰的子午流注配置
        """
        for meridian_id, mapping in MERIDIAN_METRIC_MAP.items():
            if meridian_id not in self.meridians:
                continue

            meridian = self.meridians[meridian_id]
            metric_key = mapping['metric']
            raw_value = metrics.get(metric_key, 0.0)

            # 记录原始指标
            meridian.raw_metric_value = raw_value
            meridian.raw_metric_name = mapping['label']
            meridian.raw_metric_unit = mapping['unit']

            # 将原始指标归一化到 flow_rate
            flow = self._normalize_metric(meridian_id, raw_value, metric_key)
            meridian.flow_rate = flow

            # 堵塞程度：flow 越低堵塞越严重
            if flow < 0.5:
                meridian.blockage_level = (0.5 - flow) * 2
            else:
                meridian.blockage_level = 0.0

            # 子午流注气血增益
            if zi_wu_config and meridian_id == zi_wu_config.get('peak_meridian'):
                meridian.zi_wu_boost = zi_wu_config.get('boost', 1.5)
                meridian.energy_level = min(1.5, meridian.flow_rate * meridian.zi_wu_boost)
            else:
                meridian.zi_wu_boost = 1.0
                meridian.energy_level = meridian.flow_rate

    def _normalize_metric(self, meridian_id: str, raw_value: float,
                          metric_key: str) -> float:
        """
        将真实指标归一化到 0~1 的 flow_rate
        不同经络有不同归一化逻辑
        """
        if metric_key in ('cpu_load', 'memory_usage', 'disk_usage'):
            # 使用率越高，经络越"堵"，flow_rate 越低
            return max(0.0, 1.0 - raw_value)

        elif metric_key == 'disk_io':
            # 磁盘 I/O：假设 <500 MB/s 正常，>500 开始堵
            return max(0.0, min(1.0, 1.0 - raw_value / 500.0))

        elif metric_key == 'network_latency':
            # 延迟：5ms 最优，200ms 最差
            return max(0.0, min(1.0, 1.0 - (raw_value - 5) / 195))

        elif metric_key == 'uptime':
            # uptime（小时）：>1h 算正常，越久越稳定
            # 0h = 刚启动(不稳定)，>1h = 稳定运行
            return max(0.0, min(1.0, raw_value / 24.0))

        elif metric_key == 'process_count':
            # 进程数：假设 100~500 正常范围
            # <50 太少，>500 太多
            if raw_value < 50:
                return max(0.0, raw_value / 50.0)
            elif raw_value > 500:
                return max(0.0, 1.0 - (raw_value - 500) / 500.0)
            else:
                return 1.0

        elif metric_key == 'load_avg':
            # 负载均值：假设 0~4 正常（4核机器）
            return max(0.0, min(1.0, 1.0 - raw_value / 4.0))

        elif metric_key == 'memory_available_mb':
            # 可用内存：假设 512MB 基准
            # >=512MB 算健康，0MB 最危险
            return max(0.0, min(1.0, raw_value / 512.0))

        elif metric_key == 'gateway_health':
            # Gateway 健康度：本身是 0~1
            return max(0.0, min(1.0, raw_value))

        elif metric_key in ('model_latency', 'memory_access', 'db_connection'):
            # 延迟类：0ms 最优，500ms 最差
            return max(0.0, min(1.0, 1.0 - raw_value / 500.0))

        # 默认：1.0
        return 1.0


# ============================================================
# OrganSystem — 脏腑系统（增强版）
# ============================================================

class OrganSystem:
    """脏腑系统"""

    WUXING_ORGAN_MAP = {
        '心': {'wuxing': '火', 'yin_yang': '阳', 'element': OrganType.HEART},
        '肝': {'wuxing': '木', 'yin_yang': '阴', 'element': OrganType.LIVER},
        '脾': {'wuxing': '土', 'yin_yang': '阴', 'element': OrganType.SPLEEN},
        '肺': {'wuxing': '金', 'yin_yang': '阴', 'element': OrganType.LUNG},
        '肾': {'wuxing': '水', 'yin_yang': '阴', 'element': OrganType.KIDNEY},
        '小肠': {'wuxing': '火', 'yin_yang': '阳', 'element': OrganType.SMALL_INTESTINE},
        '胆': {'wuxing': '木', 'yin_yang': '阳', 'element': OrganType.GALLBLADDER},
    }

    def __init__(self):
        self.organs: Dict[str, OrganState] = {}
        self._initialize_organs()

    def _initialize_organs(self) -> None:
        """初始化脏腑"""
        for organ_name, config in self.WUXING_ORGAN_MAP.items():
            subsystem_info = ORGAN_SUBSYSTEM_MAP.get(organ_name, {})
            self.organs[organ_name] = OrganState(
                organ_id=organ_name.lower(),
                organ_name=organ_name,
                organ_type=config['element'],
                functional_level=1.0,
                energy_consumption=0.0,
                associated_system=subsystem_info.get('subsystem', 'core'),
                subsystem_health=1.0,
                subsystem_latency=0.0,
                zi_wu_boost=1.0,
            )

    def update_functional_level(
        self,
        organ_name: str,
        level: float
    ) -> bool:
        """更新脏腑功能水平"""
        if organ_name not in self.organs:
            return False

        self.organs[organ_name].functional_level = max(0.0, min(1.0, level))
        return True

    def get_organ_state(self, organ_name: str) -> Optional[OrganState]:
        """获取脏腑状态"""
        return self.organs.get(organ_name)

    def diagnose_organ_health(self) -> Dict[str, Any]:
        """诊断脏腑健康"""
        health_report = {
            'overall': 1.0,
            'organs': {}
        }

        total_function = sum(
            organ.functional_level for organ in self.organs.values()
        )
        avg_function = total_function / len(self.organs) if self.organs else 1.0
        health_report['overall'] = avg_function

        for organ_name, organ in self.organs.items():
            wuxing = self.WUXING_ORGAN_MAP.get(organ_name, {})
            health_report['organs'][organ_name] = {
                'functional_level': organ.functional_level,
                'status': self._get_organ_status(organ.functional_level),
                'wuxing': wuxing.get('wuxing', '未知'),
                'subsystem': ORGAN_SUBSYSTEM_MAP.get(organ_name, {}).get('label', '未知'),
                'subsystem_health': organ.subsystem_health,
                'subsystem_latency': organ.subsystem_latency,
            }

        return health_report

    def _get_organ_status(self, level: float) -> str:
        """获取脏腑状态描述"""
        if level >= 0.9:
            return "功能充沛"
        elif level >= 0.7:
            return "功能正常"
        elif level >= 0.5:
            return "功能偏弱"
        else:
            return "功能不足"

    # ------ 新增：基于子系统指标更新脏腑状态 ------

    def update_from_subsystems(self, subsystem_health: Dict[str, float],
                               zi_wu_config: Optional[Dict[str, Any]] = None) -> None:
        """
        根据子系统健康度更新脏腑功能水平
        subsystem_health: {subsystem_name: health_score}
        """
        for organ_name, mapping in ORGAN_SUBSYSTEM_MAP.items():
            if organ_name not in self.organs:
                continue

            organ = self.organs[organ_name]
            sub_key = mapping['subsystem']
            health = subsystem_health.get(sub_key, 0.5)

            organ.subsystem_health = health
            organ.functional_level = max(0.0, min(1.0, health))

            # 子午流注增益
            if zi_wu_config and organ_name == zi_wu_config.get('peak_organ'):
                organ.zi_wu_boost = zi_wu_config.get('boost', 1.5)
                organ.functional_level = min(
                    1.5, organ.functional_level * organ.zi_wu_boost
                )
            else:
                organ.zi_wu_boost = 1.0


# ============================================================
# HeartSystem — 心脏系统（保留原有）
# ============================================================

class HeartSystem:
    """心脏系统 - 核心驱动"""

    def __init__(self):
        self.heart_rate = 60
        self.energy_output = 1.0
        self.rhythm_stability = 1.0
        self.beat_history: List[float] = []

    def pump_energy(self) -> float:
        """泵送能量"""
        output = self.energy_output * self.rhythm_stability

        self.beat_history.append(output)
        if len(self.beat_history) > 100:
            self.beat_history = self.beat_history[-100:]

        return output

    def adjust_output(self, target_output: float) -> None:
        """调整能量输出"""
        self.energy_output = max(0.5, min(1.5, target_output))

    def check_rhythm(self) -> Dict[str, Any]:
        """检查心律"""
        if len(self.beat_history) < 10:
            return {'stability': 1.0, 'status': '正常'}

        variance = sum(
            (beat - sum(self.beat_history)/len(self.beat_history))**2
            for beat in self.beat_history
        ) / len(self.beat_history)

        stability = max(0.0, 1.0 - variance)

        return {
            'stability': stability,
            'status': '稳定' if stability > 0.8 else '波动',
            'variance': variance
        }


# ============================================================
# QiXueMetabolism — 气血代谢系统（增强版）
# 气血根据系统指标动态计算，新增子午流注节律机制
# ============================================================

class QiXueMetabolism:
    """
    气血代谢系统（增强版）
    qi/blood 根据系统指标动态计算，新增子午流注节律机制
    """

    def __init__(self):
        self.qi_total = 100.0
        self.blood_total = 100.0
        self.fluid_balance = 1.0
        self.metabolism_rate = 1.0
        self.regeneration_rate = 0.1
        self._zi_wu_active = False
        self._last_zi_wu_hour = -1

    def consume_qi(self, amount: float) -> bool:
        """消耗气"""
        if self.qi_total >= amount:
            self.qi_total -= amount
            return True
        return False

    def generate_qi(self, amount: float) -> None:
        """生成气"""
        self.qi_total = min(100.0, self.qi_total + amount)

    def circulate_qi(self) -> float:
        """运行气循环"""
        circulation = self.qi_total * self.metabolism_rate * 0.1
        return circulation

    def update_metabolism(self, delta_time: float) -> None:
        """更新代谢"""
        consumption = self.metabolism_rate * delta_time * 0.5
        self.qi_total = max(0, self.qi_total - consumption)

        regeneration = self.regeneration_rate * delta_time
        self.qi_total = min(100.0, self.qi_total + regeneration)

    def get_metabolism_state(self) -> Dict[str, float]:
        """获取代谢状态"""
        return {
            'qi_total': self.qi_total,
            'blood_total': self.blood_total,
            'fluid_balance': self.fluid_balance,
            'metabolism_rate': self.metabolism_rate,
            'regeneration_rate': self.regeneration_rate,
        }

    # ------ 新增：基于系统指标动态计算气血 ------

    def recalculate_from_metrics(self, metrics: Dict[str, float]) -> None:
        """
        根据系统指标重新计算气血总量
        - CPU 负载高 → 气血消耗大
        - 内存充足 → 气血生成足
        - 网络畅通 → 气血运行畅
        - 磁盘充裕 → 气血根基稳
        """
        cpu_load = metrics.get('cpu_load', 0.5)
        mem_usage = metrics.get('memory_usage', 0.5)
        mem_available = max(0.0, 1.0 - mem_usage)
        disk_usage = metrics.get('disk_usage', 0.5)
        net_latency = metrics.get('network_latency', 50)
        disk_io = metrics.get('disk_io', 0)

        # 气血 = 基础值 × (内存可用率 × 0.4 + 网络畅通率 × 0.3 + 磁盘充裕率 × 0.3)
        net_smooth = max(0.0, 1.0 - (net_latency - 5) / 195)
        disk_free = max(0.0, 1.0 - min(1.0, disk_usage))

        raw_blood = 100.0 * (mem_available * 0.4 + net_smooth * 0.3 + disk_free * 0.3)

        # CPU 负载影响消耗：CPU 越高，气血消耗越大
        cpu_drain = cpu_load * 0.3
        self.qi_total = max(0.0, min(100.0, raw_blood * (1.0 - cpu_drain)))
        self.blood_total = max(0.0, min(100.0, raw_blood))

        # 气血比值决定津液平衡
        if self.blood_total > 0:
            ratio = self.qi_total / self.blood_total
            self.fluid_balance = max(0.0, min(1.5, ratio))
        else:
            self.fluid_balance = 0.5

    # ------ 新增：子午流注节律 ------

    def apply_zi_wu_rhythm(self, current_hour: Optional[int] = None,
                           meridian_states: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        子午流注：不同时段不同经络获得更多气血
        返回当前时辰的节律配置
        """
        if current_hour is None:
            current_hour = datetime.now().hour

        if current_hour == self._last_zi_wu_hour and self._zi_wu_active:
            # 同一时辰不需要重复计算
            return ZI_WU_LIU_ZHU.get(current_hour, ZI_WU_LIU_ZHU[0])

        self._last_zi_wu_hour = current_hour
        self._zi_wu_active = True

        zi_wu = ZI_WU_LIU_ZHU.get(current_hour, ZI_WU_LIU_ZHU[0])
        boost = zi_wu['boost']

        # 子午流注影响气血再生
        # 当令经络对应的脏腑气血再生增强
        peak_organ = zi_wu['peak_organ']
        if peak_organ in ORGAN_QI_WEIGHTS:
            boost_factor = ORGAN_QI_WEIGHTS.get(peak_organ, 1.0)
            self.regeneration_rate = 0.1 * boost * boost_factor
        else:
            self.regeneration_rate = 0.1 * boost

        return zi_wu


# ============================================================
# BodyMappingSystem — 人体映射系统主类（增强版）
# 提供 collect_metrics() 和 diagnose_health() 返回真实诊断
# ============================================================

class BodyMappingSystem:
    """人体映射系统主类（增强版）"""

    def __init__(self, config=None):
        self.config = config
        self.meridian_system = MeridianSystem()
        self.organ_system = OrganSystem()
        self.heart_system = HeartSystem()
        self.qi_xue_metabolism = QiXueMetabolism()
        # 新增：真实指标采集器 & 本能系统
        self.metrics_collector = SystemMetricsCollector()
        self.instinct_system = InstinctSystem()

        self.self_repair_enabled = True
        self.health_check_interval = 300
        self._last_collect_time = 0.0
        self._cached_metrics: Dict[str, float] = {}
        self._cached_zi_wu: Dict[str, Any] = {}
        self._last_instinct_reactions: Dict[str, Any] = {}

    async def get_energy_distribution(self) -> Dict[str, float]:
        """获取能量分布"""
        energy = self.heart_system.pump_energy()

        distribution = {
            'heart': energy * 0.3,
            'meridians': energy * 0.4,
            'organs': energy * 0.2,
            'circulation': energy * 0.1
        }

        return distribution

    async def regulate_meridian(
        self,
        meridian_id: str,
        target_flow: float
    ) -> bool:
        """调节经络"""
        return self.meridian_system.regulate_meridian(meridian_id, target_flow)

    # ------ 新增：采集真实指标 ------

    def collect_metrics(self, force: bool = False) -> Dict[str, float]:
        """
        采集系统指标并映射到经络/脏腑
        默认 5 秒内不重复采集（force=True 强制重新采集）
        """
        now = time.monotonic()
        if not force and now - self._last_collect_time < 5.0:
            return self._cached_metrics.copy()

        # 1. 采集真实系统指标
        metrics = self.metrics_collector.collect()
        self._cached_metrics = metrics
        self._last_collect_time = now

        # 2. 获取当前时辰的子午流注配置
        current_hour = datetime.now().hour
        zi_wu = self.qi_xue_metabolism.apply_zi_wu_rhythm(current_hour)
        self._cached_zi_wu = zi_wu

        # 3. 更新经络状态（真实指标映射）
        self.meridian_system.update_from_metrics(metrics, zi_wu)

        # 4. 更新脏腑状态（基于子系统健康度）
        subsystem_health = self._derive_subsystem_health(metrics)
        self.organ_system.update_from_subsystems(subsystem_health, zi_wu)

        # 5. 动态重新计算气血
        self.qi_xue_metabolism.recalculate_from_metrics(metrics)

        # 6. 本能反应
        meridian_qi = {
            mid: m.flow_rate * m.energy_level
            for mid, m in self.meridian_system.meridians.items()
        }
        qi_level = self.qi_xue_metabolism.qi_total / 100.0
        self._last_instinct_reactions = self.instinct_system.react_to_metrics(
            metrics, qi_level, meridian_qi
        )

        return metrics

    def _derive_subsystem_health(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """
        从系统指标推导各子系统健康度
        返回 {subsystem_name: health_score}
        """
        cpu = metrics.get('cpu_load', 0.5)
        mem = metrics.get('memory_usage', 0.5)
        net_latency = metrics.get('network_latency', 50)
        disk_usage = metrics.get('disk_usage', 0.5)
        disk_io = metrics.get('disk_io', 0)
        load_avg = metrics.get('load_avg', 0)

        return {
            'gateway':      max(0.0, min(1.0, 1.0 - cpu)),                         # 心 ← CPU
            'memory':       max(0.0, min(1.0, 1.0 - mem)),                         # 肝 ← 内存
            'config':       max(0.0, min(1.0, 1.0 - disk_usage)),                  # 脾 ← 磁盘
            'model_router': max(0.0, min(1.0, 1.0 - (net_latency - 5) / 195)),     # 肺 ← 网络
            'storage':      max(0.0, min(1.0, 1.0 - disk_io / 500.0)),             # 肾 ← 磁盘 I/O
            'data_pipeline': max(0.0, min(1.0, 1.0 - disk_io / 1000.0)),            # 小肠
            'decision':     max(0.0, min(1.0, 1.0 - cpu * 0.5 - mem * 0.5)),      # 胆 ← CPU+内存混合
        }

    async def diagnose_health(self) -> HealthState:
        """
        健康诊断（增强版：集成真实指标 + 本能系统状态 + 子午流注）
        返回真实诊断结果
        """
        # 自动采集最新指标
        self.collect_metrics()

        meridian_states = list(self.meridian_system.meridians.values())
        organ_states = list(self.organ_system.organs.values())

        vitality = self._calculate_vitality(meridian_states, organ_states)

        return HealthState(
            vitality_score=vitality,
            meridian_states=meridian_states,
            organ_states=organ_states,
            qi_total=self.qi_xue_metabolism.qi_total,
            blood_total=self.qi_xue_metabolism.blood_total,
            fluid_balance=self.qi_xue_metabolism.fluid_balance,
            system_metrics=self._cached_metrics.copy(),
            zi_wu_info=self._cached_zi_wu.copy(),
            instinct_state=self.instinct_system.get_state(),
        )

    def _calculate_vitality(
        self,
        meridians: List[MeridianState],
        organs: List[OrganState]
    ) -> float:
        """计算活力（增强版：加入子午流注加权）"""
        meridian_vitality = (
            sum(m.flow_rate * m.energy_level for m in meridians) / len(meridians)
            if meridians else 1.0
        )
        organ_vitality = (
            sum(o.functional_level * o.subsystem_health for o in organs) / len(organs)
            if organs else 1.0
        )

        heart_vitality = self.heart_system.energy_output * self.heart_system.rhythm_stability

        vitality = (
            meridian_vitality * 0.3 +
            organ_vitality * 0.4 +
            heart_vitality * 0.3
        )

        return max(0.0, min(1.0, vitality))

    async def repair(
        self,
        repair_type: str,
        target: Optional[str] = None
    ) -> bool:
        """
        执行自我修复（增强版：支持真实系统修复动作）
        """
        if not self.self_repair_enabled:
            return False

        if repair_type == 'meridian':
            if target:
                return self.meridian_system.regulate_meridian(target, 0.8)

        elif repair_type == 'organ':
            if target:
                return self.organ_system.update_functional_level(target, 0.8)

        elif repair_type == 'heart':
            self.heart_system.adjust_output(1.0)
            return True

        elif repair_type == 'full':
            for meridian_id in self.meridian_system.meridians:
                self.meridian_system.regulate_meridian(meridian_id, 0.8)
            for organ_name in self.organ_system.organs:
                self.organ_system.update_functional_level(organ_name, 0.8)
            self.heart_system.adjust_output(1.0)
            return True

        # ------ 新增：真实系统修复动作 ------

        elif repair_type == 'reduce_cpu_load':
            # 降低 CPU 负载 → 调节督脉
            self.meridian_system.regulate_meridian('du_mai', 0.8)
            if target and target in self.organ_system.organs:
                self.organ_system.update_functional_level(target, 0.8)
            return True

        elif repair_type == 'reduce_memory':
            # 释放内存 → 调节任脉
            self.meridian_system.regulate_meridian('ren_mai', 0.8)
            return True

        elif repair_type == 'clean_disk':
            # 清理磁盘 → 调节冲脉
            self.meridian_system.regulate_meridian('chong_mai', 0.8)
            return True

        elif repair_type == 'network_optimize':
            # 优化网络 → 调节带脉
            self.meridian_system.regulate_meridian('dai_mai', 0.8)
            return True

        elif repair_type == 'replenish_qi':
            # 全面恢复气血
            self.qi_xue_metabolism.generate_qi(30.0)
            self.qi_xue_metabolism.regeneration_rate = max(
                self.qi_xue_metabolism.regeneration_rate, 0.2
            )
            return True

        return False

    async def adjust_metabolism(self, adjustment: Dict[str, float]) -> None:
        """调节代谢"""
        if 'metabolism_rate' in adjustment:
            self.qi_xue_metabolism.metabolism_rate = max(0.5, min(2.0, adjustment['metabolism_rate']))

        if 'regeneration_rate' in adjustment:
            self.qi_xue_metabolism.regeneration_rate = max(0.05, min(0.5, adjustment['regeneration_rate']))

    async def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态（增强版：包含真实指标和本能系统）"""
        # 确保采集过指标
        self.collect_metrics()

        return {
            'vitality': self._calculate_vitality(
                list(self.meridian_system.meridians.values()),
                list(self.organ_system.organs.values())
            ),
            'heart_state': {
                'energy_output': self.heart_system.energy_output,
                'rhythm_stability': self.heart_system.rhythm_stability
            },
            'meridian_blockages': self.meridian_system.diagnose_blockages(),
            'organ_health': self.organ_system.diagnose_organ_health(),
            'metabolism': self.qi_xue_metabolism.get_metabolism_state(),
            # 新增
            'system_metrics': self._cached_metrics.copy(),
            'zi_wu_liu_zhu': self._cached_zi_wu.copy(),
            'instinct_system': self.instinct_system.get_state(),
        }
