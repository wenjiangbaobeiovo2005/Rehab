#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RehabGPT移动端主入口文件
为Android平台优化的版本
"""

# 为Android平台设置Kivy的环境变量
import os
os.environ['KIVY_METRICS_DENSITY'] = '2'
os.environ['KIVY_METRICS_FONTSCALE'] = '1.0'

from kivy.config import Config
# 设置适合手机屏幕的窗口大小
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')
Config.write()

from main_kivy import RehabGPTApp

if __name__ == '__main__':
    RehabGPTApp().run()