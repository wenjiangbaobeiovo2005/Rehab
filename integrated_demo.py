#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
集成演示脚本

该脚本演示了如何将FMS评估器与工具模块集成使用，模拟完整的FMS评估流程。
"""

import sys
import os
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.angle_calculations import calculate_joint_angle
from utils.landmark_filter import LandmarkFilter
from utils.symmetry_analysis import compare_bilateral_symmetry
from fms_assessors.squat import SquatAssessor


def simulate_keypoints_data():
    """模拟关键点数据"""
    # 模拟深蹲动作中的关键点数据（带噪声）
    np.random.seed(42)  # 固定随机种子以获得可重复的结果
    
    # 模拟10帧的深蹲动作数据
    frames_data = []
    for i in range(10):
        # 添加一些噪声来模拟真实情况
        noise = np.random.normal(0, 0.02, 3)  # 均值0，标准差0.02的正态分布噪声
        
        # 模拟深蹲动作中关键点的变化
        # 简化的深蹲动作，只考虑几个关键点
        landmarks = {
            0: (0.5 + noise[0], 0.1 + noise[1]*0.5, 0.0 + noise[2]),   # 鼻子
            12: (0.4 + noise[0]*0.8, 0.2 + noise[1]*0.3, 0.0 + noise[2]),  # 左肩
            11: (0.6 + noise[0]*0.8, 0.2 + noise[1]*0.3, 0.0 + noise[2]),  # 右肩
            24: (0.4 + noise[0]*0.6, 0.5 + noise[1]*0.4, 0.0 + noise[2]),  # 左髋
            23: (0.6 + noise[0]*0.6, 0.5 + noise[1]*0.4, 0.0 + noise[2]),  # 右髋
            26: (0.4 + noise[0]*0.4, 0.8 + noise[1]*0.2, 0.0 + noise[2]),  # 左膝
            25: (0.6 + noise[0]*0.4, 0.8 + noise[1]*0.2, 0.0 + noise[2]),  # 右膝
            28: (0.4 + noise[0]*0.2, 1.0 + noise[1]*0.1, 0.0 + noise[2]),  # 左踝
            27: (0.6 + noise[0]*0.2, 1.0 + noise[1]*0.1, 0.0 + noise[2]),  # 右踝
        }
        frames_data.append(landmarks)
    
    return frames_data


def process_landmarks_with_filtering(frames_data):
    """使用滤波器处理关键点数据"""
    print("=== 关键点数据滤波处理 ===")
    
    # 创建滤波器
    filter = LandmarkFilter(window_size=5)
    
    # 处理每一帧数据
    filtered_frames = []
    for i, landmarks in enumerate(frames_data):
        filtered_landmarks = filter.filter_landmarks(landmarks)
        filtered_frames.append(filtered_landmarks)
        print(f"帧 {i+1}: 已应用滤波处理")
    
    print(f"总共处理了 {len(filtered_frames)} 帧数据\n")
    return filtered_frames


def calculate_angles_from_landmarks(filtered_frames):
    """从关键点数据计算关节角度"""
    print("=== 关节角度计算 ===")
    
    angles_history = []
    for i, landmarks in enumerate(filtered_frames):
        # 计算左腿角度
        left_hip_angle = calculate_joint_angle(landmarks[12], landmarks[24], landmarks[26])
        left_knee_angle = calculate_joint_angle(landmarks[24], landmarks[26], landmarks[28])
        
        # 计算右腿角度
        right_hip_angle = calculate_joint_angle(landmarks[11], landmarks[23], landmarks[25])
        right_knee_angle = calculate_joint_angle(landmarks[23], landmarks[25], landmarks[27])
        
        # 计算双脚与肩宽的比例
        shoulder_width = abs(landmarks[11][0] - landmarks[12][0])
        foot_width = abs(landmarks[25][0] - landmarks[26][0])
        foot_shoulder_ratio = (foot_width / shoulder_width) * 100 if shoulder_width > 0 else 100
        
        angles = {
            'left_hip_angle': left_hip_angle,
            'left_knee_angle': left_knee_angle,
            'right_hip_angle': right_hip_angle,
            'right_knee_angle': right_knee_angle,
            'foot_shoulder_ratio': foot_shoulder_ratio
        }
        
        angles_history.append(angles)
        print(f"帧 {i+1}: 左髋 {left_hip_angle:.1f}°, 左膝 {left_knee_angle:.1f}°, "
              f"右髋 {right_hip_angle:.1f}°, 右膝 {right_knee_angle:.1f}°")
    
    print(f"总共计算了 {len(angles_history)} 帧的角度数据\n")
    return angles_history


def analyze_symmetry(angles_history):
    """分析左右对称性"""
    print("=== 对称性分析 ===")
    
    # 取最后一帧进行分析
    if angles_history:
        final_angles = angles_history[-1]
        print(f"最终帧角度数据:")
        print(f"  左髋: {final_angles['left_hip_angle']:.1f}°")
        print(f"  右髋: {final_angles['right_hip_angle']:.1f}°")
        print(f"  左膝: {final_angles['left_knee_angle']:.1f}°")
        print(f"  右膝: {final_angles['right_knee_angle']:.1f}°")
        
        # 对称性比较
        left_angles = {'hip': final_angles['left_hip_angle'], 'knee': final_angles['left_knee_angle']}
        right_angles = {'hip': final_angles['right_hip_angle'], 'knee': final_angles['right_knee_angle']}
        angle_pairs = [('hip', 'hip'), ('knee', 'knee')]
        
        symmetry_results = compare_bilateral_symmetry(left_angles, right_angles, angle_pairs)
        print(f"对称性分析结果:")
        for key, value in symmetry_results.items():
            print(f"  {key}: {value:.2f}")
    
    print()


def perform_fms_assessment(angles_history, filtered_frames):
    """执行FMS评估"""
    print("=== FMS深蹲动作评估 ===")
    
    # 创建评估器
    assessor = SquatAssessor()
    
    # 使用最后一帧数据进行评估
    if angles_history and filtered_frames:
        final_angles = angles_history[-1]
        final_landmarks = filtered_frames[-1]
        
        # 添加一些额外的角度参数用于评估
        extended_angles = final_angles.copy()
        extended_angles['knee_valgus'] = abs(final_angles['left_knee_angle'] - final_angles['right_knee_angle'])
        
        # 执行评估
        result = assessor.assess(extended_angles, final_landmarks)
        
        print(f"评估结果:")
        print(f"  评分: {result['score']}/3")
        print(f"  评估原因: {result['reasons'][0]}")
        if result['compensations']:
            print(f"  代偿模式: {', '.join(result['compensations'])}")
        
        # 查看历史记录
        history = assessor.get_history()
        print(f"  评估历史记录数: {len(history)}")
        
        # 计算平均评分
        avg_score = assessor.get_average_score()
        print(f"  平均评分: {avg_score:.2f}/3")
    
    print()


def main():
    """主函数"""
    print("FMS评估系统集成演示")
    print("=" * 50)
    
    # 1. 模拟关键点数据
    frames_data = simulate_keypoints_data()
    
    # 2. 使用滤波器处理关键点数据
    filtered_frames = process_landmarks_with_filtering(frames_data)
    
    # 3. 从关键点数据计算关节角度
    angles_history = calculate_angles_from_landmarks(filtered_frames)
    
    # 4. 分析左右对称性
    analyze_symmetry(angles_history)
    
    # 5. 执行FMS评估
    perform_fms_assessment(angles_history, filtered_frames)
    
    print("集成演示完成！")


if __name__ == "__main__":
    main()