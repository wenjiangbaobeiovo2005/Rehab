@echo off
REM Android APK构建脚本
REM 此脚本使用Docker构建RehabGPT的Android APK

echo 确保Docker Desktop正在运行...
echo 当前目录: %cd%
echo.

REM 检查Docker是否可用
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Docker，请确保已安装并运行Docker Desktop
    pause
    exit /b 1
)

echo 清理项目目录...
python clean_project.py
echo.

echo 开始构建Android APK...
echo 这可能需要较长时间（10-30分钟），请耐心等待...
echo.

REM 使用Kivy官方Docker镜像构建APK
docker run --rm -v "%cd%":/home/user/hostcwd kivy/buildozer buildozer android debug

if %errorlevel% equ 0 (
    echo.
    echo 构建成功完成！
    echo APK文件位于 bin/ 目录中
    echo.
) else (
    echo.
    echo 构建过程中出现错误，请检查上面的输出信息
    echo.
)

pause