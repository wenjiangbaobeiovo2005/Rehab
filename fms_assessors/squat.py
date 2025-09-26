"""
深蹲动作评估器

该模块实现了FMS深蹲动作的评估逻辑，包括评分算法和反馈建议。
"""

import numpy as np
from typing import Dict, Any, Tuple
from .base_assessor import BaseAssessor


class SquatAssessor(BaseAssessor):
    """
    深蹲动作评估器
    
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
        评估深蹲动作
        
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
        
        # 根据不同视角进行评估
        if 'left_hip_angle' in angles and 'right_hip_angle' in angles:
            # 正面视角评估
            score, reasons, compensations = self._assess_front_view(angles)
        elif 'trunk_angle' in angles:
            # 侧面视角评估
            score, reasons, compensations = self._assess_side_view(angles)
        elif 'trunk_rotation' in angles:
            # 45度角视角评估
            score, reasons, compensations = self._assess_45_view(angles)
            
        result = {
            'score': score,
            'reasons': reasons,
            'compensations': compensations,
            'similarity': similarity
        }
        
        # 保存评估结果到历史记录
        self.assessment_history.append(result)
        
        return result
        
    def _assess_front_view(self, angles: Dict[str, float]) -> Tuple[int, list, list]:
        """正面视角评估"""
        score = 3
        reasons = []
        compensations = []
        
        # 评估髋关节角度
        if angles.get('left_hip_angle', 0) < 120 or angles.get('right_hip_angle', 0) < 120:
            score = min(score, 2)
            compensations.append("髋关节屈曲不足")
            
        # 评估膝关节角度
        if angles.get('left_knee_angle', 0) < 90 or angles.get('right_knee_angle', 0) < 90:
            score = min(score, 2)
            compensations.append("膝关节屈曲不足")
            
        # 评估双脚与肩宽比例
        if angles.get('foot_shoulder_ratio', 100) < 80 or angles.get('foot_shoulder_ratio', 100) > 120:
            score = min(score, 2)
            compensations.append("双脚间距与肩宽不匹配")
            
        # 评估膝外翻
        if angles.get('knee_valgus', 0) > 15:
            score = min(score, 1)
            compensations.append("膝外翻明显")
            
        if score == 3:
            reasons.append("深蹲动作完成良好，各关节角度符合标准")
        elif score == 2:
            reasons.append("深蹲动作基本完成，但存在轻微代偿")
        else:
            reasons.append("深蹲动作完成困难，存在明显代偿")
            
        return score, reasons, compensations
        
    def _assess_side_view(self, angles: Dict[str, float]) -> Tuple[int, list, list]:
        """侧面视角评估"""
        score = 3
        reasons = []
        compensations = []
        
        # 评估躯干倾斜角度
        if angles.get('trunk_angle', 0) > 30:
            score = min(score, 2)
            compensations.append("躯干前倾过度")
            
        # 评估髋关节角度
        if angles.get('hip_angle', 0) < 120:
            score = min(score, 2)
            compensations.append("髋关节屈曲不足")
            
        # 评估膝关节角度
        if angles.get('knee_angle', 0) < 90:
            score = min(score, 2)
            compensations.append("膝关节屈曲不足")
            
        # 评估踝关节角度
        if angles.get('ankle_angle', 0) < 70:
            score = min(score, 2)
            compensations.append("踝关节背屈不足")
            
        # 评估脚跟离地
        if angles.get('heel_lift', 0) > 5:
            score = min(score, 1)
            compensations.append("脚跟离地明显")
            
        if score == 3:
            reasons.append("深蹲动作完成良好，各关节角度符合标准")
        elif score == 2:
            reasons.append("深蹲动作基本完成，但存在轻微代偿")
        else:
            reasons.append("深蹲动作完成困难，存在明显代偿")
            
        return score, reasons, compensations
        
    def _assess_45_view(self, angles: Dict[str, float]) -> Tuple[int, list, list]:
        """45度角视角评估"""
        score = 3
        reasons = []
        compensations = []
        
        # 评估侧面髋关节角度
        if angles.get('side_hip_angle', 0) < 110:
            score = min(score, 2)
            compensations.append("髋关节屈曲不足")
            
        # 评估侧面膝关节角度
        if angles.get('side_knee_angle', 0) < 90:
            score = min(score, 2)
            compensations.append("膝关节屈曲不足")
            
        # 评估躯干旋转
        if angles.get('trunk_rotation', 0) > 15:
            score = min(score, 1)
            compensations.append("躯干旋转过度")
            
        if score == 3:
            reasons.append("深蹲动作完成良好，各关节角度符合标准")
        elif score == 2:
            reasons.append("深蹲动作基本完成，但存在轻微代偿")
        else:
            reasons.append("深蹲动作完成困难，存在明显代偿")
            
        return score, reasons, compensations