import cv2
import mediapipe as mp
import numpy as np
import csv
import datetime
import os

# 初始化MediaPipe姿态估计器
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

import json
from db_manager import DatabaseManager

# 优化CSV方法以支持数据库选项并提高代码健壮性
import logging

# 在文件顶部添加日志配置（如果还没有的话）
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('PoseEstimator')

class PoseEstimator:
    """使用MediaPipe实现真实的姿态估计算法"""
    
    def __init__(self):
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.landmarks_history = []  # 存储历史姿态数据
        self.angle_history = {}  # 存储角度历史数据
        self.current_view = "front"  # 默认正面视图
        
        # 添加CSV日志相关属性
        self.csv_file = None
        self.csv_writer = None
        self.csv_file_path = None
        
        # 评估动作和视图的映射
        self.ACTIONS = {
            '深蹲': 'squat',
            '前后过栏架步': 'hurdle_step',
            '分腿蹲': 'split_squat',
            '肩部柔韧': 'shoulder_flex',
            '主动直膝抬腿': 'active_leg_raise',
            '俯卧撑': 'push_up',
            '体旋': 'trunk_rotation'
        }
        
        # 深蹲动作指引（不同视图）
        self.SQUAT_GUIDANCE = {
            'front': [
                "准备阶段：双脚与肩同宽，脚尖略微外展",
                "下降阶段：缓慢下蹲，保持膝盖与脚尖方向一致",
                "最低位置：大腿平行于地面或更低",
                "上升阶段：缓慢站起，保持核心收紧"
            ],
            'side': [
                "准备阶段：侧面朝向摄像头，双脚与肩同宽",
                "下降阶段：臀部后移，膝盖弯曲，保持背部平直",
                "最低位置：大腿平行于地面或更低",
                "上升阶段：通过脚跟发力回到起始位置"
            ],
            '45': [
                "准备阶段：45度角朝向摄像头，双脚与肩同宽",
                "下降阶段：保持身体稳定，避免躯干旋转",
                "最低位置：大腿平行于地面或更低",
                "上升阶段：保持对称发力回到起始位置"
            ]
        }
        
        # 其他动作指引
        self.ACTION_GUIDANCE = {
            'hurdle_step': [
                "准备阶段：面对栏架站立，双脚与肩同宽",
                "迈步阶段：抬起一侧腿跨过栏架",
                "支撑阶段：支撑腿保持稳定",
                "回退阶段：缓慢收回腿部回到起始位置"
            ],
            'split_squat': [
                "准备阶段：前后分腿站立，保持身体直立",
                "下降阶段：前腿膝盖弯曲，后腿膝盖接近地面",
                "最低位置：前大腿平行于地面",
                "上升阶段：通过前腿发力回到起始位置"
            ],
            'shoulder_flex': [
                "准备阶段：站立位，手臂自然下垂",
                "抬臂阶段：缓慢抬起一侧手臂至头顶",
                "保持阶段：保持5秒，感受肩部拉伸",
                "回落阶段：缓慢放下手臂回到起始位置"
            ],
            'active_leg_raise': [
                "准备阶段：仰卧位，双腿伸直",
                "抬腿阶段：保持膝盖伸直，缓慢抬起一侧腿",
                "最高位置：腿部与地面垂直",
                "回落阶段：缓慢放下腿部回到起始位置"
            ],
            'push_up': [
                "准备阶段：俯卧位，双手与肩同宽支撑",
                "下降阶段：弯曲肘部使身体下降至胸部接近地面",
                "保持阶段：在最低点保持1秒",
                "上升阶段：撑起身体回到起始位置"
            ],
            'trunk_rotation': [
                "准备阶段：四肢支撑位",
                "执行阶段：交替手膝相触",
                "保持阶段：保持躯干稳定",
                "完成阶段：回到起始位置"
            ]
        }
        
        # 参数标签映射
        self.PARAM_LABELS = {
            'squat': {
                'front': {
                    'left_hip_angle': "- 左髋角度：{:.1f}° (标准≥120°)\n",
                    'right_hip_angle': "- 右髋角度：{:.1f}° (标准≥120°)\n",
                    'left_knee_angle': "- 左膝角度：{:.1f}° (标准≥90°)\n",
                    'right_knee_angle': "- 右膝角度：{:.1f}° (标准≥90°)\n",
                    'foot_shoulder_ratio': "- 脚肩宽度比：{:.1f}% (标准80-120%)\n",
                    'knee_valgus': "- 双膝角度差：{:.1f}° (标准≤15°)\n"
                },
                'side': {
                    'trunk_angle': "- 躯干倾斜角度：{:.1f}° (标准≤30°)\n",
                    'hip_angle': "- 髋角度：{:.1f}° (标准≥120°)\n",
                    'knee_angle': "- 膝角度：{:.1f}° (标准≥90°)\n",
                    'ankle_angle': "- 踝角度：{:.1f}° (标准≥70°)\n",
                    'heel_lift': "- 脚跟离地高度：{:.1f}% (标准≤5%)\n"
                },
                '45': {
                    'side_hip_angle': "- 侧面髋角度：{:.1f}° (标准≥110°)\n",
                    'side_knee_angle': "- 侧面膝角度：{:.1f}° (标准≥90°)\n",
                    'front_hip_width': "- 正面髋宽度：{:.1f}\n",
                    'front_ankle_width': "- 正面踝宽度：{:.1f}\n",
                    'trunk_rotation': "- 躯干旋转角度：{:.1f}° (标准≤15°)\n"
                }
            },
            'hurdle_step': {
                'hip_angle': "- 髋角度：{:.1f}° (标准≥90°)\n",
                'knee_angle': "- 膝角度：{:.1f}° (标准≥90°)\n",
                'ankle_dorsiflexion': "- 踝背屈角度：{:.1f}° (标准≥10°)\n",
                'trunk_inclination': "- 躯干倾斜角度：{:.1f}° (标准≤10°)\n"
            }
        }
    
    def set_view(self, view: str) -> None:
        """设置当前视图角度"""
        self.current_view = view
        self.reset()
    
    def reset(self) -> None:
        """重置估计器状态"""
        self.landmarks_history = []
        self.angle_history = {}
        
        # 停止CSV日志记录
        if self.csv_file:
            self.csv_file.close()
            self.csv_file = None
            self.csv_writer = None
    
    def process_frame(self, frame):
        """处理单帧图像，返回处理后的帧和姿态数据"""
        # 转换为RGB格式，因为MediaPipe使用RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        
        # 绘制姿态标记
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        # 提取姿态特征和角度
        landmarks = None
        angles = None
        if results.pose_landmarks:
            landmarks = self.extract_landmarks(results.pose_landmarks)
            angles = self.calculate_angles(landmarks)
            self.landmarks_history.append(angles)
            
            # 更新角度历史记录
            for angle_name, angle_value in angles.items():
                if angle_name not in self.angle_history:
                    self.angle_history[angle_name] = []
                self.angle_history[angle_name].append(angle_value)
        
        return image, angles
    
    def extract_landmarks(self, landmarks):
        """提取关键点坐标"""
        landmark_dict = {}
        for idx, landmark in enumerate(landmarks.landmark):
            landmark_dict[idx] = (landmark.x, landmark.y, landmark.z)
        return landmark_dict
    
    def calculate_angles(self, landmarks):
        """根据当前视图计算相关角度"""
        angles = {}
        
        if self.current_view == "front":  # 正面视图角度计算
            # 计算膝关节角度
            left_knee_angle = self.calculate_joint_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            )
            right_knee_angle = self.calculate_joint_angle(
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            )
            
            # 计算髋关节角度
            left_hip_angle = self.calculate_joint_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            )
            right_hip_angle = self.calculate_joint_angle(
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
            )
            
            # 计算两脚间距与肩宽比例
            shoulder_width = self.calculate_distance(
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            )
            hip_width = self.calculate_distance(
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            )
            ankle_width = self.calculate_distance(
                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            )
            
            foot_shoulder_ratio = ankle_width / shoulder_width if shoulder_width > 0 else 0
            
            angles.update({
                'left_knee_angle': left_knee_angle,
                'right_knee_angle': right_knee_angle,
                'left_hip_angle': left_hip_angle,
                'right_hip_angle': right_hip_angle,
                'foot_shoulder_ratio': foot_shoulder_ratio * 100,  # 转换为百分比
                'knee_valgus': abs(left_knee_angle - right_knee_angle)  # 膝外翻程度
            })
            
        elif self.current_view == "side":  # 侧面视图角度计算
            # 计算躯干与地面角度
            trunk_angle = self.calculate_trunk_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            )
            
            # 计算髋关节角度
            hip_angle = self.calculate_joint_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            )
            
            # 计算膝关节角度
            knee_angle = self.calculate_joint_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            )
            
            # 计算踝关节角度
            ankle_angle = self.calculate_joint_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value]
            )
            
            # 计算脚跟离地高度
            heel_lift = self.calculate_heel_lift(
                landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value],
                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            )
            
            angles.update({
                'trunk_angle': trunk_angle,
                'hip_angle': hip_angle,
                'knee_angle': knee_angle,
                'ankle_angle': ankle_angle,
                'heel_lift': heel_lift
            })
            
        elif self.current_view == "45":  # 45度视图角度计算
            # 计算侧面相关角度
            side_hip_angle = self.calculate_joint_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            )
            side_knee_angle = self.calculate_joint_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            )
            
            # 计算正面相关角度
            front_hip_width = self.calculate_distance(
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            )
            front_ankle_width = self.calculate_distance(
                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            )
            
            # 计算躯干旋转角度
            trunk_rotation = self.calculate_trunk_rotation(
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            )
            
            angles.update({
                'side_hip_angle': side_hip_angle,
                'side_knee_angle': side_knee_angle,
                'front_hip_width': front_hip_width,
                'front_ankle_width': front_ankle_width,
                'trunk_rotation': trunk_rotation
            })
            
        return angles
    
    def calculate_joint_angle(self, a, b, c):
        """计算三点形成的关节角度（单位：度）"""
        # a, b, c 是三个点的坐标 (x, y, z)
        # 转换为numpy数组
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        # 计算向量
        ba = a - b
        bc = c - b
        
        # 计算点积和模长
        dot_product = np.dot(ba, bc)
        len_ba = np.linalg.norm(ba)
        len_bc = np.linalg.norm(bc)
        
        # 计算余弦值
        cosine_angle = dot_product / (len_ba * len_bc) if (len_ba * len_bc) > 0 else 1.0
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # 防止数值误差
        
        # 转换为角度
        angle = np.degrees(np.arccos(cosine_angle))
        return angle
    
    def calculate_distance(self, a, b):
        """计算两点之间的距离"""
        a = np.array(a)
        b = np.array(b)
        return np.linalg.norm(a - b)
    
    def calculate_trunk_angle(self, hip, shoulder):
        """计算躯干与垂直线的夹角"""
        # 计算躯干向量（从髋到肩）
        trunk_vector = np.array([shoulder[0] - hip[0], shoulder[1] - hip[1]])
        # 垂直参考向量
        vertical_vector = np.array([0, 1])  # 向下为正
        
        # 计算角度
        dot_product = np.dot(trunk_vector, vertical_vector)
        len_trunk = np.linalg.norm(trunk_vector)
        len_vertical = np.linalg.norm(vertical_vector)
        
        cosine_angle = dot_product / (len_trunk * len_vertical) if (len_trunk * len_vertical) > 0 else 1.0
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        
        angle = np.degrees(np.arccos(cosine_angle))
        return angle
    
    def calculate_heel_lift(self, heel, ankle):
        """计算脚跟离地高度（百分比）"""
        # 简单估计：脚跟y坐标与踝关节y坐标的差值
        # 值越大表示脚跟抬得越高
        return abs(heel[1] - ankle[1]) * 100
    
    def calculate_trunk_rotation(self, left_shoulder, right_shoulder, left_hip, right_hip):
        """计算躯干旋转角度"""
        # 计算肩线和腰线的角度差
        shoulder_vector = np.array([right_shoulder[0] - left_shoulder[0], right_shoulder[1] - left_shoulder[1]])
        hip_vector = np.array([right_hip[0] - left_hip[0], right_hip[1] - left_hip[1]])
        
        # 计算两个向量的角度
        dot_product = np.dot(shoulder_vector, hip_vector)
        len_shoulder = np.linalg.norm(shoulder_vector)
        len_hip = np.linalg.norm(hip_vector)
        
        if len_shoulder == 0 or len_hip == 0:
            return 0
            
        cosine_angle = dot_product / (len_shoulder * len_hip)
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        
        angle = np.degrees(np.arccos(cosine_angle))
        return angle
    
    def start_session(self, action_name, view_type, user_id=None, pain_reported=False):
        """开始新的数据库会话记录"""
        self.current_session_id = self.db_manager.start_session(
            action_type=action_name,
            view_type=view_type,
            user_id=user_id,
            pain_reported=pain_reported
        )
        return self.current_session_id
    
    def stop_session(self):
        """结束数据库会话记录"""
        if self.current_session_id:
            self.db_manager.stop_session(self.current_session_id)
            session_id = self.current_session_id
            self.current_session_id = None
            return session_id
        return None
    
    def log_to_database(self):
        """记录当前帧数据到数据库"""
        if self.current_session_id and self.landmarks_history and len(self.landmarks_history) > 0:
            current_data = self.landmarks_history[-1].copy()
            self.db_manager.log_frame_data(self.current_session_id, current_data)
    
    def save_evaluation_to_db(self, result):
        """保存评估结果到数据库"""
        if self.current_session_id and result:
            score_result = result['score_result']
            metrics = result['parameters']['metrics']
            
            return self.db_manager.save_evaluation(
                session_id=self.current_session_id,
                score=score_result['score'],
                reason=score_result['reason'],
                similarity=score_result['similarity'],
                compensations=score_result['compensations'],
                metrics=metrics
            )
        return None
    
    def start_csv_logging(self, action_name, use_database=False, user_id=None):
        """开始日志记录，支持数据库或CSV文件两种模式"""
        if use_database:
            self.start_session(action_name, self.current_view, user_id)
            return True
        
        # 原始CSV日志记录逻辑
        try:
            # 生成唯一的日志文件名，包含动作名称和时间戳
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.csv_file_path = os.path.join(self.log_dir, f"{action_name}_{timestamp}.csv")
            
            self.csv_file = open(self.csv_file_path, 'w', newline='', encoding='utf-8')
            self.csv_writer = csv.writer(self.csv_file)
            
            # 写入表头
            if self.landmarks_history and isinstance(self.landmarks_history[0], dict):
                headers = list(self.landmarks_history[0].keys())
                headers.insert(0, "timestamp")
                self.csv_writer.writerow(headers)
                logger.info(f"成功创建CSV日志文件: {self.csv_file_path}")
            return True
        except Exception as e:
            logger.error(f"创建CSV日志文件失败: {str(e)}")
            # 确保资源被释放
            if hasattr(self, 'csv_file') and self.csv_file:
                try:
                    self.csv_file.close()
                except:
                    pass
                self.csv_file = None
            self.csv_writer = None
            return False

    def log_data(self, use_database=False):
        """记录当前帧数据，根据配置写入数据库或CSV文件"""
        try:
            if use_database and self.current_session_id:
                self.log_to_database()
            elif self.csv_writer and self.landmarks_history and len(self.landmarks_history) > 0:
                current_data = self.landmarks_history[-1].copy()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                
                # 准备数据行 - 优化逻辑，确保与表头顺序一致
                first_record_keys = list(self.landmarks_history[0].keys())
                data_row = [timestamp] + [current_data.get(key, "") for key in first_record_keys]
                
                self.csv_writer.writerow(data_row)
                # 刷新到文件以确保数据保存
                self.csv_file.flush()
            return True
        except Exception as e:
            logger.error(f"记录数据失败: {str(e)}")
            return False

    def stop_csv_logging(self, use_database=False):
        """停止日志记录，关闭文件或结束数据库会话"""
        try:
            if use_database and self.current_session_id:
                return self.stop_session()
            
            if self.csv_file:
                self.csv_file.close()
                csv_path = self.csv_file_path
                self.csv_file = None
                self.csv_writer = None
                logger.info(f"成功关闭CSV日志文件: {csv_path}")
                return csv_path
            return None
        except Exception as e:
            logger.error(f"关闭CSV日志文件失败: {str(e)}")
            # 确保状态被重置
            self.csv_file = None
            self.csv_writer = None
            return None
    
    def evaluate(self, action, pain_reported=False, save_to_db=True):
        """评估动作"""
        result = super().evaluate(action, pain_reported)
        
        # 保存到数据库
        if save_to_db and self.current_session_id:
            self.save_evaluation_to_db(result)
        
        return result