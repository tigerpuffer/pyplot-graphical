#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块 - 管理AI API配置
"""
import json
import os

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path=None):
        if config_path is None:
            # 使用绝对路径，确保配置文件能正确保存
            self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        else:
            self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_config()
        return self._get_default_config()
    
    def _get_default_config(self):
        """获取默认配置"""
        return {
            "ai_provider": "",  # openai / claude / doubao / wenxin / spark / custom
            "openai_api_key": "",
            "openai_model": "gpt-3.5-turbo",
            "claude_api_key": "",
            "claude_model": "claude-3-haiku-20240307",
            "doubao_api_key": "",
            "doubao_secret": "",
            "doubao_model": "doubao-3.0",
            "wenxin_api_key": "",
            "wenxin_secret": "",
            "wenxin_model": "ernie-4.0",
            "spark_app_id": "",
            "spark_api_key": "",
            "spark_secret": "",
            "spark_model": "spark-3.5",
            "custom_api_key": "",
            "custom_api_url": "https://api.example.com/v1/chat/completions",
            "custom_model": "custom-model",
            "theme": "light",
            "auto_save": True,
            "language": "zh-CN",
            "first_run_completed": False,
            "deepseek_api_key": "",
            "deepseek_model": "deepseek-v4-flash"
        }
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return True
        except IOError:
            return False
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置项"""
        self.config[key] = value
    
    def is_ai_configured(self):
        """检查AI是否已配置"""
        provider = self.config.get("ai_provider", "")
        if provider == "openai":
            return bool(self.config.get("openai_api_key", "").strip())
        elif provider == "claude":
            return bool(self.config.get("claude_api_key", "").strip())
        elif provider == "doubao":
            return bool(self.config.get("doubao_api_key", "").strip()) and \
                   bool(self.config.get("doubao_secret", "").strip())
        elif provider == "wenxin":
            return bool(self.config.get("wenxin_api_key", "").strip()) and \
                   bool(self.config.get("wenxin_secret", "").strip())
        elif provider == "spark":
            return bool(self.config.get("spark_app_id", "").strip()) and \
                   bool(self.config.get("spark_api_key", "").strip()) and \
                   bool(self.config.get("spark_secret", "").strip())
        elif provider == "deepseek":
            return bool(self.config.get("deepseek_api_key", "").strip())
        elif provider == "custom":
            return bool(self.config.get("custom_api_key", "").strip()) and \
                   bool(self.config.get("custom_api_url", "").strip())
        return False
    
    def get_ai_provider(self):
        """获取AI提供商"""
        return self.config.get("ai_provider", "")
    
    def get_api_key(self):
        """获取API密钥"""
        provider = self.config.get("ai_provider", "")
        if provider == "openai":
            return self.config.get("openai_api_key", "")
        elif provider == "claude":
            return self.config.get("claude_api_key", "")
        elif provider == "doubao":
            return self.config.get("doubao_api_key", "")
        elif provider == "wenxin":
            return self.config.get("wenxin_api_key", "")
        elif provider == "spark":
            return self.config.get("spark_api_key", "")
        elif provider == "deepseek":
            return self.config.get("deepseek_api_key", "")
        elif provider == "custom":
            return self.config.get("custom_api_key", "")
        return ""
    
    def get_model(self):
        """获取模型名称"""
        provider = self.config.get("ai_provider", "")
        if provider == "openai":
            return self.config.get("openai_model", "gpt-3.5-turbo")
        elif provider == "claude":
            return self.config.get("claude_model", "claude-3-haiku-20240307")
        elif provider == "doubao":
            return self.config.get("doubao_model", "doubao-3.0")
        elif provider == "wenxin":
            return self.config.get("wenxin_model", "ernie-4.0")
        elif provider == "spark":
            return self.config.get("spark_model", "spark-3.5")
        elif provider == "deepseek":
            return self.config.get("deepseek_model", "deepseek-v4-flash")
        elif provider == "custom":
            return self.config.get("custom_model", "custom-model")
        return ""


# 全局配置实例
_config_manager = None

def get_config_manager():
    """获取配置管理器单例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
