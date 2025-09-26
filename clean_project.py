"""
项目清理脚本
用于删除不必要的测试文件和冗余代码，为Android构建做准备
"""

import os
import shutil

def remove_unnecessary_files():
    """删除不必要的测试文件和冗余目录"""
    # 需要删除的文件和目录列表
    files_to_remove = [
        'comprehensive_test.py',
        'core_test.py',
        'final_test_report.py',
        'functional_test.py',
        'gui_test.py',
        'simple_test.py',
        'test_active_leg_raise.py',
        'test_deepseek_reasoner.py',
        'test_path.py',
        'test_project.py',
        'main_pyqt.py',  # PyQt版本不适用于Android
        'package.bat',
        'package_en.bat',
        'package_new.bat',
        'package_simple.py',
        'simple_package.py',
        'install_packaging_tools.bat',
        'install_packaging_tools_fixed.bat',
        'install_pyinstaller.bat',
        'start_AIFMS2.0.bat',
        'new_spec.spec',
        'RehabGPT.spec',
        '深蹲评估系统.spec',
        '深蹲评估系统_PyQt.spec',
        '深蹲评估系统_mediapipe修复.spec',
        '深蹲评估系统_v2.spec',
        'AIFMS2.0_Release.zip',
        'AIFMS2.0_Source_Release.zip',
        '__init__.py'
    ]
    
    dirs_to_remove = [
        'AIFMS2.0',
        'AIFMS2.0_Organized',
        'AIFMS2.0_Release',
        'AIFMS2.0_Simple_Release',
        '__pycache__',
        '.buildozer',
        '.vscode',
        'RehabGPT',
        'release',
        'squat-evaluation-system',  # 主程序目录，但我们会保留其中的必要文件
        'build',
        'dist',
        'absolute',
        '历史数据',
        '.pytest_cache'
    ]
    
    print("开始清理项目目录...")
    
    # 删除文件
    for file in files_to_remove:
        file_path = os.path.join(os.getcwd(), file)
        if os.path.exists(file_path):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"已删除文件: {file}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"已删除目录: {file}")
            except Exception as e:
                print(f"删除 {file} 时出错: {e}")
    
    # 删除目录
    for dir_name in dirs_to_remove:
        dir_path = os.path.join(os.getcwd(), dir_name)
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"已删除目录: {dir_name}")
            except Exception as e:
                print(f"删除目录 {dir_name} 时出错: {e}")
    
    print("项目清理完成!")

if __name__ == "__main__":
    remove_unnecessary_files()