#!/usr/bin/env python3
"""
万尺 AI 分身 - 使用DeepSeek R1模型的个人AI助手
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
import requests
from dataclasses import dataclass

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
    
    def save_conversation(self, filename: str = "wanchi_conversation.json"):
        """保存对话历史"""
        data = [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp
            } for msg in self.conversation_history
        ]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_conversation(self, filename: str = "wanchi_conversation.json"):
        """加载对话历史"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.conversation_history = [
                    Message(
                        role=item["role"],
                        content=item["content"],
                        timestamp=item["timestamp"]
                    ) for item in data
                ]
    
    def clear_conversation(self):
        """清空对话历史"""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> str:
        """获取对话摘要"""
        if not self.conversation_history:
            return "暂无对话记录"
        
        total_messages = len(self.conversation_history)
        user_messages = len([msg for msg in self.conversation_history if msg.role == "user"])
        
        return f"总共 {total_messages} 条消息，用户发送了 {user_messages} 条消息"

def main():
    """主函数 - 命令行交互界面"""
    print("万尺AI分身启动中...")
    print("输入 'quit' 退出，输入 'clear' 清空对话历史，输入 'save' 保存对话")
    print("=" * 50)
    
    # 初始化AI助手
    api_key = "sk-dc449b4063f24562985ba5a86eff701c"
    assistant = WanchiAIAssistant(api_key)
    
    # 尝试加载之前的对话历史
    assistant.load_conversation()
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if user_input.lower() == 'quit':
                print("再见！")
                break
            elif user_input.lower() == 'clear':
                assistant.clear_conversation()
                print("对话历史已清空")
                continue
            elif user_input.lower() == 'save':
                assistant.save_conversation()
                print("对话已保存")
                continue
            elif user_input.lower() == 'summary':
                print(assistant.get_conversation_summary())
                continue
            
            if not user_input:
                continue
                
            # 获取AI回复
            print("\n万尺正在思考...")
            response = assistant.get_response(user_input)
            print(f"\n万尺: {response}")
            
        except KeyboardInterrupt:
            print("\n\n程序被中断，正在保存对话...")
            assistant.save_conversation()
            print("对话已保存，再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()