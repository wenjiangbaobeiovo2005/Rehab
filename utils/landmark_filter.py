"""
关键点滤波工具模块

该模块提供了对MediaPipe关键点数据进行滤波和平滑处理的函数。
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import deque


class LandmarkFilter:
    """
    关键点滤波器类
    
    使用移动平均法对关键点数据进行平滑处理，减少抖动。
    """
    
    def __init__(self, window_size: int = 5):
        """
        初始化滤波器
        
        Args:
            window_size: 移动平均窗口大小
        """
        self.window_size = window_size
        self.history: Dict[int, deque] = {}
        
    def reset(self):
        """重置滤波器历史数据"""
        self.history.clear()
        
    def filter_landmarks(self, landmarks: Dict[int, Tuple[float, float, float]]) -> Dict[int, Tuple[float, float, float]]:
        """
        对关键点数据进行滤波处理
        
        Args:
            landmarks: 原始关键点数据字典
            
        Returns:
            滤波后的关键点数据字典
        """
        filtered_landmarks = {}
        
        for landmark_id, (x, y, z) in landmarks.items():
            # 初始化历史记录
            if landmark_id not in self.history:
                self.history[landmark_id] = deque(maxlen=self.window_size)
                
            # 添加当前数据到历史记录
            self.history[landmark_id].append((x, y, z))
            
            # 计算移动平均值
            history_data = list(self.history[landmark_id])
            avg_x = sum([pt[0] for pt in history_data]) / len(history_data)
            avg_y = sum([pt[1] for pt in history_data]) / len(history_data)
            avg_z = sum([pt[2] for pt in history_data]) / len(history_data)
            
            filtered_landmarks[landmark_id] = (avg_x, avg_y, avg_z)
            
        return filtered_landmarks


def exponential_moving_average(current_value: float, 
                              previous_average: Optional[float], 
                              alpha: float = 0.3) -> float:
    """
    指数移动平均滤波
    
    Args:
        current_value: 当前值
        previous_average: 前一次的平均值
        alpha: 平滑系数，值越小越平滑 (0 < alpha <= 1)
        
    Returns:
        滤波后的值
    """
    if previous_average is None:
        return current_value
    return alpha * current_value + (1 - alpha) * previous_average


def median_filter(data: List[float], window_size: int = 3) -> List[float]:
    """
    中值滤波
    
    Args:
        data: 输入数据列表
        window_size: 滤波窗口大小（奇数）
        
    Returns:
        滤波后的数据列表
    """
    if window_size % 2 == 0:
        window_size += 1  # 确保窗口大小为奇数
        
    half_window = window_size // 2
    filtered_data = []
    
    for i in range(len(data)):
        # 确定窗口范围
        start = max(0, i - half_window)
        end = min(len(data), i + half_window + 1)
        
        # 获取窗口内的数据并排序
        window_data = sorted(data[start:end])
        
        # 取中值
        median_value = window_data[len(window_data) // 2]
        filtered_data.append(median_value)
        
    return filtered_data


def remove_outliers(data: List[float], threshold: float = 2.0) -> List[float]:
    """
    基于标准差的异常值去除
    
    Args:
        data: 输入数据列表
        threshold: 标准差阈值倍数
        
    Returns:
        去除异常值后的数据列表
    """
    if len(data) < 3:
        return data[:]
        
    mean_val = np.mean(data)
    std_val = np.std(data)
    
    filtered_data = []
    for val in data:
        if abs(val - mean_val) <= threshold * std_val:
            filtered_data.append(val)
        else:
            # 用均值替代异常值
            filtered_data.append(mean_val)
            
    return filtered_data