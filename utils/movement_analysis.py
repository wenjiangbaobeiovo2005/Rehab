"""
动作轨迹分析工具模块

该模块提供了分析人体动作轨迹的函数。
"""

import numpy as np
from typing import List, Tuple, Dict
from scipy.signal import find_peaks


def calculate_velocity(positions: List[Tuple[float, float, float]], 
                      frame_times: List[float]) -> List[Tuple[float, float, float]]:
    """
    计算关键点的速度
    
    Args:
        positions: 关键点位置序列 [(x, y, z), ...]
        frame_times: 帧时间序列 [t1, t2, ...]
        
    Returns:
        速度序列 [(vx, vy, vz), ...]
    """
    velocities = []
    
    for i in range(1, len(positions)):
        dt = frame_times[i] - frame_times[i-1]
        if dt > 0:
            dx = (positions[i][0] - positions[i-1][0]) / dt
            dy = (positions[i][1] - positions[i-1][1]) / dt
            dz = (positions[i][2] - positions[i-1][2]) / dt
            velocities.append((dx, dy, dz))
        else:
            velocities.append((0.0, 0.0, 0.0))
            
    # 第一帧速度设为0
    if velocities:
        velocities.insert(0, (0.0, 0.0, 0.0))
        
    return velocities


def calculate_acceleration(velocities: List[Tuple[float, float, float]], 
                          frame_times: List[float]) -> List[Tuple[float, float, float]]:
    """
    计算关键点的加速度
    
    Args:
        velocities: 速度序列 [(vx, vy, vz), ...]
        frame_times: 帧时间序列 [t1, t2, ...]
        
    Returns:
        加速度序列 [(ax, ay, az), ...]
    """
    accelerations = []
    
    for i in range(1, len(velocities)):
        dt = frame_times[i] - frame_times[i-1]
        if dt > 0:
            dvx = (velocities[i][0] - velocities[i-1][0]) / dt
            dvy = (velocities[i][1] - velocities[i-1][1]) / dt
            dvz = (velocities[i][2] - velocities[i-1][2]) / dt
            accelerations.append((dvx, dvy, dvz))
        else:
            accelerations.append((0.0, 0.0, 0.0))
            
    # 第一帧加速度设为0
    if accelerations:
        accelerations.insert(0, (0.0, 0.0, 0.0))
        
    return accelerations


def detect_movement_peaks(data: List[float], 
                         height: float = None, 
                         distance: int = 10) -> Tuple[List[int], Dict]:
    """
    检测动作数据中的峰值点
    
    Args:
        data: 动作数据序列
        height: 峰值最小高度
        distance: 峰值间最小距离
        
    Returns:
        (峰值索引列表, 峰值信息字典)
    """
    peaks, properties = find_peaks(data, height=height, distance=distance)
    return peaks.tolist(), properties


def calculate_movement_range(data: List[float]) -> Dict[str, float]:
    """
    计算动作范围
    
    Args:
        data: 动作数据序列
        
    Returns:
        动作范围信息字典
    """
    if not data:
        return {
            'min': 0.0,
            'max': 0.0,
            'range': 0.0,
            'mean': 0.0
        }
        
    min_val = min(data)
    max_val = max(data)
    
    return {
        'min': min_val,
        'max': max_val,
        'range': max_val - min_val,
        'mean': sum(data) / len(data)
    }


def calculate_smoothness(data: List[float]) -> float:
    """
    计算动作平滑度（基于数据的标准差）
    
    Args:
        data: 动作数据序列
        
    Returns:
        平滑度值（值越小越平滑）
    """
    if len(data) < 2:
        return 0.0
        
    return float(np.std(data))


def calculate_symmetry(left_data: List[float], 
                      right_data: List[float]) -> float:
    """
    计算左右对称性
    
    Args:
        left_data: 左侧数据序列
        right_data: 右侧数据序列
        
    Returns:
        对称性得分（0-100，100为完全对称）
    """
    if not left_data or not right_data:
        return 100.0
        
    # 取较短序列的长度
    min_len = min(len(left_data), len(right_data))
    if min_len == 0:
        return 100.0
        
    left_data = left_data[:min_len]
    right_data = right_data[:min_len]
    
    # 计算相关系数
    correlation = np.corrcoef(left_data, right_data)[0, 1]
    
    # 转换为0-100的得分
    symmetry_score = abs(correlation) * 100 if not np.isnan(correlation) else 0.0
    
    return float(symmetry_score)