from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from main_kivy import MainScreen
from user_profile_screen import UserProfileScreen
from training_plan_screen import TrainingPlanScreen


class RehabGPTApp(App):
    """主应用程序类"""
    
    def build(self):
        # 设置应用的标题
        self.title = "RehabGPT智能康复训练评估系统"
        
        # 创建屏幕管理器
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(UserProfileScreen(name='user_profile'))
        sm.add_widget(TrainingPlanScreen(name='training_plan'))
        
        return sm


if __name__ == '__main__':
    RehabGPTApp().run()