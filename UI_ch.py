import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import font_manager
import random


# 读取文件并解析数据
def read_usage_data(file_path="app_usage_log.txt"):
    usage_data = {}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("使用数据:") and ": " in line:
                    try:
                        app, usage_time = line.split(": ")
                        usage_time = float(usage_time.split()[0]) / 3600.0  # 转换为小时
                        usage_data[app] = usage_time
                    except ValueError:
                        continue
    return usage_data


# 创建Matplotlib图表画布
class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=7, height=5, dpi=100):  # 调大尺寸
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


# 绘制图表
class ChartPage(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        layout = QVBoxLayout()

        # 创建柱状图
        self.bar_chart = MplCanvas(self, width=7, height=5, dpi=100)  # 调大尺寸
        self.plot_bar_chart()
        layout.addWidget(self.bar_chart)

        self.setLayout(layout)
        self.setMinimumSize(500, 400)  # 设置最小尺寸
        self.resizeEvent = self.on_resize  # 连接窗口调整事件

    def plot_bar_chart(self):
        # 排序并只显示使用时间前8的程序
        sorted_data = sorted(self.data.items(), key=lambda x: x[1], reverse=True)[:8]
        apps, times = zip(*sorted_data)
        colors = [plt.cm.get_cmap('viridis')(random.uniform(0, 1)) for _ in range(len(apps))]

        ax = self.bar_chart.axes
        ax.clear()  # 清除以前的图表
        bars = ax.barh(apps, times, color=colors)

        # 设置文字和布局
        ax.set_xlabel('使用时间（小时）')
        ax.set_title('前8个应用程序的使用时间')
        ax.invert_yaxis()  # 翻转y轴，使最大的值在顶部

        # 在每个柱状条上标出具体数值
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.05, bar.get_y() + bar.get_height() / 2,
                    f'{width:.2f}', va='center', ha='left')

        self.adjust_layout()

    def adjust_layout(self):
        # 根据窗口大小动态调整布局
        width = self.width()
        left_margin = max(0.15, 0.25 * (700 / width))  # 动态调整左边距
        plt.subplots_adjust(left=left_margin, right=0.9)

        self.bar_chart.figure.tight_layout()
        self.bar_chart.draw()

    def on_resize(self, event):
        self.adjust_layout()  # 调整布局适应新的窗口大小
        super().resizeEvent(event)


# 其他数据页面，包含表格
class OtherDataPage(QWidget):
    def __init__(self, data):
        super().__init__()
        layout = QVBoxLayout()

        # 创建表格
        table_widget = QTableWidget()
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(2)
        table_widget.setHorizontalHeaderLabels(['程序名称', '使用时间（小时）'])
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 填充数据
        for row, (app, time) in enumerate(data.items()):
            program_item = QTableWidgetItem(app)
            time_item = QTableWidgetItem(f"{time:.2f}")

            program_item.setTextAlignment(Qt.AlignCenter)
            time_item.setTextAlignment(Qt.AlignCenter)

            table_widget.setItem(row, 0, program_item)
            table_widget.setItem(row, 1, time_item)

        # 设置表格美化
        table_widget.setStyleSheet("""
            QTableWidget { 
                background-color: #f0f0f0;
                gridline-color: #d0d0d0;
                font-size: 12pt;
                border: 1px solid #d0d0d0;
            }
            QHeaderView::section { 
                background-color: #c0c0c0; 
                padding: 4px;
                border: 1px solid #d0d0d0;
            }
            QTableWidgetItem {
                margin: 4px;
                padding: 4px;
            }
        """)
        table_widget.setAlternatingRowColors(True)
        table_widget.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addWidget(table_widget)
        self.setLayout(layout)


# 主窗口
class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("PC TimeScreen 记录你的PC屏幕使用时间 - By LaoChou")
        self.setGeometry(100, 100, 900, 600)  # 调整窗口尺寸

        tabs = QTabWidget()

        # 添加数据统计页面
        chart_page = ChartPage(data)
        tabs.addTab(chart_page, "总览图表")

        # 添加其他数据页面
        other_page = OtherDataPage(data)
        tabs.addTab(other_page, "每个程序的详细使用时间")

        self.setCentralWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置支持中文的全局字体
    font_id = QFontDatabase.addApplicationFont("C:/Windows/Fonts/msyh.ttc")  # 使用Microsoft YaHei字体
    if font_id != -1:
        app.setFont(QFont("Microsoft YaHei", 10))
    else:
        print("无法加载微软雅黑字体。")

    # 设置Matplotlib的字体为支持中文的字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 使用微软雅黑字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 如果上面的代码仍然无效，可以尝试手动设置字体路径
    font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑字体路径
    prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()

    # 读取使用时间数据
    usage_data = read_usage_data()

    # 创建并展示主窗口
    main_window = MainWindow(usage_data)
    main_window.show()

    sys.exit(app.exec_())
