import sqlite3
import datetime
import os
import json

class DatabaseManager:
    """管理深蹲评估系统的数据库操作"""
    
    def __init__(self, db_path="squat_evaluation.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.initialize_database()
    
    def initialize_database(self):
        """初始化数据库，创建所需的表"""
        # 确保数据库目录存在
        db_dir = os.path.dirname(self.db_path) or os.getcwd()
        os.makedirs(db_dir, exist_ok=True)
        
        # 连接数据库
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
        # 创建用户表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        ''')
        
        # 创建评估会话表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action_type TEXT NOT NULL,
            view_type TEXT NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            pain_reported INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # 创建帧数据表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS frame_data (
            frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            timestamp TIMESTAMP NOT NULL,
            data_json TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions (session_id)
        )
        ''')
        
        # 创建评估结果表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluations (
            evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            score REAL NOT NULL,
            reason TEXT,
            similarity REAL,
            compensations TEXT,
            metrics_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (session_id)
        )
        ''')
        
        # 创建索引以提高查询性能
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions (user_id)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_frame_data_session ON frame_data (session_id)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_evaluations_session ON evaluations (session_id)')
        
        self.connection.commit()
    
    def add_user(self, username):
        """添加新用户"""
        try:
            self.cursor.execute(
                "INSERT INTO users (username, created_at, last_login) VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                (username,)
            )
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # 用户已存在，更新最后登录时间
            self.cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?",
                (username,)
            )
            self.connection.commit()
            # 获取用户ID
            self.cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            return self.cursor.fetchone()[0]
    
    def start_session(self, action_type, view_type, user_id=None, pain_reported=False):
        """开始新的评估会话"""
        self.cursor.execute(
            "INSERT INTO sessions (user_id, action_type, view_type, start_time, pain_reported) \
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)",
            (user_id, action_type, view_type, int(pain_reported))
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def stop_session(self, session_id):
        """结束评估会话"""
        self.cursor.execute(
            "UPDATE sessions SET end_time = CURRENT_TIMESTAMP WHERE session_id = ?",
            (session_id,)
        )
        self.connection.commit()
    
    def log_frame_data(self, session_id, frame_data):
        """记录一帧姿态数据"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        data_json = json.dumps(frame_data)
        
        self.cursor.execute(
            "INSERT INTO frame_data (session_id, timestamp, data_json) VALUES (?, ?, ?)",
            (session_id, timestamp, data_json)
        )
        self.connection.commit()
    
    def log_batch_frame_data(self, session_id, frames_data):
        """批量记录多帧姿态数据（提高性能）"""
        if not frames_data:
            return
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        data_tuples = []
        
        for frame_data in frames_data:
            data_json = json.dumps(frame_data)
            data_tuples.append((session_id, timestamp, data_json))
        
        # 使用事务批量插入
        try:
            self.cursor.executemany(
                "INSERT INTO frame_data (session_id, timestamp, data_json) VALUES (?, ?, ?)",
                data_tuples
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
    
    def save_evaluation(self, session_id, score, reason, similarity, compensations, metrics):
        """保存评估结果"""
        compensations_str = json.dumps(compensations)
        metrics_json = json.dumps(metrics)
        
        self.cursor.execute(
            "INSERT INTO evaluations (session_id, score, reason, similarity, compensations, metrics_json) \
            VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, score, reason, similarity, compensations_str, metrics_json)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_session_history(self, user_id=None, limit=100):
        """获取评估会话历史"""
        query = """
        SELECT s.session_id, u.username, s.action_type, s.view_type, s.start_time, s.end_time, s.pain_reported,
               e.score, e.similarity
        FROM sessions s
        LEFT JOIN users u ON s.user_id = u.user_id
        LEFT JOIN evaluations e ON s.session_id = e.session_id
        """
        
        params = []
        if user_id:
            query += " WHERE s.user_id = ?"
            params.append(user_id)
        
        query += " ORDER BY s.start_time DESC LIMIT ?"
        params.append(limit)
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_session_data(self, session_id):
        """获取特定会话的所有数据"""
        # 获取会话信息
        self.cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        session_info = self.cursor.fetchone()
        
        # 获取帧数据
        self.cursor.execute("SELECT timestamp, data_json FROM frame_data WHERE session_id = ? ORDER BY frame_id", 
                          (session_id,))
        frame_data = []
        for row in self.cursor.fetchall():
            frame_data.append({
                'timestamp': row[0],
                'data': json.loads(row[1])
            })
        
        # 获取评估结果
        self.cursor.execute("SELECT * FROM evaluations WHERE session_id = ?", (session_id,))
        evaluation = self.cursor.fetchone()
        
        return {
            'session_info': session_info,
            'frame_data': frame_data,
            'evaluation': evaluation
        }
    
    def import_from_csv(self, csv_file_path, action_type, view_type, user_id=None):
        """从CSV文件导入数据"""
        import csv
        
        # 开始新会话
        session_id = self.start_session(action_type, view_type, user_id)
        
        # 读取CSV文件并导入数据
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)  # 跳过表头
                
                frames = []
                for row in reader:
                    if not row or len(row) < 2:
                        continue
                    
                    # 解析CSV行数据
                    # 注意：这里需要根据实际CSV格式调整解析逻辑
                    frame_data = {}
                    for i, header in enumerate(headers[1:]):  # 跳过timestamp列
                        if i + 1 < len(row):
                            try:
                                value = float(row[i+1])
                                frame_data[header] = value
                            except ValueError:
                                frame_data[header] = row[i+1]
                    
                    frames.append(frame_data)
                
                # 批量导入帧数据
                self.log_batch_frame_data(session_id, frames)
                
                # 标记会话结束
                self.stop_session(session_id)
                
                return session_id
        except Exception as e:
            print(f"导入CSV文件时出错: {e}")
            # 出错时删除会话
            self.cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            self.connection.commit()
            return None
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None