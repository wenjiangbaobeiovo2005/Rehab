#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工具模块使用演示

该脚本演示了如何在实际项目中使用utils模块中的各种工具函数。
"""

import sys
import os
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.angle_calculations import calculate_joint_angle
from utils.landmark_filter import LandmarkFilter
from utils.movement_analysis import (
    calculate_velocity, 
    calculate_acceleration, 
    detect_movement_peaks,
    calculate_movement_range
)
from utils.symmetry_analysis import compare_bilateral_symmetry


def demo_angle_calculations():
    """演示角度计算工具的使用"""
    print("=== 角度计算工具演示 ===")
    
    # 模拟关键点数据（鼻子、左肩、右肩、左髋、右髋、左膝、右膝）
    landmarks = {
        0: (0.5, 0.1, 0.0),   # 鼻子
        11: (0.6, 0.2, 0.0),  # 右肩
        12: (0.4, 0.2, 0.0),  # 左肩
        23: (0.6, 0.5, 0.0),  # 右髋
        24: (0.4, 0.5, 0.0),  # 左髋
        25: (0.6, 0.8, 0.0),  # 右膝
        26: (0.4, 0.8, 0.0),  # 左膝
    }
    
    # 计算左膝角度（髋-膝-踝，这里用髋代替踝做演示）
    left_knee_angle = calculate_joint_angle(landmarks[24], landmarks[26], landmarks[23])
    print(f"左膝角度: {left_knee_angle:.2f}度")
    
    # 计算右膝角度
    right_knee_angle = calculate_joint_angle(landmarks[23], landmarks[25], landmarks[24])
    print(f"右膝角度: {right_knee_angle:.2f}度")
    
    print()


def demo_landmark_filtering():
    """演示关键点滤波工具的使用"""
    print("=== 关键点滤波工具演示 ===")
    
    # 创建滤波器
    filter = LandmarkFilter(window_size=5)
    
    # 模拟带噪声的关键点数据
    print("滤波前的关键点数据:")
    noisy_landmarks = {
        25: (0.6 + np.random.normal(0, 0.01), 0.8 + np.random.normal(0, 0.01), 0.0),  # 右膝
        26: (0.4 + np.random.normal(0, 0.01), 0.8 + np.random.normal(0, 0.01), 0.0),  # 左膝
    }
    
    for i in range(5):
        # 添加噪声
        landmarks = {
            25: (0.6 + np.random.normal(0, 0.01), 0.8 + np.random.normal(0, 0.01), 0.0),
            26: (0.4 + np.random.normal(0, 0.01), 0.8 + np.random.normal(0, 0.01), 0.0),
        }
        print(f"  帧 {i+1}: 右膝({landmarks[25][0]:.3f}, {landmarks[25][1]:.3f}), "
              f"左膝({landmarks[26][0]:.3f}, {landmarks[26][1]:.3f})")
        
        # 应用滤波
        filtered = filter.filter_landmarks(landmarks)
        
    print("滤波后的关键点数据:")
    print(f"  右膝({filtered[25][0]:.3f}, {filtered[25][1]:.3f})")
    print(f"  左膝({filtered[26][0]:.3f}, {filtered[26][1]:.3f})")
    
    print()


def demo_movement_analysis():
    """演示动作轨迹分析工具的使用"""
    print("=== 动作轨迹分析工具演示 ===")
    
    # 模拟深蹲动作中某关键点的y坐标变化
    # 从站起到深蹲再站起的过程
    y_positions = [0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.65, 0.55, 0.45, 0.35, 0.25, 0.2]
    frame_times = [i * 0.1 for i in range(len(y_positions))]  # 每帧间隔0.1秒
    positions = [(0.5, y, 0.0) for y in y_positions]  # 假设x,z坐标不变
    
    # 计算速度
    velocities = calculate_velocity(positions, frame_times)
    print(f"速度计算完成，共{len(velocities)}个数据点")
    
    # 计算加速度
    accelerations = calculate_acceleration(velocities, frame_times)
    print(f"加速度计算完成，共{len(accelerations)}个数据点")
    
    # 检测运动峰值（深蹲的最低点）
    peaks, properties = detect_movement_peaks(y_positions)
    print(f"检测到{len(peaks)}个运动峰值")
    if peaks:
        print(f"  深蹲最低点出现在第{peaks[0]}帧，y坐标: {y_positions[peaks[0]]:.3f}")
    
    # 计算运动范围
    movement_range = calculate_movement_range(y_positions)
    print(f"运动范围: {movement_range['min']:.3f} - {movement_range['max']:.3f} (范围: {movement_range['range']:.3f})")
    
    print()


def demo_symmetry_analysis():
    """演示对称性分析工具的使用"""
    print("=== 对称性分析工具演示 ===")
    
    # 模拟左右两侧的关节角度测量
    left_angles = {
        'knee': 95,
        'hip': 85,
        'ankle': 80
    }
    
    right_angles = {
        'knee': 92,
        'hip': 87,
        'ankle': 82
    }
    
    # 比较双侧对称性
    angle_pairs = [('knee', 'knee'), ('hip', 'hip'), ('ankle', 'ankle')]
    symmetry_results = compare_bilateral_symmetry(left_angles, right_angles, angle_pairs)
    
    print("双侧对称性分析结果:")
    for key, value in symmetry_results.items():
        print(f"  {key}: {value:.2f}")
    
    print()


def main():
    """主函数"""
    print("FMS工具模块使用演示")
    print("=" * 50)
    
    demo_angle_calculations()
    demo_landmark_filtering()
    demo_movement_analysis()
    demo_symmetry_analysis()
    
    print("演示完成！")


if __name__ == "__main__":
    main()