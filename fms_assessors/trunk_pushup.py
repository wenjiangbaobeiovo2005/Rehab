"""
躯干稳定俯卧撑动作评估器

该模块实现了FMS躯干稳定俯卧撑动作的评估逻辑，包括评分算法和反馈建议。
"""

import numpy as np
from typing import Dict, Any, Tuple
from .base_assessor import BaseAssessor


class TrunkPushupAssessor(BaseAssessor):
    """
    躯干稳定俯卧撑动作评估器
    
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
        评估躯干稳定俯卧撑动作
        
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
        
        # 评估躯干稳定性
        if angles.get('trunk_stability', 100) < 90:
            score = min(score, 2)
            compensations.append("躯干稳定性不足")
            
        # 评估肘关节屈曲角度
        if angles.get('elbow_flexion', 0) < 80:
            score = min(score, 2)
            compensations.append("肘关节屈曲不足")
            
        # 评估肩部稳定性
        if angles.get('shoulder_stability', 100) < 90:
            score = min(score, 2)
            compensations.append("肩部稳定性不足")
            
        # 评估核心控制
        if angles.get('core_control', 100) < 90:
            score = min(score, 2)
            compensations.append("核心控制能力不足")
            
        # 评估身体直线度
        if angles.get('body_alignment', 100) < 90:
            score = min(score, 1)
            compensations.append("身体未保持直线")
            
        if score == 3:
            reasons.append("躯干稳定俯卧撑动作完成良好，躯干控制稳定")
        elif score == 2:
            reasons.append("躯干稳定俯卧撑动作基本完成，但存在轻微代偿")
        else:
            reasons.append("躯干稳定俯卧撑动作完成困难，存在明显代偿")
            
        result = {
            'score': score,
            'reasons': reasons,
            'compensations': compensations,
            'similarity': similarity
        }
        
        # 保存评估结果到历史记录
        self.assessment_history.append(result)
        
        return result