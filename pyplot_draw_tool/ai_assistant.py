#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI核心助手模块 - 智能图表生成
支持多种AI服务商，提供自然语言到图表的转换
"""
import json
import re
import pandas as pd
from config_manager import get_config_manager


class AIAssistantCore:
    """AI核心助手类"""

    def __init__(self):
        self.config = get_config_manager()
        self.provider = self.config.get_ai_provider()
        self.api_key = self.config.get_api_key()
        self.model = self.config.get_model()
        self._api_client = None

    def _get_api_client(self):
        """获取API客户端"""
        if self._api_client is None:
            if self.provider == "openai":
                self._api_client = OpenAIClient(self.api_key, self.model)
            elif self.provider == "claude":
                self._api_client = ClaudeClient(self.api_key, self.model)
            elif self.provider == "doubao":
                self._api_client = DoubaoClient(self.api_key, self.config.get("doubao_secret", ""), self.model)
            elif self.provider == "wenxin":
                self._api_client = WenxinClient(self.api_key, self.config.get("wenxin_secret", ""), self.model)
            elif self.provider == "spark":
                self._api_client = SparkClient(
                    self.config.get("spark_app_id", ""),
                    self.api_key,
                    self.config.get("spark_secret", ""),
                    self.model
                )
            elif self.provider == "deepseek":
                self._api_client = DeepSeekClient(self.api_key, self.model)
            elif self.provider == "custom":
                self._api_client = CustomClient(self.api_key, self.config.get("custom_api_url", ""), self.model)
            else:
                raise ValueError(f"不支持的AI提供商: {self.provider}")
        return self._api_client

    def read_excel(self, file_path):
        """读取Excel文件，返回数据摘要"""
        try:
            if file_path.endswith('.xls'):
                try:
                    df = pd.read_excel(file_path, engine='xlrd')
                except ImportError:
                    return {
                        "success": False,
                        "error": "读取.xls格式需要安装xlrd库。\n请在终端运行: pip install xlrd>=2.0.1\n或建议将文件另存为.xlsx格式"
                    }
            elif file_path.endswith('.xlsx'):
                try:
                    df = pd.read_excel(file_path, engine='openpyxl')
                except ImportError:
                    return {
                        "success": False,
                        "error": "读取.xlsx格式需要安装openpyxl库。\n请在终端运行: pip install openpyxl"
                    }
            else:
                df = pd.read_excel(file_path)

            return {
                "success": True,
                "data": df,
                "columns": list(df.columns),
                "shape": df.shape,
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "head": df.head(10).to_dict(orient='records')
            }
        except Exception as e:
            return {"success": False, "error": f"读取Excel失败: {str(e)}"}

    def generate_chart_params(self, user_request, excel_data=None):
        """根据用户描述生成图表参数"""
        excel_summary = self._prepare_excel_summary(excel_data) if excel_data else ""

        prompt = f"""你是一个Matplotlib图表配置助手。根据用户的需求，生成图表配置参数。

{excel_summary}

用户需求: {user_request}

请以JSON格式返回图表配置参数，格式如下：
{{
    "chart_type": "折线图|柱状图|散点图|直方图|饼图|雷达图",
    "title": "图表标题",
    "xlabel": "X轴标签",
    "ylabel": "Y轴标签",
    "data_description": "数据来源和结构描述",
    "x_data_sample": ["类别1", "类别2", "类别3"],
    "y_data_labels": ["数据系列1", "数据系列2"],
    "grid": true,
    "legend": true
}}

只返回JSON，不要有其他内容。"""

        try:
            response = self._get_api_client().chat(prompt)
            return self._parse_json_response(response)
        except Exception as e:
            return {"success": False, "error": str(e), "raw_response": response if 'response' in dir() else None}

    def generate_matplotlib_code(self, user_request, excel_data=None, chart_params=None):
        """生成完整的Matplotlib代码"""
        excel_summary = self._prepare_excel_summary(excel_data) if excel_data else ""
        params_json = json.dumps(chart_params, ensure_ascii=False) if chart_params else ""

        prompt = f"""你是一个Matplotlib代码生成专家。根据用户需求生成完整的、可运行的Python代码。

{excel_summary}

用户需求: {user_request}

图表参数: {params_json}

要求:
1. 生成完整可运行的Python代码，包含import语句
2. 使用matplotlib.pyplot和numpy
3. 如果有Excel数据，直接将数据硬编码到代码中作为变量，不要使用pd.read_excel()读取外部文件
4. 代码应该可以直接运行生成图表
5. 中文使用SimHei字体
6. 添加适当的注释说明代码功能

请只返回代码，不要有其他内容。代码用```python包裹。"""

        try:
            response = self._get_api_client().chat(prompt)
            code = self._extract_code_block(response)
            return {"success": True, "code": code}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _prepare_excel_summary(self, excel_data):
        """准备Excel数据摘要"""
        if not excel_data:
            return ""

        summary = ["\n\n【Excel数据信息】"]
        summary.append(f"数据形状: {excel_data.get('shape', (0, 0))[0]} 行 × {excel_data.get('shape', (0, 0))[1]} 列")

        columns = excel_data.get('columns', [])
        columns_str = [str(col) for col in columns]
        summary.append(f"列名: {', '.join(columns_str)}")

        summary.append("\n前10行数据示例:")
        for i, row in enumerate(excel_data.get('head', [])):
            summary.append(f"  行{i+1}: {row}")
        summary.append("\n数据类型:")
        for col, dtype in excel_data.get('dtypes', {}).items():
            summary.append(f"  {col}: {dtype}")

        return "\n".join(summary)

    def _parse_json_response(self, response):
        """解析JSON响应"""
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                data["success"] = True
                return data
            return {"success": False, "error": "无法解析JSON响应", "raw_response": response}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"JSON解析失败: {str(e)}", "raw_response": response}

    def _extract_code_block(self, response):
        """提取代码块"""
        code_match = re.search(r'```python\n(.*?)```', response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        return response.strip()


class OpenAIClient:
    """OpenAI API客户端"""

    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def chat(self, message):
        import urllib.request
        import urllib.error

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7
        }

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"OpenAI API错误 ({e.code}): {error_body}")
        except Exception as e:
            raise Exception(f"请求失败: {str(e)}")


class ClaudeClient:
    """Claude API客户端"""

    def __init__(self, api_key, model="claude-3-haiku-20240307"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.anthropic.com/v1/messages"

    def chat(self, message):
        import urllib.request
        import urllib.error

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "anthropic-dangerous-direct-browser-access": "true"
        }

        data = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": message}]
        }

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['content'][0]['text']
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"Claude API错误 ({e.code}): {error_body}")
        except Exception as e:
            raise Exception(f"请求失败: {str(e)}")


class DoubaoClient:
    """豆包API客户端"""

    def __init__(self, api_key, secret, model="doubao-3.0"):
        self.api_key = api_key
        self.secret = secret
        self.model = model

    def chat(self, message):
        raise Exception("豆包API需要OAuth2认证，请使用其他AI提供商或手动实现认证流程")


class WenxinClient:
    """文心一言API客户端"""

    def __init__(self, api_key, secret, model="ernie-4.0"):
        self.api_key = api_key
        self.secret = secret
        self.model = model
        self._access_token = None

    def _get_access_token(self):
        """获取Access Token"""
        import urllib.request
        import urllib.parse

        if self._access_token:
            return self._access_token

        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret
        }

        req = urllib.request.Request(
            f"{token_url}?{urllib.parse.urlencode(params)}"
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                self._access_token = result.get('access_token')
                return self._access_token
        except Exception as e:
            raise Exception(f"获取百度Access Token失败: {str(e)}")

    def chat(self, message):
        import urllib.request
        import urllib.parse

        access_token = self._get_access_token()
        api_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}]
        }

        req = urllib.request.Request(
            api_url,
            data=json.dumps(data).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                if 'error_code' in result:
                    raise Exception(f"文心一言API错误: {result.get('error_msg', '未知错误')}")
                return result['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            raise Exception(f"文心一言API错误 ({e.code}): {e.read().decode('utf-8')}")
        except Exception as e:
            raise Exception(f"请求失败: {str(e)}")


class SparkClient:
    """讯飞星火API客户端"""

    def __init__(self, app_id, api_key, secret, model="spark-3.5"):
        self.app_id = app_id
        self.api_key = api_key
        self.secret = secret
        self.model = model

    def chat(self, message):
        raise Exception("讯飞星火API需要WebSocket连接，请使用其他AI提供商或手动实现")


class DeepSeekClient:
    """DeepSeek API客户端（兼容OpenAI格式）"""

    def __init__(self, api_key, model="deepseek-v4-flash"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

    def chat(self, message):
        import urllib.request
        import urllib.error

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7
        }

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            raise Exception(f"DeepSeek API错误 ({e.code}): {e.read().decode('utf-8')}")
        except Exception as e:
            raise Exception(f"请求失败: {str(e)}")


class CustomClient:
    """自定义API客户端（兼容OpenAI格式）"""

    def __init__(self, api_key, api_url, model="custom-model"):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model

    def chat(self, message):
        import urllib.request
        import urllib.error

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7
        }

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            raise Exception(f"API错误 ({e.code}): {e.read().decode('utf-8')}")
        except Exception as e:
            raise Exception(f"请求失败: {str(e)}")


def get_ai_assistant():
    """获取AI助手实例"""
    return AIAssistantCore()