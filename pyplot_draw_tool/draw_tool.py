# 全能Matplotlib图形化绘图工具 —— 支持所有图表类型，零代码操作
# 作者：红鳍东方鲀
# 版本：1.0.1
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
class DrawTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Python绘图工具")
        self.root.geometry("650x650")
        self.root.resizable(True, True)
        
        # 初始化图表类型映射
        self._init_chart_mapping()
        
        # 初始化GUI组件
        self._init_gui()
    
    def _create_dataset_inputs(self):
        """创建数据集输入字段"""
        # 清除现有数据集输入
        for dataset in self.dataset_frames:
            frame = dataset['frame']
            for widget in frame.winfo_children():
                widget.destroy()
            frame.destroy()
        self.dataset_frames = []
        
        # 获取数据集数量
        count = int(self.dataset_count.get())
        
        # 创建新的数据集输入
        frame_data = self.root.nametowidget(".!labelframe")
        for i in range(count):
            frame = tk.Frame(frame_data)
            frame.grid(row=i+2, column=0, columnspan=2, sticky="we", padx=5, pady=5)
            
            # 数据集标签
            tk.Label(frame, text=f"数据集 {i+1} 标签：", font=("微软雅黑", 10)).grid(row=0, column=0, padx=5, pady=4, sticky="w")
            entry_label = ttk.Entry(frame, width=15)
            entry_label.grid(row=0, column=1, padx=5, pady=4)
            entry_label.insert(0, f"数据集 {i+1}")
            
            # Y轴数据
            tk.Label(frame, text=f"Y轴数据：", font=('微软雅黑', 10)).grid(row=0, column=2, padx=5, pady=4, sticky="w")
            entry_y = tk.Text(frame, width=30, height=2)
            entry_y.grid(row=0, column=3, padx=5, pady=4)
            
            # 误差数据
            tk.Label(frame, text=f"误差数据：", font=('微软雅黑', 10)).grid(row=0, column=4, padx=5, pady=4, sticky="w")
            entry_err = tk.Text(frame, width=20, height=2)
            entry_err.grid(row=0, column=5, padx=5, pady=4)
            
            # 颜色控制
            tk.Label(frame, text=f"颜色：", font=('微软雅黑', 10)).grid(row=0, column=6, padx=5, pady=4, sticky="w")
            color_options = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'cyan', 'yellow', 'black']
            combo_color = ttk.Combobox(frame, values=color_options, width=8, state='readonly')
            combo_color.grid(row=0, column=7, padx=5, pady=4)
            # 默认颜色
            default_colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink']
            combo_color.current(default_colors.index(default_colors[i % len(default_colors)]))
            
            self.dataset_frames.append({
                "frame": frame,
                "label": entry_label,
                "y_data": entry_y,
                "err_data": entry_err,
                "color": combo_color
            })
    
    def _on_dataset_count_change(self, event):
        """处理数据集数量变化事件"""
        self._create_dataset_inputs()
    
    def _init_gui(self):
        # 标题
        tk.Label(self.root, text="python绘图工具", font=("微软雅黑", 18, "bold")).pack(pady=15)
        
        # ========== 第一部分：数据输入区 ==========
        frame_data = tk.LabelFrame(self.root, text="数据输入（逗号分隔数字）", font=("微软雅黑", 12))
        frame_data.pack(fill="x", padx=20, pady=5)
        
        # 数据集数量选择
        tk.Label(frame_data, text="数据集数量：", font=('微软雅黑', 11)).grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.dataset_count = ttk.Combobox(frame_data, values=[1, 2, 3, 4, 5, 6, 7], width=5, state="readonly")
        self.dataset_count.current(0)
        self.dataset_count.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        self.dataset_count.bind("<<ComboboxSelected>>", self._on_dataset_count_change)
        
        # X轴数据
        tk.Label(frame_data, text="X轴数据（类别）：", font=('微软雅黑', 11)).grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.entry_x = tk.Text(frame_data, width=60, height=2)
        self.entry_x.grid(row=1, column=1, padx=5, pady=8)
        
        # 数据集输入区域
        self.dataset_frames = []
        self._create_dataset_inputs()
        
        # ========== 第二部分：图表设置区 ==========
        frame_setting = tk.LabelFrame(self.root, text="图表设置", font=("微软雅黑", 12))
        frame_setting.pack(fill="x", padx=20, pady=5)
        
        # 图表类型
        tk.Label(frame_setting, text="图表类型：", font=("微软雅黑", 11)).grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.chart_types = ["折线图", "柱状图", "散点图", "误差棒图", "直方图", "饼图", "雷达图"]
        self.combo_chart = ttk.Combobox(frame_setting, values=self.chart_types, width=18, state="readonly")
        self.combo_chart.current(0)
        self.combo_chart.grid(row=0, column=1, padx=5, pady=8)
        # 添加图表类型切换事件
        self.combo_chart.bind("<<ComboboxSelected>>", self._on_chart_type_change)
        
        # 标题/标签
        tk.Label(frame_setting, text="图表标题：", font=("微软雅黑", 11)).grid(row=0, column=2, padx=5, pady=8, sticky="w")
        self.entry_title = ttk.Entry(frame_setting, width=18)
        self.entry_title.grid(row=0, column=3, padx=5, pady=8)
        
        tk.Label(frame_setting, text="X轴标签：", font=("微软雅黑", 11)).grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.entry_xlabel = ttk.Entry(frame_setting, width=18)
        self.entry_xlabel.grid(row=1, column=1, padx=5, pady=8)
        
        tk.Label(frame_setting, text="Y轴标签：", font=("微软雅黑", 11)).grid(row=1, column=2, padx=5, pady=8, sticky="w")
        self.entry_ylabel = ttk.Entry(frame_setting, width=18)
        self.entry_ylabel.grid(row=1, column=3, padx=5, pady=8)
        
        # 样式
        self.var_grid = tk.BooleanVar()
        chk_grid = ttk.Checkbutton(frame_setting, text="显示网格", variable=self.var_grid)
        chk_grid.grid(row=2, column=0, padx=5, pady=8, sticky="w")
        
        self.var_legend = tk.BooleanVar()
        chk_legend = ttk.Checkbutton(frame_setting, text="显示图例", variable=self.var_legend)
        chk_legend.grid(row=2, column=1, padx=5, pady=8)
        
        # 显示数值选项
        self.var_show_values = tk.BooleanVar()
        chk_show_values = ttk.Checkbutton(frame_setting, text="显示数值", variable=self.var_show_values)
        chk_show_values.grid(row=3, column=0, padx=5, pady=8, sticky="w")
        
        # ========== 第三部分：操作按钮区 ==========
        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=20)
        
        btn_example = ttk.Button(frame_btn, text="📌 填充示例数据", width=18, command=self.fill_example)
        btn_example.grid(row=0, column=0, padx=15)
        
        btn_plot = ttk.Button(frame_btn, text="🚀 一键绘制图表", width=18, command=self.plot_data)
        btn_plot.grid(row=0, column=1, padx=15)
        
        btn_clear = ttk.Button(frame_btn, text="🧹 清空所有数据", width=18, command=self.clear_all)
        btn_clear.grid(row=0, column=2, padx=15)
        
        # 作者信息
        tk.Label(self.root, text="作者：红鳍东方鲀", font=('微软雅黑', 9), fg="gray").pack(pady=5)
    
    # 初始化图表类型映射
    def _init_chart_mapping(self):
        """初始化图表类型到绘制函数的映射"""
        self.chart_mapping = {
            "折线图": self._plot_line,
            "柱状图": self._plot_bar,
            "散点图": self._plot_scatter,
            "误差棒图": self._plot_errorbar,
            "直方图": self._plot_hist,
            "饼图": self._plot_pie,
            "雷达图": self._plot_radar
        }
    
    # 核心绘图函数（灵活调用Matplotlib）
    def plot_data(self):
        try:
            # 1. 获取用户输入的X轴数据
            x_data = self._parse_data(self.entry_x.get(1.0, tk.END), str)

            # 2. 获取多个数据集的Y轴数据和误差数据
            datasets = []
            
            for i, frame in enumerate(self.dataset_frames):
                label = frame['label'].get().strip() or f"数据集 {i+1}"
                y_str = frame['y_data'].get(1.0, tk.END)
                err_str = frame['err_data'].get(1.0, tk.END)
                color = frame['color'].get().strip() or 'blue'  # 获取颜色设置
                
                if not y_str or y_str.strip() == '':
                    raise ValueError(f"请输入数据集 {i+1} 的Y轴数据")
                
                y_data = self._parse_data(y_str, float)
                error = self._parse_data(err_str, float) if err_str and err_str.strip() != '' else None
                
                # 验证数据长度
                if len(y_data) != len(x_data):
                    raise ValueError(f"数据集 {i+1} 的Y轴数据长度必须与X轴数据长度一致")
                if error and len(error) != len(y_data):
                    raise ValueError(f"数据集 {i+1} 的误差数据长度必须与Y轴数据长度一致")
                
                datasets.append({
                    'label': label,
                    'y_data': y_data,
                    'error': error,
                    'color': color
                })

            # 3. 获取样式设置
            title = self.entry_title.get()
            x_label = self.entry_xlabel.get()
            y_label = self.entry_ylabel.get()
            chart_type = self.combo_chart.get()
            show_grid = self.var_grid.get()
            show_legend = self.var_legend.get()
            show_values = self.var_show_values.get()

            # 4. 创建画布
            plt.figure(figsize=(10, 6))

            # 5. 根据选择的图表类型绘图（使用字典映射）
            if chart_type in self.chart_mapping:
                self.chart_mapping[chart_type](x_data, datasets, show_values)
            else:
                raise ValueError("不支持的图表类型")

            # 6. 统一设置图表样式
            if chart_type != "饼图" and chart_type != "雷达图":
                plt.title(title, fontsize=14)
                plt.xlabel(x_label, fontsize=12)
                plt.ylabel(y_label, fontsize=12)
                if show_grid:
                    plt.grid(linestyle='--', alpha=0.5)
                if show_legend:
                    plt.legend()

            # 7. 显示图表
            plt.tight_layout()
            plt.show()

        except ValueError as e:
            messagebox.showerror("错误", f"数据格式错误！\n错误信息：{str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误！\n错误信息：{str(e)}")
    
    # 折线图绘制（支持多个数据集和误差棒）
    def _plot_line(self, x_data, datasets, show_values=False):
        markers = ['o', 's', '^', 'v', 'D']
        for i, dataset in enumerate(datasets):
            if dataset['error']:
                plt.errorbar(x_data, dataset['y_data'], yerr=dataset['error'], fmt=f'-{markers[i%len(markers)]}', 
                            color=dataset['color'], capsize=5, label=dataset['label'])
            else:
                line, = plt.plot(x_data, dataset['y_data'], color=dataset['color'], linewidth=2, 
                         marker=markers[i%len(markers)], label=dataset['label'])
            
            # 显示数值
            if show_values:
                for j, (x, y) in enumerate(zip(x_data, dataset['y_data'])):
                    offset = dataset['error'][j] if dataset['error'] and j < len(dataset['error']) else 0
                    plt.text(x, y + offset + 0.05, f'{y:.2f}', ha='center', va='bottom', fontsize=8, color=dataset['color'])
    
    # 柱状图绘制（支持分组柱状图和误差棒）
    def _plot_bar(self, x_data, datasets, show_values=False):
        import numpy as np
        n = len(x_data)
        width = 0.8 / len(datasets)
        x_pos = np.arange(n)
        
        for i, dataset in enumerate(datasets):
            offset = (i - len(datasets)/2 + 0.5) * width
            if dataset['error']:
                bars = plt.bar(x_pos + offset, dataset['y_data'], width=width, color=dataset['color'], 
                        yerr=dataset['error'], capsize=3, label=dataset['label'])
            else:
                bars = plt.bar(x_pos + offset, dataset['y_data'], width=width, color=dataset['color'], 
                        label=dataset['label'])
            
            # 显示数值
            if show_values:
                for bar, val in zip(bars, dataset['y_data']):
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (dataset['error'][dataset['y_data'].index(val)] if dataset['error'] and dataset['y_data'].index(val) < len(dataset['error']) else 0) + 0.02,
                            f'{val:.2f}', ha='center', va='bottom', fontsize=8)
        
        plt.xticks(x_pos, x_data)
    
    # 散点图绘制（支持多个数据集）
    def _plot_scatter(self, x_data, datasets, show_values=False):
        markers = ['o', 's', '^', 'v', 'D']
        for i, dataset in enumerate(datasets):
            plt.scatter(x_data, dataset['y_data'], color=dataset['color'], 
                        marker=markers[i%len(markers)], s=50, label=dataset['label'])
            
            # 显示数值
            if show_values:
                for j, (x, y) in enumerate(zip(x_data, dataset['y_data'])):
                    plt.text(x, y + 0.05, f'{y:.2f}', ha='center', va='bottom', fontsize=8, color=dataset['color'])
    
    # 误差棒图绘制（支持多个数据集）
    def _plot_errorbar(self, x_data, datasets, show_values=False):
        markers = ['o', 's', '^', 'v', 'D']
        for i, dataset in enumerate(datasets):
            if not dataset['error']:
                raise ValueError(f"数据集 {i+1} 需要输入误差数据")
            plt.errorbar(x_data, dataset['y_data'], yerr=dataset['error'], 
                        fmt=f'-{markers[i%len(markers)]}', color=dataset['color'], 
                        capsize=5, label=dataset['label'])
            
            # 显示数值
            if show_values:
                for j, (x, y) in enumerate(zip(x_data, dataset['y_data'])):
                    plt.text(x, y + dataset['error'][j] + 0.05, f'{y:.2f}', ha='center', va='bottom', fontsize=8, color=dataset['color'])
    
    # 直方图绘制
    def _plot_hist(self, x_data, datasets, show_values=False):
        for i, dataset in enumerate(datasets):
            counts, bins, patches = plt.hist(dataset['y_data'], bins=8, alpha=0.6, color=dataset['color'], 
                    label=dataset['label'])
            
            # 显示数值
            if show_values:
                for count, patch in zip(counts, patches):
                    if count > 0:
                        plt.text(patch.get_x() + patch.get_width()/2, patch.get_height() + 0.1, 
                                f'{int(count)}', ha='center', va='bottom', fontsize=8, color=dataset['color'])
    
    # 饼图绘制
    def _plot_pie(self, x_data, datasets, show_values=False):
        if len(datasets) > 1:
            messagebox.showwarning("提示", "饼图只支持单个数据集！")
            return
        dataset = datasets[0]
        labels = self._process_pie_labels(x_data)
        wedges, texts, autotexts = plt.pie(dataset['y_data'], labels=labels, 
                colors=plt.cm.Paired(np.linspace(0,1,len(dataset['y_data']))), 
                autopct='%1.1f%%' if show_values else None)
        
        # 显示数值
        if show_values:
            for wedge, val in zip(wedges, dataset['y_data']):
                autotexts[list(wedges).index(wedge)].set_text(f'{val:.2f}')
    
    # 雷达图绘制（支持多个数据集）
    def _plot_radar(self, x_data, datasets):
        if len(x_data) < 3:
            messagebox.showwarning("提示", "雷达图需要至少3个数据点！")
            return
        
        num_vars = len(x_data)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        
        ax = plt.subplot(111, polar=True)
        
        for dataset in datasets:
            y_data = dataset['y_data'] + dataset['y_data'][:1]
            ax.plot(angles, y_data, color=dataset['color'], linewidth=2, marker='o', 
                    label=dataset['label'])
            ax.fill(angles, y_data, color=dataset['color'], alpha=0.25)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(x_data)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    # 数据解析函数
    def _parse_data(self, input_str, data_type):
        """解析输入字符串为指定类型的数据列表"""
        try:
            # 先处理空字符串情况
            if not input_str or input_str.strip() == '':
                raise ValueError("数据不能为空")
            
            # 处理空格、逗号和换行符的情况
            # 先将所有连续的空格、逗号和换行符替换为单个逗号
            import re
            processed_str = re.sub(r'[\s,\n\r]+', ',', input_str.strip())
            
            data = list(map(data_type, processed_str.split(',')))
            if not data:
                raise ValueError("数据不能为空")
            return data
        except ValueError as e:
            if "数据不能为空" in str(e):
                raise
            raise ValueError("请输入有效的数字，用空格或逗号分隔")
    
    # 数据验证函数
    def _validate_data(self, chart_type, x_data, y_data, error):
        """验证数据是否符合图表类型要求"""
        if chart_type == "雷达图":
            if len(x_data) < 3 or len(y_data) < 3:
                raise ValueError("雷达图需要至少3个数据点")
        elif chart_type != "直方图":
            if len(x_data) != len(y_data):
                raise ValueError("X轴和Y轴数据长度必须一致")
        
        if chart_type == "误差棒图":
            if error is None:
                raise ValueError("误差棒图需要输入误差数据")
            if len(error) != len(y_data):
                raise ValueError("误差数据长度必须与Y轴数据一致")
    
    # 饼图标签处理函数
    def _process_pie_labels(self, x_data):
        """处理饼图标签，确保标签为字符串类型"""
        labels = []
        for label in x_data:
            if isinstance(label, (int, float)):
                labels.append(str(label))
            else:
                labels.append(label)
        return labels
    
    # 一键填充示例数据（新手友好）
    def fill_example(self):
        # 设置数据集数量为4
        self.dataset_count.current(3)  # 索引3对应值4
        self._on_dataset_count_change(None)
        
        # 填充X轴数据
        self.entry_x.delete(1.0, tk.END)
        self.entry_x.insert(1.0, "0,2.5,5,7.5")
        
        # 填充数据集数据
        examples = [
            {"label": "0", "y_data": "0.2,1.1,0.95,0.55", "err_data": "0.05,0.1,0.08,0.06", "color": "blue"},
            {"label": "2.5", "y_data": "0.5,1.15,0.98,0.6", "err_data": "0.06,0.12,0.09,0.07", "color": "orange"},
            {"label": "5", "y_data": "0.48,1.0,0.96,0.58", "err_data": "0.05,0.11,0.08,0.06", "color": "green"},
            {"label": "7.5", "y_data": "0.45,0.95,0.94,0.56", "err_data": "0.04,0.1,0.07,0.05", "color": "red"}
        ]
        
        for i, example in enumerate(examples):
            if i < len(self.dataset_frames):
                frame = self.dataset_frames[i]
                frame['label'].delete(0, tk.END)
                frame['label'].insert(0, example["label"])
                frame['y_data'].delete(1.0, tk.END)
                frame['y_data'].insert(1.0, example["y_data"])
                frame['err_data'].delete(1.0, tk.END)
                frame['err_data'].insert(1.0, example["err_data"])
                color_options = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'cyan', 'yellow', 'black']
                frame['color'].current(color_options.index(example["color"]))
        
        # 填充其他设置
        self.entry_title.delete(0, tk.END)
        self.entry_title.insert(0, "多数据集示例")
        self.entry_xlabel.delete(0, tk.END)
        self.entry_xlabel.insert(0, "葡萄糖浓度 (g/L)")
        self.entry_ylabel.delete(0, tk.END)
        self.entry_ylabel.insert(0, "DCW (g/L)")
    
    # 清空所有数据
    def clear_all(self):
        """清空所有输入字段"""
        self.entry_x.delete(1.0, tk.END)
        for i, frame in enumerate(self.dataset_frames):
            frame['label'].delete(0, tk.END)
            frame['label'].insert(0, f"数据集 {i+1}")
            frame['y_data'].delete(1.0, tk.END)
            frame['err_data'].delete(1.0, tk.END)
            # 恢复默认颜色
            default_colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink']
            color_options = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'cyan', 'yellow', 'black']
            frame['color'].current(color_options.index(default_colors[i % len(default_colors)]))
        self.entry_title.delete(0, tk.END)
        self.entry_xlabel.delete(0, tk.END)
        self.entry_ylabel.delete(0, tk.END)
    
    # 图表类型切换事件处理
    def _on_chart_type_change(self, event):
        """处理图表类型切换事件，提供用户提示"""
        chart_type = self.combo_chart.get()
        if chart_type == "误差棒图":
            messagebox.showinfo("提示", "误差棒图需要输入误差数据，请在误差数据字段中填写相应数据")
        elif chart_type == "雷达图":
            messagebox.showinfo("提示", "雷达图需要至少3个数据点，请确保X轴和Y轴数据长度一致且不少于3个")
        elif chart_type == "饼图":
            messagebox.showinfo("提示", "饼图将使用X轴数据作为标签，Y轴数据作为数值")
        elif chart_type == "直方图":
            messagebox.showinfo("提示", "直方图只使用Y轴数据，X轴数据将被忽略")

# 运行主程序
def main():
    root = tk.Tk()
    app = DrawTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()