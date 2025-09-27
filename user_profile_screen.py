from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp

from ai_assistant import AIFitnessAssistant
from user_profile import UserProfile


class UserProfileScreen(Screen):
    """用户信息输入界面"""
    
    def __init__(self, **kwargs):
        super(UserProfileScreen, self).__init__(**kwargs)
        self.user_profile = UserProfile()
        self.assessment_results = []
        self.api_key = None
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户信息输入界面"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # 标题
        title = Label(
            text="用户信息录入",
            font_size=sp(24),
            bold=True,
            size_hint_y=0.1
        )
        main_layout.add_widget(title)
        
        # 表单区域
        form_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.8)
        
        # 基本信息
        form_layout.add_widget(Label(text="年龄:", font_size=sp(16), halign='right'))
        self.age_input = TextInput(multiline=False, font_size=sp(16))
        form_layout.add_widget(self.age_input)
        
        form_layout.add_widget(Label(text="性别:", font_size=sp(16), halign='right'))
        self.gender_spinner = Spinner(
            text='男',
            values=('男', '女'),
            font_size=sp(16)
        )
        form_layout.add_widget(self.gender_spinner)
        
        form_layout.add_widget(Label(text="身高(cm):", font_size=sp(16), halign='right'))
        self.height_input = TextInput(multiline=False, font_size=sp(16))
        form_layout.add_widget(self.height_input)
        
        form_layout.add_widget(Label(text="体重(kg):", font_size=sp(16), halign='right'))
        self.weight_input = TextInput(multiline=False, font_size=sp(16))
        form_layout.add_widget(self.weight_input)
        
        form_layout.add_widget(Label(text="运动经验:", font_size=sp(16), halign='right'))
        self.experience_input = TextInput(multiline=True, font_size=sp(16))
        form_layout.add_widget(self.experience_input)
        
        form_layout.add_widget(Label(text="训练目标:", font_size=sp(16), halign='right'))
        self.goals_input = TextInput(multiline=True, font_size=sp(16))
        form_layout.add_widget(self.goals_input)
        
        form_layout.add_widget(Label(text="伤病史:", font_size=sp(16), halign='right'))
        self.injury_input = TextInput(multiline=True, font_size=sp(16))
        form_layout.add_widget(self.injury_input)
        
        form_layout.add_widget(Label(text="每周训练频率:", font_size=sp(16), halign='right'))
        self.frequency_spinner = Spinner(
            text='3',
            values=[str(i) for i in range(1, 8)],
            font_size=sp(16)
        )
        form_layout.add_widget(self.frequency_spinner)
        
        # API密钥输入（可选）
        form_layout.add_widget(Label(text="API密钥(可选):", font_size=sp(16), halign='right'))
        self.api_key_input = TextInput(multiline=False, font_size=sp(16), password=True)
        form_layout.add_widget(self.api_key_input)
        
        main_layout.add_widget(form_layout)
        
        # 按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=dp(10))
        
        back_btn = Button(text="返回", font_size=sp(16))
        back_btn.bind(on_press=self.go_back)
        button_layout.add_widget(back_btn)
        
        self.save_btn = Button(text="保存并生成方案", font_size=sp(16))
        self.save_btn.bind(on_press=self.save_and_generate)
        button_layout.add_widget(self.save_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def set_assessment_results(self, results):
        """设置评估结果数据"""
        self.assessment_results = results
    
    def go_back(self, instance):
        """返回主界面"""
        self.manager.current = 'main'
    
    def save_and_generate(self, instance):
        """保存用户信息并生成训练方案"""
        try:
            # 验证并保存基本信息
            age = int(self.age_input.text) if self.age_input.text else None
            gender = self.gender_spinner.text
            height = float(self.height_input.text) if self.height_input.text else None
            weight = float(self.weight_input.text) if self.weight_input.text else None
            
            self.user_profile.set_basic_info(age, gender, height, weight)
            self.user_profile.set_sport_experience(self.experience_input.text)
            self.user_profile.set_goals(self.goals_input.text)
            self.user_profile.set_injury_history(self.injury_input.text)
            self.user_profile.set_training_frequency(int(self.frequency_spinner.text))
            
            # 获取API密钥
            api_key = self.api_key_input.text if self.api_key_input.text else None
            
            # 生成训练方案
            self.generate_training_plan(api_key)
            
        except ValueError as e:
            popup = Popup(
                title='输入错误',
                content=Label(text='请输入有效的数字信息'),
                size_hint=(0.6, 0.3)
            )
            popup.open()
        except Exception as e:
            popup = Popup(
                title='错误',
                content=Label(text=f'发生错误: {str(e)}'),
                size_hint=(0.6, 0.3)
            )
            popup.open()
    
    def generate_training_plan(self, api_key=None):
        """生成个性化训练方案"""
        try:
            # 创建AI助手实例
            if api_key:
                assistant = AIFitnessAssistant(api_key=api_key)
            else:
                # 使用环境变量中的API密钥
                assistant = AIFitnessAssistant()
            
            # 生成训练方案
            plan = assistant.generate_personalized_plan(
                self.user_profile.get_profile(),
                self.assessment_results
            )
            
            # 显示训练方案
            self.show_training_plan(plan)
            
        except Exception as e:
            popup = Popup(
                title='生成失败',
                content=Label(text=f'生成训练方案时出错: {str(e)}'),
                size_hint=(0.8, 0.4)
            )
            popup.open()
    
    def show_training_plan(self, plan):
        """显示训练方案"""
        # 切换到训练方案展示界面
        plan_screen = self.manager.get_screen('training_plan')
        plan_screen.set_plan_content(plan)
        self.manager.current = 'training_plan'