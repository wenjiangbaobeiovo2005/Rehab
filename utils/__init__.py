"""
工具模块

该模块包含功能性动作筛查（FMS）系统使用的各种工具函数，
用于角度计算、关键点处理、动作分析等。

功能描述:
- 提供标准的角度计算方法
- 实现关键点数据的滤波和平滑处理
- 提供动作轨迹分析功能
- 实现左右对称性分析

模块列表:
- angle_calculations: 关节角度计算工具
- landmark_filter: 关键点滤波平滑处理
- movement_analysis: 动作轨迹分析
- symmetry_analysis: 左右对称性分析

使用示例:
    from utils.angle_calculations import calculate_joint_angle
    angle = calculate_joint_angle(landmark_a, landmark_b, landmark_c)
"""