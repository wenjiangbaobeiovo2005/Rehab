# RehabGPT智能康复训练评估系统 - Android构建指南

## 项目概述

RehabGPT是一个基于计算机视觉与人工智能的功能性动作筛查系统，旨在通过AI技术自动化评估人体基本动作模式的质量，辅助运动康复、体能训练和健康筛查。

## 构建Android APK的说明

由于Buildozer工具在Windows环境下对Android的支持有限，建议使用以下方法之一来构建Android APK：

### 方法1：使用WSL (Windows Subsystem for Linux)

1. 安装WSL2和Ubuntu：
   ```bash
   wsl --install -d Ubuntu
   ```

2. 在WSL中安装必要的依赖：
   ```bash
   sudo apt update
   sudo apt install -y build-essential libffi-dev libssl-dev python3-dev python3-pip
   pip3 install buildozer
   ```

3. 安装Android构建依赖：
   ```bash
   sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

4. 安装Android SDK和NDK：
   ```bash
   buildozer android doctor
   ```

5. 构建APK：
   ```bash
   buildozer android debug
   ```

### 方法2：使用Docker

1. 安装Docker Desktop

2. 使用Kivy官方Docker镜像构建：
   ```bash
   docker run --rm -v "$PWD":/home/user/hostcwd kivy/buildozer buildozer android debug
   ```

### 方法3：使用GitHub Actions (推荐)

1. Fork项目到你的GitHub账户

2. 在项目中创建.github/workflows/android.yml文件：
   ```yaml
   name: Build Android APK
   
   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
   
   jobs:
     build:
       runs-on: ubuntu-latest
       
       steps:
       - uses: actions/checkout@v3
       
       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.8'
           
       - name: Install dependencies
         run: |
           pip install --upgrade pip
           pip install buildozer
           
       - name: Install build dependencies
         run: |
           sudo apt update
           sudo apt install -y build-essential libffi-dev libssl-dev python3-dev python3-pip
           sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
           
       - name: Build APK
         run: |
           buildozer android debug
           
       - name: Upload APK
         uses: actions/upload-artifact@v3
         with:
           name: RehabGPT-APK
           path: bin/*.apk
   ```

3. 推送代码到GitHub，Actions会自动构建APK

## 项目结构

```
.
├── main.py                 # Kivy应用入口点
├── main_kivy.py            # 主界面实现
├── pose_estimator.py       # 姿态估计算法
├── buildozer.spec          # Android构建配置
├── requirements.txt        # Python依赖
└── README_ANDROID.md       # 本说明文件
```

## 注意事项

1. MediaPipe在移动设备上的性能可能与桌面版有所差异
2. Android设备的摄像头权限和访问方式需要特别处理
3. 屏幕尺寸适配是关键，需要设计响应式UI
4. 由于项目依赖较多，APK文件可能会比较大

## 故障排除

1. 如果遇到构建错误，请检查buildozer.spec配置文件
2. 确保所有依赖版本兼容
3. 在WSL中构建时，确保有足够的磁盘空间