"""
角度计算工具模块

该模块提供了计算人体关节角度的函数。
"""

import numpy as np
from typing import Tuple


def calculate_joint_angle(a: Tuple[float, float, float], 
                         b: Tuple[float, float, float], 
                         c: Tuple[float, float, float]) -> float:
    """
    计算三点形成的关节角度（单位：度）
    
    Args:
        a: 第一个点的坐标 (x, y, z)
        b: 关节中心点的坐标 (x, y, z)
        c: 第三个点的坐标 (x, y, z)
        
    Returns:
        关节角度（度）
    """
    # 转换为numpy数组
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    # 计算向量
    ba = a - b
    bc = c - b
    
    # 计算点积和模长
    dot_product = np.dot(ba, bc)
    len_ba = np.linalg.norm(ba)
    len_bc = np.linalg.norm(bc)
    
    # 计算余弦值
    cosine_angle = dot_product / (len_ba * len_bc) if (len_ba * len_bc) > 0 else 1.0
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # 防止数值误差
    
    # 转换为角度
    angle = np.degrees(np.arccos(cosine_angle))
    return angle


def calculate_distance(a: Tuple[float, float, float], 
                      b: Tuple[float, float, float]) -> float:
    """
    计算两点之间的距离
    
    Args:
        a: 第一个点的坐标 (x, y, z)
        b: 第二个点的坐标 (x, y, z)
        
    Returns:
        两点之间的距离
    """
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a - b)


def calculate_trunk_angle(hip: Tuple[float, float, float], 
                         shoulder: Tuple[float, float, float]) -> float:
    """
    计算躯干与垂直线的夹角
    
    Args:
        hip: 髋关节坐标 (x, y, z)
        shoulder: 肩膀坐标 (x, y, z)
        
    Returns:
        躯干与垂直线的夹角（度）
    """
    # 计算躯干向量（从髋到肩）
    trunk_vector = np.array([shoulder[0] - hip[0], shoulder[1] - hip[1]])
    # 垂直参考向量
    vertical_vector = np.array([0, 1])  # 向下为正
    
    # 计算角度
    dot_product = np.dot(trunk_vector, vertical_vector)
    len_trunk = np.linalg.norm(trunk_vector)
    len_vertical = np.linalg.norm(vertical_vector)
    
    cosine_angle = dot_product / (len_trunk * len_vertical) if (len_trunk * len_vertical) > 0 else 1.0
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    angle = np.degrees(np.arccos(cosine_angle))
    return angle


def calculate_heel_lift(heel: Tuple[float, float, float], 
                       ankle: Tuple[float, float, float]) -> float:
    """
    计算脚跟离地高度（百分比）
    
    Args:
        heel: 脚跟坐标 (x, y, z)
        ankle: 踝关节坐标 (x, y, z)
        
    Returns:
        脚跟离地高度（相对于踝关节y坐标的百分比）
    """
    # 简单估计：脚跟y坐标与踝关节y坐标的差值
    # 值越大表示脚跟抬得越高
    return abs(heel[1] - ankle[1]) * 100


def calculate_trunk_rotation(left_shoulder: Tuple[float, float, float],
                            right_shoulder: Tuple[float, float, float],
                            left_hip: Tuple[float, float, float],
                            right_hip: Tuple[float, float, float]) -> float:
    """
    计算躯干旋转角度
    
    Args:
        left_shoulder: 左肩坐标 (x, y, z)
        right_shoulder: 右肩坐标 (x, y, z)
        left_hip: 左髋坐标 (x, y, z)
        right_hip: 右髋坐标 (x, y, z)
        
    Returns:
        躯干旋转角度（度）
    """
    # 计算肩线和腰线的角度差
    shoulder_vector = np.array([right_shoulder[0] - left_shoulder[0], right_shoulder[1] - left_shoulder[1]])
    hip_vector = np.array([right_hip[0] - left_hip[0], right_hip[1] - left_hip[1]])
    
    # 计算两个向量的角度
    dot_product = np.dot(shoulder_vector, hip_vector)
    len_shoulder = np.linalg.norm(shoulder_vector)
    len_hip = np.linalg.norm(hip_vector)
    
    if len_shoulder == 0 or len_hip == 0:
        return 0
        
    cosine_angle = dot_product / (len_shoulder * len_hip)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    angle = np.degrees(np.arccos(cosine_angle))
    return angle