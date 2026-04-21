"""
测试配置导出和导入功能
"""
import json

# 创建一个模拟的配置数据
test_config = {
    "x_axis_data": "0,2.5,5,7.5",
    "chart_type": "折线图",
    "title": "多数据集示例",
    "x_label": "葡萄糖浓度 (g/L)",
    "y_label": "DCW (g/L)",
    "show_grid": True,
    "show_legend": True,
    "show_values": True,
    "dataset_count": 4,
    "datasets": [
        {
            "label": "0",
            "y_data": "0.2,1.1,0.95,0.55",
            "err_data": "0.05,0.1,0.08,0.06",
            "color": "blue"
        },
        {
            "label": "2.5",
            "y_data": "0.5,1.15,0.98,0.6",
            "err_data": "0.06,0.12,0.09,0.07",
            "color": "orange"
        },
        {
            "label": "5",
            "y_data": "0.48,1.0,0.96,0.58",
            "err_data": "0.05,0.11,0.08,0.06",
            "color": "green"
        },
        {
            "label": "7.5",
            "y_data": "0.45,0.95,0.94,0.56",
            "err_data": "0.04,0.1,0.07,0.05",
            "color": "red"
        }
    ]
}

# 测试导出配置
test_file = 'test_config.json'
try:
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_config, f, ensure_ascii=False, indent=2)
    print(f"[OK] 配置文件已成功导出到: {test_file}")

    # 测试导入配置
    with open(test_file, 'r', encoding='utf-8') as f:
        loaded_config = json.load(f)

    print("[OK] 配置文件已成功导入")
    print("\n导入的配置内容:")
    print(f"  - 图表类型: {loaded_config['chart_type']}")
    print(f"  - 标题: {loaded_config['title']}")
    print(f"  - 数据集数量: {loaded_config['dataset_count']}")
    print(f"  - 数据集:")
    for i, dataset in enumerate(loaded_config['datasets']):
        print(f"    {i+1}. {dataset['label']} - {dataset['color']}")

    # 验证数据完整性
    if loaded_config == test_config:
        print("\n[OK] 导出和导入的数据完全一致！")
    else:
        print("\n[WARNING] 导出和导入的数据不一致")

except Exception as e:
    print(f"[ERROR] 错误: {str(e)}")
