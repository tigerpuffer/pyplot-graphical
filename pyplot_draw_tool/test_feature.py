#!/usr/bin/env python3
# 测试柱状图使用数据集标签代替X轴的功能

import tkinter as tk
from draw_tool import DrawTool

# 创建测试函数
def test_bar_with_dataset_labels():
    root = tk.Tk()
    app = DrawTool(root)
    
    # 设置为柱状图
    app.combo_chart.current(1)  # 1对应柱状图
    
    # 设置数据集数量为3
    app.dataset_count.current(2)  # 2对应3个数据集
    app._on_dataset_count_change(None)
    
    # 清空X轴数据
    app.entry_x.delete(1.0, tk.END)
    
    # 设置数据集标签和Y轴数据
    datasets = [
        {"label": "A", "y_data": "10"},
        {"label": "B", "y_data": "20"},
        {"label": "C", "y_data": "15"}
    ]
    
    for i, data in enumerate(datasets):
        frame = app.dataset_frames[i]
        frame['label'].delete(0, tk.END)
        frame['label'].insert(0, data["label"])
        frame['y_data'].delete(1.0, tk.END)
        frame['y_data'].insert(1.0, data["y_data"])
    
    # 设置图表标题和标签
    app.entry_title.delete(0, tk.END)
    app.entry_title.insert(0, "测试：使用数据集标签作为X轴")
    app.entry_xlabel.delete(0, tk.END)
    app.entry_xlabel.insert(0, "类别")
    app.entry_ylabel.delete(0, tk.END)
    app.entry_ylabel.insert(0, "数值")
    
    # 显示数值
    app.var_show_values.set(True)
    
    print("测试准备完成，点击'一键绘制图表'按钮查看结果")
    print("预期结果：三个柱状图，分别对应标签A、B、C，颜色不同")
    
    root.mainloop()

if __name__ == "__main__":
    test_bar_with_dataset_labels()
