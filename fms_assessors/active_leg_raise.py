"""
主动直腿上抬动作评估器

该模块实现了FMS主动直腿上抬动作的评估逻辑，包括评分算法和反馈建议。
"""

import numpy as np
from typing import Dict, Any, Tuple
from .base_assessor import BaseAssessor


class ActiveLegRaiseAssessor(BaseAssessor):
    """
    主动直腿上抬动作评估器
    
    评估标准：
    - 3分：动作完成度高，无代偿
    - 2分：动作基本完成，有轻微代偿
    - 1分：动作完成困难，有明显代偿
    """
    
    # 定义评分阈值
    THRESHOLDS = {
        'thigh_angle_3': 70,   # 3分标准：大腿与地面夹角≥70度
        'thigh_angle_2': 60,   # 2分标准：大腿与地面夹角≥60度
        'thigh_angle_1': 50,   # 1分标准：大腿与地面夹角≥50度
    }
    
    def __init__(self):
        """初始化评估器"""
        super().__init__()
        
    def reset(self):
        """重置评估器状态"""
        super().reset()
        
    def assess(self, angles: Dict[str, float], landmarks: Dict[int, Tuple[float, float, float]]) -> Dict[str, Any]:
        """
        评估主动直腿上抬动作
        
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
        
        # 评估大腿抬升角度
        thigh_angle = angles.get('thigh_angle', 0)
        if thigh_angle < self.THRESHOLDS['thigh_angle_3']:
            score = 2 if thigh_angle >= self.THRESHOLDS['thigh_angle_2'] else 1
            if thigh_angle < self.THRESHOLDS['thigh_angle_2']:
                score = 1
            compensations.append(f"大腿抬升角度不足: {thigh_angle:.1f}°")
            
        # 评估支撑腿稳定性
        if angles.get('support_leg_stability', 100) < 90:
            score = min(score, 2)
            compensations.append("支撑腿稳定性不足")
            
        # 评估骨盆倾斜
        if abs(angles.get('pelvis_tilt', 0)) > 10:
            score = min(score, 2)
            compensations.append("骨盆倾斜过度")
            
        # 评估膝关节伸直
        if angles.get('knee_flexion', 0) > 10:  # 膝关节应该基本伸直
            score = min(score, 2)
            compensations.append("抬腿侧膝关节未充分伸直")
            
        if score == 3:
            reasons.append(f"主动直腿上抬动作完成良好，大腿抬升角度达到{thigh_angle:.1f}°")
        elif score == 2:
            reasons.append(f"主动直腿上抬动作基本完成，大腿抬升角度为{thigh_angle:.1f}°，存在轻微代偿")
        else:
            reasons.append(f"主动直腿上抬动作完成困难，大腿抬升角度仅为{thigh_angle:.1f}°，存在明显代偿")
            
        result = {
            'score': score,
            'reasons': reasons,
            'compensations': compensations,
            'similarity': similarity
        }
        
        # 保存评估结果到历史记录
        self.assessment_history.append(result)
        
        return result