"""
FMS动作评估器模块

该模块包含功能性动作筛查（FMS）系统的各个动作评估器，
每个评估器负责评估特定的动作模式并提供评分和反馈。

功能描述:
- 每个评估器实现统一的接口，包括初始化、重置、评估等核心方法
- 提供标准的FMS评分算法和个性化反馈建议
- 支持不同视角（正面、侧面、45度角）的动作评估

模块列表:
- squat: 深蹲动作评估器
- hurdle_step: 跨栏步动作评估器
- inline_lunge: 直线弓步蹲动作评估器
- shoulder_mobility: 肩部灵活性动作评估器
- active_leg_raise: 主动直腿上抬动作评估器
- trunk_pushup: 躯干稳定俯卧撑动作评估器
- rotary_stability: 旋转稳定性动作评估器

使用示例:
    from fms_assessors import SquatAssessor
    assessor = SquatAssessor()
    result = assessor.assess(angles, landmarks)
    
注意:
当前项目中，这些评估器并未直接在主程序中使用，评估逻辑已整合到pose_estimator.py文件中。
这些评估器类保留用于未来可能的模块化重构。
"""

from .squat import SquatAssessor
from .hurdle_step import HurdleStepAssessor
from .inline_lunge import InlineLungeAssessor
from .shoulder_mobility import ShoulderMobilityAssessor
from .active_leg_raise import ActiveLegRaiseAssessor
from .trunk_pushup import TrunkPushupAssessor
from .rotary_stability import RotaryStabilityAssessor
from .base_assessor import BaseAssessor