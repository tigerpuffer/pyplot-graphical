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
var globalConfig = {
    chartType: "",
    enableXAxis: true,
    showGrid: true,
    showLegend: true,
    showValues: false,
    titleCell: "",
    xlabelCell: "",
    ylabelCell: "",
    xaxisCell: "",
    datasets: []
};

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
        resetConfig();

        // 步骤1: 选择图表类型
        if (!selectChartType()) {
            return; // 用户取消
        }

        // 步骤2: 配置基本选项
        if (!configureBasicOptions()) {
            return; // 用户取消
        }

        // 步骤3: 选择标签单元格
        if (!selectLabelCells()) {
            return; // 用户取消
        }

        // 步骤4: 配置X轴(如果启用)
        if (globalConfig.enableXAxis && !selectXAxisCell()) {
            return; // 用户取消
        }

        // 步骤5: 添加数据集
        if (!configureDatasets()) {
            return; // 用户取消
        }

        // 步骤6: 导出JSON
        exportToJSON();

    } catch (e) {
        alert("发生错误: " + e.message);
    }
}

/**
 * 重置配置
 */
function resetConfig() {
    globalConfig = {
        chartType: "折线图",
        enableXAxis: true,
        showGrid: true,
        showLegend: true,
        showValues: false,
        titleCell: "",
        xlabelCell: "",
        ylabelCell: "",
        xaxisCell: "",
        datasets: []
    };
}

/**
 * 步骤1: 选择图表类型
 */
function selectChartType() {
    var chartTypes = ["折线图", "柱状图", "散点图", "误差棒图", "直方图", "饼图", "雷达图"];
    var result = showSelectDialog(
        "步骤 1/5: 选择图表类型",
        "请选择要绘制的图表类型:",
        chartTypes,
        0
    );

    if (result == null) {
        return false; // 用户取消
    }

    globalConfig.chartType = result;
    return true;
}

/**
 * 步骤2: 配置基本选项
 */
function configureBasicOptions() {
    var form = createBasicOptionsForm();
    var result = showFormDialog(
        "步骤 2/5: 配置基本选项",
        form
    );

    if (result == null) {
        return false; // 用户取消
    }

    globalConfig.enableXAxis = result.enableXAxis;
    globalConfig.showGrid = result.showGrid;
    globalConfig.showLegend = result.showLegend;
    globalConfig.showValues = result.showValues;

    return true;
}

/**
 * 步骤3: 选择标签单元格
 */
function selectLabelCells() {
    alert("步骤 3/5: 选择标签单元格\n\n接下来将依次选择:\n1. 图表标题单元格\n2. X轴标签单元格\n3. Y轴标签单元格\n\n请点击确定后,用鼠标选择相应的单元格。");

    // 选择图表标题
    var titleCell = selectCell("请选择图表标题所在的单元格");
    if (titleCell == null) return false;
    globalConfig.titleCell = titleCell;

    // 选择X轴标签
    var xlabelCell = selectCell("请选择X轴标签所在的单元格");
    if (xlabelCell == null) return false;
    globalConfig.xlabelCell = xlabelCell;

    // 选择Y轴标签
    var ylabelCell = selectCell("请选择Y轴标签所在的单元格");
    if (ylabelCell == null) return false;
    globalConfig.ylabelCell = ylabelCell;

    return true;
}

/**
 * 步骤4: 选择X轴数据单元格(如果启用X轴)
 */
function selectXAxisCell() {
    var xaxisCell = selectCell("请选择X轴数据所在的单元格区域\n(可以是单个单元格或多个单元格)");
    if (xaxisCell == null) return false;
    globalConfig.xaxisCell = xaxisCell;
    return true;
}

/**
 * 步骤5: 配置数据集
 */
function configureDatasets() {
    globalConfig.datasets = [];

    while (true) {
        var addMore = confirm("步骤 5/5: 配置数据集\n\n当前已添加 " + globalConfig.datasets.length + " 个数据集\n\n是否继续添加数据集?\n\n点击[确定]添加数据集\n点击[取消]完成配置");

        if (!addMore) {
            break;
        }

        var dataset = configureSingleDataset(globalConfig.datasets.length + 1);
        if (dataset == null) {
            break; // 用户取消添加
        }

        globalConfig.datasets.push(dataset);
    }

    if (globalConfig.datasets.length == 0) {
        alert("至少需要添加一个数据集!");
        return false;
    }

    return true;
}

/**
 * 配置单个数据集
 */
function configureSingleDataset(datasetIndex) {
    alert("配置数据集 #" + datasetIndex + "\n\n接下来将依次选择:\n1. 数据集标签单元格\n2. Y轴数据单元格区域\n3. 误差数据单元格区域(可选)\n4. 颜色(可选)\n\n请点击确定后,用鼠标选择相应的单元格。");

    var dataset = {};

    // 选择数据集标签
    var labelCell = selectCell("数据集 #" + datasetIndex + ": 请选择数据集标签所在的单元格");
    if (labelCell == null) return null;
    dataset.labelCell = labelCell;

    // 选择Y轴数据
    var ydataCell = selectCell("数据集 #" + datasetIndex + ": 请选择Y轴数据所在的单元格区域");
    if (ydataCell == null) return null;
    dataset.ydataCell = ydataCell;

    // 选择误差数据(可选)
    var useError = confirm("数据集 #" + datasetIndex + ": 是否包含误差数据?\n\n点击[确定]选择误差数据\n点击[取消]跳过");
    if (useError) {
        var errdataCell = selectCell("数据集 #" + datasetIndex + ": 请选择误差数据所在的单元格区域");
        if (errdataCell == null) return null;
        dataset.errdataCell = errdataCell;
    } else {
        dataset.errdataCell = "";
    }

    // 选择颜色(可选)
    var colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "cyan", "yellow", "black"];
    var defaultColor = colors[datasetIndex % colors.length];
    var color = showSelectDialog(
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
function exportToJSON() {
    try {
        var wb = Application.ActiveWorkbook;
        var ws = wb.ActiveSheet;

        // 读取单元格数据
        var title = getCellValue(ws, globalConfig.titleCell);
        var xlabel = getCellValue(ws, globalConfig.xlabelCell);
        var ylabel = getCellValue(ws, globalConfig.ylabelCell);

        // 读取X轴数据
        var xaxisData = "";
        if (globalConfig.enableXAxis && globalConfig.xaxisCell) {
            xaxisData = getRangeValues(ws, globalConfig.xaxisCell);
        }

        // 读取数据集数据
        var datasets = [];
        for (var i = 0; i < globalConfig.datasets.length; i++) {
            var ds = globalConfig.datasets[i];
            var datasetConfig = {
                "label": getCellValue(ws, ds.labelCell),
                "y_data": getRangeValues(ws, ds.ydataCell),
                "err_data": ds.errdataCell ? getRangeValues(ws, ds.errdataCell) : "",
                "color": ds.color
            };
            datasets.push(datasetConfig);
        }

        // 构建配置对象
        var config = {
            "x_axis_data": xaxisData,
            "chart_type": globalConfig.chartType,
            "title": title,
            "x_label": xlabel,
            "y_label": ylabel,
            "show_grid": globalConfig.showGrid,
            "show_legend": globalConfig.showLegend,
            "show_values": globalConfig.showValues,
            "dataset_count": datasets.length,
            "datasets": datasets
        };

        // 转换为JSON字符串
        var jsonStr = JSON.stringify(config, null, 2);

        // 选择保存路径
        var fileDialog = Application.FileDialog(msoFileDialogSaveAs);
        fileDialog.Title = "保存JSON配置文件";
        fileDialog.FilterIndex = 1;
        fileDialog.Filters.Clear();
        fileDialog.Filters.Add("JSON文件", "*.json");
        fileDialog.Filters.Add("所有文件", "*.*");

        if (fileDialog.Show() == -1) {
            var filePath = fileDialog.SelectedItems.Item(1);

            // 写入文件
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

// ==================== 辅助函数 ====================

/**
 * 显示选择对话框
 */
function showSelectDialog(title, prompt, options, selectedIndex) {
    var result = Application.InputBox(
        prompt + "\n\n请输入选项编号:\n" + getOptionList(options),
        title,
        selectedIndex + 1
    );

    if (result == false) {
        return null; // 用户取消
    }

    var index = parseInt(result) - 1;
    if (index >= 0 && index < options.length) {
        return options[index];
    }

    return null;
}

/**
 * 获取选项列表字符串
 */
function getOptionList(options) {
    var list = "";
    for (var i = 0; i < options.length; i++) {
        list += (i + 1) + ". " + options[i] + "\n";
    }
    return list;
}

/**
 * 创建基本选项表单
 */
function createBasicOptionsForm() {
    return {
        "enableXAxis": {type: "checkbox", label: "启用X轴数据", default: true},
        "showGrid": {type: "checkbox", label: "显示网格", default: true},
        "showLegend": {type: "checkbox", label: "显示图例", default: true},
        "showValues": {type: "checkbox", label: "显示数值", default: false}
    };
}

/**
 * 显示表单对话框(简化版)
 */
function showFormDialog(title, form) {
    var prompt = title + "\n\n请输入以下选项(1=是, 0=否):\n";

    var fields = [];
    for (var key in form) {
        fields.push(key);
        prompt += "\n" + form[key].label + " [" + (form[key].default ? "1" : "0") + "]:";
    }

    var result = {};
    for (var i = 0; i < fields.length; i++) {
        var field = fields[i];
        var fieldConfig = form[field];
        var input = Application.InputBox(fieldConfig.label + "\n(输入1=是, 0=否)", title, fieldConfig.default ? "1" : "0");

        if (input == false) {
            return null; // 用户取消
        }

        result[field] = (input == "1" || input == 1 || input == true);
    }

    return result;
}

/**
 * 选择单元格
 */
function selectCell(prompt) {
    Application.ScreenUpdating = false;
    var selectedRange = Application.InputBox(
        prompt,
        "选择单元格",
        Type: 8
    );
    Application.ScreenUpdating = true;

    if (selectedRange == false || selectedRange == null) {
        return null; // 用户取消
    }

    return selectedRange.Address;
}

/**
 * 获取单元格值
 */
function getCellValue(ws, address) {
    try {
        var cell = ws.Range(address);
        return cell.Value || "";
    } catch (e) {
        return "";
    }
}

/**
 * 获取单元格区域值
 */
function getRangeValues(ws, address) {
    try {
        var range = ws.Range(address);
        var values = [];

        if (range.Cells.Count == 1) {
            // 单个单元格
            return range.Value || "";
        } else {
            // 多个单元格
            for (var i = 1; i <= range.Cells.Count; i++) {
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

// ==================== 快捷函数 ====================

/**
 * 快速导出(使用默认设置)
 */
function QuickExport() {
    StartExportWizard();
}

/**
 * 显示帮助信息
 */
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
