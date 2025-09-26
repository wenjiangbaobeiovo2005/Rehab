from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line

import cv2
import numpy as np
import datetime
import os
from pose_estimator import PoseEstimator

class StyledButton(Button):
    """自定义样式按钮"""
    def __init__(self, **kwargs):
        super(StyledButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.color = (1, 1, 1, 1)
        self.font_size = sp(14)
        self.padding = (dp(10), dp(5))
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.6, 1.0, 1)  # 默认蓝色背景
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class StartButton(StyledButton):
    """开始按钮样式"""
    def __init__(self, **kwargs):
        super(StartButton, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.7, 0.3, 1)  # 绿色
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
        self.bind(pos=self.update_rect, size=self.update_rect)

class StopButton(StyledButton):
    """停止按钮样式"""
    def __init__(self, **kwargs):
        super(StopButton, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.8, 0.2, 0.2, 1)  # 红色
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
        self.bind(pos=self.update_rect, size=self.update_rect)

class DataButton(StyledButton):
    """数据收集按钮样式"""
    def __init__(self, **kwargs):
        super(DataButton, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.6, 0.5, 1.0, 1)  # 紫色
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
        self.bind(pos=self.update_rect, size=self.update_rect)

class ApiButton(StyledButton):
    """API接入按钮样式"""
    def __init__(self, **kwargs):
        super(ApiButton, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1.0, 0.6, 0.3, 1)  # 橙色
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
        self.bind(pos=self.update_rect, size=self.update_rect)

class PlanButton(StyledButton):
    """训练方案按钮样式"""
    def __init__(self, **kwargs):
        super(PlanButton, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.3, 0.7, 0.9, 1)  # 浅蓝色
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
        self.bind(pos=self.update_rect, size=self.update_rect)

class MainScreen(Screen):
    """主界面屏幕"""
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.pose_estimator = PoseEstimator()
        self.cap = None
        self.is_capturing = False
        self.current_action = "深蹲"
        self.is_evaluating = False
        self.is_pain_reported = False
        self.is_data_collecting = False  # 添加数据收集标志
        self.api_url = "http://localhost:5000/api/v1"
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI组件"""
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 应用标题
        title_label = Label(
            text="深蹲评估系统", 
            font_size=sp(20), 
            bold=True,
            color=(0.2, 0.3, 0.5, 1),
            size_hint_y=0.08
        )
        main_layout.add_widget(title_label)
        
        # 顶部控制栏 - 增加功能按钮区域
        top_bar = BoxLayout(orientation='vertical', size_hint_y=0.2, spacing=5)
        
        # 第一行：动作选择、视图选择、控制按钮
        top_bar_row1 = BoxLayout(orientation='horizontal', size_hint_y=0.5, spacing=10)
        
        # 动作选择下拉框
        action_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=2)
        action_label = Label(text="选择动作", font_size='12sp', size_hint_y=0.3)
        self.action_spinner = Spinner(
            text='深蹲',
            values=('深蹲', '前后过栏架步', '分腿蹲', '肩部柔韧', '主动直膝抬腿', '俯卧撑', '体旋'),
            size_hint_y=0.7,
            font_size='13sp'
        )
        self.action_spinner.bind(text=self.on_action_change)
        action_layout.add_widget(action_label)
        action_layout.add_widget(self.action_spinner)
        top_bar_row1.add_widget(action_layout)
        
        # 视图选择按钮组
        view_layout = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=2)
        view_label = Label(text="选择视图", font_size='12sp', size_hint_y=0.3)
        buttons_layout = BoxLayout(spacing=5, size_hint_y=0.7)
        
        self.front_btn = ToggleButton(
            text='正面', 
            group='view', 
            state='down',
            background_color=(0.2, 0.6, 1.0, 1),
            color=(1, 1, 1, 1),
            font_size='12sp'
        )
        self.side_btn = ToggleButton(
            text='侧面', 
            group='view',
            background_color=(0.7, 0.7, 0.7, 1),
            color=(0, 0, 0, 1),
            font_size='12sp'
        )
        self.angle45_btn = ToggleButton(
            text='45°', 
            group='view',
            background_color=(0.7, 0.7, 0.7, 1),
            color=(0, 0, 0, 1),
            font_size='12sp'
        )
        
        self.front_btn.bind(on_press=lambda x: self.set_view('front'))
        self.side_btn.bind(on_press=lambda x: self.set_view('side'))
        self.angle45_btn.bind(on_press=lambda x: self.set_view('45'))
        
        buttons_layout.add_widget(self.front_btn)
        buttons_layout.add_widget(self.side_btn)
        buttons_layout.add_widget(self.angle45_btn)
        view_layout.add_widget(view_label)
        view_layout.add_widget(buttons_layout)
        top_bar_row1.add_widget(view_layout)
        
        # 控制按钮
        control_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=2)
        control_label = Label(text="控制", font_size='12sp', size_hint_y=0.3)
        buttons_layout = BoxLayout(spacing=5, size_hint_y=0.7)
        
        self.start_btn = StartButton(text='开始')
        self.stop_btn = StopButton(text='停止', disabled=True)
        
        self.start_btn.bind(on_press=self.start_capture)
        self.stop_btn.bind(on_press=self.stop_capture)
        
        buttons_layout.add_widget(self.start_btn)
        buttons_layout.add_widget(self.stop_btn)
        control_layout.add_widget(control_label)
        control_layout.add_widget(buttons_layout)
        top_bar_row1.add_widget(control_layout)
        
        top_bar.add_widget(top_bar_row1)
        
        # 第二行：新增功能按钮 - 收集数据、接入API、生成训练方案
        top_bar_row2 = BoxLayout(orientation='horizontal', size_hint_y=0.5, spacing=dp(10))
        
        # 数据收集按钮
        self.data_btn = DataButton(text='收集数据')
        self.data_btn.bind(on_press=self.collect_data)
        top_bar_row2.add_widget(self.data_btn)
        
        # API接入按钮
        self.api_btn = ApiButton(text='接入API')
        self.api_btn.bind(on_press=self.api_integration)
        top_bar_row2.add_widget(self.api_btn)
        
        # 训练方案按钮
        self.plan_btn = PlanButton(text='训练方案')
        self.plan_btn.bind(on_press=self.generate_plan)
        top_bar_row2.add_widget(self.plan_btn)
        
        top_bar.add_widget(top_bar_row2)
        main_layout.add_widget(top_bar)
        
        # 中间区域：视频显示和指引信息
        middle_layout = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=dp(10))
        
        # 视频显示区域
        video_layout = FloatLayout(size_hint_y=0.7)
        self.video_image = Image(
            allow_stretch=True,
            keep_ratio=True
        )
        video_layout.add_widget(self.video_image)
        middle_layout.add_widget(video_layout)
        
        # 动作指引信息区域
        guidance_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)
        guidance_label = Label(
            text='动作指引:', 
            font_size=sp(14), 
            bold=True,
            halign='left',
            size_hint_y=0.3
        )
        guidance_label.bind(size=guidance_label.setter('text_size'))
        
        # 使用ScrollView包装指引文本，以便在内容过多时可以滚动
        scroll_view = ScrollView(size_hint_y=0.7)
        self.guidance_text = Label(
            text='请将摄像头对准身体正面，双脚与肩同宽，双手向前平举，然后开始深蹲动作。',
            font_size=sp(12),
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        self.guidance_text.bind(size=self.update_guidance_text_size)
        scroll_view.add_widget(self.guidance_text)
        
        guidance_layout.add_widget(guidance_label)
        guidance_layout.add_widget(scroll_view)
        middle_layout.add_widget(guidance_layout)
        
        main_layout.add_widget(middle_layout)
        
        video_container.add_widget(self.video_display)
        video_container.add_widget(self.status_indicator)
        main_layout.add_widget(video_container)
        
        # 底部信息区域
        info_layout = BoxLayout(orientation='vertical', size_hint_y=0.22, spacing=dp(10))
        
        guidance_container.add_widget(guidance_label)
        guidance_container.add_widget(self.guidance_text)
        info_layout.add_widget(guidance_container)
        
        # 评估信息和参数
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=0.7, spacing=10)
        
        # 左侧：评估结果
        eval_container = FloatLayout(size_hint_x=0.5)
        with eval_container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            RoundedRectangle(pos=eval_container.pos, size=eval_container.size, radius=[dp(8)])
        
        eval_label = Label(
            text='评估结果', 
            pos_hint={'top': 1, 'left': 0},
            size_hint=(0.5, 0.15),
            font_size='13sp', 
            bold=True,
            color=(0.2, 0.3, 0.5, 1)
        )
        
        # 疼痛报告复选框
        pain_layout = BoxLayout(orientation='horizontal', pos_hint={'top': 0.8, 'left': 0}, size_hint=(0.9, 0.15))
        pain_check = CheckBox(size_hint_x=0.2)
        pain_check.bind(active=self.on_pain_check)
        pain_label = Label(text='疼痛报告', font_size='12sp')
        pain_layout.add_widget(pain_check)
        pain_layout.add_widget(pain_label)
        
        # 评估分数
        self.score_label = Label(
            text='分数: --/3', 
            pos_hint={'top': 0.6, 'center_x': 0.5},
            size_hint=(0.5, 0.2),
            font_size='16sp', 
            bold=True,
            color=(0.2, 0.6, 1.0, 1)
        )
        
        # 评估进度条
        progress_layout = BoxLayout(orientation='vertical', pos_hint={'bottom': 0.1, 'left': 0.1}, size_hint=(0.8, 0.2))
        self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=0.3)
        progress_label = Label(text="评估进度", font_size='10sp', size_hint_y=0.4)
        progress_layout.add_widget(progress_label)
        progress_layout.add_widget(self.progress_bar)
        
        eval_container.add_widget(eval_label)
        eval_container.add_widget(pain_layout)
        eval_container.add_widget(self.score_label)
        eval_container.add_widget(progress_layout)
        
        # 右侧：参数信息
        params_container = FloatLayout(size_hint_x=0.5)
        with params_container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            RoundedRectangle(pos=params_container.pos, size=params_container.size, radius=[dp(8)])
        
        params_label = Label(
            text='动作参数', 
            pos_hint={'top': 1, 'left': 0},
            size_hint=(0.5, 0.1),
            font_size='13sp', 
            bold=True,
            color=(0.2, 0.3, 0.5, 1)
        )
        
        self.params_text = TextInput(
            text="等待数据...",
            pos_hint={'top': 0.85, 'left': 0.05},
            size_hint=(0.9, 0.75),
            readonly=True,
            multiline=True,
            font_size='12sp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        
        params_container.add_widget(params_label)
        params_container.add_widget(self.params_text)
        
        bottom_layout.add_widget(eval_container)
        bottom_layout.add_widget(params_container)
        info_layout.add_widget(bottom_layout)
        main_layout.add_widget(info_layout)
        
        self.add_widget(main_layout)
        
        # 绑定窗口大小变化事件
        Window.bind(size=self.on_window_size_change)
    
    def update_guidance_text_size(self, instance, value):
        """更新指引文本的尺寸"""
        instance.text_size = (instance.width - dp(10), None)
    
    def on_window_size_change(self, instance, value):
        """处理窗口大小变化"""
        # 更新视频背景尺寸
        if hasattr(self, 'video_image'):
            self.video_image.size = (value[0]-dp(20), self.video_image.size[1])
        
        # 更新指引文本尺寸
        if hasattr(self, 'guidance_text'):
            self.guidance_text.text_size = (value[0] * 0.9, None)
    
    def on_action_change(self, spinner, text):
        """处理动作选择变化"""
        self.current_action = text
        self.update_guidance()
    
    def set_view(self, view):
        """设置当前视图并更新按钮样式"""
        self.pose_estimator.set_view(view)
        self.update_guidance()
        
        # 更新按钮样式
        button_styles = {
            'front': self.front_btn,
            'side': self.side_btn,
            '45': self.angle45_btn
        }
        
        for btn_view, btn in button_styles.items():
            if btn_view == view:
                btn.background_color = (0.2, 0.6, 1.0, 1)
                btn.color = (1, 1, 1, 1)
            else:
                btn.background_color = (0.7, 0.7, 0.7, 1)
                btn.color = (0, 0, 0, 1)
    
    def update_guidance(self):
        """更新动作指引信息"""
        guidance_texts = {
            '深蹲': {
                'front': '请将摄像头对准身体正面，双脚与肩同宽，双手向前平举，然后开始深蹲动作。',
                'side': '请将摄像头对准身体侧面，单脚着地，另一只脚抬起，然后开始深蹲动作。',
                '45': '请将摄像头对准身体45度角，保持身体稳定，然后开始深蹲动作。'
            },
            '前后过栏架步': {
                'front': '请将摄像头对准身体正面，将一个物体放在脚前方作为栏架，然后进行跨步动作。',
                'side': '请将摄像头对准身体侧面，将一个物体放在脚前方作为栏架，然后进行跨步动作。',
                '45': '请将摄像头对准身体45度角，将一个物体放在脚前方作为栏架，然后进行跨步动作。'
            },
            '分腿蹲': {
                'front': '请将摄像头对准身体正面，一脚向前迈出大步，然后进行弓步蹲动作。',
                'side': '请将摄像头对准身体侧面，一脚向前迈出大步，然后进行弓步蹲动作。',
                '45': '请将摄像头对准身体45度角，一脚向前迈出大步，然后进行弓步蹲动作。'
            },
            '肩部柔韧': {
                'front': '请将摄像头对准身体正面，一手从上方，一手从下方，尝试在背后握手。',
                'side': '请将摄像头对准身体侧面，一手从上方，一手从下方，尝试在背后握手。',
                '45': '请将摄像头对准身体45度角，一手从上方，一手从下方，尝试在背后握手。'
            },
            '主动直膝抬腿': {
                'front': '请将摄像头对准身体正面，保持站立姿势，然后尽可能高地抬起一只脚。',
                'side': '请将摄像头对准身体侧面，保持站立姿势，然后尽可能高地抬起一只脚。',
                '45': '请将摄像头对准身体45度角，保持站立姿势，然后尽可能高地抬起一只脚。'
            },
            '俯卧撑': {
                'front': '请将摄像头对准身体正面，进行标准俯卧撑动作，保持身体平直。',
                'side': '请将摄像头对准身体侧面，进行标准俯卧撑动作，保持身体平直。',
                '45': '请将摄像头对准身体45度角，进行标准俯卧撑动作，保持身体平直。'
            },
            '体旋': {
                'front': '请将摄像头对准身体正面，保持四肢着地姿势，然后进行旋转稳定性测试。',
                'side': '请将摄像头对准身体侧面，保持四肢着地姿势，然后进行旋转稳定性测试。',
                '45': '请将摄像头对准身体45度角，保持四肢着地姿势，然后进行旋转稳定性测试。'
            }
        }
        
        view = self.pose_estimator.current_view
        action = self.current_action
        if action in guidance_texts and view in guidance_texts[action]:
            self.guidance_text.text = guidance_texts[action][view]
        else:
            self.guidance_text.text = "请开始动作评估"
    
    def on_pain_check(self, checkbox, value):
        """处理疼痛报告复选框变化"""
        self.is_pain_reported = value
    
    def start_capture(self, instance):
        """开始视频捕获"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                Logger.error("无法打开摄像头")
                return
                
            self.is_capturing = True
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            
            # 设置视频帧率
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # 开始更新视频帧
            Clock.schedule_interval(self.update_frame, 1.0/30.0)
            
            Logger.info("视频捕获已开始")
        except Exception as e:
            Logger.error(f"启动视频捕获时出错: {str(e)}")
    
    def stop_capture(self, instance):
        """停止视频捕获"""
        self.is_capturing = False
        Clock.unschedule(self.update_frame)
        
        if self.cap:
            self.cap.release()
            self.cap = None
            
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.video_image.texture = None
        
        Logger.info("视频捕获已停止")
    
    def update_frame(self, dt):
        """更新视频帧"""
        if not self.is_capturing or not self.cap:
            return
            
        ret, frame = self.cap.read()
        if not ret:
            return
            
        try:
            # 处理视频帧
            processed_frame = self.process_frame(frame)
            
            # 将OpenCV图像转换为Kivy纹理
            buf = cv2.flip(processed_frame, 0).tostring()
            texture = Texture.create(
                size=(processed_frame.shape[1], processed_frame.shape[0]), 
                colorfmt='bgr'
            )
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            
            # 更新图像显示
            self.video_image.texture = texture
        except Exception as e:
            Logger.error(f"更新视频帧时出错: {str(e)}")
    
    def collect_data(self, instance):
        """处理数据收集"""
        Logger.info("开始数据收集")
        # 这里应该实现数据收集逻辑
        
    def api_integration(self, instance):
        """处理API接入"""
        Logger.info("接入API功能")
        # 这里应该实现API接入逻辑
        
    def generate_plan(self, instance):
        """处理训练方案生成"""
        Logger.info("生成训练方案")
        # 这里应该实现训练方案生成逻辑
    
    def show_api_data_options(self):
        """显示API数据发送选项"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 发送类型选择
        content.add_widget(Label(text="选择要发送的数据类型:"))
        
        send_last_session_btn = StyledButton(text="发送最近一次评估数据")
        send_all_data_btn = StyledButton(text="发送所有历史数据")
        cancel_btn = StyledButton(text="取消")
        
        content.add_widget(send_last_session_btn)
        content.add_widget(send_all_data_btn)
        content.add_widget(cancel_btn)
        
        popup = Popup(title="API数据发送选项", content=content, size_hint=(0.7, 0.5))
        
        def send_last_session(instance):
            self.status_indicator.text = "正在发送最近评估数据..."
            try:
                # 获取最近一次评估数据
                if hasattr(self.pose_estimator, 'db_manager') and self.pose_estimator.db_manager:
                    # 从数据库获取最近会话
                    session_history = self.pose_estimator.db_manager.get_session_history(limit=1)
                    if session_history and len(session_history) > 0:
                        session_id = session_history[0][0]
                        session_data = self.pose_estimator.db_manager.get_session_data(session_id)
                        
                        # 发送数据到API
                        response = requests.post(
                            f"{self.api_url}/data",
                            json=session_data,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if response.status_code == 200:
                            self.status_indicator.text = "最近评估数据发送成功"
                            self.status_indicator.color = (0.2, 0.7, 0.3, 1)
                        else:
                            self.status_indicator.text = f"数据发送失败: {response.status_code}"
                            self.status_indicator.color = (0.8, 0.2, 0.2, 1)
                    else:
                        self.status_indicator.text = "没有找到评估数据"
                        self.status_indicator.color = (0.8, 0.6, 0.0, 1)
                else:
                    self.status_indicator.text = "数据库未初始化"
                    self.status_indicator.color = (0.8, 0.2, 0.2, 1)
            except Exception as e:
                self.status_indicator.text = f"数据发送错误: {str(e)}"
                self.status_indicator.color = (0.8, 0.2, 0.2, 1)
            popup.dismiss()
        
        send_last_session_btn.bind(on_press=send_last_session)
        send_all_data_btn.bind(on_press=lambda x: self.status_indicator.text("此功能正在开发中"))
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def generate_training_plan(self, instance):
        """生成个性化训练方案"""
        try:
            self.status_indicator.text = "正在生成训练方案..."
            self.status_indicator.color = (0.3, 0.7, 0.9, 1)  # 浅蓝色
            
            # 创建用户信息输入弹窗
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            
            age_input = TextInput(hint_text="年龄")
            weight_input = TextInput(hint_text="体重(kg)")
            height_input = TextInput(hint_text="身高(cm)")
            experience_input = Spinner(
                text='初学者',
                values=('初学者', '中级', '高级'),
                size_hint_y=None,
                height=40
            )
            
            submit_btn = StyledButton(text="生成方案")
            cancel_btn = StyledButton(text="取消")
            
            buttons_box = BoxLayout(spacing=10)
            buttons_box.add_widget(submit_btn)
            buttons_box.add_widget(cancel_btn)
            
            content.add_widget(Label(text="请输入您的个人信息"))
            content.add_widget(Label(text="年龄:"))
            content.add_widget(age_input)
            content.add_widget(Label(text="体重(kg):"))
            content.add_widget(weight_input)
            content.add_widget(Label(text="身高(cm):"))
            content.add_widget(height_input)
            content.add_widget(Label(text="训练经验:"))
            content.add_widget(experience_input)
            content.add_widget(buttons_box)
            
            popup = Popup(title="个性化训练方案", content=content, size_hint=(0.7, 0.6))
            
            def on_generate(instance):
                # 收集用户信息
                user_info = {
                    'age': age_input.text,
                    'weight': weight_input.text,
                    'height': height_input.text,
                    'experience': experience_input.text
                }
                
                # 获取最近的评估结果
                recent_evaluation = None
                if hasattr(self.pose_estimator, 'db_manager') and self.pose_estimator.db_manager:
                    session_history = self.pose_estimator.db_manager.get_session_history(limit=1)
                    if session_history and len(session_history) > 0:
                        session_id = session_history[0][0]
                        session_data = self.pose_estimator.db_manager.get_session_data(session_id)
                        recent_evaluation = session_data.get('evaluation')
                
                # 生成训练方案
                training_plan = self._create_training_plan(user_info, recent_evaluation)
                
                # 显示训练方案
                plan_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
                plan_text = TextInput(text=training_plan, multiline=True, readonly=True, size_hint_y=0.9)
                close_btn = StyledButton(text="关闭", size_hint_y=0.1)
                
                plan_content.add_widget(plan_text)
                plan_content.add_widget(close_btn)
                
                plan_popup = Popup(title="您的个性化训练方案", content=plan_content, size_hint=(0.8, 0.8))
                close_btn.bind(on_press=plan_popup.dismiss)
                plan_popup.open()
                
                self.status_indicator.text = "训练方案生成完成"
                self.status_indicator.color = (0.2, 0.7, 0.3, 1)
                popup.dismiss()
            
            submit_btn.bind(on_press=on_generate)
            cancel_btn.bind(on_press=popup.dismiss)
            
            popup.open()
        except Exception as e:
            self.status_indicator.text = f"生成训练方案错误: {str(e)}"
            self.status_indicator.color = (0.8, 0.2, 0.2, 1)
    
    def _create_training_plan(self, user_info, evaluation_result):
        """根据用户信息和评估结果创建训练方案"""
        # 基础训练方案模板
        plan = "个性化深蹲训练方案\n\n"
        plan += "一、用户信息\n"
        plan += f"- 年龄: {user_info['age'] or '未提供'}\n"
        plan += f"- 体重: {user_info['weight'] or '未提供'} kg\n"
        plan += f"- 身高: {user_info['height'] or '未提供'} cm\n"
        plan += f"- 训练经验: {user_info['experience']}\n\n"
        
        # 如果有评估结果，根据评估结果调整方案
        if evaluation_result:
            score = evaluation_result[2]  # 假设评估结果中的第3个元素是分数
            plan += "二、基于您的评估结果\n"
            plan += f"- 最近评估得分: {score}/3\n\n"
            
            # 根据得分调整训练建议
            if score >= 2.5:
                plan += "三、训练建议\n"
                plan += "您的深蹲动作质量良好！以下是进阶训练方案：\n\n"
                plan += "1. 负重深蹲: 使用杠铃或哑铃增加训练强度\n"
                plan += "2. 单腿深蹲: 提高核心稳定性和下肢力量\n"
                plan += "3. 深蹲跳: 增强爆发力\n"
                plan += "频率: 每周3-4次，每次3-4组，每组8-12次\n"
            elif score >= 1.5:
                plan += "三、训练建议\n"
                plan += "您的深蹲动作基础不错，但仍有改进空间：\n\n"
                plan += "1. 标准深蹲: 重点关注动作质量\n"
                plan += "2. 静态深蹲: 保持深蹲姿势5-10秒，增强肌肉耐力\n"
                plan += "3. 弹力带辅助深蹲: 改善动作轨迹\n"
                plan += "频率: 每周3次，每次3组，每组10-15次\n"
            else:
                plan += "三、训练建议\n"
                plan += "建议从基础动作开始，逐步提高：\n\n"
                plan += "1. 箱式深蹲: 使用箱子控制下蹲深度\n"
                plan += "2. 靠墙静蹲: 改善膝盖内扣问题\n"
                plan += "3. 弹力带激活: 训练前激活臀部肌肉\n"
                plan += "频率: 每周2-3次，每次2-3组，每组12-20次\n"
        else:
            # 没有评估结果，提供通用训练方案
            experience = user_info['experience']
            plan += "二、通用训练方案\n"
            
            if experience == '初学者':
                plan += "针对初学者的基础深蹲训练：\n\n"
                plan += "1. 空气深蹲: 无负重练习，重点掌握动作模式\n"
                plan += "2. 箱式深蹲: 使用椅子或箱子辅助控制深度\n"
                plan += "3. 徒手箭步蹲: 增强下肢稳定性\n"
                plan += "频率: 每周2次，每次2-3组，每组10-15次\n"
            elif experience == '中级':
                plan += "针对中级训练者的进阶方案：\n\n"
                plan += "1. 哑铃深蹲: 增加负重，提高训练强度\n"
                plan += "2. 保加利亚分腿蹲: 改善双腿力量不平衡\n"
                plan += "3. 过头深蹲: 增强核心稳定性\n"
                plan += "频率: 每周3次，每次3-4组，每组8-12次\n"
            else:
                plan += "针对高级训练者的强化方案：\n\n"
                plan += "1. 杠铃深蹲: 大重量训练，提高整体力量\n"
                plan += "2. 前蹲: 重点锻炼股四头肌\n"
                plan += "3. 单腿深蹲: 极限挑战下肢力量和稳定性\n"
                plan += "频率: 每周3-4次，每次4组，每组6-10次\n"
        
        # 通用注意事项
        plan += "\n四、注意事项\n"
        plan += "1. 始终保持正确姿势，避免膝盖内扣\n"
        plan += "2. 训练前充分热身，训练后拉伸放松\n"
        plan += "3. 如感到疼痛，立即停止训练并咨询专业人士\n"
        plan += "4. 保证充足的休息和营养，促进肌肉恢复\n"
        
        return plan

class RehabGPTApp(App):
    """主应用程序类"""
    
    def build(self):
        # 设置应用的标题
        self.title = "RehabGPT智能康复训练评估系统"
        
        # 创建屏幕管理器
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        
        return sm

if __name__ == '__main__':
    RehabGPTApp().run()