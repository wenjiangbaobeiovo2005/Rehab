#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
综合性测试脚本
用于快速测试项目的所有核心功能
"""

import sys
import os
import traceback

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有模块导入"""
    print("=== 测试模块导入 ===")
    
    modules_to_test = [
        # 核心模块
        'main_kivy',
        'pose_estimator',
        'ai_assistant',
        'db_manager',
        'user_profile',
        'training_plan_screen',
        'user_profile_screen',
        
        # FMS评估器模块
        'fms_assessors.base_assessor',
        'fms_assessors.squat',
        'fms_assessors.hurdle_step',
        'fms_assessors.inline_lunge',
        'fms_assessors.shoulder_mobility',
        'fms_assessors.active_leg_raise',
        'fms_assessors.trunk_pushup',
        'fms_assessors.rotary_stability',
        
        # 工具模块
        'utils.angle_calculations',
        'utils.landmark_filter',
        'utils.movement_analysis',
        'utils.symmetry_analysis',
    ]
    
    failed_imports = []
    successful_imports = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            successful_imports.append(module)
            print(f"✓ {module}")
        except Exception as e:
            failed_imports.append((module, str(e)))
            print(f"✗ {module}: {e}")
    
    return len(failed_imports) == 0, failed_imports

def test_fms_assessors():
    """测试FMS评估器"""
    print("\n=== 测试FMS评估器 ===")
    
    try:
        from fms_assessors.squat import SquatAssessor
        from fms_assessors.hurdle_step import HurdleStepAssessor
        from fms_assessors.inline_lunge import InlineLungeAssessor
        from fms_assessors.shoulder_mobility import ShoulderMobilityAssessor
        from fms_assessors.active_leg_raise import ActiveLegRaiseAssessor
        from fms_assessors.trunk_pushup import TrunkPushupAssessor
        from fms_assessors.rotary_stability import RotaryStabilityAssessor
        
        # 创建评估器实例
        assessors = [
            ("SquatAssessor", SquatAssessor()),
            ("HurdleStepAssessor", HurdleStepAssessor()),
            ("InlineLungeAssessor", InlineLungeAssessor()),
            ("ShoulderMobilityAssessor", ShoulderMobilityAssessor()),
            ("ActiveLegRaiseAssessor", ActiveLegRaiseAssessor()),
            ("TrunkPushupAssessor", TrunkPushupAssessor()),
            ("RotaryStabilityAssessor", RotaryStabilityAssessor()),
        ]
        
        # 测试每个评估器的基本功能
        for name, assessor in assessors:
            try:
                # 测试reset方法
                assessor.reset()
                print(f"✓ {name} 实例化和reset()成功")
            except Exception as e:
                print(f"✗ {name} 测试失败: {e}")
                return False, f"{name} 测试失败: {e}"
        
        print("✓ 所有FMS评估器测试通过")
        return True, ""
        
    except Exception as e:
        error_msg = f"FMS评估器测试失败: {str(e)}"
        print(f"✗ {error_msg}")
        return False, error_msg

def test_utils():
    """测试工具模块"""
    print("\n=== 测试工具模块 ===")
    
    try:
        from utils.angle_calculations import calculate_joint_angle
        from utils.landmark_filter import LandmarkFilter
        # 注意：movement_analysis和symmetry_analysis主要是函数模块，没有特定的类
        
        # 测试角度计算
        try:
            # 使用一些示例坐标测试角度计算
            angle = calculate_joint_angle((0, 0, 0), (1, 0, 0), (1, 1, 0))
            print(f"✓ 关节角度计算功能正常: {angle:.2f}度")
        except Exception as e:
            print(f"✗ 关节角度计算失败: {e}")
            return False, f"关节角度计算失败: {e}"
        
        # 测试LandmarkFilter类
        try:
            filter_instance = LandmarkFilter()
            filter_instance.reset()
            print("✓ LandmarkFilter 实例化和reset()成功")
        except Exception as e:
            print(f"✗ LandmarkFilter 测试失败: {e}")
            return False, f"LandmarkFilter 测试失败: {e}"
            
        # 测试movement_analysis模块中的函数
        try:
            from utils.movement_analysis import calculate_velocity
            # 简单测试函数是否可调用
            print("✓ MovementAnalysis 函数可导入")
        except Exception as e:
            print(f"✗ MovementAnalysis 函数导入失败: {e}")
            return False, f"MovementAnalysis 函数导入失败: {e}"
            
        # 测试symmetry_analysis模块中的函数
        try:
            from utils.symmetry_analysis import compare_bilateral_symmetry
            # 简单测试函数是否可调用
            print("✓ SymmetryAnalysis 函数可导入")
        except Exception as e:
            print(f"✗ SymmetryAnalysis 函数导入失败: {e}")
            return False, f"SymmetryAnalysis 函数导入失败: {e}"
        
        print("✓ 所有工具模块测试通过")
        return True, ""
        
    except Exception as e:
        error_msg = f"工具模块测试失败: {str(e)}"
        print(f"✗ {error_msg}")
        return False, error_msg

def test_requirements():
    """测试依赖包安装"""
    print("\n=== 测试依赖包 ===")
    
    required_packages = [
        'kivy',
        'cv2',  # opencv-python
        'mediapipe',
        'numpy',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
                print(f"✓ opencv-python (cv2) 安装正常")
            else:
                __import__(package)
                print(f"✓ {package} 安装正常")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} 未安装或导入失败")
        except Exception as e:
            print(f"✗ {package} 导入时出错: {e}")
            missing_packages.append(package)
    
    if missing_packages:
        return False, f"缺少依赖包: {', '.join(missing_packages)}"
    else:
        print("✓ 所有依赖包测试通过")
        return True, ""

def test_kivy_app():
    """测试Kivy应用创建"""
    print("\n=== 测试Kivy应用创建 ===")
    
    try:
        # 尝试导入Kivy组件
        from kivy.app import App
        from kivy.uix.widget import Widget
        print("✓ Kivy基础组件导入成功")
        
        # 尝试导入项目中的Kivy相关模块
        import main_kivy
        print("✓ main_kivy 模块导入成功")
        
        print("✓ Kivy应用测试通过")
        return True, ""
        
    except Exception as e:
        error_msg = f"Kivy应用测试失败: {str(e)}"
        print(f"✗ {error_msg}")
        return False, error_msg

def run_all_tests():
    """运行所有测试"""
    print("开始综合性测试...\n")
    
    all_passed = True
    errors = []
    
    # 1. 测试模块导入
    imports_passed, import_errors = test_imports()
    if not imports_passed:
        all_passed = False
        errors.extend(import_errors)
    
    # 2. 测试FMS评估器
    fms_passed, fms_error = test_fms_assessors()
    if not fms_passed:
        all_passed = False
        errors.append(fms_error)
    
    # 3. 测试工具模块
    utils_passed, utils_error = test_utils()
    if not utils_passed:
        all_passed = False
        errors.append(utils_error)
    
    # 4. 测试依赖包
    req_passed, req_error = test_requirements()
    if not req_passed:
        all_passed = False
        errors.append(req_error)
    
    # 5. 测试Kivy应用
    kivy_passed, kivy_error = test_kivy_app()
    if not kivy_passed:
        all_passed = False
        errors.append(kivy_error)
    
    # 输出总结
    print("\n" + "="*50)
    print("测试总结:")
    if all_passed:
        print("✓ 所有测试通过！项目可以正常运行。")
        return True
    else:
        print("✗ 部分测试失败:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print("\n请根据上述错误信息修复问题。")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"测试过程中发生未预期的错误: {e}")
        traceback.print_exc()
        sys.exit(1)