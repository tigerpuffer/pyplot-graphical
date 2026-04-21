# PyPlot Draw Tool

A user-friendly GUI tool for creating various types of charts with Matplotlib. No coding required!

## Features

- **Multiple Chart Types**: Line charts, bar charts, scatter plots, error bar charts, histograms, pie charts, and radar charts
- **Multiple Datasets**: Support for 1-5 datasets with custom labels
- **Error Bars**: Add error bars to your data
- **Customization**: Title, labels, grid, legend, and value display options
- **User-Friendly Interface**: Intuitive GUI with example data
- **Value Display**: Option to show exact values on the chart

## Installation

```bash
pip install pyplot-draw-tool
```

## Usage

### Command Line

```bash
pyplot-draw-tool
```

### Python

```python
from pyplot_draw_tool.draw_tool import main
main()
```

## How to Use

1. **Select Dataset Count**: Choose how many datasets you want to plot (1-5)
2. **Enter X-axis Data**: Input category names separated by commas
3. **Enter Dataset Data**: For each dataset, enter:
   - Label: Name of the dataset
   - Y-axis Data: Numeric values separated by commas
   - Error Data: Optional error values separated by commas
4. **Chart Settings**:
   - Chart Type: Select the type of chart you want
   - Title: Enter a title for your chart
   - X-axis Label: Label for the X-axis
   - Y-axis Label: Label for the Y-axis
   - Show Grid: Check to display grid lines
   - Show Legend: Check to display legend
   - Show Values: Check to display exact values on the chart
5. **Draw Chart**: Click the "🚀 一键绘制图表" button to generate your chart

## Example

```
# X-axis data
叶绿素a,叶绿素b,类胡萝卜素

# Dataset 1 (label: 0)
Y-axis: 9.0477,0.0,7.9016
Error: 0.5,0,0.5

# Dataset 2 (label: 2.5)
Y-axis: 1.2331,0.0,1.2603
Error: 0.1,0,0.1

# Dataset 3 (label: 5)
Y-axis: 0.9578,0.0,0.9676
Error: 0.1,0,0.1

# Dataset 4 (label: 7.5)
Y-axis: 0.5673,0.0,0.6878
Error: 0.1,0,0.1
```

## Requirements

- Python 3.6+
- Matplotlib
- NumPy
- Tkinter (comes with Python)

## License

MIT License
