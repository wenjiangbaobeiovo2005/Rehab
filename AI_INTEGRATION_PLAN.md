# AIFMS 2.0 AI集成方案

## 概述

本文档描述了如何将DeepSeek AI API集成到AIFMS 2.0系统中，以根据FMS评估结果为用户生成个性化训练方案。

## 系统架构

### 新增模块

1. **AI助手模块** (`ai_assistant.py`)
   - 负责与DeepSeek API通信
   - 构建提示词并解析响应
   - 生成个性化训练方案

2. **用户信息模块** (`user_profile.py`)
   - 收集和管理用户基本信息
   - 为AI助手提供用户背景数据

## 功能实现

### 1. 数据收集流程

1. 用户基本信息收集
   - 年龄、性别、身高、体重
   - 运动经验
   - 训练目标
   - 伤病史
   - 训练频率

2. FMS动作评估
   - 完成所有7个FMS动作的评估
   - 记录每个动作的评分和反馈
   - 收集关键角度数据

### 2. AI方案生成

1. 数据整合
   - 将用户信息和FMS评估结果组合
   - 构建发送给AI的提示词

2. 调用DeepSeek API
   - 使用`requests`库发送HTTP请求
   - 处理API响应

3. 结果处理
   - 解析AI生成的个性化方案
   - 格式化输出结果

### 3. 方案内容

AI生成的个性化方案应包括：

1. 总体评估总结
   - 用户整体动作质量
   - 主要功能性限制
   - 潜在受伤风险

2. 个性化训练建议
   - 针对低分动作的具体改善练习
   - 推荐训练频率和强度
   - 注意事项和进阶路径

3. 短期目标(2-4周)
   - 可量化的目标
   - 预期改进幅度

4. 长期目标(2-3个月)
   - 可达成的整体改善目标
   - 功能性提升预期

## 模型选择

### DeepSeek-Chat
- 适用于一般性的对话和简单推理任务
- 响应速度快
- 适合基础的训练方案生成

### DeepSeek-Reasoner
- 专为复杂推理任务设计
- 具有更强的逻辑分析和问题解决能力
- 适合生成更深入、更个性化的训练方案
- 响应时间可能较长，但质量更高

## 使用方法

### 1. 环境配置

1. 安装依赖包:
   ```
   pip install -r requirements.txt
   ```

2. 设置DeepSeek API密钥:
   ```bash
   # Windows
   set DEEPSEEK_API_KEY=your_api_key_here
   
   # Linux/Mac
   export DEEPSEEK_API_KEY=your_api_key_here
   ```

### 2. 代码集成

1. 导入模块:
   ```python
   from ai_assistant import AIFitnessAssistant
   from user_profile import UserProfile
   ```

2. 创建用户信息:
   ```python
   user = UserProfile()
   user.set_basic_info(28, "男", 175, 70)
   user.set_sport_experience("3年健身经验")
   user.set_goals("改善动作质量")
   ```

3. 收集FMS评估结果:
   ```python
   assessment_results = [
       {
           "movement_name": "深蹲",
           "score": 2,
           "feedback": ["膝外翻", "躯干前倾"],
           "angles": {"left_knee_angle": 75, "right_knee_angle": 65}
       }
       # ... 其他动作评估结果
   ]
   ```

4. 生成个性化方案:
   ```python
   # 使用默认的deepseek-reasoner模型
   assistant = AIFitnessAssistant()
   
   # 或指定使用其他模型
   assistant = AIFitnessAssistant(model="deepseek-chat")
   
   plan = assistant.generate_personalized_plan(
       user.get_profile(), 
       assessment_results
   )
   ```

## GUI集成建议

为了在图形界面中集成AI功能，建议添加以下组件：

1. **用户信息输入界面**
   - 表单用于收集用户基本信息
   - 文本框用于输入运动经验和目标

2. **评估结果展示界面**
   - 显示所有FMS动作的评分和反馈
   - 可视化关键角度数据

3. **AI方案展示界面**
   - 显示AI生成的个性化训练方案
   - 支持方案导出为PDF或文本文件

4. **方案导出功能**
   - 保存个性化方案到本地文件
   - 支持多种格式(PDF, TXT, JSON)

## 安全和隐私考虑

1. **API密钥安全**
   - 不在代码中硬编码API密钥
   - 使用环境变量存储密钥
   - 提供密钥输入界面作为备选方案

2. **用户数据保护**
   - 明确告知用户数据使用方式
   - 不存储用户敏感信息
   - 提供数据删除选项

## 错误处理

1. **网络连接问题**
   - 提供重试机制
   - 显示友好的错误信息

2. **API调用失败**
   - 处理超时和API错误响应
   - 提供备用方案或建议

3. **数据格式错误**
   - 验证输入数据格式
   - 提供数据修正建议

## 测试脚本

提供了专门的测试脚本 [test_deepseek_reasoner.py](file://c:\Users\23849\Desktop\深蹲\test_deepseek_reasoner.py) 用于验证与DeepSeek Reasoner模型的集成：

```bash
python test_deepseek_reasoner.py
```

## 未来扩展

1. **多语言支持**
   - 支持生成不同语言的训练方案

2. **方案跟踪功能**
   - 记录用户训练进度
   - 根据进展调整方案

3. **社区分享功能**
   - 允许用户分享成功案例
   - 提供方案模板库

## 结论

通过集成DeepSeek AI API，特别是使用deepseek-reasoner模型，AIFMS 2.0系统可以为用户提供更加个性化和专业的训练建议，显著提升系统的实用价值和用户体验。该集成方案考虑了数据安全、用户隐私和系统可扩展性，为未来功能扩展奠定了良好基础。