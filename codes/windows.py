import os

from PyQt5.QtCore import QSize, QUrl, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QLabel


class HotMapWindows(QMainWindow):
    """
    热力图和主要城市评论数及平均分 主窗口类
    """
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setGeometry(200, 200, 1250, 650)
        self.browser = QWebEngineView()
        # 所有分析结果存放目录
        self.default_dir = '../result/'

    def show_hot_map(self, movie_name, index):
        title = ['主要城市评论数及平均分', '全国热力图']
        self.setWindowTitle(movie_name + title[index])
        html = self.default_dir + movie_name + '/' + movie_name + title[index] + '.html'
        # windows下注意要替换文件路径中的 '\' 为 '/'
        html = 'file:///' + os.path.abspath(html).replace('\\', '/')
        self.browser.load(QUrl(html))
        self.setCentralWidget(self.browser)


class WordCloudWindows(QMainWindow):
    """
    词云图 主窗口类
    """
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setGeometry(200, 200, 650, 650)
        self.browser = QLabel()
        self.default_dir = '../result/'

    def show_word_cloud(self, movie_name):
        title = '词云'
        self.setWindowTitle(movie_name + title)
        png = self.default_dir + movie_name + '/' + movie_name + title + '.png'
        # 理由pixmap解析图片
        pixmap = QPixmap(png)
        # 等比例缩放图片
        scaredPixmap = pixmap.scaled(QSize(600, 600), aspectRatioMode=Qt.KeepAspectRatio)
        # 设置图片
        self.browser.setPixmap(scaredPixmap)
        # 判断选择的类型 根据类型做相应的图片处理
        self.browser.show()
        self.setCentralWidget(self.browser)
