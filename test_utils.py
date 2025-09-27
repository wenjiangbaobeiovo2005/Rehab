#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试工具模块
"""

import sys
import os
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_angle_calculations():
    """测试角度计算工具"""
    print("角度计算工具测试")
    print("=" * 30)
    
    try:
        from utils.angle_calculations import (
            calculate_joint_angle,
            calculate_distance,
            calculate_trunk_angle,
            calculate_heel_lift,
            calculate_trunk_rotation
        )
        
        # 测试关节角度计算
        a = (0, 0, 0)  # 点A
        b = (1, 1, 0)  # 关节点B
        c = (2, 0, 0)  # 点C
        angle = calculate_joint_angle(a, b, c)
        print(f"✓ 关节角度计算: {angle:.2f}度")
        
        # 测试距离计算
        distance = calculate_distance(a, c)
        print(f"✓ 距离计算: {distance:.2f}")
        
        # 测试躯干角度计算
        hip = (0.5, 0.6, 0)
        shoulder = (0.5, 0.3, 0)
        trunk_angle = calculate_trunk_angle(hip, shoulder)
        print(f"✓ 躯干角度计算: {trunk_angle:.2f}度")
        
        # 测试脚跟离地高度计算
        heel = (0.5, 0.1, 0)
        ankle = (0.5, 0.0, 0)
        heel_lift = calculate_heel_lift(heel, ankle)
        print(f"✓ 脚跟离地高度计算: {heel_lift:.2f}")
        
        # 测试躯干旋转角度计算
        left_shoulder = (0.3, 0.3, 0)
        right_shoulder = (0.7, 0.3, 0)
        left_hip = (0.3, 0.6, 0)
        right_hip = (0.7, 0.6, 0)
        trunk_rotation = calculate_trunk_rotation(left_shoulder, right_shoulder, left_hip, right_hip)
        print(f"✓ 躯干旋转角度计算: {trunk_rotation:.2f}度")
        
    except Exception as e:
        print(f"✗ 角度计算工具测试失败: {e}")


def test_landmark_filter():
    """测试关键点滤波器"""
    print("\n关键点滤波器测试")
    print("=" * 30)
    
    try:
        from utils.landmark_filter import LandmarkFilter
        
        # 创建滤波器实例
        filter = LandmarkFilter(window_size=3)
        print("✓ 关键点滤波器实例化成功")
        
        # 测试滤波功能
        landmarks = {
            0: (0.5, 0.2, 0.8),   # 鼻子
            12: (0.4, 0.4, 0.9),  # 左肩
            11: (0.6, 0.4, 0.9),  # 右肩
        }
        
        filtered = filter.filter_landmarks(landmarks)
        print("✓ 关键点滤波功能正常")
        print(f"  滤波后关键点数量: {len(filtered)}")
        
        # 测试重置功能
        filter.reset()
        print("✓ 重置功能正常")
        
    except Exception as e:
        print(f"✗ 关键点滤波器测试失败: {e}")


def test_movement_analysis():
    """测试动作轨迹分析工具"""
    print("\n动作轨迹分析工具测试")
    print("=" * 30)
    
    try:
        from utils.movement_analysis import (
            calculate_velocity,
            calculate_acceleration,
            detect_movement_peaks,
            calculate_movement_range,
            calculate_smoothness,
            calculate_symmetry
        )
        
        # 测试速度计算
        positions = [(0, 0, 0), (1, 1, 0), (2, 2, 0), (3, 3, 0)]
        frame_times = [0, 0.1, 0.2, 0.3]
        velocities = calculate_velocity(positions, frame_times)
        print(f"✓ 速度计算功能正常，结果数量: {len(velocities)}")
        
        # 测试加速度计算
        accelerations = calculate_acceleration(velocities, frame_times)
        print(f"✓ 加速度计算功能正常，结果数量: {len(accelerations)}")
        
        # 测试峰值检测
        y_positions = [0, 0.1, 0.3, 0.6, 0.8, 1.0, 0.9, 0.7, 0.4, 0.2, 0.1, 0]
        peaks, properties = detect_movement_peaks(y_positions)
        print(f"✓ 峰值检测功能正常，峰值数: {len(peaks)}")
        
        # 测试动作范围计算
        movement_range = calculate_movement_range(y_positions)
        print(f"✓ 动作范围计算功能正常")
        
        # 测试平滑度计算
        smoothness = calculate_smoothness(y_positions)
        print(f"✓ 平滑度计算: {smoothness:.2f}")
        
        # 测试对称性计算
        left_data = [0.1, 0.3, 0.6, 0.8, 1.0, 0.9, 0.7, 0.4, 0.2, 0.1]
        right_data = [0.1, 0.3, 0.6, 0.8, 1.0, 0.9, 0.7, 0.4, 0.2, 0.1]
        symmetry = calculate_symmetry(left_data, right_data)
        print(f"✓ 对称性计算: {symmetry:.2f}")
        
    except Exception as e:
        print(f"✗ 动作轨迹分析工具测试失败: {e}")


def test_symmetry_analysis():
    """测试对称性分析工具"""
    print("\n对称性分析工具测试")
    print("=" * 30)
    
    try:
        from utils.symmetry_analysis import (
            compare_bilateral_symmetry,
            calculate_symmetry_index,
            detect_asymmetry_patterns,
            evaluate_movement_symmetry
        )
        
        # 测试双侧对称性比较
        left_angles = {'knee': 90, 'hip': 85}
        right_angles = {'knee': 88, 'hip': 87}
        angle_pairs = [('knee', 'knee'), ('hip', 'hip')]
        symmetry_results = compare_bilateral_symmetry(left_angles, right_angles, angle_pairs)
        print(f"✓ 双侧对称性比较功能正常")
        print(f"  对称性结果: {symmetry_results}")
        
        # 测试对称性指数计算
        left_measurements = [90, 85, 80]
        right_measurements = [88, 87, 82]
        symmetry_index = calculate_symmetry_index(left_measurements, right_measurements)
        print(f"✓ 对称性指数计算: {symmetry_index:.2f}")
        
        # 测试不对称模式检测
        angles_history = [
            {'left_knee': 90, 'right_knee': 88},
            {'left_knee': 92, 'right_knee': 86},
            {'left_knee': 89, 'right_knee': 85}
        ]
        asymmetries = detect_asymmetry_patterns(angles_history)
        print(f"✓ 不对称模式检测功能正常")
        
        # 测试动作对称性评估
        current_angles = {'left_knee_angle': 90, 'right_knee_angle': 88}
        movement_symmetry = evaluate_movement_symmetry(current_angles)
        print(f"✓ 动作对称性评估功能正常")
        
    except Exception as e:
        print(f"✗ 对称性分析工具测试失败: {e}")


def test_module_imports():
    """测试模块导入"""
    print("工具模块导入测试")
    print("=" * 30)
    
    try:
        from utils import (
            calculate_joint_angle,
            calculate_distance,
            calculate_trunk_angle,
            calculate_heel_lift,
            calculate_trunk_rotation,
            LandmarkFilter,
            calculate_velocity,
            calculate_acceleration,
            detect_movement_peaks,
            compare_bilateral_symmetry,
            calculate_symmetry_index,
            evaluate_movement_symmetry
        )
        print("✓ 所有工具模块导入成功")
    except Exception as e:
        print(f"✗ 工具模块导入失败: {e}")


if __name__ == "__main__":
    test_module_imports()
    test_angle_calculations()
    test_landmark_filter()
    test_movement_analysis()
    test_symmetry_analysis()
    print("\n所有测试完成")