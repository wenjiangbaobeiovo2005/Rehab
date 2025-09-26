"""
对称性分析工具模块

该模块提供了分析人体左右对称性的函数。
"""

import numpy as np
from typing import Dict, List, Tuple


def compare_bilateral_symmetry(left_angles: Dict[str, float], 
                              right_angles: Dict[str, float],
                              angle_pairs: List[Tuple[str, str]]) -> Dict[str, float]:
    """
    比较左右两侧关节角度的对称性
    
    Args:
        left_angles: 左侧关节角度字典
        right_angles: 右侧关节角度字典
        angle_pairs: 需要比较的角度对列表 [('left_key', 'right_key'), ...]
        
    Returns:
        对称性分析结果字典
    """
    symmetry_results = {}
    
    for left_key, right_key in angle_pairs:
        if left_key in left_angles and right_key in right_angles:
            left_val = left_angles[left_key]
            right_val = right_angles[right_key]
            
            # 计算对称性差异（绝对值）
            diff = abs(left_val - right_val)
            
            # 计算对称性得分（0-100，100为完全对称）
            # 使用较小值作为基准计算百分比差异
            base_val = min(abs(left_val), abs(right_val))
            if base_val > 0:
                symmetry_score = max(0, 100 - (diff / base_val) * 100)
            else:
                symmetry_score = 100.0 if diff == 0 else 0.0
                
            symmetry_results[f"{left_key}_symmetry"] = symmetry_score
            symmetry_results[f"{left_key}_difference"] = diff
            
    return symmetry_results


def calculate_symmetry_index(left_measurements: List[float], 
                           right_measurements: List[float]) -> float:
    """
    计算对称性指数
    
    Args:
        left_measurements: 左侧测量值列表
        right_measurements: 右侧测量值列表
        
    Returns:
        对称性指数（0-1，1为完全对称）
    """
    if not left_measurements or not right_measurements:
        return 1.0
        
    left_mean = sum(left_measurements) / len(left_measurements)
    right_mean = sum(right_measurements) / len(right_measurements)
    
    if left_mean == 0 and right_mean == 0:
        return 1.0
        
    # 对称性指数计算公式
    si = 1 - (abs(left_mean - right_mean) / max(abs(left_mean), abs(right_mean)))
    
    return max(0, si)  # 确保结果非负


def detect_asymmetry_patterns(angles_history: List[Dict[str, float]], 
                            threshold: float = 15.0) -> List[str]:
    """
    检测不对称模式
    
    Args:
        angles_history: 角度历史数据列表
        threshold: 不对称阈值（度）
        
    Returns:
        检测到的不对称模式列表
    """
    if len(angles_history) < 2:
        return []
        
    asymmetries = []
    
    # 获取所有角度键
    angle_keys = set()
    for frame in angles_history:
        angle_keys.update(frame.keys())
        
    # 分析每种角度的左右差异
    for key in angle_keys:
        # 查找对应的左右角度键
        if key.startswith('left_'):
            right_key = key.replace('left_', 'right_', 1)
        elif key.startswith('right_'):
            right_key = key.replace('right_', 'left_', 1)
        else:
            continue
            
        # 收集历史数据
        left_values = []
        right_values = []
        
        for frame in angles_history:
            if key in frame:
                left_values.append(frame[key])
            if right_key in frame:
                right_values.append(frame[right_key])
                
        if not left_values or not right_values:
            continue
            
        # 计算平均差异
        avg_left = sum(left_values) / len(left_values)
        avg_right = sum(right_values) / len(right_values)
        diff = abs(avg_left - avg_right)
        
        if diff > threshold:
            asymmetries.append(f"{key.replace('left_', '').replace('right_', '')}不对称({diff:.1f}°)")
            
    return asymmetries


def evaluate_movement_symmetry(angles: Dict[str, float]) -> Dict[str, float]:
    """
    评估动作对称性
    
    Args:
        angles: 当前角度字典
        
    Returns:
        对称性评估结果字典
    """
    symmetry_scores = {}
    
    # 评估膝关节对称性
    if 'left_knee_angle' in angles and 'right_knee_angle' in angles:
        left_knee = angles['left_knee_angle']
        right_knee = angles['right_knee_angle']
        knee_diff = abs(left_knee - right_knee)
        symmetry_scores['knee_symmetry'] = max(0, 100 - knee_diff)
        
    # 评估髋关节对称性
    if 'left_hip_angle' in angles and 'right_hip_angle' in angles:
        left_hip = angles['left_hip_angle']
        right_hip = angles['right_hip_angle']
        hip_diff = abs(left_hip - right_hip)
        symmetry_scores['hip_symmetry'] = max(0, 100 - hip_diff)
        
    # 评估踝关节对称性
    if 'left_ankle_angle' in angles and 'right_ankle_angle' in angles:
        left_ankle = angles['left_ankle_angle']
        right_ankle = angles['right_ankle_angle']
        ankle_diff = abs(left_ankle - right_ankle)
        symmetry_scores['ankle_symmetry'] = max(0, 100 - ankle_diff)
        
    return symmetry_scores