#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置对话框模块 - AI API配置向导
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
from config_manager import get_config_manager


class SettingsDialog:
    """设置对话框"""
    
    def __init__(self, parent):
        self.parent = parent
        self.config = get_config_manager()
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("设置")
        self.dialog.geometry("750x700")
        self.dialog.resizable(False, False)
        
        # 居中显示
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._load_current_settings()
    
    def _create_widgets(self):
        """创建对话框部件"""
        # 创建notebook用于选项卡
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ===== AI设置选项卡 =====
        self.ai_frame = ttk.Frame(notebook)
        notebook.add(self.ai_frame, text="  AI API设置  ")
        
        # 配置ai_frame的网格布局
        self.ai_frame.columnconfigure(0, weight=1)
        self.ai_frame.rowconfigure(0, weight=1)
        
        self._create_ai_settings_tab()
        
        # ===== 使用指南选项卡 =====
        guide_frame = ttk.Frame(notebook)
        notebook.add(guide_frame, text="  使用指南  ")
        
        self._create_guide_tab(guide_frame)
    
    def _create_ai_settings_tab(self):
        """创建AI设置选项卡"""
        # 为整个选项卡创建滚动区域
        main_scroll_frame = tk.Frame(self.ai_frame)
        main_scroll_frame.pack(fill='both', expand=True, padx=10, pady=(10, 0))
        
        # 底部按钮区域（在滚动区域外部）
        btn_frame = tk.Frame(self.ai_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        save_btn = tk.Button(btn_frame, text="保存", width=10, 
                  command=self._save_settings, bg='#4CAF50', fg='white', font=('微软雅黑', 10, 'bold'))
        save_btn.pack(side='right', padx=10)
        tk.Button(btn_frame, text="取消", width=10, 
                  command=self.dialog.destroy).pack(side='right', padx=10)
        
        main_canvas = tk.Canvas(main_scroll_frame, height=550)
        main_canvas.pack(side='left', fill='both', expand=True)
        
        main_scrollbar = ttk.Scrollbar(main_scroll_frame, orient='vertical', command=main_canvas.yview)
        main_scrollbar.pack(side='right', fill='y')
        
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox('all')))
        
        self.inner_content_frame = tk.Frame(main_canvas)
        main_canvas.create_window((0, 0), window=self.inner_content_frame, anchor='nw')
        
        # 说明文本
        intro_label = tk.Label(self.inner_content_frame, text="配置AI API以启用AI助手功能", 
                               font=('微软雅黑', 12, 'bold'))
        intro_label.pack(pady=10)
        
        # 选择AI服务商
        provider_frame = tk.LabelFrame(self.inner_content_frame, text="选择AI服务商", font=('微软雅黑', 10))
        provider_frame.pack(fill='x', padx=20, pady=10)
        
        self.provider_var = tk.StringVar(value="openai")
        
        # 使用Frame和Canvas实现滚动
        scroll_frame = tk.Frame(provider_frame)
        scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(scroll_frame, height=250)
        canvas.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(scroll_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        self.provider_inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.provider_inner_frame, anchor='nw')
        
        # OpenAI选项
        self._create_provider_option("openai", "OpenAI (GPT系列)", 
                                    "GPT系列模型，能力强，广泛使用\n• GPT-3.5-turbo：免费额度，便宜快速\n• GPT-4o：最新模型，效果最好")
        
        # Claude选项
        self._create_provider_option("claude", "Anthropic Claude", 
                                    "Claude系列模型，长文本处理好\n• Claude 3 Haiku：快速，便宜\n• Claude 3 Opus：最强模型")
        
        # 豆包选项
        self._create_provider_option("doubao", "🤖 豆包 (国产)", 
                                    "字节跳动出品，国内访问快\n• Doubao 3.0：最新模型\n• 支持中文对话效果好")
        
        # 文心一言选项
        self._create_provider_option("wenxin", "🔷 文心一言 (国产)", 
                                    "百度出品，中文理解强\n• ERNIE 4.0：最新模型\n• 适合中文场景")
        
        # 星火认知选项
        self._create_provider_option("spark", "🔥 讯飞星火 (国产)", 
                                    "科大讯飞出品，语音能力强\n• Spark 3.5：最新模型\n• 多模态能力强")
        
        # DeepSeek选项
        self._create_provider_option("deepseek", "🔮 DeepSeek", 
                                    "深度求索，代码能力强\n• DeepSeek-R1：最新模型\n• 代码生成能力出色")
        
        # 通用API选项
        self._create_provider_option("custom", "⚙️ 通用API (自定义)", 
                                    "支持任何兼容OpenAI格式的API\n• 如：本地模型、企业内部部署\n• 需要手动配置API地址")
        
        # 模型选择
        self.model_frame = tk.LabelFrame(self.inner_content_frame, text="选择模型", font=('微软雅黑', 10))
        self.model_frame.pack(fill='x', padx=20, pady=10)
        
        self._create_model_combos()
        
        # API密钥输入区
        self.api_key_frame = tk.LabelFrame(self.inner_content_frame, text="API配置", font=('微软雅黑', 10))
        self.api_key_frame.pack(fill='x', padx=20, pady=10)
        
        # 动态显示不同服务商的配置项
        self._create_api_config_fields()
        
        # 获取API密钥按钮
        btn_get_key = tk.Button(self.inner_content_frame, text="如何获取API密钥?", 
                                command=self._show_api_key_guide, cursor='hand2')
        btn_get_key.pack(pady=10)
        
        # 测试连接按钮
        btn_test = tk.Button(self.inner_content_frame, text="测试连接", 
                             command=self._test_connection)
        btn_test.pack(pady=10)
    
    def _create_provider_option(self, value, label, description):
        """创建服务商选项"""
        frame = tk.LabelFrame(self.provider_inner_frame, text=label, 
                              font=('微软雅黑', 9), padx=10, pady=10)
        frame.pack(fill='x', pady=5)
        
        rb = tk.Radiobutton(frame, text="", variable=self.provider_var, 
                            value=value, command=self._on_provider_change)
        rb.pack(side='left')
        
        desc_label = tk.Label(frame, text=description, font=('微软雅黑', 8), 
                              justify='left', wraplength=550)
        desc_label.pack(side='left', fill='x', expand=True)
    
    def _create_api_config_fields(self):
        """创建API配置字段"""
        self.api_fields = {}
        self.api_labels = {}  # 用于保存标签引用
        
        # OpenAI API Key
        row = 0
        self.api_labels['openai_label'] = tk.Label(self.api_key_frame, text="API Key:", font=('微软雅黑', 9))
        self.api_labels['openai_label'].grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.api_fields['openai_key'] = tk.Entry(self.api_key_frame, width=50, show='*')
        self.api_fields['openai_key'].grid(row=row, column=1, padx=10, pady=5)
        
        # Claude API Key
        row += 1
        self.api_labels['claude_label'] = tk.Label(self.api_key_frame, text="Claude Key:", font=('微软雅黑', 9))
        self.api_labels['claude_label'].grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.api_fields['claude_key'] = tk.Entry(self.api_key_frame, width=50, show='*')
        self.api_fields['claude_key'].grid(row=row, column=1, padx=10, pady=5)
        
        # 豆包 API Key 和 Secret
        row += 1
        self.api_labels['doubao_key_label'] = tk.Label(self.api_key_frame, text="豆包 API Key:", font=('微软雅黑', 9))
        self.api_labels['doubao_key_label'].grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.api_fields['doubao_key'] = tk.Entry(self.api_key_frame, width=30, show='*')
        self.api_fields['doubao_key'].grid(row=row, column=1, padx=10, pady=5)
        
        self.api_labels['doubao_secret_label'] = tk.Label(self.api_key_frame, text="豆包 Secret:", font=('微软雅黑', 9))
        self.api_labels['doubao_secret_label'].grid(row=row, column=2, sticky='w', padx=10, pady=5)
        self.api_fields['doubao_secret'] = tk.Entry(self.api_key_frame, width=30, show='*')
        self.api_fields['doubao_secret'].grid(row=row, column=3, padx=10, pady=5)
        
        # 文心一言 API Key 和 Secret
        row += 1
        self.api_labels['wenxin_key_label'] = tk.Label(self.api_key_frame, text="文心一言 API Key:", font=('微软雅黑', 9))
        self.api_labels['wenxin_key_label'].grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.api_fields['wenxin_key'] = tk.Entry(self.api_key_frame, width=30, show='*')
        self.api_fields['wenxin_key'].grid(row=row, column=1, padx=10, pady=5)
        
        self.api_labels['wenxin_secret_label'] = tk.Label(self.api_key_frame, text="文心一言 Secret:", font=('微软雅黑', 9))
        self.api_labels['wenxin_secret_label'].grid(row=row, column=2, sticky='w', padx=10, pady=5)
        self.api_fields['wenxin_secret'] = tk.Entry(self.api_key_frame, width=30, show='*')
        self.api_fields['wenxin_secret'].grid(row=row, column=3, padx=10, pady=5)
        
        # 讯飞星火 App ID、API Key 和 Secret
        row += 1
        self.api_labels['spark_appid_label'] = tk.Label(self.api_key_frame, text="星火 App ID:", font=('微软雅黑', 9))
        self.api_labels['spark_appid_label'].grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.api_fields['spark_appid'] = tk.Entry(self.api_key_frame, width=20)
        self.api_fields['spark_appid'].grid(row=row, column=1, padx=10, pady=5)
        
        self.api_labels['spark_key_label'] = tk.Label(self.api_key_frame, text="星火 API Key:", font=('微软雅黑', 9))
        self.api_labels['spark_key_label'].grid(row=row, column=2, sticky='w', padx=10, pady=5)
        self.api_fields['spark_key'] = tk.Entry(self.api_key_frame, width=20, show='*')
        self.api_fields['spark_key'].grid(row=row, column=3, padx=10, pady=5)
        
        self.api_labels['spark_secret_label'] = tk.Label(self.api_key_frame, text="星火 Secret:", font=('微软雅黑', 9))
        self.api_labels['spark_secret_label'].grid(row=row, column=4, sticky='w', padx=10, pady=5)
        self.api_fields['spark_secret'] = tk.Entry(self.api_key_frame, width=20, show='*')
        self.api_fields['spark_secret'].grid(row=row, column=5, padx=10, pady=5)
        
        # DeepSeek API Key
        row += 1
        self.api_labels['deepseek_label'] = tk.Label(self.api_key_frame, text="DeepSeek Key:", font=('微软雅黑', 9))
        self.api_labels['deepseek_label'].grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.api_fields['deepseek_key'] = tk.Entry(self.api_key_frame, width=50, show='*')
        self.api_fields['deepseek_key'].grid(row=row, column=1, padx=10, pady=5)
        
        # 通用API Key 和 URL
        row += 1
        self.api_labels['custom_key_label'] = tk.Label(self.api_key_frame, text="自定义 API Key:", font=('微软雅黑', 9))
        self.api_labels['custom_key_label'].grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.api_fields['custom_key'] = tk.Entry(self.api_key_frame, width=30, show='*')
        self.api_fields['custom_key'].grid(row=row, column=1, padx=10, pady=5)
        
        self.api_labels['custom_url_label'] = tk.Label(self.api_key_frame, text="API URL:", font=('微软雅黑', 9))
        self.api_labels['custom_url_label'].grid(row=row, column=2, sticky='w', padx=10, pady=5)
        self.api_fields['custom_url'] = tk.Entry(self.api_key_frame, width=30)
        self.api_fields['custom_url'].grid(row=row, column=3, padx=10, pady=5)
        
        self._on_provider_change()
    
    def _create_model_combos(self):
        """创建模型选择下拉框"""
        # OpenAI模型
        self.openai_model_var = tk.StringVar(value="gpt-3.5-turbo")
        openai_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
        self.openai_combo = ttk.Combobox(self.model_frame, values=openai_models, 
                                          textvariable=self.openai_model_var, state='readonly', width=30)
        self.openai_combo.pack(fill='x', padx=10, pady=5)
        
        # Claude模型
        self.claude_model_var = tk.StringVar(value="claude-3-haiku-20240307")
        claude_models = ["claude-opus-4-20250514", "claude-sonnet-4-20250514", 
                        "claude-3-opus-20240229", "claude-3-sonnet-20240229",
                        "claude-3-haiku-20240307"]
        self.claude_combo = ttk.Combobox(self.model_frame, values=claude_models,
                                         textvariable=self.claude_model_var, state='readonly', width=30)
        self.claude_combo.pack(fill='x', padx=10, pady=5)
        
        # 豆包模型
        self.doubao_model_var = tk.StringVar(value="doubao-3.0")
        doubao_models = ["doubao-3.0", "doubao-2.0", "doubao-lite"]
        self.doubao_combo = ttk.Combobox(self.model_frame, values=doubao_models,
                                         textvariable=self.doubao_model_var, state='readonly', width=30)
        self.doubao_combo.pack(fill='x', padx=10, pady=5)
        
        # 文心一言模型
        self.wenxin_model_var = tk.StringVar(value="ernie-4.0")
        wenxin_models = ["ernie-4.0", "ernie-3.5", "ernie-3.0"]
        self.wenxin_combo = ttk.Combobox(self.model_frame, values=wenxin_models,
                                         textvariable=self.wenxin_model_var, state='readonly', width=30)
        self.wenxin_combo.pack(fill='x', padx=10, pady=5)
        
        # 讯飞星火模型
        self.spark_model_var = tk.StringVar(value="spark-3.5")
        spark_models = ["spark-3.5", "spark-3.0", "spark-2.0"]
        self.spark_combo = ttk.Combobox(self.model_frame, values=spark_models,
                                         textvariable=self.spark_model_var, state='readonly', width=30)
        self.spark_combo.pack(fill='x', padx=10, pady=5)
        
        # DeepSeek模型
        self.deepseek_model_var = tk.StringVar(value="deepseek-v4-flash")
        deepseek_models = ["deepseek-v4-flash", "deepseek-v4-pro", "deepseek-chat", "deepseek-reasoner"]
        self.deepseek_combo = ttk.Combobox(self.model_frame, values=deepseek_models,
                                           textvariable=self.deepseek_model_var, state='readonly', width=30)
        self.deepseek_combo.pack(fill='x', padx=10, pady=5)
        
        # 自定义模型
        self.custom_model_var = tk.StringVar(value="custom-model")
        self.custom_entry = ttk.Entry(self.model_frame, textvariable=self.custom_model_var, width=30)
        self.custom_entry.pack(fill='x', padx=10, pady=5)
        
        # 默认只显示OpenAI
        self.claude_combo.pack_forget()
        self.doubao_combo.pack_forget()
        self.wenxin_combo.pack_forget()
        self.spark_combo.pack_forget()
        self.deepseek_combo.pack_forget()
        self.custom_entry.pack_forget()
    
    def _on_provider_change(self):
        """提供商变更事件"""
        provider = self.provider_var.get()
        
        # 隐藏所有API字段和标签
        for key, field in self.api_fields.items():
            field.grid_forget()
        for key, label in self.api_labels.items():
            label.grid_forget()
        
        # 显示对应服务商的字段和标签
        if provider == "openai":
            self.api_labels['openai_label'].grid(row=0, column=0, sticky='w', padx=10, pady=5)
            self.api_fields['openai_key'].grid(row=0, column=1, padx=10, pady=5)
            self.openai_combo.pack(fill='x', padx=10, pady=5)
            self.claude_combo.pack_forget()
            self.doubao_combo.pack_forget()
            self.wenxin_combo.pack_forget()
            self.spark_combo.pack_forget()
            self.custom_entry.pack_forget()
        elif provider == "claude":
            self.api_labels['claude_label'].grid(row=1, column=0, sticky='w', padx=10, pady=5)
            self.api_fields['claude_key'].grid(row=1, column=1, padx=10, pady=5)
            self.claude_combo.pack(fill='x', padx=10, pady=5)
            self.openai_combo.pack_forget()
            self.doubao_combo.pack_forget()
            self.wenxin_combo.pack_forget()
            self.spark_combo.pack_forget()
            self.custom_entry.pack_forget()
        elif provider == "doubao":
            self.api_labels['doubao_key_label'].grid(row=2, column=0, sticky='w', padx=10, pady=5)
            self.api_fields['doubao_key'].grid(row=2, column=1, padx=10, pady=5)
            self.api_labels['doubao_secret_label'].grid(row=2, column=2, sticky='w', padx=10, pady=5)
            self.api_fields['doubao_secret'].grid(row=2, column=3, padx=10, pady=5)
            self.doubao_combo.pack(fill='x', padx=10, pady=5)
            self.openai_combo.pack_forget()
            self.claude_combo.pack_forget()
            self.wenxin_combo.pack_forget()
            self.spark_combo.pack_forget()
            self.custom_entry.pack_forget()
        elif provider == "wenxin":
            self.api_labels['wenxin_key_label'].grid(row=3, column=0, sticky='w', padx=10, pady=5)
            self.api_fields['wenxin_key'].grid(row=3, column=1, padx=10, pady=5)
            self.api_labels['wenxin_secret_label'].grid(row=3, column=2, sticky='w', padx=10, pady=5)
            self.api_fields['wenxin_secret'].grid(row=3, column=3, padx=10, pady=5)
            self.wenxin_combo.pack(fill='x', padx=10, pady=5)
            self.openai_combo.pack_forget()
            self.claude_combo.pack_forget()
            self.doubao_combo.pack_forget()
            self.spark_combo.pack_forget()
            self.custom_entry.pack_forget()
        elif provider == "spark":
            self.api_labels['spark_appid_label'].grid(row=4, column=0, sticky='w', padx=10, pady=5)
            self.api_fields['spark_appid'].grid(row=4, column=1, padx=10, pady=5)
            self.api_labels['spark_key_label'].grid(row=4, column=2, sticky='w', padx=10, pady=5)
            self.api_fields['spark_key'].grid(row=4, column=3, padx=10, pady=5)
            self.api_labels['spark_secret_label'].grid(row=4, column=4, sticky='w', padx=10, pady=5)
            self.api_fields['spark_secret'].grid(row=4, column=5, padx=10, pady=5)
            self.spark_combo.pack(fill='x', padx=10, pady=5)
            self.openai_combo.pack_forget()
            self.claude_combo.pack_forget()
            self.doubao_combo.pack_forget()
            self.wenxin_combo.pack_forget()
            self.custom_entry.pack_forget()
        elif provider == "deepseek":
            self.api_labels['deepseek_label'].grid(row=5, column=0, sticky='w', padx=10, pady=5)
            self.api_fields['deepseek_key'].grid(row=5, column=1, padx=10, pady=5)
            self.deepseek_combo.pack(fill='x', padx=10, pady=5)
            self.openai_combo.pack_forget()
            self.claude_combo.pack_forget()
            self.doubao_combo.pack_forget()
            self.wenxin_combo.pack_forget()
            self.spark_combo.pack_forget()
            self.custom_entry.pack_forget()
        elif provider == "custom":
            self.api_labels['custom_key_label'].grid(row=6, column=0, sticky='w', padx=10, pady=5)
            self.api_fields['custom_key'].grid(row=6, column=1, padx=10, pady=5)
            self.api_labels['custom_url_label'].grid(row=6, column=2, sticky='w', padx=10, pady=5)
            self.api_fields['custom_url'].grid(row=6, column=3, padx=10, pady=5)
            self.custom_entry.pack(fill='x', padx=10, pady=5)
            self.openai_combo.pack_forget()
            self.claude_combo.pack_forget()
            self.doubao_combo.pack_forget()
            self.wenxin_combo.pack_forget()
            self.spark_combo.pack_forget()
    
    def _create_guide_tab(self, parent):
        """创建使用指南选项卡"""
        guide_text = """
=== OpenAI API 获取指南 ===

1. 访问 OpenAI 官网
   打开浏览器访问: https://platform.openai.com

2. 注册/登录账号
   如果没有账号，点击"Sign up"注册
   如果有账号，点击"Log in"登录

3. 获取API密钥
   登录后，点击右上角头像 -> "API keys"
   点击 "Create new secret key" 创建密钥
   复制生成的密钥（以 sk- 开头）

4. 注意事项
   - API密钥就像密码，请勿泄露给他人
   - 首次使用需要充值或有免费额度
   - 可以设置用量限制防止超额

=== Claude API 获取指南 ===

1. 访问 Anthropic 官网
   打开浏览器访问: https://www.anthropic.com

2. 注册/登录账号
   访问: https://console.anthropic.com/
   使用Google账号或邮箱注册

3. 获取API密钥
   登录后，点击 "API Keys" 
   点击 "Create Key" 创建密钥
   复制生成的密钥

4. 注意事项
   - Claude有免费试用额度
   - 不同模型价格不同

=== 豆包 API 获取指南 ===

1. 访问豆包开放平台
   打开浏览器访问: https://www.doubao.com

2. 注册/登录账号
   使用字节跳动账号登录

3. 创建应用并获取密钥
   - 进入开发者控制台
   - 创建新应用
   - 获取 API Key 和 Secret Key

4. 注意事项
   - 国内访问速度快
   - 有免费调用额度

=== 文心一言 API 获取指南 ===

1. 访问百度智能云
   打开浏览器访问: https://cloud.baidu.com

2. 注册/登录账号
   使用百度账号登录

3. 创建应用并获取密钥
   - 进入文心一言开放平台
   - 创建新应用
   - 获取 API Key 和 Secret Key

4. 注意事项
   - 中文理解能力强
   - 有免费调用额度

=== 讯飞星火 API 获取指南 ===

1. 访问讯飞开放平台
   打开浏览器访问: https://www.xfyun.cn

2. 注册/登录账号
   使用手机号注册

3. 创建应用并获取密钥
   - 进入控制台
   - 创建新应用
   - 获取 App ID、API Key 和 Secret Key

4. 注意事项
   - 语音能力强
   - 有免费调用额度

=== 通用API配置说明 ===

如果您使用其他兼容OpenAI格式的API：
1. 在API URL中输入完整的API地址
2. 在API Key中输入认证密钥
3. 在模型名称中输入目标模型名

示例：
- 本地Ollama: http://localhost:11434/v1/chat/completions
- 企业内部部署的模型

=== 常见问题 ===

Q: API需要付费吗？
A: 大部分平台都有免费试用额度，超出后需要付费。

Q: 我的密钥安全吗？
A: 密钥只保存在您的本地电脑配置文件中，不会上传到任何服务器。

Q: 测试连接失败怎么办？
A: 请检查：1) 密钥是否正确 2) 网络是否正常 3) 账户是否有足够额度
        """
        
        text_widget = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=('Consolas', 9))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', guide_text)
        text_widget.config(state='disabled')  # 只读
    
    def _show_api_key_guide(self):
        """显示API密钥获取指南"""
        guide_win = tk.Toplevel(self.dialog)
        guide_win.title("如何获取API密钥")
        guide_win.geometry("550x450")
        
        provider = self.provider_var.get()
        
        guides = {
            "openai": ("OpenAI", "https://platform.openai.com/api-keys", """
=== OpenAI API 获取步骤 ===

第一步：访问OpenAI平台
   打开浏览器访问以下网址：
   https://platform.openai.com/api-keys

第二步：登录或注册
   - 如果有OpenAI账号，直接登录
   - 如果没有，点击"Sign up"注册

第三步：创建API密钥
   1. 登录后进入API Keys页面
   2. 点击 "Create new secret key" 按钮
   3. 可以给密钥起个名字（如：pyplot）
   4. 点击创建
   5. 【重要】立即复制密钥，它只显示一次！

第四步：粘贴密钥
   复制密钥后，粘贴到设置对话框的API Key输入框中。

【视频教程】
如需更详细的教程，可以观看B站相关视频。
            """),
            "claude": ("Claude", "https://console.anthropic.com/", """
=== Claude API 获取步骤 ===

第一步：访问Anthropic Console
   打开浏览器访问以下网址：
   https://console.anthropic.com/

第二步：登录或注册
   - 使用Google账号或邮箱注册
   - 按照提示完成验证

第三步：创建API密钥
   1. 登录后进入 API Keys 页面
   2. 点击 "Create Key" 按钮
   3. 输入密钥名称（如：pyplot）
   4. 选择权限（默认即可）
   5. 点击创建
   6. 【重要】立即复制密钥，它只显示一次！

第四步：粘贴密钥
   复制密钥后，粘贴到设置对话框的API Key输入框中。

注意事项：
- Claude API有免费试用额度
- 不同版本的Claude模型能力不同
            """),
            "doubao": ("豆包", "https://www.doubao.com", """
=== 豆包 API 获取步骤 ===

第一步：访问豆包开放平台
   打开浏览器访问以下网址：
   https://www.doubao.com

第二步：登录账号
   - 使用字节跳动账号登录
   - 如果没有账号，先注册

第三步：进入开发者控制台
   1. 登录后点击右上角头像
   2. 选择 "开发者控制台"

第四步：创建应用
   1. 点击 "创建应用"
   2. 填写应用信息
   3. 提交审核

第五步：获取密钥
   应用审核通过后，即可获取：
   - API Key
   - Secret Key

注意事项：
- 国内访问速度快
- 有免费调用额度
- 需要完成实名认证
            """),
            "wenxin": ("文心一言", "https://cloud.baidu.com/product/wenxinworkshop", """
=== 文心一言 API 获取步骤 ===

第一步：访问百度智能云
   打开浏览器访问以下网址：
   https://cloud.baidu.com/product/wenxinworkshop

第二步：登录账号
   - 使用百度账号登录
   - 如果没有账号，先注册

第三步：创建应用
   1. 进入文心一言开放平台
   2. 点击 "创建应用"
   3. 填写应用信息

第四步：获取密钥
   创建成功后，即可获取：
   - API Key
   - Secret Key

注意事项：
- 中文理解能力强
- 有免费调用额度
            """),
            "spark": ("讯飞星火", "https://www.xfyun.cn/services/spark", """
=== 讯飞星火 API 获取步骤 ===

第一步：访问讯飞开放平台
   打开浏览器访问以下网址：
   https://www.xfyun.cn/services/spark

第二步：登录账号
   - 使用手机号注册登录

第三步：创建应用
   1. 进入控制台
   2. 点击 "创建应用"
   3. 选择 "星火认知大模型"

第四步：获取密钥
   创建成功后，即可获取：
   - App ID
   - API Key
   - Secret Key

注意事项：
- 语音能力强
- 有免费调用额度
            """),
            "custom": ("通用API", "", """
=== 通用API 配置说明 ===

如果您使用其他兼容OpenAI格式的API：

【配置步骤】
1. 在 "自定义 API Key" 输入框中输入认证密钥
2. 在 "API URL" 输入框中输入完整的API地址
3. 在模型输入框中输入目标模型名称

【常见示例】

1. 本地Ollama部署
   API URL: http://localhost:11434/v1/chat/completions
   API Key: 任意非空字符串
   模型名称: 如 "llama3"

2. 企业内部部署模型
   API URL: 根据实际部署地址填写
   API Key: 联系管理员获取

3. 其他兼容平台
   参考对应平台的API文档

【注意事项】
- 确保API格式与OpenAI兼容
- 确保网络可以访问目标地址
            """)
        }
        
        name, url, guide_text = guides.get(provider, ("未知", "", "暂无指南"))
        
        text = scrolledtext.ScrolledText(guide_win, wrap=tk.WORD, font=('微软雅黑', 10))
        text.pack(fill='both', expand=True, padx=20, pady=20)
        text.insert('1.0', guide_text)
        text.config(state='disabled')
        
        if url:
            tk.Button(guide_win, text=f"打开 {name} 官网", 
                     command=lambda: webbrowser.open(url)).pack(pady=10)
    
    def _load_current_settings(self):
        """加载当前设置"""
        self.provider_var.set(self.config.get("ai_provider", "openai"))
        
        # 加载所有密钥
        self.api_fields['openai_key'].insert(0, self.config.get("openai_api_key", ""))
        self.api_fields['claude_key'].insert(0, self.config.get("claude_api_key", ""))
        self.api_fields['doubao_key'].insert(0, self.config.get("doubao_api_key", ""))
        self.api_fields['doubao_secret'].insert(0, self.config.get("doubao_secret", ""))
        self.api_fields['wenxin_key'].insert(0, self.config.get("wenxin_api_key", ""))
        self.api_fields['wenxin_secret'].insert(0, self.config.get("wenxin_secret", ""))
        self.api_fields['spark_appid'].insert(0, self.config.get("spark_app_id", ""))
        self.api_fields['spark_key'].insert(0, self.config.get("spark_api_key", ""))
        self.api_fields['spark_secret'].insert(0, self.config.get("spark_secret", ""))
        self.api_fields['deepseek_key'].insert(0, self.config.get("deepseek_api_key", ""))
        self.api_fields['custom_key'].insert(0, self.config.get("custom_api_key", ""))
        self.api_fields['custom_url'].insert(0, self.config.get("custom_api_url", ""))
        
        # 加载模型
        self.openai_model_var.set(self.config.get("openai_model", "gpt-3.5-turbo"))
        self.claude_model_var.set(self.config.get("claude_model", "claude-3-haiku-20240307"))
        self.doubao_model_var.set(self.config.get("doubao_model", "doubao-3.0"))
        self.wenxin_model_var.set(self.config.get("wenxin_model", "ernie-4.0"))
        self.spark_model_var.set(self.config.get("spark_model", "spark-3.5"))
        self.deepseek_model_var.set(self.config.get("deepseek_model", "deepseek-r1"))
        self.custom_model_var.set(self.config.get("custom_model", "custom-model"))
        
        self._on_provider_change()
    
    def _test_connection(self):
        """测试API连接"""
        provider = self.provider_var.get()
        
        # 检查必要配置
        if provider == "openai":
            api_key = self.api_fields['openai_key'].get().strip()
            if not api_key:
                messagebox.showwarning("提示", "请先输入API密钥")
                return
        elif provider == "claude":
            api_key = self.api_fields['claude_key'].get().strip()
            if not api_key:
                messagebox.showwarning("提示", "请先输入API密钥")
                return
        elif provider == "doubao":
            api_key = self.api_fields['doubao_key'].get().strip()
            secret = self.api_fields['doubao_secret'].get().strip()
            if not api_key or not secret:
                messagebox.showwarning("提示", "请输入API Key和Secret")
                return
        elif provider == "wenxin":
            api_key = self.api_fields['wenxin_key'].get().strip()
            secret = self.api_fields['wenxin_secret'].get().strip()
            if not api_key or not secret:
                messagebox.showwarning("提示", "请输入API Key和Secret")
                return
        elif provider == "spark":
            appid = self.api_fields['spark_appid'].get().strip()
            api_key = self.api_fields['spark_key'].get().strip()
            secret = self.api_fields['spark_secret'].get().strip()
            if not appid or not api_key or not secret:
                messagebox.showwarning("提示", "请输入App ID、API Key和Secret")
                return
        elif provider == "custom":
            api_key = self.api_fields['custom_key'].get().strip()
            api_url = self.api_fields['custom_url'].get().strip()
            if not api_key or not api_url:
                messagebox.showwarning("提示", "请输入API Key和API URL")
                return
        
        messagebox.showinfo("测试连接", 
                           f"正在测试 {provider} 连接...\n\n"
                           "请确保网络连接正常。\n"
                           "测试功能即将上线。")
    
    def _save_settings(self):
        """保存设置"""
        if not hasattr(self, 'openai_model_var'):
            messagebox.showerror("错误", "设置初始化未完成，请关闭对话框后重试。")
            return
            
        provider = self.provider_var.get()
        
        # 保存配置
        self.config.set("ai_provider", provider)
        
        # 保存OpenAI配置
        self.config.set("openai_api_key", self.api_fields['openai_key'].get().strip())
        self.config.set("openai_model", self.openai_model_var.get())
        
        # 保存Claude配置
        self.config.set("claude_api_key", self.api_fields['claude_key'].get().strip())
        self.config.set("claude_model", self.claude_model_var.get())
        
        # 保存豆包配置
        self.config.set("doubao_api_key", self.api_fields['doubao_key'].get().strip())
        self.config.set("doubao_secret", self.api_fields['doubao_secret'].get().strip())
        self.config.set("doubao_model", self.doubao_model_var.get())
        
        # 保存文心一言配置
        self.config.set("wenxin_api_key", self.api_fields['wenxin_key'].get().strip())
        self.config.set("wenxin_secret", self.api_fields['wenxin_secret'].get().strip())
        self.config.set("wenxin_model", self.wenxin_model_var.get())
        
        # 保存星火配置
        self.config.set("spark_app_id", self.api_fields['spark_appid'].get().strip())
        self.config.set("spark_api_key", self.api_fields['spark_key'].get().strip())
        self.config.set("spark_secret", self.api_fields['spark_secret'].get().strip())
        self.config.set("spark_model", self.spark_model_var.get())
        
        # 保存DeepSeek配置
        self.config.set("deepseek_api_key", self.api_fields['deepseek_key'].get().strip())
        self.config.set("deepseek_model", self.deepseek_model_var.get())
        
        # 保存自定义配置
        self.config.set("custom_api_key", self.api_fields['custom_key'].get().strip())
        self.config.set("custom_api_url", self.api_fields['custom_url'].get().strip())
        self.config.set("custom_model", self.custom_model_var.get())
        
        if self.config.save_config():
            messagebox.showinfo("成功", "设置已保存！\n\n"
                                 "现在您可以使用AI助手功能了。")
            self.dialog.destroy()
        else:
            messagebox.showerror("错误", "保存设置失败，请重试。")


class FirstRunWizard:
    """首次运行向导 - 引导用户配置API"""
    
    def __init__(self, parent):
        self.parent = parent
        self.config = get_config_manager()
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("欢迎使用 pyplot-draw-tool")
        self.dialog.geometry("700x650")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.step = 1
        self._create_widgets()
    
    def _create_widgets(self):
        """创建向导部件"""
        # 标题
        title = tk.Label(self.dialog, text="🎉 欢迎使用 AI 绘图助手！", 
                        font=('微软雅黑', 18, 'bold'))
        title.pack(pady=20)
        
        # 步骤指示器
        self.step_frame = tk.Frame(self.dialog)
        self.step_frame.pack(pady=10)
        
        self.step_labels = []
        for i in range(1, 4):
            lbl = tk.Label(self.step_frame, text=f"步骤{i}", 
                          width=12, font=('微软雅黑', 9))
            lbl.pack(side='left', padx=5)
            self.step_labels.append(lbl)
        
        self._update_step_indicators()
        
        # 内容区域（带滚动）
        scroll_frame = tk.Frame(self.dialog)
        scroll_frame.pack(fill='both', expand=True, padx=40, pady=10)
        
        canvas = tk.Canvas(scroll_frame, height=400)
        canvas.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(scroll_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        self.content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.content_frame, anchor='nw')
        
        self._show_step_1()
        
        # 按钮区域
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=20)
        
        self.btn_back = tk.Button(btn_frame, text="上一步", width=10, 
                                  command=self._go_back, state='disabled')
        self.btn_back.pack(side='left', padx=10)
        
        self.btn_next = tk.Button(btn_frame, text="下一步", width=10, 
                                  command=self._go_next)
        self.btn_next.pack(side='left', padx=10)
        
        self.btn_skip = tk.Button(btn_frame, text="跳过", width=10, 
                                  command=self._skip_wizard)
        self.btn_skip.pack(side='left', padx=10)
    
    def _update_step_indicators(self):
        """更新步骤指示器"""
        for i, lbl in enumerate(self.step_labels):
            if i + 1 == self.step:
                lbl.config(bg='lightblue', relief='sunken')
            else:
                lbl.config(bg='SystemButtonFace', relief='raised')
    
    def _clear_content(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _show_step_1(self):
        """步骤1：介绍AI功能"""
        self._clear_content()
        
        intro = tk.Label(self.content_frame, text="🤖 AI 智能助手功能", 
                        font=('微软雅黑', 14, 'bold'))
        intro.pack(pady=(0, 20))
        
        features = """
使用 AI 助手，您可以：

✨ 基础绘图智能化
   用自然语言描述需求，AI自动填写图表参数
   例如："画一个展示季度销售额的柱状图，有两个数据集"

✨ 自定义代码生成
   描述您想要的图表，AI生成完整的Matplotlib代码
   支持复杂图表如双Y轴、热力图等

✨ 支持多种AI模型
   🌍 国际：OpenAI GPT、Anthropic Claude
   🇨🇳 国产：豆包、文心一言、讯飞星火
   ⚙️ 通用：支持自定义API

要使用这些功能，您需要配置一个AI API密钥。
        """
        
        text = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, 
                                         font=('微软雅黑', 10), height=18, width=70)
        text.pack(fill='both', expand=True)
        text.insert('1.0', features)
        text.config(state='disabled')
    
    def _show_step_2(self):
        """步骤2：选择AI服务商"""
        self._clear_content()
        
        title = tk.Label(self.content_frame, text="选择 AI 服务商", 
                        font=('微软雅黑', 14, 'bold'))
        title.pack(pady=(0, 20))
        
        desc = tk.Label(self.content_frame, 
                       text="请选择您想使用的AI服务提供商：", 
                       font=('微软雅黑', 10))
        desc.pack(pady=(0, 20))
        
        # 确保provider_var已初始化
        if not hasattr(self, 'provider_var'):
            self.provider_var = tk.StringVar(value="openai")
        else:
            self.provider_var.set("openai")
        
        # 分组显示 - 国际AI
        intl_frame = tk.LabelFrame(self.content_frame, text="🌍 国际AI", 
                                   font=('微软雅黑', 10), padx=10, pady=10)
        intl_frame.pack(fill='x', pady=10)
        
        # OpenAI选项
        openai_frame = tk.Frame(intl_frame)
        openai_frame.pack(fill='x', pady=5)
        openai_rb = tk.Radiobutton(openai_frame, text="OpenAI (GPT系列)", 
                       variable=self.provider_var, value="openai")
        openai_rb.pack(side='left')
        openai_rb.select()  # 默认选中
        tk.Label(openai_frame, text="• GPT-3.5-turbo免费额度，GPT-4o效果最好", 
                font=('微软雅黑', 8), fg='gray').pack(side='left', padx=10)
        
        # Claude选项
        claude_frame = tk.Frame(intl_frame)
        claude_frame.pack(fill='x', pady=5)
        tk.Radiobutton(claude_frame, text="Anthropic Claude", 
                       variable=self.provider_var, value="claude").pack(side='left')
        tk.Label(claude_frame, text="• 长文本处理强，Claude 3 Opus效果最好", 
                font=('微软雅黑', 8), fg='gray').pack(side='left', padx=10)
        
        # 国产AI - 单独分组
        china_frame = tk.LabelFrame(self.content_frame, text="🇨🇳 国产AI", 
                                    font=('微软雅黑', 10), padx=10, pady=10)
        china_frame.pack(fill='x', pady=10)
        
        # 豆包选项
        doubao_frame = tk.Frame(china_frame)
        doubao_frame.pack(fill='x', pady=5)
        tk.Radiobutton(doubao_frame, text="🤖 豆包", 
                       variable=self.provider_var, value="doubao").pack(side='left')
        tk.Label(doubao_frame, text="• 字节跳动出品，国内访问快，中文对话效果好", 
                font=('微软雅黑', 8), fg='gray').pack(side='left', padx=10)
        
        # 文心一言选项
        wenxin_frame = tk.Frame(china_frame)
        wenxin_frame.pack(fill='x', pady=5)
        tk.Radiobutton(wenxin_frame, text="🔷 文心一言", 
                       variable=self.provider_var, value="wenxin").pack(side='left')
        tk.Label(wenxin_frame, text="• 百度出品，中文理解能力强", 
                font=('微软雅黑', 8), fg='gray').pack(side='left', padx=10)
        
        # 讯飞星火选项
        spark_frame = tk.Frame(china_frame)
        spark_frame.pack(fill='x', pady=5)
        tk.Radiobutton(spark_frame, text="🔥 讯飞星火", 
                       variable=self.provider_var, value="spark").pack(side='left')
        tk.Label(spark_frame, text="• 科大讯飞出品，语音能力强，多模态能力出色", 
                font=('微软雅黑', 8), fg='gray').pack(side='left', padx=10)
        
        # 通用API - 支持自定义部署
        custom_frame = tk.LabelFrame(self.content_frame, text="⚙️ 通用API (自定义)", 
                                     font=('微软雅黑', 10), padx=10, pady=10)
        custom_frame.pack(fill='x', pady=10)
        
        custom_inner = tk.Frame(custom_frame)
        custom_inner.pack(fill='x', pady=5)
        tk.Radiobutton(custom_inner, text="通用API接口", 
                       variable=self.provider_var, value="custom").pack(side='left')
        tk.Label(custom_inner, text="• 支持本地模型(Ollama)、企业内部部署、其他兼容平台", 
                font=('微软雅黑', 8), fg='gray').pack(side='left', padx=10)
        
        # 通用API说明
        custom_note = tk.Label(custom_frame, 
                              text="📌 使用示例：本地Ollama -> API URL: http://localhost:11434/v1/chat/completions",
                              font=('微软雅黑', 8), fg='blue', justify='left')
        custom_note.pack(fill='x', pady=5)
        
        # 确保下一步按钮可用
        self.btn_next.config(state='normal', text="下一步")
    
    def _show_step_3(self):
        """步骤3：获取API密钥"""
        self._clear_content()
        
        title = tk.Label(self.content_frame, text="输入 API 密钥", 
                        font=('微软雅黑', 14, 'bold'))
        title.pack(pady=(0, 10))
        
        provider = self.provider_var.get()
        
        provider_info = {
            "openai": ("OpenAI", "https://platform.openai.com/api-keys"),
            "claude": ("Claude", "https://console.anthropic.com/"),
            "doubao": ("豆包", "https://www.doubao.com"),
            "wenxin": ("文心一言", "https://cloud.baidu.com/product/wenxinworkshop"),
            "spark": ("讯飞星火", "https://www.xfyun.cn/services/spark"),
            "custom": ("通用API", "")
        }
        
        name, url = provider_info.get(provider, ("未知", ""))
        
        url_label = tk.Label(self.content_frame, text=f"请获取您的 {name} API密钥：", 
                            font=('微软雅黑', 10))
        url_label.pack(pady=(0, 10))
        
        if url:
            btn_url = tk.Button(self.content_frame, text=f"👉 点击获取 {name} API密钥", 
                               command=lambda: webbrowser.open(url),
                               font=('微软雅黑', 11), cursor='hand2')
            btn_url.pack(pady=10)
        
        steps_text = {
            "openai": """
获取步骤：

1. 点击上方按钮打开OpenAI官网
2. 注册或登录账号
3. 进入 API Keys 页面
4. 点击 "Create new secret key" 创建密钥
5. 复制生成的密钥（以 sk- 开头）
6. 将密钥粘贴到下方输入框
            """,
            "claude": """
获取步骤：

1. 点击上方按钮打开Claude官网
2. 注册或登录账号
3. 进入 API Keys 页面
4. 点击 "Create Key" 创建密钥
5. 复制生成的密钥
6. 将密钥粘贴到下方输入框
            """,
            "doubao": """
获取步骤：

1. 点击上方按钮打开豆包官网
2. 登录字节跳动账号
3. 进入开发者控制台
4. 创建应用并获取 API Key 和 Secret Key
5. 将密钥粘贴到下方输入框
            """,
            "wenxin": """
获取步骤：

1. 点击上方按钮打开百度智能云
2. 登录百度账号
3. 进入文心一言开放平台
4. 创建应用并获取 API Key 和 Secret Key
5. 将密钥粘贴到下方输入框
            """,
            "spark": """
获取步骤：

1. 点击上方按钮打开讯飞开放平台
2. 注册并登录账号
3. 进入控制台创建应用
4. 获取 App ID、API Key 和 Secret Key
5. 将密钥粘贴到下方输入框
            """,
            "custom": """
配置步骤：

1. 输入您的自定义API密钥
2. 输入API服务地址（如 http://localhost:11434/v1/chat/completions）
3. 输入模型名称
            """
        }
        
        steps_label = tk.Label(self.content_frame, text=steps_text.get(provider, ""), 
                              font=('微软雅黑', 9), justify='left')
        steps_label.pack(pady=10)
        
        # 根据服务商显示不同的输入框
        if provider in ["openai", "claude"]:
            tk.Label(self.content_frame, text="粘贴您的 API Key：", 
                    font=('微软雅黑', 10)).pack(pady=(10, 5))
            self.api_key_entry = tk.Entry(self.content_frame, width=50, show='*')
            self.api_key_entry.pack(pady=5)
        elif provider in ["doubao", "wenxin"]:
            tk.Label(self.content_frame, text="API Key：", 
                    font=('微软雅黑', 10)).pack(pady=(10, 5))
            self.api_key_entry = tk.Entry(self.content_frame, width=50, show='*')
            self.api_key_entry.pack(pady=5)
            
            tk.Label(self.content_frame, text="Secret Key：", 
                    font=('微软雅黑', 10)).pack(pady=(10, 5))
            self.api_secret_entry = tk.Entry(self.content_frame, width=50, show='*')
            self.api_secret_entry.pack(pady=5)
        elif provider == "spark":
            tk.Label(self.content_frame, text="App ID：", 
                    font=('微软雅黑', 10)).pack(pady=(10, 5))
            self.spark_appid_entry = tk.Entry(self.content_frame, width=50)
            self.spark_appid_entry.pack(pady=5)
            
            tk.Label(self.content_frame, text="API Key：", 
                    font=('微软雅黑', 10)).pack(pady=(10, 5))
            self.api_key_entry = tk.Entry(self.content_frame, width=50, show='*')
            self.api_key_entry.pack(pady=5)
            
            tk.Label(self.content_frame, text="Secret Key：", 
                    font=('微软雅黑', 10)).pack(pady=(10, 5))
            self.api_secret_entry = tk.Entry(self.content_frame, width=50, show='*')
            self.api_secret_entry.pack(pady=5)
        elif provider == "custom":
            tk.Label(self.content_frame, text="API Key：", 
                    font=('微软雅黑', 10)).pack(pady=(10, 5))
            self.api_key_entry = tk.Entry(self.content_frame, width=50, show='*')
            self.api_key_entry.pack(pady=5)
            
            tk.Label(self.content_frame, text="API URL：", 
                    font=('微软雅黑', 10)).pack(pady=(10, 5))
            self.api_url_entry = tk.Entry(self.content_frame, width=50)
            self.api_url_entry.pack(pady=5)
            
            tk.Label(self.content_frame, text="模型名称：", 
                    font=('微软雅黑', 10)).pack(pady=(10, 5))
            self.model_entry = tk.Entry(self.content_frame, width=50)
            self.model_entry.pack(pady=5)
        
        tk.Label(self.content_frame, 
                text="⚠️ 密钥将安全保存在本地，不会上传到任何服务器", 
                font=('微软雅黑', 8), fg='green').pack(pady=10)
    
    def _go_back(self):
        """上一步"""
        if self.step > 1:
            self.step -= 1
            self._update_step_indicators()
            if self.step == 1:
                self._show_step_1()
                self.btn_back.config(state='disabled')
            elif self.step == 2:
                self._show_step_2()
                self.btn_back.config(state='normal')
            self.btn_next.config(text="下一步")
    
    def _go_next(self):
        """下一步"""
        if self.step == 1:
            self.step = 2
            self._update_step_indicators()
            self._show_step_2()
            self.btn_back.config(state='normal')
            # 步骤2默认应该显示下一步按钮
        elif self.step == 2:
            self.step = 3
            self._update_step_indicators()
            self._show_step_3()
            self.btn_next.config(text="完成")
            self.btn_skip.config(text="跳过")
        elif self.step == 3:
            self._finish_wizard()
    
    def _skip_wizard(self):
        """跳过向导"""
        self.config.set("first_run_completed", True)
        self.config.save_config()
        self.dialog.destroy()
    
    def _finish_wizard(self):
        """完成向导"""
        provider = self.provider_var.get()
        
        # 保存配置
        self.config.set("ai_provider", provider)
        
        if provider == "openai":
            api_key = self.api_key_entry.get().strip() if hasattr(self, 'api_key_entry') else ""
            self.config.set("openai_api_key", api_key)
            self.config.set("openai_model", "gpt-3.5-turbo")
        elif provider == "claude":
            api_key = self.api_key_entry.get().strip() if hasattr(self, 'api_key_entry') else ""
            self.config.set("claude_api_key", api_key)
            self.config.set("claude_model", "claude-3-haiku-20240307")
        elif provider == "doubao":
            api_key = self.api_key_entry.get().strip() if hasattr(self, 'api_key_entry') else ""
            secret = self.api_secret_entry.get().strip() if hasattr(self, 'api_secret_entry') else ""
            self.config.set("doubao_api_key", api_key)
            self.config.set("doubao_secret", secret)
            self.config.set("doubao_model", "doubao-3.0")
        elif provider == "wenxin":
            api_key = self.api_key_entry.get().strip() if hasattr(self, 'api_key_entry') else ""
            secret = self.api_secret_entry.get().strip() if hasattr(self, 'api_secret_entry') else ""
            self.config.set("wenxin_api_key", api_key)
            self.config.set("wenxin_secret", secret)
            self.config.set("wenxin_model", "ernie-4.0")
        elif provider == "spark":
            appid = self.spark_appid_entry.get().strip() if hasattr(self, 'spark_appid_entry') else ""
            api_key = self.api_key_entry.get().strip() if hasattr(self, 'api_key_entry') else ""
            secret = self.api_secret_entry.get().strip() if hasattr(self, 'api_secret_entry') else ""
            self.config.set("spark_app_id", appid)
            self.config.set("spark_api_key", api_key)
            self.config.set("spark_secret", secret)
            self.config.set("spark_model", "spark-3.5")
        elif provider == "custom":
            api_key = self.api_key_entry.get().strip() if hasattr(self, 'api_key_entry') else ""
            api_url = self.api_url_entry.get().strip() if hasattr(self, 'api_url_entry') else ""
            model = self.model_entry.get().strip() if hasattr(self, 'model_entry') else "custom-model"
            self.config.set("custom_api_key", api_key)
            self.config.set("custom_api_url", api_url)
            self.config.set("custom_model", model)
        
        # 标记已完成首次向导
        self.config.set("first_run_completed", True)
        self.config.save_config()
        
        messagebox.showinfo("设置完成", 
                           "🎉 配置已保存！\n\n"
                           "您随时可以在菜单栏「工具→设置」中修改配置。\n"
                           "现在可以开始使用AI助手功能了！")
        self.dialog.destroy()


def show_settings(parent):
    """显示设置对话框"""
    SettingsDialog(parent)


def show_first_run_wizard(parent):
    """显示首次运行向导"""
    config = get_config_manager()
    if not config.get("first_run_completed", False):
        FirstRunWizard(parent)
