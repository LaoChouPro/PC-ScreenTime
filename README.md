# PC-ScreenTime
这是一个用于记录PC用户屏幕使用时间的可视化软件，目前安装打包版本仅支持中文，源码有英文版本。由老抽开发。This is a program that can record the screentime of PC, and show these data in visual charts and tables. Developed by LaoChou.
要安装本程序请前往[http://laochou.cloud/GitHub/PC_ScreenTime/]下载安装文件。目前仅支持中文安装。
Plese click the link [http://laochou.cloud/GitHub/PC_ScreenTime/] to download the setup file. Only Chinese available currently.
## ScreenShot 程序运行时展示
![Alt Text](http://laochou.cloud/GitHub/PC_ScreenTime/images/%E6%80%BB%E8%A7%88%E5%9B%BE%E8%A1%A8.png)
![Alt Text](http://laochou.cloud/GitHub/PC_ScreenTime/images/%E8%AF%A6%E7%BB%86%E8%A1%A8%E6%A0%BC.png)
它可以统计你的每个应用的使用时常。
It can record your PC's screentime.
## Introduction (English)
The Screen Time Tracker is a Python-based application designed to monitor and record the usage time of different applications on a Windows operating system. This software helps users to better understand how much time they spend on various applications, which can be useful for improving productivity and managing time effectively. The program runs in the background, quietly tracking the active window and logging the time spent on each application.

## 简介 (中文)
屏幕使用时间监控器是一个基于 Python 的应用程序，旨在监控和记录在 Windows 操作系统上不同应用程序的使用时间。该程序在后台运行，静默地跟踪活动窗口，并记录每个应用程序的使用时间。

---

## Features (English)
- **Real-Time Tracking:** Monitors the active window in real-time and logs the time spent on each application.
- **Data Storage:** The usage data is stored locally in a text file, ensuring privacy and ease of access.
- **Custom Application Names:** When a new application is detected, the user is prompted to enter a name for the application, which is then stored for future reference.
- **Background Operation:** The application runs silently in the background, without affecting the user's work.

## 功能 (中文)
- **实时跟踪:** 实时监控活动窗口，并记录每个应用程序的使用时间。
- **数据存储:** 使用数据存储在本地的文本文件中，确保隐私和便捷的访问。
- **自定义应用名称:** 当检测到新应用程序时，程序会提示用户输入应用程序的名称，并将其存储以供将来参考。
- **后台运行:** 程序在后台静默运行，不影响用户的工作。

---

## How It Works (English)
The Screen Time Tracker operates by continuously monitoring the active window title on the user's system. It uses the `win32gui` and `psutil` libraries to fetch the process name of the currently active window. If the application has not been tracked before, the user is prompted to input a custom name for the application. The application name, along with the time spent on it, is then logged into a local text file (`app_usage_log.txt`). The application runs in the background, with a system tray icon for easy access and control.

## 工作原理 (中文)
屏幕使用时间监控器通过持续监控用户系统上的活动窗口标题来运行。它使用 `win32gui` 和 `psutil` 库来获取当前活动窗口的进程名称。如果该应用程序以前没有被跟踪过，程序会提示用户输入自定义名称。然后将应用程序名称及其使用时间记录到本地文本文件（`app_usage_log.txt`）中。程序在后台运行，带有一个系统托盘图标，方便访问和控制。

---

## License (English)
This software is provided "as is," without warranty of any kind, express or implied. It is intended for personal, non-commercial use only. The author is not responsible for any damages or issues arising from the use of this software. Use it at your own risk.

## 许可证 (中文)
本软件按“原样”提供，不提供任何形式的明示或暗示担保。它仅供个人非商业用途。作者不对因使用本软件而产生的任何损害或问题负责。使用本软件的风险由您自行承担。

---

## Contact (English)
For any questions or feedback, please contact the author at [laochou6423@gmail.com].

## 联系方式 (中文)
如有任何问题或反馈，请联系作者：[laochou6423@gmail.com]。
