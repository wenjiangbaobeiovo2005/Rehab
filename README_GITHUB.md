# 如何在GitHub上构建Android APK

## 步骤1：Fork项目到您的GitHub账户

1. 访问 [原项目地址](https://github.com/wenjiangbaobeiovo2005/Rehab)
2. 点击右上角的"Fork"按钮
3. 选择您的GitHub账户作为目标

## 步骤2：配置GitHub个人访问令牌(PAT)

1. 登录您的GitHub账户
2. 进入 Settings > Developer settings > Personal access tokens > Tokens (classic)
3. 点击"Generate new token" > "Generate new token (classic)"
4. 给令牌起个名字，比如"RehabGPT-Android"
5. 选择适当的权限，至少需要`repo`权限
6. 点击"Generate token"
7. 复制生成的令牌并保存到安全的地方

## 步骤3：推送代码到您的fork仓库

如果您还没有克隆项目到本地：

```bash
git clone https://github.com/wenjiangbaobeiovo2005/Rehab.git
cd Rehab
```

添加您的fork作为远程仓库：

```bash
git remote add fork https://github.com/YOUR_USERNAME/Rehab.git
```

将代码推送到您的fork：

```bash
git push fork main
```

如果遇到身份验证问题，请使用您的PAT作为密码：

```bash
git push https://YOUR_USERNAME:YOUR_PAT@github.com/YOUR_USERNAME/Rehab.git main
```

## 步骤4：触发GitHub Actions构建

1. 访问您的fork仓库页面
2. 点击"Actions"选项卡
3. 您应该能看到"Build Android APK"工作流
4. 推送代码后，构建应该会自动开始
5. 等待构建完成（大约需要20-40分钟）

## 步骤5：下载APK

1. 构建完成后，在Actions页面点击最后一次运行
2. 在"Artifacts"部分，您应该能看到"RehabGPT-APK"
3. 点击下载并解压获取APK文件

## 故障排除

如果构建失败：

1. 检查日志中的错误信息
2. 确保buildozer.spec文件配置正确
3. 确保所有依赖项都正确列出
4. 查看"build-logs"工件获取详细日志信息