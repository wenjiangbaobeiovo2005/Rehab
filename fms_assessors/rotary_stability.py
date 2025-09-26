"""
旋转稳定性动作评估器

该模块实现了FMS旋转稳定性动作的评估逻辑，包括评分算法和反馈建议。
"""

import numpy as np
from typing import Dict, Any, Tuple
from .base_assessor import BaseAssessor


class RotaryStabilityAssessor(BaseAssessor):
    """
    旋转稳定性动作评估器
    
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
        评估旋转稳定性动作
        
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
        
        # 评估躯干旋转控制
        if angles.get('trunk_rotation_control', 100) < 90:
            score = min(score, 2)
            compensations.append("躯干旋转控制能力不足")
            
        # 评估四肢协调性
        if angles.get('limb_coordination', 100) < 90:
            score = min(score, 2)
            compensations.append("四肢协调性不足")
            
        # 评估核心稳定性
        if angles.get('core_stability', 100) < 90:
            score = min(score, 2)
            compensations.append("核心稳定性不足")
            
        # 评估动作流畅性
        if angles.get('movement_fluidity', 100) < 90:
            score = min(score, 2)
            compensations.append("动作流畅性不足")
            
        # 评估对侧肢体配合
        if angles.get('contralateral_coordination', 100) < 90:
            score = min(score, 1)
            compensations.append("对侧肢体配合不佳")
            
        if score == 3:
            reasons.append("旋转稳定性动作完成良好，躯干控制稳定")
        elif score == 2:
            reasons.append("旋转稳定性动作基本完成，但存在轻微代偿")
        else:
            reasons.append("旋转稳定性动作完成困难，存在明显代偿")
            
        result = {
            'score': score,
            'reasons': reasons,
            'compensations': compensations,
            'similarity': similarity
        }
        
        # 保存评估结果到历史记录
        self.assessment_history.append(result)
        
        return result