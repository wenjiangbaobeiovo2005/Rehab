# Android APK 构建说明

由于在本地Windows环境中构建Android APK可能遇到各种环境配置问题，我们推荐使用GitHub Actions进行自动构建。

## 方法一：使用GitHub Actions构建（推荐）

### 步骤：

1. 将项目代码推送到GitHub仓库
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Android build"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. GitHub Actions会自动触发构建流程，您可以在仓库的"Actions"选项卡中查看构建进度。

3. 构建完成后，APK文件会作为artifact上传，您可以下载使用。

## 方法二：本地Docker构建

如果您仍希望在本地构建，请确保：

1. Docker Desktop正在运行
2. 网络连接稳定
3. 首次运行时耐心等待镜像下载完成

```cmd
docker run --rm -v "%cd%":/home/user/hostcwd kivy/buildozer buildozer android debug
```

## 方法三：使用WSL2构建

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

## 注意事项

- 首次构建会下载大量依赖，可能需要30分钟或更长时间
- 构建过程需要至少4GB的可用磁盘空间
- 确保项目目录中包含以下必要文件：
  - main.py (应用入口)
  - buildozer.spec (构建配置)
  - requirements.txt (依赖列表)
  - main_kivy.py (Kivy应用代码)
  - pose_estimator.py (姿态估计算法)
```