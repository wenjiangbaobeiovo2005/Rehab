from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp, sp
import os
from datetime import datetime


class TrainingPlanScreen(Screen):
    """训练方案展示界面"""
    
    def __init__(self, **kwargs):
        super(TrainingPlanScreen, self).__init__(**kwargs)
        self.plan_content = ""
        self.setup_ui()
    
    def setup_ui(self):
        """设置训练方案展示界面"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # 标题
        title = Label(
            text="个性化训练方案",
            font_size=sp(24),
            bold=True,
            size_hint_y=0.1
        )
        main_layout.add_widget(title)
        
        # 方案内容显示区域
        content_layout = BoxLayout(orientation='vertical', size_hint_y=0.8)
        
        # 滚动视图包装方案内容
        scroll_view = ScrollView()
        self.plan_text = TextInput(
            text="",
            font_size=sp(14),
            readonly=True,
            multiline=True
        )
        scroll_view.add_widget(self.plan_text)
        content_layout.add_widget(scroll_view)
        
        main_layout.add_widget(content_layout)
        
        # 按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=dp(10))
        
        back_btn = Button(text="返回", font_size=sp(16))
        back_btn.bind(on_press=self.go_back)
        button_layout.add_widget(back_btn)
        
        save_btn = Button(text="保存方案", font_size=sp(16))
        save_btn.bind(on_press=self.save_plan)
        button_layout.add_widget(save_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def set_plan_content(self, content):
        """设置训练方案内容"""
        self.plan_content = content
        self.plan_text.text = content
    
    def go_back(self, instance):
        """返回主界面"""
        self.manager.current = 'main'
    
    def save_plan(self, instance):
        """保存训练方案到文件"""
        try:
            # 创建文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_plan_{timestamp}.txt"
            
            # 保存文件
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.plan_content)
            
            # 显示成功消息
            popup = Popup(
                title='保存成功',
                content=Label(text=f'训练方案已保存到文件: {filename}'),
                size_hint=(0.6, 0.3)
            )
            popup.open()
            
        except Exception as e:
            popup = Popup(
                title='保存失败',
                content=Label(text=f'保存训练方案时出错: {str(e)}'),
                size_hint=(0.6, 0.3)
            )
            popup.open()