class UserProfile:
    """
    用户信息类，用于收集和管理用户基本信息
    为AI助手提供用户背景数据
    """
    
    def __init__(self):
        self.age = None
        self.gender = None
        self.height = None  # cm
        self.weight = None  # kg
        self.sport_experience = ""
        self.goals = ""
        self.injury_history = ""
        self.training_frequency = None  # times per week
    
    def set_basic_info(self, age, gender, height, weight):
        """
        设置用户基本信息
        
        Args:
            age (int): 年龄
            gender (str): 性别
            height (float): 身高(cm)
            weight (float): 体重(kg)
        """
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
    
    def set_sport_experience(self, experience):
        """
        设置运动经验
        
        Args:
            experience (str): 运动经验描述
        """
        self.sport_experience = experience
    
    def set_goals(self, goals):
        """
        设置训练目标
        
        Args:
            goals (str): 训练目标描述
        """
        self.goals = goals
    
    def set_injury_history(self, history):
        """
        设置伤病史
        
        Args:
            history (str): 伤病史描述
        """
        self.injury_history = history
    
    def set_training_frequency(self, frequency):
        """
        设置训练频率
        
        Args:
            frequency (int): 每周训练次数
        """
        self.training_frequency = frequency
    
    def get_profile(self):
        """
        获取完整的用户信息
        
        Returns:
            dict: 包含所有用户信息的字典
        """
        return {
            "age": self.age,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "sport_experience": self.sport_experience,
            "goals": self.goals,
            "injury_history": self.injury_history,
            "training_frequency": self.training_frequency
        }
    
    def is_complete(self):
        """
        检查用户信息是否完整
        
        Returns:
            bool: 如果基本信息完整返回True，否则返回False
        """
        return all([self.age, self.gender, self.height, self.weight])