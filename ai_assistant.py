import requests
import json
import os
from typing import List, Dict, Any


class AIFitnessAssistant:
    """
    AI助手类，负责与DeepSeek API通信，构建提示词并解析响应
    生成个性化训练方案
    """
    
    def __init__(self, api_key: str = None, model: str = "deepseek-reasoner"):
        """
        初始化AI助手
        
        Args:
            api_key (str, optional): DeepSeek API密钥
            model (str): 使用的模型，默认为deepseek-reasoner
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.model = model
        self.base_url = "https://api.deepseek.com/v1"
        
        # 检查API密钥
        if not self.api_key:
            raise ValueError("未提供DeepSeek API密钥，请设置DEEPSEEK_API_KEY环境变量或在初始化时传入api_key参数")
    
    def _build_prompt(self, user_profile: Dict[str, Any], assessment_results: List[Dict]) -> str:
        """
        构建发送给AI的提示词
        
        Args:
            user_profile (dict): 用户信息
            assessment_results (list): FMS评估结果列表
            
        Returns:
            str: 构建的提示词
        """
        prompt = f"""
你是一个专业的运动康复和体能训练专家。根据以下用户信息和FMS功能性动作筛查结果，为用户生成一份详细的个性化训练方案。

用户基本信息：
- 年龄：{user_profile.get('age', '未提供')}岁
- 性别：{user_profile.get('gender', '未提供')}
- 身高：{user_profile.get('height', '未提供')}cm
- 体重：{user_profile.get('weight', '未提供')}kg
- 运动经验：{user_profile.get('sport_experience', '未提供')}
- 训练目标：{user_profile.get('goals', '未提供')}
- 伤病史：{user_profile.get('injury_history', '未提供')}
- 训练频率：每周{user_profile.get('training_frequency', '未提供')}次

FMS评估结果：
"""
        
        for result in assessment_results:
            prompt += f"""
动作名称：{result.get('movement_name', '未知')}
评分：{result.get('score', '未评分')}
反馈：{', '.join(result.get('feedback', []))}
关键角度数据：{json.dumps(result.get('angles', {}), ensure_ascii=False)}
"""
        
        prompt += """
请根据以上信息，生成一份详细的个性化训练方案，必须包含以下内容：

1. 总体评估总结
   - 用户整体动作质量分析
   - 主要功能性限制
   - 潜在受伤风险

2. 个性化训练建议
   - 针对低分动作(评分≤2分)的具体改善练习
   - 推荐训练频率和强度
   - 注意事项和进阶路径

3. 短期目标(2-4周)
   - 可量化的目标
   - 预期改进幅度

4. 长期目标(2-3个月)
   - 可达成的整体改善目标
   - 功能性提升预期

要求：
- 使用专业但易懂的语言
- 针对用户具体情况给出具体建议
- 练习描述要详细，便于用户理解执行
- 考虑用户的伤病史，避免相关风险动作
- 方案应安全、有效、可执行
- 以中文输出结果

请直接输出训练方案内容，不要包含其他说明或解释。
"""
        
        return prompt
    
    def _send_request(self, prompt: str) -> str:
        """
        发送请求到DeepSeek API
        
        Args:
            prompt (str): 发送给AI的提示词
            
        Returns:
            str: AI返回的响应内容
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个专业的运动康复和体能训练专家。"},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API请求失败: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求错误: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"响应解析错误: {str(e)}")
        except KeyError as e:
            raise Exception(f"响应格式错误: {str(e)}")
    
    def generate_personalized_plan(self, user_profile: Dict[str, Any], 
                                 assessment_results: List[Dict]) -> str:
        """
        生成个性化训练方案
        
        Args:
            user_profile (dict): 用户信息
            assessment_results (list): FMS评估结果列表
            
        Returns:
            str: 个性化训练方案
        """
        # 构建提示词
        prompt = self._build_prompt(user_profile, assessment_results)
        
        # 发送请求并获取响应
        try:
            plan = self._send_request(prompt)
            return plan
        except Exception as e:
            return f"生成训练方案时出错: {str(e)}"
    
    def set_api_key(self, api_key: str):
        """
        设置API密钥
        
        Args:
            api_key (str): DeepSeek API密钥
        """
        self.api_key = api_key