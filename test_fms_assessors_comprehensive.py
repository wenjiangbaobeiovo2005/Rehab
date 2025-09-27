#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FMS评估器综合测试脚本

该脚本用于测试所有FMS评估器的功能完整性和正确性。
"""

import sys
import os
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_squat_assessor():
    """测试深蹲评估器"""
    print("=== 深蹲评估器测试 ===")
    
    try:
        from fms_assessors.squat import SquatAssessor
        
        # 创建评估器实例
        assessor = SquatAssessor()
        print("✓ 深蹲评估器实例化成功")
        
        # 测试重置功能
        assessor.reset()
        print("✓ 重置功能正常")
        
        # 测试正面视角评估
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
        
        front_result = assessor.assess(front_angles, front_landmarks)
        print(f"✓ 正面视角评估完成，评分: {front_result['score']}")
        print(f"  评估原因: {front_result['reasons']}")
        print(f"  代偿模式: {front_result['compensations']}")
        
        # 测试侧面视角评估
        side_angles = {
            'trunk_angle': 15,
            'hip_angle': 125,
            'knee_angle': 95,
            'ankle_angle': 75,
            'heel_lift': 2
        }
        
        side_result = assessor.assess(side_angles, front_landmarks)
        print(f"✓ 侧面视角评估完成，评分: {side_result['score']}")
        
        # 测试45度角视角评估
        angle45_angles = {
            'side_hip_angle': 120,
            'side_knee_angle': 90,
            'trunk_rotation': 5
        }
        
        angle45_result = assessor.assess(angle45_angles, front_landmarks)
        print(f"✓ 45度角视角评估完成，评分: {angle45_result['score']}")
        
        # 测试历史记录功能
        history = assessor.get_history()
        print(f"✓ 历史记录功能正常，记录数: {len(history)}")
        
        # 测试平均评分功能
        avg_score = assessor.get_average_score()
        print(f"✓ 平均评分计算正常: {avg_score:.2f}")
        
    except Exception as e:
        print(f"✗ 深蹲评估器测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_hurdle_step_assessor():
    """测试跨栏步评估器"""
    print("\n=== 跨栏步评估器测试 ===")
    
    try:
        from fms_assessors.hurdle_step import HurdleStepAssessor
        
        # 创建评估器实例
        assessor = HurdleStepAssessor()
        print("✓ 跨栏步评估器实例化成功")
        
        # 测试评估功能
        angles = {
            'hip_angle': 95,
            'knee_angle': 92,
            'ankle_dorsiflexion': 15,
            'trunk_inclination': 5
        }
        
        landmarks = {
            0: (0.5, 0.1, 0.0),   # 鼻子
            23: (0.6, 0.5, 0.0),  # 髋关节
            25: (0.6, 0.8, 0.0),  # 膝关节
            27: (0.6, 1.0, 0.0),  # 踝关节
        }
        
        result = assessor.assess(angles, landmarks)
        print(f"✓ 跨栏步评估完成，评分: {result['score']}")
        print(f"  评估原因: {result['reasons']}")
        print(f"  代偿模式: {result['compensations']}")
        
    except Exception as e:
        print(f"✗ 跨栏步评估器测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_inline_lunge_assessor():
    """测试直线弓步蹲评估器"""
    print("\n=== 直线弓步蹲评估器测试 ===")
    
    try:
        from fms_assessors.inline_lunge import InlineLungeAssessor
        
        # 创建评估器实例
        assessor = InlineLungeAssessor()
        print("✓ 直线弓步蹲评估器实例化成功")
        
        # 测试评估功能
        angles = {
            'front_leg_hip_angle': 100,
            'front_leg_knee_angle': 95,
            'back_leg_knee_angle': 5,
            'trunk_inclination': 10,
            'feet_separation': 15
        }
        
        landmarks = {
            23: (0.6, 0.5, 0.0),  # 前腿髋关节
            25: (0.6, 0.8, 0.0),  # 前腿膝关节
            27: (0.6, 1.0, 0.0),  # 前腿踝关节
            24: (0.4, 0.5, 0.0),  # 后腿髋关节
            26: (0.4, 0.8, 0.0),  # 后腿膝关节
            28: (0.4, 1.0, 0.0),  # 后腿踝关节
        }
        
        result = assessor.assess(angles, landmarks)
        print(f"✓ 直线弓步蹲评估完成，评分: {result['score']}")
        print(f"  评估原因: {result['reasons']}")
        print(f"  代偿模式: {result['compensations']}")
        
    except Exception as e:
        print(f"✗ 直线弓步蹲评估器测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_shoulder_mobility_assessor():
    """测试肩部灵活性评估器"""
    print("\n=== 肩部灵活性评估器测试 ===")
    
    try:
        from fms_assessors.shoulder_mobility import ShoulderMobilityAssessor
        
        # 创建评估器实例
        assessor = ShoulderMobilityAssessor()
        print("✓ 肩部灵活性评估器实例化成功")
        
        # 测试评估功能
        angles = {
            'shoulder_elevation': 165,
            'shoulder_abduction': 162,
            'shoulder_internal_rotation': 65,
            'shoulder_extension': 55
        }
        
        landmarks = {
            11: (0.6, 0.2, 0.0),  # 右肩
            12: (0.4, 0.2, 0.0),  # 左肩
            13: (0.6, 0.4, 0.0),  # 右肘
            14: (0.4, 0.4, 0.0),  # 左肘
        }
        
        result = assessor.assess(angles, landmarks)
        print(f"✓ 肩部灵活性评估完成，评分: {result['score']}")
        print(f"  评估原因: {result['reasons']}")
        print(f"  代偿模式: {result['compensations']}")
        
    except Exception as e:
        print(f"✗ 肩部灵活性评估器测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_active_leg_raise_assessor():
    """测试主动直腿上抬评估器"""
    print("\n=== 主动直腿上抬评估器测试 ===")
    
    try:
        from fms_assessors.active_leg_raise import ActiveLegRaiseAssessor
        
        # 创建评估器实例
        assessor = ActiveLegRaiseAssessor()
        print("✓ 主动直腿上抬评估器实例化成功")
        
        # 测试评估功能
        angles = {
            'thigh_angle': 75,
            'support_leg_stability': 95,
            'pelvis_tilt': 5,
            'knee_flexion': 5
        }
        
        landmarks = {
            23: (0.6, 0.5, 0.0),  # 髋关节
            25: (0.6, 0.8, 0.0),  # 膝关节
            27: (0.6, 1.0, 0.0),  # 踝关节
        }
        
        result = assessor.assess(angles, landmarks)
        print(f"✓ 主动直腿上抬评估完成，评分: {result['score']}")
        print(f"  评估原因: {result['reasons']}")
        print(f"  代偿模式: {result['compensations']}")
        
    except Exception as e:
        print(f"✗ 主动直腿上抬评估器测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_trunk_pushup_assessor():
    """测试躯干稳定俯卧撑评估器"""
    print("\n=== 躯干稳定俯卧撑评估器测试 ===")
    
    try:
        from fms_assessors.trunk_pushup import TrunkPushupAssessor
        
        # 创建评估器实例
        assessor = TrunkPushupAssessor()
        print("✓ 躯干稳定俯卧撑评估器实例化成功")
        
        # 测试评估功能
        angles = {
            'trunk_stability': 95,
            'elbow_flexion': 85,
            'shoulder_stability': 92,
            'core_control': 90,
            'body_alignment': 93
        }
        
        landmarks = {
            11: (0.6, 0.2, 0.0),  # 右肩
            12: (0.4, 0.2, 0.0),  # 左肩
            13: (0.6, 0.4, 0.0),  # 右肘
            14: (0.4, 0.4, 0.0),  # 左肘
            23: (0.6, 0.5, 0.0),  # 右髋
            24: (0.4, 0.5, 0.0),  # 左髋
        }
        
        result = assessor.assess(angles, landmarks)
        print(f"✓ 躯干稳定俯卧撑评估完成，评分: {result['score']}")
        print(f"  评估原因: {result['reasons']}")
        print(f"  代偿模式: {result['compensations']}")
        
    except Exception as e:
        print(f"✗ 躯干稳定俯卧撑评估器测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_rotary_stability_assessor():
    """测试旋转稳定性评估器"""
    print("\n=== 旋转稳定性评估器测试 ===")
    
    try:
        from fms_assessors.rotary_stability import RotaryStabilityAssessor
        
        # 创建评估器实例
        assessor = RotaryStabilityAssessor()
        print("✓ 旋转稳定性评估器实例化成功")
        
        # 测试评估功能
        angles = {
            'trunk_rotation_control': 95,
            'limb_coordination': 92,
            'core_stability': 90,
            'movement_fluidity': 93,
            'contralateral_coordination': 91
        }
        
        landmarks = {
            0: (0.5, 0.1, 0.0),   # 鼻子
            11: (0.6, 0.2, 0.0),  # 右肩
            12: (0.4, 0.2, 0.0),  # 左肩
            23: (0.6, 0.5, 0.0),  # 右髋
            24: (0.4, 0.5, 0.0),  # 左髋
        }
        
        result = assessor.assess(angles, landmarks)
        print(f"✓ 旋转稳定性评估完成，评分: {result['score']}")
        print(f"  评估原因: {result['reasons']}")
        print(f"  代偿模式: {result['compensations']}")
        
    except Exception as e:
        print(f"✗ 旋转稳定性评估器测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_all_assessors_import():
    """测试所有评估器导入"""
    print("=== FMS评估器导入测试 ===")
    
    try:
        from fms_assessors import (
            SquatAssessor,
            HurdleStepAssessor,
            InlineLungeAssessor,
            ShoulderMobilityAssessor,
            ActiveLegRaiseAssessor,
            TrunkPushupAssessor,
            RotaryStabilityAssessor
        )
        print("✓ 所有FMS评估器导入成功")
        return True
    except Exception as e:
        print(f"✗ FMS评估器导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("FMS评估器综合测试")
    print("=" * 50)
    
    # 测试导入
    if not test_all_assessors_import():
        print("由于导入失败，终止测试")
        return
    
    # 测试各个评估器
    test_squat_assessor()
    test_hurdle_step_assessor()
    test_inline_lunge_assessor()
    test_shoulder_mobility_assessor()
    test_active_leg_raise_assessor()
    test_trunk_pushup_assessor()
    test_rotary_stability_assessor()
    
    print("\n" + "=" * 50)
    print("所有测试完成")


if __name__ == "__main__":
    main()