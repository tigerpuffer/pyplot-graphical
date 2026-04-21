#!/usr/bin/env python3
# 测试误差棒图使用数据集标签代替X轴的功能

import tkinter as tk
from draw_tool import DrawTool

# 创建测试函数
def test_errorbar_with_dataset_labels():
    root = tk.Tk()
    app = DrawTool(root)
    
    # 设置为误差棒图
    app.combo_chart.current(3)  # 3对应误差棒图
    
    # 设置数据集数量为3
    app.dataset_count.current(2)  # 2对应3个数据集
    app._on_dataset_count_change(None)
    
    # 清空X轴数据
    app.entry_x.delete(1.0, tk.END)
    
    # 设置数据集标签、Y轴数据和误差数据
    datasets = [
        {"label": "A", "y_data": "10", "err_data": "1"},
        {"label": "B", "y_data": "20", "err_data": "1.5"},
        {"label": "C", "y_data": "15", "err_data": "0.8"}
    ]
    
    for i, data in enumerate(datasets):
        frame = app.dataset_frames[i]
        frame['label'].delete(0, tk.END)
        frame['label'].insert(0, data["label"])
        frame['y_data'].delete(1.0, tk.END)
        frame['y_data'].insert(1.0, data["y_data"])
        frame['err_data'].delete(1.0, tk.END)
        frame['err_data'].insert(1.0, data["err_data"])
    
    # 设置图表标题和标签
    app.entry_title.delete(0, tk.END)
    app.entry_title.insert(0, "测试：使用数据集标签作为X轴的误差棒图")
    app.entry_xlabel.delete(0, tk.END)
    app.entry_xlabel.insert(0, "类别")
    app.entry_ylabel.delete(0, tk.END)
    app.entry_ylabel.insert(0, "数值")
    
    # 显示数值
    app.var_show_values.set(True)
    
    print("测试准备完成，点击'一键绘制图表'按钮查看结果")
    print("预期结果：三个误差棒，分别对应标签A、B、C，颜色不同")
    
    root.mainloop()

if __name__ == "__main__":
    test_errorbar_with_dataset_labels()
