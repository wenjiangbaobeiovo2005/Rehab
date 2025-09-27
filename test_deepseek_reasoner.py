#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试DeepSeek Reasoner模型集成
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_assistant import AIFitnessAssistant
from user_profile import UserProfile


def test_deepseek_integration():
    """测试DeepSeek集成"""
    print("DeepSeek Reasoner模型集成测试")
    print("=" * 50)
    
    # 创建用户信息
    user = UserProfile()
    user.set_basic_info(28, "男", 175, 70)
    user.set_sport_experience("3年健身经验，主要进行力量训练")
    user.set_goals("改善动作质量，提高深蹲深度")
    user.set_injury_history("无重大伤病史，偶尔腰部紧张")
    user.set_training_frequency(4)
    
    # 模拟FMS评估结果
    assessment_results = [
        {
            "movement_name": "深蹲",
            "score": 2,
            "feedback": ["膝外翻", "躯干前倾"],
            "angles": {"left_knee_angle": 75, "right_knee_angle": 65, "trunk_angle": 45}
        },
        {
            "movement_name": "跨栏步",
            "score": 3,
            "feedback": ["轻微髋关节不对称"],
            "angles": {"hip_angle_left": 30, "hip_angle_right": 28}
        },
        {
            "movement_name": "直线弓步蹲",
            "score": 2,
            "feedback": ["后腿稳定性不足"],
            "angles": {"front_knee_angle": 80, "back_knee_angle": 20}
        },
        {
            "movement_name": "肩部灵活性",
            "score": 2,
            "feedback": ["肩部柔韧性受限"],
            "angles": {"shoulder_flexion": 120}
        },
        {
            "movement_name": "主动直腿上抬",
            "score": 3,
            "feedback": ["轻微腘绳肌紧张"],
            "angles": {"leg_raise_angle": 70}
        },
        {
            "movement_name": "躯干稳定俯卧撑",
            "score": 1,
            "feedback": ["核心稳定性差", "腰部下沉"],
            "angles": {"trunk_deviation": 15}
        },
        {
            "movement_name": "旋转稳定性",
            "score": 2,
            "feedback": ["动作不对称"],
            "angles": {"rotation_stability": 3}
        }
    ]
    
    # 获取API密钥
    api_key = "sk-523e2ec2192b4f3e844fa3f3e8d25afb"  # 用户提供的API密钥
    
    try:
        # 创建AI助手实例
        assistant = AIFitnessAssistant(api_key=api_key, model="deepseek-reasoner")
        
        print("正在生成个性化训练方案...")
        print("-" * 30)
        
        # 生成个性化训练方案
        plan = assistant.generate_personalized_plan(
            user.get_profile(),
            assessment_results
        )
        
        print(plan)
        print("\n" + "=" * 50)
        print("测试完成")
        
        # 保存方案到文件
        with open("personalized_training_plan.txt", "w", encoding="utf-8") as f:
            f.write(plan)
        print("训练方案已保存到 personalized_training_plan.txt")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")


if __name__ == "__main__":
    test_deepseek_integration()