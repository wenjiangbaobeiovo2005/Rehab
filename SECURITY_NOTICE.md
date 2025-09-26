# 安全说明

## API密钥安全警告

**重要提醒：请妥善保管您的API密钥！**

您已经将DeepSeek API密钥添加到项目中的[.env](file://c:\Users\23849\Desktop\深蹲\.env)文件。为了保护您的账户安全，请注意以下事项：

### 安全风险

1. **不要将[.env](file://c:\Users\23849\Desktop\深蹲\.env)文件提交到代码仓库**
   - [.gitignore](file://c:\Users\23849\Desktop\深蹲\.gitignore)文件应该包含`.env`条目，防止其被意外提交

2. **不要在代码中硬编码API密钥**
   - 我们已经通过环境变量和配置文件的方式安全地管理密钥

3. **不要分享包含API密钥的文件**
   - 如果您需要分享项目，请删除或清空[.env](file://c:\Users\23849\Desktop\深蹲\.env)文件中的敏感信息

### 最佳实践

1. **使用环境变量**
   ```bash
   # Windows
   set DEEPSEEK_API_KEY=your_api_key_here
   
   # Linux/Mac
   export DEEPSEEK_API_KEY=your_api_key_here
   ```

2. **使用配置文件**
   - 项目中的[.env](file://c:\Users\23849\Desktop\深蹲\.env)文件
   - 确保该文件不在版本控制系统中

3. **定期更换API密钥**
   - 定期在DeepSeek平台生成新的API密钥
   - 及时更新项目中的密钥配置

### 项目安全特性

本项目采用了以下安全措施来保护您的API密钥：

1. **多层密钥加载机制**
   - 优先从环境变量加载
   - 备选从本地[.env](file://c:\Users\23849\Desktop\深蹲\.env)文件加载
   - 避免在代码中硬编码密钥

2. **密钥管理模块**
   - [api_key_manager.py](file://c:\Users\23849\Desktop\深蹲\squat-evaluation-system\api_key_manager.py)提供了统一的密钥管理接口
   - 支持多种密钥加载方式

3. **错误处理**
   - 当未找到API密钥时给出明确提示
   - 不会在错误信息中暴露密钥内容

### 如果您怀疑密钥泄露

1. 立即前往DeepSeek平台重新生成API密钥
2. 更新项目中的[.env](file://c:\Users\23849\Desktop\深蹲\.env)文件
3. 检查是否有包含密钥的文件被不当分享

### 更多信息

- [DeepSeek API文档](https://api-docs.deepseek.com/)
- [API密钥管理最佳实践](https://help.deepseek.com/)