# RehabGPT智能康复训练评估系统 - 安卓转换方案

## 项目分析

### 当前技术栈
- **核心逻辑**：Python + MediaPipe (姿态估计)
- **GUI框架**：PyQt5
- **图像处理**：OpenCV, NumPy
- **数据可视化**：Matplotlib
- **依赖管理**：requirements.txt
- **安卓打包工具**：buildozer (存在基础配置)

### 主要功能
1. 人体姿态检测与关键点提取
2. 多角度(正面、侧面、45度)动作评估
3. 动作分析与评分系统
4. 数据导出与报告生成
5. 多种康复动作评估支持

## 安卓转换方案

### 技术选择
考虑到项目特性和已有资源，我们将采用以下方案：
- 保留核心的MediaPipe姿态估计和评估逻辑
- 使用**Kivy**框架重写UI界面(替代PyQt5)
- 利用已有的buildozer.spec配置进行打包
- 调整Matplotlib相关功能为Kivy兼容的可视化方案

### 转换步骤

#### 1. 创建Kivy主应用文件
```python
# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2
import mediapipe as mp
import numpy as np
import time
import datetime
import os
import csv

# 导入核心逻辑
from pose_estimator import PoseEstimator

class RehabGPTApp(App):
    def build(self):
        # 主界面布局
        self.main_layout = BoxLayout(orientation='vertical')
        
        # 创建顶部视频显示区域
        self.video_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6))
        self.video_frame = Image()
        self.video_layout.add_widget(self.video_frame)
        
        # 创建控制面板
        self.control_panel = BoxLayout(orientation='vertical', size_hint=(0.4, 1))
        # TODO: 添加控制按钮、动作选择等
        
        self.video_layout.add_widget(self.control_panel)
        
        # 创建结果标签页
        self.result_tabs = TabbedPanel(size_hint=(1, 0.4))
        # TODO: 添加评估结果、参数详情等标签页
        
        self.main_layout.add_widget(self.video_layout)
        self.main_layout.add_widget(self.result_tabs)
        
        # 初始化姿态估计器
        self.estimator = PoseEstimator()
        
        # 启动视频捕获
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/30.0)  # 30fps
        
        return self.main_layout
    
    def update(self, dt):
        # 捕获视频帧并处理
        ret, frame = self.capture.read()
        if ret:
            # 使用姿态估计器处理帧
            processed_frame, angles = self.estimator.process_frame(frame)
            
            # 转换为Kivy纹理
            buf = cv2.flip(processed_frame, 0).tobytes()
            texture = Texture.create(size=(processed_frame.shape[1], processed_frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.video_frame.texture = texture

if __name__ == '__main__':
    RehabGPTApp().run()
```

#### 2. 提取核心逻辑到独立模块
```python
# pose_estimator.py
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
        
    # 复制原始项目中的所有方法...
    def set_view(self, view: str) -> None:
        # 原始实现
    
    def reset(self) -> None:
        # 原始实现
        
    def process_frame(self, frame):
        # 原始实现
        
    # 其他方法...
```

#### 3. 更新buildozer.spec文件
```python
# (str) Title of your application
title = RehabGPT智能康复训练评估系统

# (str) Package name
package.name = rehabgpt

# (str) Package domain (needed for android/ios packaging)
package.domain = org.rehabgpt

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy,numpy,opencv-python,mediapipe,requests

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation
orientation = landscape

# (list) Permissions
sandroid.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
sandroid.api = 31

# (int) Minimum API your APK will support.
sandroid.minapi = 21

# (int) Android SDK version to use
sandroid.sdk = 28

# (str) Android NDK version to use
sandroid.ndk = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
sandroid.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path = 

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path = 
```

#### 4. 创建Kivy布局文件
```python
# rehabgpt.kv
<RehabGPTApp>:
    # 主布局样式
    BoxLayout:
        orientation: 'vertical'
        
        # 视频显示区域样式
        BoxLayout:
            size_hint: (1, 0.6)
            
            Image:
                id: video_frame
                allow_stretch: True
                keep_ratio: True
                
            BoxLayout:
                orientation: 'vertical'
                size_hint: (0.4, 1)
                spacing: 10
                padding: 10
                
                # 动作选择
                Label:
                    text: '选择评估动作'
                    font_size: 18
                    bold: True
                    
                Spinner:
                    id: action_spinner
                    text: '请选择动作'
                    values: ['深蹲', '前后过栏架步', '分腿蹲', '肩部柔韧', '主动直膝抬腿', '俯卧撑', '体旋']
                    size_hint_y: None
                    height: 40
                    on_text: root.on_action_changed(self.text)
                    
                # 视图角度选择
                Label:
                    text: '拍摄角度（仅深蹲）'
                    font_size: 18
                    bold: True
                    
                GridLayout:
                    cols: 3
                    
                    ToggleButton:
                        text: '正面'
                        group: 'view'
                        state: 'down'
                        on_state: root.on_view_changed('front', self.state)
                        
                    ToggleButton:
                        text: '侧面'
                        group: 'view'
                        on_state: root.on_view_changed('side', self.state)
                        
                    ToggleButton:
                        text: '45°角'
                        group: 'view'
                        on_state: root.on_view_changed('45', self.state)
                        
                # 控制按钮
                GridLayout:
                    cols: 2
                    spacing: 5
                    
                    Button:
                        text: '开始评估'
                        on_press: root.start_evaluation()
                        background_color: 0.2, 0.8, 0.2, 1
                        
                    Button:
                        text: '停止评估'
                        on_press: root.stop_evaluation()
                        background_color: 0.8, 0.2, 0.2, 1
                        
                    Button:
                        text: '导出数据'
                        on_press: root.export_csv_data()
                        background_color: 0.2, 0.2, 0.8, 1
                        
                    Button:
                        text: '生成评估报告'
                        on_press: root.generate_score()
                        background_color: 0.8, 0.5, 0, 1
                        
                    Button:
                        text: '重新评估'
                        on_press: root.reassess_action()
                        background_color: 0.5, 0, 0.5, 1
                        
                    Button:
                        text: '重置'
                        on_press: root.reset_evaluation()
                        background_color: 0.4, 0.4, 0.4, 1
                        
                # 疼痛报告按钮
                Button:
                    text: '报告疼痛'
                    on_press: root.report_pain()
                    background_color: 0.7, 0.2, 0.2, 1
                    size_hint_y: None
                    height: 40
                    
                # 状态显示
                Label:
                    id: status_label
                    text: '状态：欢迎使用RehabGPT智能康复训练评估系统'
                    color: 0.1, 0.6, 0.1, 1
                    font_size: 14
                    bold: True
                    
                # 动作指引
                Label:
                    id: guidance_label
                    text: '动作指引：请选择评估动作'
                    color: 0, 0.4, 0.8, 1
                    font_size: 14
                    bold: True
                    text_size: self.size
                    valign: 'top'
                    
                # 动作说明
                TextInput:
                    id: action_info
                    readonly: True
                    hint_text: '选择动作后显示标准动作说明...'
                    multiline: True
        
        # 结果标签页
        TabbedPanel:
            size_hint: (1, 0.4)
            
            TabbedPanelItem:
                text: '评分结果'
                
                BoxLayout:
                    orientation: 'vertical'
                    
                    Label:
                        id: score_label
                        text: 'RehabGPT 评估结果'
                        font_size: 20
                        bold: True
                        
                    TextInput:
                        id: score_details
                        readonly: True
                        multiline: True
            
            TabbedPanelItem:
                text: '参数详情'
                
                TextInput:
                    id: param_details
                    readonly: True
                    multiline: True
            
            TabbedPanelItem:
                text: '代偿分析'
                
                TextInput:
                    id: compensation_analysis
                    readonly: True
                    multiline: True
            
            TabbedPanelItem:
                text: '参数趋势图表'
                
                # 这里需要使用Kivy的图表组件替代Matplotlib
                BoxLayout:
                    id: trend_chart_layout
                    orientation: 'vertical'
            
            TabbedPanelItem:
                text: '多角度综合分析'
                
                TextInput:
                    id: comprehensive_analysis
                    readonly: True
                    multiline: True
```

## 实施建议

1. **分步实施**：
   - 先完成核心逻辑的提取和测试
   - 然后构建基础的Kivy UI框架
   - 逐步添加所有功能模块
   - 最后进行测试和优化

2. **兼容性考虑**：
   - MediaPipe在安卓上的性能可能与桌面版有所差异，可能需要调整参数
   - 安卓设备的摄像头权限和访问方式需要特别处理
   - 屏幕尺寸适配是关键，需要设计响应式UI

3. **测试策略**：
   - 使用buildozer在本地构建测试APK
   - 在不同型号的安卓设备上进行功能和性能测试
   - 特别测试摄像头捕获和姿态识别的稳定性

4. **性能优化**：
   - 考虑降低视频分辨率以提高处理速度
   - 实现姿态估计的批处理模式
   - 针对移动设备优化算法参数

## 所需工具和资源

1. **开发环境**：
   - Python 3.8+ 
   - Kivy 2.0+ 
   - Buildozer 
   - Android SDK/NDK

2. **测试设备**：
   - 至少一台Android 5.0+设备
   - 支持摄像头的平板或手机

3. **其他资源**：
   - 应用图标和启动画面
   - 安卓设备调试工具

通过以上方案，我们可以将现有的RehabGPT智能康复训练评估系统转换为一个功能完整的安卓应用，保持核心功能的同时，提供良好的移动用户体验。