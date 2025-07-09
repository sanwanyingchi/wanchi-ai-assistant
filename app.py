#!/usr/bin/env python3
"""
万尺 AI 分身 Web 界面
"""

from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import uuid
import os
import json
from datetime import datetime
import requests
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Message:
    role: str
    content: str
    timestamp: str

class WanchiAIAssistant:
    def __init__(self, api_key: str):
        """初始化万尺AI分身"""
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.conversation_history: List[Message] = []
        self.personality_prompt = self._build_personality_prompt()
        
    def _build_personality_prompt(self) -> str:
        """构建万尺的个性化提示词"""
        return """你是万尺，一个真实的人。请以万尺的身份和口吻回答所有问题。

关于万尺的特点：
- 说话风格自然、亲切，像朋友一样交流
- 回答问题时会结合个人经验和见解
- 对技术和编程有深入了解
- 喜欢分享知识，但不会过于正式或教条
- 会用"我"来称呼自己，就像真正的万尺在说话
- 回答问题时会考虑上下文和对话历史

请始终保持万尺的角色，以第一人称回答问题，就像万尺本人在与用户对话一样。"""

    def add_message(self, role: str, content: str):
        """添加消息到对话历史"""
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat()
        )
        self.conversation_history.append(message)
        
    def get_response(self, user_input: str) -> str:
        """获取AI回复"""
        # 添加用户消息
        self.add_message("user", user_input)
        
        # 构建完整的消息历史
        messages = [{"role": "system", "content": self.personality_prompt}]
        
        # 添加对话历史（最近20轮对话）
        recent_history = self.conversation_history[-20:]
        for msg in recent_history:
            if msg.role in ["user", "assistant"]:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-r1",
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7,
                "stream": False
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                self.add_message("assistant", ai_response)
                return ai_response
            else:
                error_msg = f"API请求失败，状态码: {response.status_code}"
                self.add_message("assistant", error_msg)
                return error_msg
                
        except Exception as e:
            error_msg = f"抱歉，我暂时无法回答你的问题。错误：{str(e)}"
            self.add_message("assistant", error_msg)
            return error_msg
    
    def clear_conversation(self):
        """清空对话历史"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """获取对话历史"""
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp
            } for msg in self.conversation_history
        ]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# 全局变量存储AI助手实例
assistants = {}

def get_assistant(session_id: str) -> WanchiAIAssistant:
    """获取或创建AI助手实例"""
    if session_id not in assistants:
        api_key = "sk-dc449b4063f24562985ba5a86eff701c"
        assistants[session_id] = WanchiAIAssistant(api_key)
    return assistants[session_id]

@app.route('/')
def index():
    """主页面"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400
        
        session_id = session.get('session_id')
        assistant = get_assistant(session_id)
        
        # 获取AI回复
        response = assistant.get_response(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    """获取对话历史"""
    session_id = session.get('session_id')
    assistant = get_assistant(session_id)
    
    return jsonify({
        'history': assistant.get_conversation_history()
    })

@app.route('/clear', methods=['POST'])
def clear():
    """清空对话历史"""
    session_id = session.get('session_id')
    assistant = get_assistant(session_id)
    assistant.clear_conversation()
    
    return jsonify({'message': '对话历史已清空'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)