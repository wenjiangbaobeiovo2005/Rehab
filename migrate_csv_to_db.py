import os
import argparse
from db_manager import DatabaseManager

def migrate_all_csv_to_db(csv_dir, db_path="squat_evaluation.db"):
    """将目录中的所有CSV文件导入到数据库"""
    # 初始化数据库管理器
    db_manager = DatabaseManager(db_path)
    
    # 创建默认用户
    default_user_id = db_manager.add_user("default_user")
    
    # 获取目录中的所有CSV文件
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    
    print(f"找到 {len(csv_files)} 个CSV文件需要导入")
    
    # 逐个导入文件
    imported_count = 0
    for csv_file in csv_files:
        csv_path = os.path.join(csv_dir, csv_file)
        
        # 从文件名解析动作类型
        # 假设文件名格式为：squat_data_20250808_212714.csv
        action_type = "unknown"
        if "squat" in csv_file.lower():
            action_type = "深蹲"
        elif "hurdle" in csv_file.lower():
            action_type = "前后过栏架步"
        elif "split" in csv_file.lower():
            action_type = "分腿蹲"
        # 可以根据需要添加更多动作类型的识别
        
        # 假设视图类型需要手动确认，这里简化为side
        view_type = "side"
        
        print(f"正在导入: {csv_file} (动作类型: {action_type}, 视图: {view_type})")
        
        # 导入文件
        session_id = db_manager.import_from_csv(csv_path, action_type, view_type, default_user_id)
        if session_id:
            print(f"  导入成功，会话ID: {session_id}")
            imported_count += 1
        else:
            print(f"  导入失败")
    
    print(f"\n导入完成！成功导入 {imported_count}/{len(csv_files)} 个文件")
    
    # 关闭数据库连接
    db_manager.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将CSV数据导入到数据库")
    parser.add_argument("--csv_dir", type=str, default="./历史数据", 
                       help="包含CSV文件的目录路径")
    parser.add_argument("--db_path", type=str, default="squat_evaluation.db", 
                       help="数据库文件路径")
    
    args = parser.parse_args()
    
    # 检查CSV目录是否存在
    if not os.path.exists(args.csv_dir):
        print(f"错误：CSV目录 '{args.csv_dir}' 不存在")
        exit(1)
    
    # 开始迁移
    migrate_all_csv_to_db(args.csv_dir, args.db_path)