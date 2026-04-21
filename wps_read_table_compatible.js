/**
 * WPS表格宏 - 从已有表格读取数据并导出JSON配置
 * 用于Python绘图工具的配置导入
 *
 * 功能特点:
 * 1. 用对话框选择图表类型
 * 2. X轴可选择是否启用
 * 3. 网格、图例、数值用选项框配置
 * 4. 标签和数据通过选择单元格来配置
 */

// 全局变量存储配置
var g_chartType = "";
var g_enableXAxis = true;
var g_showGrid = true;
var g_showLegend = true;
var g_showValues = false;
var g_titleCell = "";
var g_xlabelCell = "";
var g_ylabelCell = "";
var g_xaxisCell = "";
var g_datasets = [];

/**
 * 主函数 - 启动配置向导
 */
function StartExportWizard() {
    try {
        var wb = Application.ActiveWorkbook;
        if (wb == null) {
            alert("请先打开一个WPS表格文件!");
            return;
        }

        // 重置配置
        ResetConfig();

        // 步骤1: 选择图表类型
        if (!SelectChartType()) {
            return;
        }

        // 步骤2: 配置基本选项
        if (!ConfigureBasicOptions()) {
            return;
        }

        // 步骤3: 选择标签单元格
        if (!SelectLabelCells()) {
            return;
        }

        // 步骤4: 配置X轴(如果启用)
        if (g_enableXAxis && !SelectXAxisCell()) {
            return;
        }

        // 步骤5: 添加数据集
        if (!ConfigureDatasets()) {
            return;
        }

        // 步骤6: 导出JSON
        ExportToJSON();

    } catch (e) {
        alert("发生错误: " + e.message);
    }
}

/**
 * 重置配置
 */
function ResetConfig() {
    g_chartType = "折线图";
    g_enableXAxis = true;
    g_showGrid = true;
    g_showLegend = true;
    g_showValues = false;
    g_titleCell = "";
    g_xlabelCell = "";
    g_ylabelCell = "";
    g_xaxisCell = "";
    g_datasets = [];
}

/**
 * 步骤1: 选择图表类型
 */
function SelectChartType() {
    var chartTypes = ["折线图", "柱状图", "散点图", "误差棒图", "直方图", "饼图", "雷达图"];
    var result = ShowSelectDialog(
        "步骤 1/5: 选择图表类型",
        "请选择要绘制的图表类型:",
        chartTypes,
        0
    );

    if (result == null) {
        return false;
    }

    g_chartType = result;
    return true;
}

/**
 * 步骤2: 配置基本选项
 */
function ConfigureBasicOptions() {
    var result = ShowBasicOptionsDialog();
    if (result == null) {
        return false;
    }

    g_enableXAxis = result.enableXAxis;
    g_showGrid = result.showGrid;
    g_showLegend = result.showLegend;
    g_showValues = result.showValues;

    return true;
}

/**
 * 步骤3: 选择标签单元格
 */
function SelectLabelCells() {
    alert("步骤 3/5: 选择标签单元格\n\n接下来将依次选择:\n1. 图表标题单元格\n2. X轴标签单元格\n3. Y轴标签单元格\n\n请点击确定后,用鼠标选择相应的单元格。");

    var titleCell = SelectCell("请选择图表标题所在的单元格");
    if (titleCell == null) return false;
    g_titleCell = titleCell;

    var xlabelCell = SelectCell("请选择X轴标签所在的单元格");
    if (xlabelCell == null) return false;
    g_xlabelCell = xlabelCell;

    var ylabelCell = SelectCell("请选择Y轴标签所在的单元格");
    if (ylabelCell == null) return false;
    g_ylabelCell = ylabelCell;

    return true;
}

/**
 * 步骤4: 选择X轴数据单元格(如果启用X轴)
 */
function SelectXAxisCell() {
    var xaxisCell = SelectCell("请选择X轴数据所在的单元格区域\n(可以是单个单元格或多个单元格)");
    if (xaxisCell == null) return false;
    g_xaxisCell = xaxisCell;
    return true;
}

/**
 * 步骤5: 配置数据集
 */
function ConfigureDatasets() {
    g_datasets = [];

    while (true) {
        var addMore = confirm("步骤 5/5: 配置数据集\n\n当前已添加 " + g_datasets.length + " 个数据集\n\n是否继续添加数据集?\n\n点击[确定]添加数据集\n点击[取消]完成配置");

        if (!addMore) {
            break;
        }

        var dataset = ConfigureSingleDataset(g_datasets.length + 1);
        if (dataset == null) {
            break;
        }

        g_datasets.push(dataset);
    }

    if (g_datasets.length == 0) {
        alert("至少需要添加一个数据集!");
        return false;
    }

    return true;
}

/**
 * 配置单个数据集
 */
function ConfigureSingleDataset(datasetIndex) {
    alert("配置数据集 #" + datasetIndex + "\n\n接下来将依次选择:\n1. 数据集标签单元格\n2. Y轴数据单元格区域\n3. 误差数据单元格区域(可选)\n4. 颜色(可选)\n\n请点击确定后,用鼠标选择相应的单元格。");

    var dataset = {};

    var labelCell = SelectCell("数据集 #" + datasetIndex + ": 请选择数据集标签所在的单元格");
    if (labelCell == null) return null;
    dataset.labelCell = labelCell;

    var ydataCell = SelectCell("数据集 #" + datasetIndex + ": 请选择Y轴数据所在的单元格区域");
    if (ydataCell == null) return null;
    dataset.ydataCell = ydataCell;

    var useError = confirm("数据集 #" + datasetIndex + ": 是否包含误差数据?\n\n点击[确定]选择误差数据\n点击[取消]跳过");
    if (useError) {
        var errdataCell = SelectCell("数据集 #" + datasetIndex + ": 请选择误差数据所在的单元格区域");
        if (errdataCell == null) return null;
        dataset.errdataCell = errdataCell;
    } else {
        dataset.errdataCell = "";
    }

    var colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "cyan", "yellow", "black"];
    var defaultColor = colors[datasetIndex % colors.length];
    var color = ShowSelectDialog(
        "数据集 #" + datasetIndex + ": 选择颜色(可选)",
        "请选择数据集的颜色:",
        colors,
        colors.indexOf(defaultColor)
    );

    if (color != null) {
        dataset.color = color;
    } else {
        dataset.color = defaultColor;
    }

    return dataset;
}

/**
 * 导出JSON文件
 */
function ExportToJSON() {
    try {
        var wb = Application.ActiveWorkbook;
        var ws = wb.ActiveSheet;

        var title = GetCellValue(ws, g_titleCell);
        var xlabel = GetCellValue(ws, g_xlabelCell);
        var ylabel = GetCellValue(ws, g_ylabelCell);

        var xaxisData = "";
        if (g_enableXAxis && g_xaxisCell) {
            xaxisData = GetRangeValues(ws, g_xaxisCell);
        }

        var datasets = [];
        var i;
        for (i = 0; i < g_datasets.length; i++) {
            var ds = g_datasets[i];
            var datasetConfig = {};
            datasetConfig.label = GetCellValue(ws, ds.labelCell);
            datasetConfig.y_data = GetRangeValues(ws, ds.ydataCell);
            datasetConfig.err_data = ds.errdataCell ? GetRangeValues(ws, ds.errdataCell) : "";
            datasetConfig.color = ds.color;
            datasets.push(datasetConfig);
        }

        var config = {};
        config.x_axis_data = xaxisData;
        config.chart_type = g_chartType;
        config.title = title;
        config.x_label = xlabel;
        config.y_label = ylabel;
        config.show_grid = g_showGrid;
        config.show_legend = g_showLegend;
        config.show_values = g_showValues;
        config.dataset_count = datasets.length;
        config.datasets = datasets;

        var jsonStr = JSON.stringify(config, null, 2);

        var fileDialog = Application.FileDialog(1);
        fileDialog.Title = "保存JSON配置文件";
        fileDialog.FilterIndex = 1;
        fileDialog.Filters.Clear();
        fileDialog.Filters.Add("JSON文件", "*.json");
        fileDialog.Filters.Add("所有文件", "*.*");

        if (fileDialog.Show() == -1) {
            var filePath = fileDialog.SelectedItems.Item(1);

            var fso = new ActiveXObject("Scripting.FileSystemObject");
            var file = fso.CreateTextFile(filePath, true, true);
            file.Write(jsonStr);
            file.Close();

            alert("配置文件已成功保存到:\n" + filePath + "\n\n现在可以在Python绘图工具中导入此文件!");
        }

    } catch (e) {
        alert("导出失败!\n错误信息: " + e.message);
    }
}

function ShowSelectDialog(title, prompt, options, selectedIndex) {
    var result = Application.InputBox(
        prompt + "\n\n请输入选项编号:\n" + GetOptionList(options),
        title,
        selectedIndex + 1
    );

    if (result == false) {
        return null;
    }

    var index = parseInt(result) - 1;
    if (index >= 0 && index < options.length) {
        return options[index];
    }

    return null;
}

function GetOptionList(options) {
    var list = "";
    var i;
    for (i = 0; i < options.length; i++) {
        list = list + (i + 1) + ". " + options[i] + "\n";
    }
    return list;
}

function ShowBasicOptionsDialog() {
    var result = {};

    var input1 = Application.InputBox("启用X轴数据?\n(输入1=是, 0=否)", "步骤 2/5: 配置基本选项", "1");
    if (input1 == false) return null;
    result.enableXAxis = (input1 == "1" || input1 == 1 || input1 == true);

    var input2 = Application.InputBox("显示网格?\n(输入1=是, 0=否)", "步骤 2/5: 配置基本选项", "1");
    if (input2 == false) return null;
    result.showGrid = (input2 == "1" || input2 == 1 || input2 == true);

    var input3 = Application.InputBox("显示图例?\n(输入1=是, 0=否)", "步骤 2/5: 配置基本选项", "1");
    if (input3 == false) return null;
    result.showLegend = (input3 == "1" || input3 == 1 || input3 == true);

    var input4 = Application.InputBox("显示数值?\n(输入1=是, 0=否)", "步骤 2/5: 配置基本选项", "0");
    if (input4 == false) return null;
    result.showValues = (input4 == "1" || input4 == 1 || input4 == true);

    return result;
}

function SelectCell(prompt) {
    Application.ScreenUpdating = false;
    var selectedRange = Application.InputBox(prompt, "选择单元格", 8);
    Application.ScreenUpdating = true;

    if (selectedRange == false || selectedRange == null) {
        return null;
    }

    return selectedRange.Address;
}

function GetCellValue(ws, address) {
    try {
        var cell = ws.Range(address);
        return cell.Value || "";
    } catch (e) {
        return "";
    }
}

function GetRangeValues(ws, address) {
    try {
        var range = ws.Range(address);
        var values = [];

        if (range.Cells.Count == 1) {
            return range.Value || "";
        } else {
            var i;
            for (i = 1; i <= range.Cells.Count; i++) {
                var val = range.Cells(i).Value;
                if (val != null && val != "") {
                    values.push(val);
                }
            }
            return values.join(",");
        }
    } catch (e) {
        return "";
    }
}

function QuickExport() {
    StartExportWizard();
}

function ShowHelp() {
    var helpText = "WPS表格宏 - 从已有表格导出JSON配置\n\n" +
                   "使用步骤:\n" +
                   "1. 运行 StartExportWizard 开始配置向导\n" +
                   "2. 按照提示选择图表类型和各种选项\n" +
                   "3. 用鼠标选择相应的单元格\n" +
                   "4. 添加一个或多个数据集\n" +
                   "5. 导出JSON文件\n\n" +
                   "注意事项:\n" +
                   "- 确保表格已打开\n" +
                   "- 数据格式要正确(数值用逗号分隔)\n" +
                   "- 误差数据是可选的\n" +
                   "- 颜色也是可选的\n\n" +
                   "函数列表:\n" +
                   "- StartExportWizard: 启动配置向导\n" +
                   "- ShowHelp: 显示帮助信息";

    alert(helpText);
}
