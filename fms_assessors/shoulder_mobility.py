"""
肩部灵活性动作评估器

该模块实现了FMS肩部灵活性动作的评估逻辑，包括评分算法和反馈建议。
"""

import numpy as np
from typing import Dict, Any, Tuple
from .base_assessor import BaseAssessor


class ShoulderMobilityAssessor(BaseAssessor):
    """
    肩部灵活性动作评估器
    
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
        评估肩部灵活性动作
        
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
        
        # 评估肩部抬升角度
        if angles.get('shoulder_elevation', 0) < 160:
            score = min(score, 2)
            compensations.append("肩部抬升不足")
            
        # 评估肩部外展角度
        if angles.get('shoulder_abduction', 0) < 160:
            score = min(score, 2)
            compensations.append("肩部外展不足")
            
        # 评估肩部内旋角度
        if angles.get('shoulder_internal_rotation', 0) < 60:
            score = min(score, 2)
            compensations.append("肩部内旋不足")
            
        # 评估肩部后伸角度
        if angles.get('shoulder_extension', 0) < 50:
            score = min(score, 2)
            compensations.append("肩部后伸不足")
            
        if score == 3:
            reasons.append("肩部灵活性动作完成良好，各关节角度符合标准")
        elif score == 2:
            reasons.append("肩部灵活性动作基本完成，但存在轻微代偿")
        else:
            reasons.append("肩部灵活性动作完成困难，存在明显代偿")
            
        result = {
            'score': score,
            'reasons': reasons,
            'compensations': compensations,
            'similarity': similarity
        }
        
        # 保存评估结果到历史记录
        self.assessment_history.append(result)
        
        return result