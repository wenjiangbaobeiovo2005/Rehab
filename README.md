# AIFMS 2.0 - 功能性动作筛查系统

AIFMS (AI Functional Movement Screen) 2.0 是一个基于计算机视觉和人工智能的功能性动作筛查系统。该系统使用MediaPipe进行人体姿态估计，能够评估7种基本的FMS动作模式，为用户提供动作质量评分和个性化反馈建议。

## 功能特点

- 基于MediaPipe的姿态检测技术
- 支持7种FMS动作评估：
  - 深蹲 (Squat)
  - 跨栏步 (Hurdle Step)
  - 直线弓步蹲 (Inline Lunge)
  - 肩部灵活性 (Shoulder Mobility)
  - 主动直腿上抬 (Active Leg Raise)
  - 躯干稳定俯卧撑 (Trunk Pushup)
  - 旋转稳定性 (Rotary Stability)
- 实时动作分析和反馈
- 数据记录和分析功能
- 可视化界面
- 支持Windows和Android平台

## 系统要求

### Windows版本
- Windows 10/11 或其他支持的操作系统
- Python 3.7 或更高版本
- 支持的摄像头设备

### Android版本
- Android 5.0 (API 21) 或更高版本
- 支持的摄像头设备
- 摄像头和存储权限

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

### Windows版本（PyQt5界面）

```bash
python main_pyqt.py
```

### 跨平台版本（Kivy界面，支持Windows和Android）

```bash
python main_kivy.py
```

## 打包为可执行文件

### Windows打包

使用PyInstaller和提供的spec文件打包：

```bash
pyinstaller AIFMS2.0.spec
```

打包后的可执行文件将位于 `dist/AIFMS2.0` 目录中。

### Android打包

要构建Android应用，需要使用Buildozer工具。请按照以下步骤操作：

1. 安装Buildozer：

```bash
pip install buildozer
```

2. 构建APK：

```bash
buildozer android debug
```

构建完成后，APK文件将位于`bin`目录中。

## 项目结构

```
.
├── main_pyqt.py                # 原始PyQt5版本的主程序
├── main_kivy.py                # Kivy版本的主程序（用于Android）
├── pose_estimator.py           # 核心姿态估计算法模块
├── squat-evaluation-system/    # 主程序目录（原始结构）
│   ├── fms_assessors/          # FMS动作评估器
│   ├── utils/                  # 工具函数
│   ├── main_pyqt.py            # 原始主程序入口
│   └── pose.py                 # 原始姿态检测模块
├── AIFMS2.0.spec               # PyInstaller打包配置文件
├── buildozer.spec              # Android打包配置文件
├── requirements.txt            # 项目依赖列表
└── README.md                   # 项目说明文件
```

## 评估器说明

每个FMS评估器都实现了统一的接口：
- `assess(angles, landmarks)`: 评估动作并返回评分和反馈
- `reset()`: 重置评估器状态

## Android转换说明

项目已转换为支持Android平台，主要做了以下改进：

1. 核心逻辑提取：将姿态估计和评估逻辑从原PyQt5界面中分离到`pose_estimator.py`模块
2. 使用Kivy框架重写界面，创建了`main_kivy.py`作为安卓应用的主入口
3. 配置了`buildozer.spec`文件，包含必要的Android构建参数和权限设置
4. 更新了`requirements.txt`文件，添加了Kivy依赖

## 注意事项

1. 首次运行时可能需要下载MediaPipe模型文件
2. 确保摄像头设备正常工作
3. 为了获得最佳效果，请在光线充足的环境中使用
4. Android版本构建需要Android SDK、NDK等工具，Buildozer会自动下载这些工具
5. 构建Android应用过程可能需要较长时间，请确保网络连接稳定