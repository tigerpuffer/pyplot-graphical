"""
测试保存图片功能
"""
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建测试图表
x = ['A', 'B', 'C', 'D', 'E']
y1 = [10, 15, 13, 17, 14]
y2 = [8, 12, 16, 11, 13]

plt.figure(figsize=(10, 6))
plt.plot(x, y1, 'o-', label='数据集1', color='blue', linewidth=2, markersize=8)
plt.plot(x, y2, 's-', label='数据集2', color='orange', linewidth=2, markersize=8)
plt.title('测试图表', fontsize=14)
plt.xlabel('X轴标签', fontsize=12)
plt.ylabel('Y轴标签', fontsize=12)
plt.grid(linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()

# 保存测试图片
test_file = 'test_output.png'
plt.savefig(test_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"测试图片已保存到: {test_file}")
print("保存功能正常工作！")

# 显示图表
plt.show()
