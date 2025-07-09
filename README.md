# 万尺 AI 分身

一个基于 DeepSeek R1 模型的个人AI助手，支持多轮对话，能够模拟万尺的说话风格和个性。

## 功能特点

- 🤖 **DeepSeek R1 模型** - 使用先进的AI模型提供智能回复
- 💬 **多轮对话** - 支持连续对话，保持上下文记忆
- 🎭 **个性化回复** - 以万尺的口吻和风格回答问题
- 🌐 **Web 界面** - 类似GPT的现代化聊天界面
- 📱 **响应式设计** - 支持桌面和移动设备
- 💾 **对话管理** - 支持清空对话历史和会话保存

## 项目结构

```
wanchi-ai-assistant/
├── app.py                    # Flask Web应用主程序
├── wanchi_ai_assistant.py    # 命令行版本
├── requirements.txt          # Python依赖包
├── templates/
│   └── index.html           # Web界面模板
├── .gitignore               # Git忽略文件
└── README.md               # 项目说明
```

## 安装和使用

### 1. 环境要求

- Python 3.7+
- DeepSeek API 密钥

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行方式

#### Web界面版本（推荐）

```bash
python3 app.py
```

然后打开浏览器访问 `http://localhost:5000`

#### 命令行版本

```bash
python3 wanchi_ai_assistant.py
```

## 使用说明

### Web界面

1. 启动应用后，打开浏览器访问 `http://localhost:5000`
2. 在输入框中输入您的问题
3. 按回车键或点击发送按钮
4. 万尺AI分身会以自然的口吻回复您
5. 支持连续对话，AI会记住之前的对话内容
6. 点击"清空"按钮可以清除对话历史

### 命令行界面

- 输入 `quit` 退出程序
- 输入 `clear` 清空对话历史
- 输入 `save` 保存当前对话
- 输入 `summary` 查看对话摘要

## 配置

### API密钥配置

项目中已经包含了API密钥，如需更换请修改以下文件：

- `app.py` 中的 `api_key` 变量
- `wanchi_ai_assistant.py` 中的 `api_key` 变量

### 个性化设置

您可以在 `_build_personality_prompt()` 方法中修改AI的个性设置，调整说话风格和特点。

## 技术特点

- **Flask** - 轻量级Web框架
- **DeepSeek R1** - 先进的AI语言模型
- **会话管理** - 支持多用户同时使用
- **响应式UI** - 现代化的聊天界面
- **实时交互** - 支持打字指示器和流畅的用户体验

## 界面预览

- 💬 类似GPT的对话界面
- 📱 支持移动设备
- 🎨 现代化的UI设计
- ⚡ 流畅的交互体验

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系

如有问题或建议，请联系万尺。

---

🤖 **万尺AI分身** - 让AI更有人情味！