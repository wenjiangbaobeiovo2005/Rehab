#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试FMS评估器模块
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fms_assessors import (
    SquatAssessor,
    HurdleStepAssessor,
    InlineLungeAssessor,
    ShoulderMobilityAssessor,
    ActiveLegRaiseAssessor,
    TrunkPushupAssessor,
    RotaryStabilityAssessor,
    BaseAssessor
)

def test_imports():
    """测试所有评估器是否可以正确导入"""
    print("FMS评估器模块导入测试")
    print("=" * 50)
    
    # 测试基类（不能直接实例化，只能测试导入）
    print("1. 测试基类导入...")
    try:
        # 不实例化抽象基类，只测试是否可以导入
        print("   ✓ BaseAssessor 导入成功")
    except Exception as e:
        print(f"   ✗ BaseAssessor 导入失败: {e}")
    
    # 测试具体评估器
    assessors = [
        ("SquatAssessor", SquatAssessor),
        ("HurdleStepAssessor", HurdleStepAssessor),
        ("InlineLungeAssessor", InlineLungeAssessor),
        ("ShoulderMobilityAssessor", ShoulderMobilityAssessor),
        ("ActiveLegRaiseAssessor", ActiveLegRaiseAssessor),
        ("TrunkPushupAssessor", TrunkPushupAssessor),
        ("RotaryStabilityAssessor", RotaryStabilityAssessor)
    ]
    
    for name, AssessorClass in assessors:
        print(f"2. 测试 {name}...")
        try:
            assessor = AssessorClass()
            print(f"   ✓ {name} 导入并实例化成功")
            
            # 测试方法是否存在
            if hasattr(assessor, 'reset') and callable(getattr(assessor, 'reset')):
                print(f"   ✓ {name}.reset() 方法存在")
            else:
                print(f"   ✗ {name}.reset() 方法缺失")
                
            if hasattr(assessor, 'assess') and callable(getattr(assessor, 'assess')):
                print(f"   ✓ {name}.assess() 方法存在")
            else:
                print(f"   ✗ {name}.assess() 方法缺失")
                
        except Exception as e:
            print(f"   ✗ {name} 导入或实例化失败: {e}")

def test_squat_assessor():
    """测试深蹲评估器"""
    print("\n深蹲评估器功能测试")
    print("=" * 50)
    
    try:
        assessor = SquatAssessor()
        print("✓ 深蹲评估器实例化成功")
        
        # 测试重置功能
        assessor.reset()
        print("✓ 重置功能正常")
        
        # 测试评估功能（使用模拟数据）
        angles = {
            'left_knee_angle': 80,
            'right_knee_angle': 82,
            'left_hip_angle': 90,
            'right_hip_angle': 88
        }
        
        landmarks = {
            0: (0.5, 0.2, 0.8),   # 鼻子
            12: (0.4, 0.4, 0.9),  # 左肩
            11: (0.6, 0.4, 0.9),  # 右肩
            24: (0.4, 0.6, 0.8),  # 左臀
            23: (0.6, 0.6, 0.8),  # 右臀
            26: (0.4, 0.8, 0.7),  # 左膝
            25: (0.6, 0.8, 0.7),  # 右膝
            32: (0.4, 1.0, 0.6),  # 左脚跟
            31: (0.6, 1.0, 0.6),  # 右脚跟
        }
        
        result = assessor.assess(angles, landmarks)
        print("✓ 评估功能正常")
        print(f"  评估结果: {result}")
        
    except Exception as e:
        print(f"✗ 深蹲评估器测试失败: {e}")

if __name__ == "__main__":
    test_imports()
    test_squat_assessor()
    print("\n测试完成")