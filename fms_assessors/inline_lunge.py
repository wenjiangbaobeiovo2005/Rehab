"""
直线弓步蹲动作评估器

该模块实现了FMS直线弓步蹲动作的评估逻辑，包括评分算法和反馈建议。
"""

import numpy as np
from typing import Dict, Any, Tuple
from .base_assessor import BaseAssessor


class InlineLungeAssessor(BaseAssessor):
    """
    直线弓步蹲动作评估器
    
    评估标准：
    - 3分：动作完成度高，无代偿
    - 2分：动作基本完成，有轻微代偿
    - 1分：动作完成困难，有明显代偿
    """
    
    def __init__(self):
        """初始化评估器"""
        super().__init__()
        
    def reset(self):
        """重置评估器状态"""
        super().reset()
        
    def assess(self, angles: Dict[str, float], landmarks: Dict[int, Tuple[float, float, float]]) -> Dict[str, Any]:
        """
        评估直线弓步蹲动作
        
        Args:
            angles: 关节角度字典
            landmarks: 关键点坐标字典
            
        Returns:
            包含评分结果和反馈的字典
        """
        score = 3  # 默认评分
        reasons = []
        compensations = []
        similarity = 100.0
        
        # 评估前腿髋关节角度
        if angles.get('front_leg_hip_angle', 0) < 90:
            score = min(score, 2)
            compensations.append("前腿髋关节屈曲不足")
            
        # 评估前腿膝关节角度
        if angles.get('front_leg_knee_angle', 0) < 90:
            score = min(score, 2)
            compensations.append("前腿膝关节屈曲不足")
            
        # 评估后腿膝关节角度
        if angles.get('back_leg_knee_angle', 0) > 10:  # 应该接近0度
            score = min(score, 2)
            compensations.append("后腿膝关节未充分屈曲")
            
        # 评估躯干倾斜角度
        if angles.get('trunk_inclination', 0) > 15:
            score = min(score, 2)
            compensations.append("躯干倾斜过度")
            
        # 评估双足间距
        if angles.get('feet_separation', 0) < 10:  # 应该有足够间距
            score = min(score, 2)
            compensations.append("双足间距不足")
            
        if score == 3:
            reasons.append("直线弓步蹲动作完成良好，各关节角度符合标准")
        elif score == 2:
            reasons.append("直线弓步蹲动作基本完成，但存在轻微代偿")
        else:
            reasons.append("直线弓步蹲动作完成困难，存在明显代偿")
            
        result = {
            'score': score,
            'reasons': reasons,
            'compensations': compensations,
            'similarity': similarity
        }
        
        # 保存评估结果到历史记录
        self.assessment_history.append(result)
        
        return result