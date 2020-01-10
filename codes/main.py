import sys

from PyQt5 import QtWidgets

from codes.ui import UI_Form
from codes.windows import HotMapWindows, WordCloudWindows

# 主方法入口
if __name__ == '__main__':
    # 获取当前文件路径
    # d = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"  # 获取当前文件所在路径
    # d = re.sub(r'\\', '/', d)  # 将路径中的分隔符\替换为/
    # 实例化QApplication类
    app = QtWidgets.QApplication(sys.argv)
    main_win = QtWidgets.QMainWindow()
    # 显示热力图，主要城市评论数及平均分窗口
    hot_win = HotMapWindows()
    # 显示词云图窗口
    word_win = WordCloudWindows()
    # 初始化主窗口
    ui = UI_Form()
    ui.init_ui(main_win, hot_win, word_win)
    # 显示主窗口
    main_win.show()
    sys.exit(app.exec_())
