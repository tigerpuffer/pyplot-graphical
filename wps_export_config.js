/**
 * WPS表格宏 - 导出数据为JSON配置文件
 * 用于Python绘图工具的配置导入
 *
 * 使用说明:
 * 1. 在WPS表格中按以下格式组织数据:
 *    - Sheet1: 基本设置
 *    - Sheet2: 数据集数据
 * 2. 运行此宏即可生成JSON配置文件
 */

function ExportToJSON() {
    try {
        var wb = Application.ActiveWorkbook;
        if (wb == null) {
            alert("请先打开一个WPS表格文件!");
            return;
        }

        // 获取工作表
        var sheetConfig = wb.Sheets.Item("基本设置");
        var sheetData = wb.Sheets.Item("数据集");

        if (sheetConfig == null || sheetData == null) {
            alert("缺少必要的工作表!\n请确保存在'基本设置'和'数据集'两个工作表");
            return;
        }

        // 读取基本设置
        var x_axis_data = sheetConfig.Range("B2").Value || "";
        var chart_type = sheetConfig.Range("B3").Value || "折线图";
        var title = sheetConfig.Range("B4").Value || "";
        var x_label = sheetConfig.Range("B5").Value || "";
        var y_label = sheetConfig.Range("B6").Value || "";
        var show_grid = (sheetConfig.Range("B7").Value == "是" || sheetConfig.Range("B7").Value == true);
        var show_legend = (sheetConfig.Range("B8").Value == "是" || sheetConfig.Range("B8").Value == true);
        var show_values = (sheetConfig.Range("B9").Value == "是" || sheetConfig.Range("B9").Value == true);

        // 读取数据集数据
        var datasets = [];
        var row = 2; // 从第2行开始读取数据(第1行是标题)

        while (true) {
            var label = sheetData.Range("A" + row).Value;
            var y_data = sheetData.Range("B" + row).Value;
            var err_data = sheetData.Range("C" + row).Value;
            var color = sheetData.Range("D" + row).Value;

            // 如果标签为空,说明数据读取完毕
            if (label == null || label == "") {
                break;
            }

            // 添加数据集
            datasets.push({
                "label": label || "",
                "y_data": y_data || "",
                "err_data": err_data || "",
                "color": color || "blue"
            });

            row++;
        }

        // 构建配置对象
        var config = {
            "x_axis_data": x_axis_data,
            "chart_type": chart_type,
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "show_grid": show_grid,
            "show_legend": show_legend,
            "show_values": show_values,
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

        if (fileDialog.Show() == -1) { // 用户点击了保存按钮
            var filePath = fileDialog.SelectedItems.Item(1);

            // 写入文件
            var fso = new ActiveXObject("Scripting.FileSystemObject");
            var file = fso.CreateTextFile(filePath, true, true); // true=overwrite, true=unicode
            file.Write(jsonStr);
            file.Close();

            alert("配置文件已成功保存到:\n" + filePath);
        }

    } catch (e) {
        alert("导出失败!\n错误信息: " + e.message);
    }
}

/**
 * 创建示例数据模板
 * 运行此函数可以在当前工作簿中创建示例数据
 */
function CreateTemplate() {
    try {
        var wb = Application.ActiveWorkbook;
        var ws;

        // 创建"基本设置"工作表
        try {
            ws = wb.Sheets.Add();
            ws.Name = "基本设置";
        } catch (e) {
            ws = wb.Sheets.Item("基本设置");
        }

        // 设置标题
        ws.Range("A1:B1").Merge();
        ws.Range("A1").Value = "基本设置";
        ws.Range("A1").Font.Bold = true;
        ws.Range("A1").Font.Size = 14;
        ws.Range("A1").Interior.Color = 4210752; // RGB(64,64,64)
        ws.Range("A1").Font.Color = 16777215; // 白色

        // 设置列标题
        ws.Range("A2:A9").Value = [
            "X轴数据(类别):",
            "图表类型:",
            "图表标题:",
            "X轴标签:",
            "Y轴标签:",
            "显示网格:",
            "显示图例:",
            "显示数值:"
        ];

        // 设置列宽
        ws.Range("A:A").ColumnWidth = 15;
        ws.Range("B:B").ColumnWidth = 30;

        // 设置示例数据
        ws.Range("B2").Value = "0,2.5,5,7.5";
        ws.Range("B3").Value = "折线图";
        ws.Range("B4").Value = "多数据集示例";
        ws.Range("B5").Value = "葡萄糖浓度 (g/L)";
        ws.Range("B6").Value = "DCW (g/L)";
        ws.Range("B7").Value = "是";
        ws.Range("B8").Value = "是";
        ws.Range("B9").Value = "是";

        // 添加图表类型提示
        ws.Range("C3").Value = "可选: 折线图,柱状图,散点图,误差棒图,直方图,饼图,雷达图";
        ws.Range("C3").Font.Color = 255; // 红色
        ws.Range("C3").Font.Size = 8;

        // 添加网格/图例/数值提示
        ws.Range("C7").Value = "是/否";
        ws.Range("C8").Value = "是/否";
        ws.Range("C9").Value = "是/否";
        ws.Range("C7:C9").Font.Color = 255;
        ws.Range("C7:C9").Font.Size = 8;

        // 创建"数据集"工作表
        try {
            ws = wb.Sheets.Add();
            ws.Name = "数据集";
        } catch (e) {
            ws = wb.Sheets.Item("数据集");
        }

        // 设置标题
        ws.Range("A1:D1").Merge();
        ws.Range("A1").Value = "数据集数据";
        ws.Range("A1").Font.Bold = true;
        ws.Range("A1").Font.Size = 14;
        ws.Range("A1").Interior.Color = 4210752;
        ws.Range("A1").Font.Color = 16777215;

        // 设置列标题
        ws.Range("A1:D1").Value = ["数据集标签", "Y轴数据", "误差数据", "颜色"];
        ws.Range("A1:D1").Font.Bold = true;
        ws.Range("A1:D1").Interior.Color = 15790320; // 浅蓝色

        // 设置示例数据
        ws.Range("A2:D5").Value = [
            ["0", "0.2,1.1,0.95,0.55", "0.05,0.1,0.08,0.06", "blue"],
            ["2.5", "0.5,1.15,0.98,0.6", "0.06,0.12,0.09,0.07", "orange"],
            ["5", "0.48,1.0,0.96,0.58", "0.05,0.11,0.08,0.06", "green"],
            ["7.5", "0.45,0.95,0.94,0.56", "0.04,0.1,0.07,0.05", "red"]
        ];

        // 设置列宽
        ws.Range("A:A").ColumnWidth = 15;
        ws.Range("B:B").ColumnWidth = 25;
        ws.Range("C:C").ColumnWidth = 25;
        ws.Range("D:D").ColumnWidth = 12;

        // 添加颜色提示
        ws.Range("E2:E5").Value = [
            "可选颜色: blue, orange, green, red, purple, brown, pink, cyan, yellow, black",
            "",
            "",
            ""
        ];
        ws.Range("E2").Font.Color = 255;
        ws.Range("E2").Font.Size = 8;
        ws.Range("E2").WrapText = true;

        alert("示例模板已创建成功!\n\n请填写数据后运行 ExportToJSON 函数导出JSON配置。");

    } catch (e) {
        alert("创建模板失败!\n错误信息: " + e.message);
    }
}

// 注册快捷键 (可选)
// Application.OnKey("^e", "ExportToJSON");  // Ctrl+E 导出JSON
// Application.OnKey("^t", "CreateTemplate"); // Ctrl+T 创建模板
