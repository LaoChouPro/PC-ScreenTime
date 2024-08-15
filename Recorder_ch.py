
import sys
import os
import time
import threading
import psutil
import win32gui
import win32process
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox, QSystemTrayIcon, QMenu, QAction, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer

class Worker(QObject):
    new_app_detected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_app = None
        self.app_usage = {}
        self.app_names = {}
        self.is_dialog_open = False
        self.load_existing_data()
        self.load_app_names()

    def get_active_window_title(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return None
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()
        except Exception as e:
            print(f"获取活动窗口标题时出错: {e}")
            return None

    def track_app_usage(self):
        last_app_change_time = time.time()

        while True:
            try:
                active_app = self.get_active_window_title()
                if active_app and active_app != self.current_app:
                    if active_app not in self.app_names and not self.is_dialog_open:
                        self.is_dialog_open = True
                        self.new_app_detected.emit(active_app)
                        time.sleep(1)  # 等待用户输入处理完成
                        continue

                    current_time = time.time()
                    if self.current_app:
                        elapsed_time = current_time - last_app_change_time
                        # 更新app_usage字典
                        app_name = self.app_names.get(self.current_app, self.current_app)
                        self.app_usage[app_name] = self.app_usage.get(app_name, 0) + elapsed_time

                    self.current_app = active_app
                    last_app_change_time = current_time

                    # 调用保存方法，确保数据写入
                    self.save_usage_data()

                time.sleep(5)

            except Exception as e:
                print(f"追踪应用使用时间时出错: {e}")

    def load_existing_data(self, file_path="app_usage_log.txt"):
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("使用数据:") and ": " in line:
                        try:
                            app, usage_time = line.split(": ")
                            usage_time = float(usage_time.split()[0])
                            self.app_usage[app] = usage_time  # 只加载文件中的数据，不做累加
                        except ValueError:
                            continue

    def load_app_names(self, file_path="app_names.txt"):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if ": " in line:
                        process_name, app_name = line.split(": ")
                        self.app_names[process_name] = app_name

    def save_app_names(self, file_path="app_names.txt"):
        with open(file_path, "w", encoding="utf-8") as file:
            for process_name, app_name in self.app_names.items():
                file.write(f"{process_name}: {app_name}\n")

    def save_usage_data(self, file_path="app_usage_log.txt"):
        try:
            print(f"保存使用数据到 {file_path}")  # 调试信息
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"\n{datetime.now()} - 使用数据:\n")
                for app, usage_time in self.app_usage.items():
                    file.write(f"{app}: {usage_time:.2f} 秒\n")
            print(f"使用数据已成功保存到 {file_path}")  # 调试信息
        except Exception as e:
            print(f"保存使用数据时出错: {e}")

    def add_app_name(self, process_name, app_name):
        self.app_names[process_name] = app_name
        if app_name not in self.app_usage:
            self.app_usage[app_name] = 0  # 初始化新的应用程序的使用时间
        self.save_app_names()
        self.is_dialog_open = False

class RecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = Worker()
        self.worker.new_app_detected.connect(self.handle_new_app)
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self)
        self.tray_icon.setToolTip("PC ScreenTime - By LaoChou")
        tray_menu = QMenu(self)
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        msg_box = QMessageBox()
        msg_box.setWindowTitle("PC ScreenTime 屏幕使用时间 - 已启动")
        msg_box.setText("PC ScreenTime 服务已启动。\n作者：LaoChou")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg_box.exec_()

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.worker.track_app_usage)
        self.timer.start(1000)

    def handle_new_app(self, process_name):
        app_name, ok = QInputDialog.getText(self, "PC ScreenTime - 我们检测到您正在使用新的应用程序",
                                            f"请输入您打开的应用的名称: {process_name}",
                                            flags=Qt.WindowStaysOnTopHint)
        if ok and app_name:
            self.worker.add_app_name(process_name, app_name)
        else:
            self.worker.is_dialog_open = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = RecorderApp()
    main_window.hide()
    sys.exit(app.exec_())
