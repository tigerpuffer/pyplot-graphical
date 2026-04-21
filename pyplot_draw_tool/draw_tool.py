# 全能Matplotlib图形化绘图工具 —— 支持所有图表类型，零代码操作
# 作者：红鳍东方鲀
# 版本：1.1.0
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib.patches import RegularPolygon
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 自定义多边形雷达图投影
def radar_factory(num_vars, frame='polygon'):
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    
    class RadarAxes(PolarAxes):
        name = 'radar'
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            lines = super().plot(*args, **kwargs)
            for line in lines:
                x, y = line.get_data()
                if x[0] != x[-1]:
                    x = np.append(x, x[0])
                    y = np.append(y, y[0])
                    line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels, fontsize=16)

        def _gen_axes_patch(self):
            if frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'polygon':
                verts = unit_poly_verts(theta)
                verts.append(verts[0])
                path = Path(verts)
                spine = Spine(self, 'circle', path)
                spine.set_transform(self.transAxes)
                return {'circle': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    def unit_poly_verts(theta):
        x = 0.5 * np.cos(theta) + 0.5
        y = 0.5 * np.sin(theta) + 0.5
        return [(x[i], y[i]) for i in range(len(x))]

    register_projection(RadarAxes)
    return theta
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

        btn_save = ttk.Button(frame_btn, text="💾 保存图片", width=18, command=self.save_figure)
        btn_save.grid(row=0, column=2, padx=15)

        btn_clear = ttk.Button(frame_btn, text="🧹 清空所有数据", width=18, command=self.clear_all)
        btn_clear.grid(row=0, column=3, padx=15)

        # 配置管理按钮
        frame_config = tk.Frame(self.root)
        frame_config.pack(pady=10)

        btn_export = ttk.Button(frame_config, text="📤 导出配置", width=18, command=self.export_config)
        btn_export.grid(row=0, column=0, padx=15)

        btn_import = ttk.Button(frame_config, text="📥 导入配置", width=18, command=self.import_config)
        btn_import.grid(row=0, column=1, padx=15)
        
        # 作者信息
        tk.Label(self.root, text="作者：红鳍东方鲀", font=('微软雅黑', 9), fg="gray").pack(pady=5)
        tk.Label(self.root, text="版本：v1.0.3", font=('微软雅黑', 9), fg="gray").pack(pady=5)
    
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
            x_data_str = self.entry_x.get(1.0, tk.END)
            chart_type = self.combo_chart.get()
            
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
                
                datasets.append({
                    'label': label,
                    'y_data': y_data,
                    'error': error,
                    'color': color
                })

            # 3. 处理X轴数据
            if (chart_type == "柱状图" or chart_type == "误差棒图") and (not x_data_str or x_data_str.strip() == ''):
                # 对于柱状图和误差棒图，如果X轴数据为空，则使用数据集标签作为X轴
                x_data = [dataset['label'] for dataset in datasets]
                # 验证每个数据集的Y轴数据长度为1
                for i, dataset in enumerate(datasets):
                    if len(dataset['y_data']) != 1:
                        raise ValueError(f"当使用数据集标签作为X轴时，数据集 {i+1} 的Y轴数据长度必须为1")
                    if dataset['error'] and len(dataset['error']) != 1:
                        raise ValueError(f"当使用数据集标签作为X轴时，数据集 {i+1} 的误差数据长度必须为1")
            else:
                # 正常处理X轴数据
                x_data = self._parse_data(x_data_str, str)
                # 验证数据长度 - 对于柱状图和误差棒图，允许X轴数据与Y轴数据长度不一致
                for i, dataset in enumerate(datasets):
                    if chart_type not in ["柱状图", "误差棒图"] and len(dataset['y_data']) != len(x_data):
                        raise ValueError(f"数据集 {i+1} 的Y轴数据长度必须与X轴数据长度一致")
                    if dataset['error'] and len(dataset['error']) != len(dataset['y_data']):
                        raise ValueError(f"数据集 {i+1} 的误差数据长度必须与Y轴数据长度一致")

            # 4. 获取样式设置
            title = self.entry_title.get()
            x_label = self.entry_xlabel.get()
            y_label = self.entry_ylabel.get()
            show_grid = self.var_grid.get()
            show_legend = self.var_legend.get()
            show_values = self.var_show_values.get()

            # 5. 创建画布
            plt.figure(figsize=(10, 6))

            # 6. 根据选择的图表类型绘图（使用字典映射）
            if chart_type in self.chart_mapping:
                self.chart_mapping[chart_type](x_data, datasets, show_values)
            else:
                raise ValueError("不支持的图表类型")

            # 7. 统一设置图表样式
            if chart_type != "饼图" and chart_type != "雷达图":
                plt.title(title, fontsize=14)
                plt.xlabel(x_label, fontsize=12)
                plt.ylabel(y_label, fontsize=12)
                if show_grid:
                    plt.grid(linestyle='--', alpha=0.5)
                if show_legend:  # 允许所有图表类型显示图例
                    plt.legend()

            # 8. 显示图表
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
        
        # 检查是否是使用数据集标签作为X轴的情况
        if len(datasets) == n and all(len(dataset['y_data']) == 1 for dataset in datasets):
            # 使用数据集标签作为X轴时，每个数据集对应一个柱状图
            x_pos = np.arange(n)
            width = 0.8
            
            for i, dataset in enumerate(datasets):
                if dataset['error']:
                    bars = plt.bar(x_pos[i], dataset['y_data'][0], width=width, color=dataset['color'],
                            yerr=dataset['error'][0], capsize=3)
                else:
                    bars = plt.bar(x_pos[i], dataset['y_data'][0], width=width, color=dataset['color'])
                
                # 显示数值
                if show_values:
                    val = dataset['y_data'][0]
                    plt.text(x_pos[i], val + (dataset['error'][0] if dataset['error'] else 0) + 0.02,
                            f'{val:.2f}', ha='center', va='bottom', fontsize=8)
        else:
            # 检查是否所有数据集的Y轴数据长度相同
            if all(len(dataset['y_data']) == len(datasets[0]['y_data']) for dataset in datasets):
                # 检查Y轴数据长度是否与X轴数据长度相同
                if len(datasets[0]['y_data']) == n:
                    # 传统分组柱状图
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
                else:
                    # 新模式：每个X轴标签对应一组数据集
                    num_datasets = len(datasets)
                    width = 0.8 / num_datasets
                    
                    for i, x_label in enumerate(x_data):
                        x_pos = np.arange(len(datasets[0]['y_data'])) + i * (num_datasets * width + 0.2)
                        
                        for j, dataset in enumerate(datasets):
                            offset = j * width
                            if dataset['error']:
                                bars = plt.bar(x_pos + offset, dataset['y_data'], width=width, color=dataset['color'], 
                                        yerr=dataset['error'], capsize=3, label=dataset['label'] if i == 0 else "")
                            else:
                                bars = plt.bar(x_pos + offset, dataset['y_data'], width=width, color=dataset['color'], 
                                        label=dataset['label'] if i == 0 else "")
                            
                            # 显示数值
                            if show_values:
                                for bar, val in zip(bars, dataset['y_data']):
                                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (dataset['error'][dataset['y_data'].index(val)] if dataset['error'] and dataset['y_data'].index(val) < len(dataset['error']) else 0) + 0.02,
                                            f'{val:.2f}', ha='center', va='bottom', fontsize=8)
                    
                    # 设置X轴标签
                    plt.xticks(np.arange(len(x_data)) * (num_datasets * width + 0.2) + (num_datasets * width) / 2, x_data)
            else:
                # 传统分组柱状图
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
        
        # 检查是否是使用数据集标签作为X轴的情况
        if len(datasets) == len(x_data) and all(len(dataset['y_data']) == 1 for dataset in datasets):
            # 使用数据集标签作为X轴时，每个数据集对应一个误差棒
            x_pos = range(len(x_data))
            
            for i, dataset in enumerate(datasets):
                if not dataset['error']:
                    raise ValueError(f"数据集 {i+1} 需要输入误差数据")
                plt.errorbar(x_pos[i], dataset['y_data'][0], yerr=dataset['error'][0], 
                            fmt=f'-{markers[i%len(markers)]}', color=dataset['color'], 
                            capsize=5, label=dataset['label'] if i == 0 else "")
                
                # 显示数值
                if show_values:
                    y = dataset['y_data'][0]
                    plt.text(x_pos[i], y + dataset['error'][0] + 0.05, f'{y:.2f}', ha='center', va='bottom', fontsize=8, color=dataset['color'])
            
            plt.xticks(x_pos, x_data)
        else:
            # 传统误差棒图
            for i, dataset in enumerate(datasets):
                if not dataset['error']:
                    raise ValueError(f"数据集 {i+1} 需要输入误差数据")
                plt.errorbar(x_data, dataset['y_data'], yerr=dataset['error'], 
                            fmt=f'-{markers[i%len(markers)]}', color=dataset['color'], 
                            capsize=5, label=dataset['label'] if i == 0 else "")
                
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
    def _plot_radar(self, x_data, datasets, show_values=False):
        if len(x_data) < 3:
            messagebox.showwarning("提示", "雷达图需要至少3个数据点！")
            return
        
        num_vars = len(x_data)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # 闭合
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        # 设置径向轴范围
        max_value = max(max(dataset['y_data']) for dataset in datasets) if datasets else 1
        ax.set_ylim(0, max_value * 1.2)
        
        # 绘制每一组数据
        markers = ['s', 'o', '^', 'v', 'D']
        for i, dataset in enumerate(datasets):
            y_data = dataset['y_data'] + dataset['y_data'][:1]  # 闭合
            ax.plot(angles, y_data, color=dataset['color'], marker=markers[i%len(markers)],
                    markersize=10, linewidth=2, label=dataset['label'])
            ax.fill(angles, y_data, color=dataset['color'], alpha=0.25)
        
        # 设置轴标签
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(x_data)
        
        # 添加图例
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=12)
    
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

    # 保存图片功能
    def save_figure(self):
        """保存图表为高分辨率图片"""
        try:
            # 检查是否有活动的图表
            if not plt.get_fignums():
                messagebox.showwarning("提示", "请先绘制图表，然后再保存图片！")
                return

            # 创建保存文件对话框
            filetypes = [
                ('PNG 图片', '*.png'),
                ('JPG 图片', '*.jpg'),
                ('PDF 文档', '*.pdf'),
                ('SVG 矢量图', '*.svg'),
                ('TIF 图片', '*.tif'),
                ('EPS 文档', '*.eps'),
                ('所有文件', '*.*')
            ]

            file_path = filedialog.asksaveasfilename(
                title="保存图表",
                defaultextension='.png',
                filetypes=filetypes
            )

            if not file_path:
                return  # 用户取消了保存

            # 根据文件扩展名确定保存格式
            file_ext = file_path.split('.')[-1].lower()

            # 创建分辨率选择对话框
            dpi_dialog = tk.Toplevel(self.root)
            dpi_dialog.title("设置图片分辨率")
            dpi_dialog.geometry("400x320")
            dpi_dialog.resizable(False, False)

            # 居中显示对话框
            dpi_dialog.transient(self.root)
            dpi_dialog.grab_set()

            tk.Label(dpi_dialog, text="选择图片分辨率 (DPI):", font=("微软雅黑", 11)).pack(pady=15)

            dpi_var = tk.IntVar(value=300)
            dpi_options = [
                ("屏幕质量 (72 DPI)", 72),
                ("标准质量 (150 DPI)", 150),
                ("高质量 (300 DPI)", 300),
                ("超高质量 (600 DPI)", 600),
                ("打印质量 (1200 DPI)", 1200)
            ]

            for text, value in dpi_options:
                tk.Radiobutton(dpi_dialog, text=text, variable=dpi_var, value=value,
                              font=("微软雅黑", 10)).pack(anchor="w", padx=30, pady=2)

            # 自定义DPI选项
            frame_custom = tk.Frame(dpi_dialog)
            frame_custom.pack(pady=10, padx=20)
            tk.Label(frame_custom, text="自定义:", font=("微软雅黑", 10)).pack(side="left")
            custom_dpi = ttk.Entry(frame_custom, width=8)
            custom_dpi.pack(side="left", padx=5)
            tk.Label(frame_custom, text="DPI", font=("微软雅黑", 10)).pack(side="left")

            # 保存和取消按钮
            btn_frame = tk.Frame(dpi_dialog)
            btn_frame.pack(pady=20)

            save_result = {'confirmed': False}

            def confirm_save():
                try:
                    if custom_dpi.get().strip():
                        custom_dpi_value = int(custom_dpi.get())
                        if custom_dpi_value < 10 or custom_dpi_value > 5000:
                            messagebox.showerror("错误", "DPI值必须在10到5000之间！")
                            return
                        dpi = custom_dpi_value
                    else:
                        dpi = dpi_var.get()

                    # 保存图片
                    plt.savefig(file_path, dpi=dpi, bbox_inches='tight',
                               facecolor='white', edgecolor='none')
                    save_result['confirmed'] = True
                    dpi_dialog.destroy()
                    messagebox.showinfo("成功", f"图表已成功保存到:\n{file_path}")
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的数字！")
                except Exception as e:
                    messagebox.showerror("错误", f"保存失败：{str(e)}")

            def cancel_save():
                dpi_dialog.destroy()

            ttk.Button(btn_frame, text="保存", width=10, command=confirm_save).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="取消", width=10, command=cancel_save).pack(side="left", padx=5)

            # 等待对话框关闭
            self.root.wait_window(dpi_dialog)

        except Exception as e:
            messagebox.showerror("错误", f"保存图片时发生错误：{str(e)}")

    # 导出配置功能
    def export_config(self):
        """导出当前绘图配置到JSON文件"""
        try:
            # 收集所有配置数据
            config = {
                "x_axis_data": self.entry_x.get(1.0, tk.END).strip(),
                "chart_type": self.combo_chart.get(),
                "title": self.entry_title.get(),
                "x_label": self.entry_xlabel.get(),
                "y_label": self.entry_ylabel.get(),
                "show_grid": self.var_grid.get(),
                "show_legend": self.var_legend.get(),
                "show_values": self.var_show_values.get(),
                "dataset_count": self.dataset_count.get(),
                "datasets": []
            }

            # 收集每个数据集的配置
            for i, frame in enumerate(self.dataset_frames):
                dataset_config = {
                    "label": frame['label'].get(),
                    "y_data": frame['y_data'].get(1.0, tk.END).strip(),
                    "err_data": frame['err_data'].get(1.0, tk.END).strip(),
                    "color": frame['color'].get()
                }
                config["datasets"].append(dataset_config)

            # 保存文件对话框
            file_path = filedialog.asksaveasfilename(
                title="导出配置",
                defaultextension='.json',
                filetypes=[('JSON 配置文件', '*.json'), ('所有文件', '*.*')]
            )

            if not file_path:
                return  # 用户取消了保存

            # 写入JSON文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("成功", f"配置已成功导出到:\n{file_path}")

        except Exception as e:
            messagebox.showerror("错误", f"导出配置时发生错误：{str(e)}")

    # 导入配置功能
    def import_config(self):
        """从JSON文件导入绘图配置"""
        try:
            # 打开文件对话框
            file_path = filedialog.askopenfilename(
                title="导入配置",
                filetypes=[('JSON 配置文件', '*.json'), ('所有文件', '*.*')]
            )

            if not file_path:
                return  # 用户取消了导入

            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 验证配置文件格式
            required_keys = ['x_axis_data', 'chart_type', 'title', 'x_label', 'y_label',
                           'show_grid', 'show_legend', 'show_values', 'dataset_count', 'datasets']
            for key in required_keys:
                if key not in config:
                    messagebox.showerror("错误", f"配置文件格式错误：缺少 {key}")
                    return

            # 恢复图表类型
            if config['chart_type'] in self.chart_types:
                self.combo_chart.current(self.chart_types.index(config['chart_type']))

            # 恢复标题和标签
            self.entry_title.delete(0, tk.END)
            self.entry_title.insert(0, config['title'])
            self.entry_xlabel.delete(0, tk.END)
            self.entry_xlabel.insert(0, config['x_label'])
            self.entry_ylabel.delete(0, tk.END)
            self.entry_ylabel.insert(0, config['y_label'])

            # 恢复复选框状态
            self.var_grid.set(config['show_grid'])
            self.var_legend.set(config['show_legend'])
            self.var_show_values.set(config['show_values'])

            # 恢复X轴数据
            self.entry_x.delete(1.0, tk.END)
            self.entry_x.insert(1.0, config['x_axis_data'])

            # 恢复数据集数量
            dataset_count = int(config['dataset_count'])
            if dataset_count in [1, 2, 3, 4, 5, 6, 7]:
                self.dataset_count.current(dataset_count - 1)
                self._on_dataset_count_change(None)

                # 恢复每个数据集的配置
                for i, dataset_config in enumerate(config['datasets']):
                    if i < len(self.dataset_frames):
                        frame = self.dataset_frames[i]
                        frame['label'].delete(0, tk.END)
                        frame['label'].insert(0, dataset_config['label'])
                        frame['y_data'].delete(1.0, tk.END)
                        frame['y_data'].insert(1.0, dataset_config['y_data'])
                        frame['err_data'].delete(1.0, tk.END)
                        frame['err_data'].insert(1.0, dataset_config['err_data'])

                        # 恢复颜色
                        color = dataset_config['color']
                        color_options = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'cyan', 'yellow', 'black']
                        if color in color_options:
                            frame['color'].current(color_options.index(color))

            messagebox.showinfo("成功", f"配置已成功导入！\n现在可以点击\"一键绘制图表\"按钮来绘制图表")

        except json.JSONDecodeError:
            messagebox.showerror("错误", "配置文件格式错误，不是有效的JSON文件")
        except Exception as e:
            messagebox.showerror("错误", f"导入配置时发生错误：{str(e)}")

# 运行主程序
def main():
    root = tk.Tk()
    app = DrawTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()