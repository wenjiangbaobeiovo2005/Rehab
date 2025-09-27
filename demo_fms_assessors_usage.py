#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FMS评估器使用演示

该脚本演示了如何在实际项目中使用FMS评估器模块。
"""

import sys
import os
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_squat_assessment():
    """演示深蹲动作评估"""
    print("=== 深蹲动作评估演示 ===")
    
    from fms_assessors.squat import SquatAssessor
    
    # 创建评估器实例
    assessor = SquatAssessor()
    
    # 模拟不同情况的深蹲评估
    
    # 1. 标准深蹲（正面视角）
    print("1. 标准深蹲（正面视角）:")
    front_angles = {
        'left_hip_angle': 125,
        'right_hip_angle': 123,
        'left_knee_angle': 95,
        'right_knee_angle': 93,
        'foot_shoulder_ratio': 105,
        'knee_valgus': 5
    }
    
    front_landmarks = {
        0: (0.5, 0.1, 0.0),   # 鼻子
        12: (0.4, 0.2, 0.0),  # 左肩
        11: (0.6, 0.2, 0.0),  # 右肩
        24: (0.4, 0.5, 0.0),  # 左髋
        23: (0.6, 0.5, 0.0),  # 右髋
        26: (0.4, 0.8, 0.0),  # 左膝
        25: (0.6, 0.8, 0.0),  # 右膝
    }
    
    result = assessor.assess(front_angles, front_landmarks)
    print(f"   评分: {result['score']}/3")
    print(f"   评估结果: {result['reasons'][0]}")
    if result['compensations']:
        print(f"   代偿模式: {', '.join(result['compensations'])}")
    print()
    
    # 2. 有代偿的深蹲（膝外翻）
    print("2. 有代偿的深蹲（膝外翻）:")
    compensatory_angles = {
        'left_hip_angle': 115,
        'right_hip_angle': 113,
        'left_knee_angle': 85,
        'right_knee_angle': 83,
        'foot_shoulder_ratio': 95,
        'knee_valgus': 20  # 膝外翻严重
    }
    
    result = assessor.assess(compensatory_angles, front_landmarks)
    print(f"   评分: {result['score']}/3")
    print(f"   评估结果: {result['reasons'][0]}")
    if result['compensations']:
        print(f"   代偿模式: {', '.join(result['compensations'])}")
    print()


def demo_comprehensive_fms_assessment():
    """演示完整的FMS评估"""
    print("=== 完整FMS评估演示 ===")
    
    # 导入所有评估器
    from fms_assessors import (
        SquatAssessor,
        HurdleStepAssessor,
        InlineLungeAssessor,
        ShoulderMobilityAssessor,
        ActiveLegRaiseAssessor,
        TrunkPushupAssessor,
        RotaryStabilityAssessor
    )
    
    # 创建所有评估器实例
    assessors = {
        '深蹲': SquatAssessor(),
        '跨栏步': HurdleStepAssessor(),
        '直线弓步蹲': InlineLungeAssessor(),
        '肩部灵活性': ShoulderMobilityAssessor(),
        '主动直腿上抬': ActiveLegRaiseAssessor(),
        '躯干稳定俯卧撑': TrunkPushupAssessor(),
        '旋转稳定性': RotaryStabilityAssessor()
    }
    
    # 模拟用户评估数据
    assessment_data = {
        '深蹲': {
            'angles': {
                'left_hip_angle': 120,
                'right_hip_angle': 118,
                'left_knee_angle': 90,
                'right_knee_angle': 88,
                'foot_shoulder_ratio': 100,
                'knee_valgus': 8
            },
            'landmarks': {
                0: (0.5, 0.1, 0.0),
                12: (0.4, 0.2, 0.0),
                11: (0.6, 0.2, 0.0),
                24: (0.4, 0.5, 0.0),
                23: (0.6, 0.5, 0.0),
                26: (0.4, 0.8, 0.0),
                25: (0.6, 0.8, 0.0),
            }
        },
        '跨栏步': {
            'angles': {
                'hip_angle': 90,
                'knee_angle': 85,
                'ankle_dorsiflexion': 12,
                'trunk_inclination': 8
            },
            'landmarks': {
                0: (0.5, 0.1, 0.0),
                23: (0.6, 0.5, 0.0),
                25: (0.6, 0.8, 0.0),
                27: (0.6, 1.0, 0.0),
            }
        },
        '直线弓步蹲': {
            'angles': {
                'front_leg_hip_angle': 95,
                'front_leg_knee_angle': 88,
                'back_leg_knee_angle': 8,
                'trunk_inclination': 12,
                'feet_separation': 12
            },
            'landmarks': {
                23: (0.6, 0.5, 0.0),
                25: (0.6, 0.8, 0.0),
                27: (0.6, 1.0, 0.0),
                24: (0.4, 0.5, 0.0),
                26: (0.4, 0.8, 0.0),
                28: (0.4, 1.0, 0.0),
            }
        },
        '肩部灵活性': {
            'angles': {
                'shoulder_elevation': 155,
                'shoulder_abduction': 152,
                'shoulder_internal_rotation': 55,
                'shoulder_extension': 45
            },
            'landmarks': {
                11: (0.6, 0.2, 0.0),
                12: (0.4, 0.2, 0.0),
                13: (0.6, 0.4, 0.0),
                14: (0.4, 0.4, 0.0),
            }
        },
        '主动直腿上抬': {
            'angles': {
                'thigh_angle': 65,  # 较低的抬腿角度
                'support_leg_stability': 92,
                'pelvis_tilt': 7,
                'knee_flexion': 6
            },
            'landmarks': {
                23: (0.6, 0.5, 0.0),
                25: (0.6, 0.8, 0.0),
                27: (0.6, 1.0, 0.0),
            }
        },
        '躯干稳定俯卧撑': {
            'angles': {
                'trunk_stability': 85,
                'elbow_flexion': 80,
                'shoulder_stability': 88,
                'core_control': 82,
                'body_alignment': 85
            },
            'landmarks': {
                11: (0.6, 0.2, 0.0),
                12: (0.4, 0.2, 0.0),
                13: (0.6, 0.4, 0.0),
                14: (0.4, 0.4, 0.0),
                23: (0.6, 0.5, 0.0),
                24: (0.4, 0.5, 0.0),
            }
        },
        '旋转稳定性': {
            'angles': {
                'trunk_rotation_control': 88,
                'limb_coordination': 85,
                'core_stability': 82,
                'movement_fluidity': 90,
                'contralateral_coordination': 87
            },
            'landmarks': {
                0: (0.5, 0.1, 0.0),
                11: (0.6, 0.2, 0.0),
                12: (0.4, 0.2, 0.0),
                23: (0.6, 0.5, 0.0),
                24: (0.4, 0.5, 0.0),
            }
        }
    }
    
    # 执行评估
    results = {}
    total_score = 0
    
    print("FMS评估结果:")
    print("-" * 40)
    
    for movement_name, assessor in assessors.items():
        data = assessment_data[movement_name]
        result = assessor.assess(data['angles'], data['landmarks'])
        results[movement_name] = result
        score = result['score']
        total_score += score
        
        print(f"{movement_name}: {score}/3分")
        print(f"  评估: {result['reasons'][0]}")
        if result['compensations']:
            print(f"  代偿: {', '.join(result['compensations'])}")
        print()
    
    print(f"总分: {total_score}/21分")
    
    # 分析结果
    print("评估分析:")
    print("-" * 40)
    
    # 找出评分最低的动作
    min_score = min(results.items(), key=lambda x: x[1]['score'])
    print(f"需要重点关注的动作: {min_score[0]} ({min_score[1]['score']}/3分)")
    
    # 统计代偿模式
    all_compensations = []
    for movement_name, result in results.items():
        all_compensations.extend(result['compensations'])
    
    if all_compensations:
        print(f"常见代偿模式: {', '.join(set(all_compensations))}")
    else:
        print("未发现明显代偿模式")
    
    print()


def demo_history_and_statistics():
    """演示历史记录和统计功能"""
    print("=== 历史记录和统计功能演示 ===")
    
    from fms_assessors.squat import SquatAssessor
    
    # 创建评估器实例
    assessor = SquatAssessor()
    
    # 模拟多次评估
    assessment_data = [
        {
            'angles': {'left_hip_angle': 120, 'right_hip_angle': 118, 'left_knee_angle': 90, 'right_knee_angle': 88, 'foot_shoulder_ratio': 100, 'knee_valgus': 8},
            'landmarks': {0: (0.5, 0.1, 0.0), 12: (0.4, 0.2, 0.0), 11: (0.6, 0.2, 0.0), 24: (0.4, 0.5, 0.0), 23: (0.6, 0.5, 0.0), 26: (0.4, 0.8, 0.0), 25: (0.6, 0.8, 0.0)}
        },
        {
            'angles': {'left_hip_angle': 125, 'right_hip_angle': 123, 'left_knee_angle': 95, 'right_knee_angle': 93, 'foot_shoulder_ratio': 105, 'knee_valgus': 5},
            'landmarks': {0: (0.5, 0.1, 0.0), 12: (0.4, 0.2, 0.0), 11: (0.6, 0.2, 0.0), 24: (0.4, 0.5, 0.0), 23: (0.6, 0.5, 0.0), 26: (0.4, 0.8, 0.0), 25: (0.6, 0.8, 0.0)}
        },
        {
            'angles': {'left_hip_angle': 115, 'right_hip_angle': 113, 'left_knee_angle': 85, 'right_knee_angle': 83, 'foot_shoulder_ratio': 95, 'knee_valgus': 12},
            'landmarks': {0: (0.5, 0.1, 0.0), 12: (0.4, 0.2, 0.0), 11: (0.6, 0.2, 0.0), 24: (0.4, 0.5, 0.0), 23: (0.6, 0.5, 0.0), 26: (0.4, 0.8, 0.0), 25: (0.6, 0.8, 0.0)}
        }
    ]
    
    # 执行多次评估
    for i, data in enumerate(assessment_data, 1):
        result = assessor.assess(data['angles'], data['landmarks'])
        print(f"第{i}次评估: {result['score']}/3分")
    
    # 查看历史记录
    history = assessor.get_history()
    print(f"\n历史记录总数: {len(history)}")
    
    # 计算平均评分
    avg_score = assessor.get_average_score()
    print(f"平均评分: {avg_score:.2f}/3分")
    
    print()


def main():
    """主函数"""
    print("FMS评估器使用演示")
    print("=" * 50)
    
    demo_squat_assessment()
    demo_comprehensive_fms_assessment()
    demo_history_and_statistics()
    
    print("演示完成！")


if __name__ == "__main__":
    main()