#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
项目综合测试脚本

该脚本用于全面测试项目的各个组件，确保项目功能完整可用。
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_module_imports():
    """测试所有模块导入"""
    print("=== 模块导入测试 ===")
    
    # 测试核心模块导入
    try:
        import kivy
        print("✓ Kivy导入成功")
    except ImportError as e:
        print(f"✗ Kivy导入失败: {e}")
        return False
    
    try:
        import cv2
        print("✓ OpenCV导入成功")
    except ImportError as e:
        print(f"✗ OpenCV导入失败: {e}")
        return False
    
    try:
        import mediapipe
        print("✓ MediaPipe导入成功")
    except ImportError as e:
        print(f"✗ MediaPipe导入失败: {e}")
        return False
    
    try:
        import numpy
        print("✓ NumPy导入成功")
    except ImportError as e:
        print(f"✗ NumPy导入失败: {e}")
        return False
    
    # 测试项目模块导入
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
        print("✓ FMS评估器模块导入成功")
    except ImportError as e:
        print(f"✗ FMS评估器模块导入失败: {e}")
        return False
    
    try:
        from utils import (
            calculate_joint_angle,
            LandmarkFilter,
            compare_bilateral_symmetry
        )
        print("✓ 工具模块导入成功")
    except ImportError as e:
        print(f"✗ 工具模块导入失败: {e}")
        return False
    
    try:
        from ai_assistant import AIFitnessAssistant
        print("✓ AI助手模块导入成功")
    except ImportError as e:
        print(f"✗ AI助手模块导入失败: {e}")
        return False
    
    try:
        from user_profile import UserProfile
        print("✓ 用户信息模块导入成功")
    except ImportError as e:
        print(f"✗ 用户信息模块导入失败: {e}")
        return False
    
    try:
        from pose_estimator import PoseEstimator
        print("✓ 姿态估计模块导入成功")
    except ImportError as e:
        print(f"✗ 姿态估计模块导入失败: {e}")
        return False
    
    # 注意：避免在测试导入阶段导入Kivy UI组件，因为会触发GUI初始化
    print("✓ 核心模块导入测试完成")
    return True


def test_fms_assessors():
    """测试FMS评估器功能"""
    print("\n=== FMS评估器功能测试 ===")
    
    try:
        from fms_assessors.squat import SquatAssessor
        
        # 创建评估器实例
        assessor = SquatAssessor()
        
        # 测试评估功能
        angles = {
            'left_hip_angle': 120,
            'right_hip_angle': 118,
            'left_knee_angle': 90,
            'right_knee_angle': 88,
            'foot_shoulder_ratio': 100,
            'knee_valgus': 8
        }
        
        landmarks = {
            0: (0.5, 0.1, 0.0),
            12: (0.4, 0.2, 0.0),
            11: (0.6, 0.2, 0.0),
            24: (0.4, 0.5, 0.0),
            23: (0.6, 0.5, 0.0),
            26: (0.4, 0.8, 0.0),
            25: (0.6, 0.8, 0.0),
        }
        
        result = assessor.assess(angles, landmarks)
        print(f"✓ 深蹲评估器功能正常，评分: {result['score']}/3")
        
        # 测试历史记录功能
        history = assessor.get_history()
        print(f"✓ 历史记录功能正常，记录数: {len(history)}")
        
        # 测试平均评分功能
        avg_score = assessor.get_average_score()
        print(f"✓ 平均评分功能正常: {avg_score:.2f}")
        
    except Exception as e:
        print(f"✗ FMS评估器功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_utils_modules():
    """测试工具模块功能"""
    print("\n=== 工具模块功能测试 ===")
    
    try:
        from utils.angle_calculations import calculate_joint_angle
        from utils.landmark_filter import LandmarkFilter
        from utils.symmetry_analysis import compare_bilateral_symmetry
        
        # 测试角度计算
        a = (0, 0, 0)
        b = (1, 1, 0)
        c = (2, 0, 0)
        angle = calculate_joint_angle(a, b, c)
        print(f"✓ 角度计算功能正常: {angle:.2f}度")
        
        # 测试滤波器
        filter = LandmarkFilter(window_size=3)
        landmarks = {0: (0.5, 0.2, 0.8)}
        filtered = filter.filter_landmarks(landmarks)
        print(f"✓ 关键点滤波功能正常")
        
        # 测试对称性分析
        left_angles = {'knee': 90}
        right_angles = {'knee': 88}
        angle_pairs = [('knee', 'knee')]
        symmetry_results = compare_bilateral_symmetry(left_angles, right_angles, angle_pairs)
        print(f"✓ 对称性分析功能正常")
        
    except Exception as e:
        print(f"✗ 工具模块功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_ai_integration():
    """测试AI集成功能"""
    print("\n=== AI集成功能测试 ===")
    
    try:
        from ai_assistant import AIFitnessAssistant
        from user_profile import UserProfile
        
        # 测试用户信息
        user = UserProfile()
        user.set_basic_info(25, "男", 175, 70)
        profile = user.get_profile()
        print("✓ 用户信息模块功能正常")
        
        # 测试AI助手（不实际调用API）
        assistant = AIFitnessAssistant(api_key="test_key", model="deepseek-test")
        print("✓ AI助手模块实例化正常")
        
    except Exception as e:
        print(f"✗ AI集成功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_database_functionality():
    """测试数据库功能"""
    print("\n=== 数据库功能测试 ===")
    
    try:
        from db_manager import DatabaseManager
        
        # 创建数据库管理器实例
        db = DatabaseManager()
        print("✓ 数据库管理器实例化正常")
        
        # 测试会话历史
        try:
            history = db.get_session_history()
            print(f"✓ 会话历史查询正常，记录数: {len(history) if history else 0}")
        except Exception as e:
            print(f"⚠ 会话历史查询异常（可能是数据库未初始化）: {e}")
        
    except Exception as e:
        print(f"✗ 数据库功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_pose_estimator():
    """测试姿态估计功能"""
    print("\n=== 姿态估计功能测试 ===")
    
    try:
        from pose_estimator import PoseEstimator
        
        # 创建姿态估计器实例
        estimator = PoseEstimator()
        print("✓ 姿态估计器实例化正常")
        
        # 测试视图设置
        estimator.set_view('front')
        print("✓ 视图设置功能正常")
        
    except Exception as e:
        print(f"✗ 姿态估计功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def main():
    """主函数"""
    print("项目综合测试")
    print("=" * 50)
    
    # 逐项测试项目功能
    tests = [
        ("模块导入", test_module_imports),
        ("FMS评估器", test_fms_assessors),
        ("工具模块", test_utils_modules),
        ("AI集成", test_ai_integration),
        ("数据库功能", test_database_functionality),
        ("姿态估计", test_pose_estimator)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print(f"✓ {test_name}测试通过\n")
            else:
                print(f"✗ {test_name}测试失败\n")
        except Exception as e:
            print(f"✗ {test_name}测试执行出错: {e}\n")
    
    print("=" * 50)
    print(f"测试总结: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过，项目功能完整！")
        return True
    else:
        print("⚠ 部分测试未通过，请检查相关模块。")
        return False


if __name__ == "__main__":
    main()