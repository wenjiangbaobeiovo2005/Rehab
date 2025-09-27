"""
FMS评估器基类模块

该模块定义了所有FMS动作评估器的统一接口。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List


class BaseAssessor(ABC):
    """
    FMS评估器抽象基类
    
    所有具体的FMS动作评估器都应该继承此类并实现相应的方法。
    """
    
    def __init__(self):
        """初始化评估器"""
        self.assessment_history = []
        
    @abstractmethod
    def reset(self):
        """
        重置评估器状态
        
        清除历史记录和其他状态信息。
        """
        self.assessment_history = []
        
    @abstractmethod
    def assess(self, angles: Dict[str, float], landmarks: Dict[int, Tuple[float, float, float]]) -> Dict[str, Any]:
        """
        评估动作质量
        
        Args:
            angles: 关节角度字典
            landmarks: 关键点坐标字典
            
        Returns:
            包含评分结果和反馈的字典，格式如下：
            {
                'score': int,           # 评分 (1-3分)
                'reasons': List[str],   # 评分原因
                'compensations': List[str],  # 代偿模式
                'similarity': float,    # 与标准动作的相似度 (0-100)
                'parameters': Dict[str, Any]  # 详细参数信息（可选）
            }
        """
        pass
        
    def get_history(self) -> List[Dict[str, Any]]:
        """
        获取评估历史记录
        
        Returns:
            评估历史记录列表
        """
        return self.assessment_history.copy()
        
    def get_average_score(self) -> float:
        """
        获取平均评分
        
        Returns:
            历史评估的平均评分
        """
        if not self.assessment_history:
            return 0.0
            
        total_score = sum(record['score'] for record in self.assessment_history)
        return total_score / len(self.assessment_history)