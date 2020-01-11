import collections
import os

import imageio
import jieba
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5 import QtCore, QtWidgets
from pyecharts import Geo, Line, Bar, Overlap
from wordcloud import WordCloud, ImageColorGenerator

from codes.constant import movie_list, get_json_data


# 主窗口
class UI_Form(object):

    def __init__(self):
        # 主窗口默认电影为第一个
        default = movie_list[0]
        self.movie_name = default.get('name')
        self.movie_id = default.get('id')
        self.default_dir = '../result/'
        # 创建结果保存目录
        if not os.path.exists(self.default_dir):
            os.mkdir(self.default_dir)

    def init_ui(self, Form, hot_win, word_win):
        """
        主窗口初始化
        :param Form: QMainWindow
        :param hot_win: 热力图窗口
        :param word_win: 词云窗口
        """
        self.hot_win = hot_win
        self.word_win = word_win
        Form.setObjectName("Form")
        Form.resize(382, 206)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(70, 20, 251, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setDuplicatesEnabled(False)
        # 初始化下拉菜单项数
        self.comboBox.setObjectName("comboBox")
        for _ in movie_list:
            self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 80, 235, 89))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.commentNum = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.commentNum.setAlignment(QtCore.Qt.AlignCenter)
        self.commentNum.setObjectName("commentNum")
        self.horizontalLayout_2.addWidget(self.commentNum)
        self.viewCommentNum = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.viewCommentNum.setObjectName("viewCommentNum")
        self.horizontalLayout_2.addWidget(self.viewCommentNum)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.hotMap = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.hotMap.setAlignment(QtCore.Qt.AlignCenter)
        self.hotMap.setObjectName("hotMap")
        self.horizontalLayout_3.addWidget(self.hotMap)
        self.viewHotMap = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.viewHotMap.setObjectName("viewHotMap")
        self.horizontalLayout_3.addWidget(self.viewHotMap)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.wordCloud = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.wordCloud.setAlignment(QtCore.Qt.AlignCenter)
        self.wordCloud.setObjectName("wordCloud")
        self.horizontalLayout_4.addWidget(self.wordCloud)
        self.viewWordCloud = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.viewWordCloud.setObjectName("viewWordCloud")
        self.horizontalLayout_4.addWidget(self.viewWordCloud)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.hide()
        self.fresh_ui(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def hide(self):
        """
        隐藏查看内容
        """
        self.wordCloud.setVisible(False)
        self.viewWordCloud.setVisible(False)
        self.hotMap.setVisible(False)
        self.viewHotMap.setVisible(False)
        self.commentNum.setVisible(False)
        self.viewCommentNum.setVisible(False)

    def show(self):
        """
        显示查看内容
        """
        self.wordCloud.setVisible(True)
        self.viewWordCloud.setVisible(True)
        self.hotMap.setVisible(True)
        self.viewHotMap.setVisible(True)
        self.commentNum.setVisible(True)
        self.viewCommentNum.setVisible(True)

    def fresh_ui(self, Form):
        """
        刷新当前UI界面
        :param Form: QMainWindow
        """
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "猫眼电影影评分析"))
        self.label.setText(_translate("Form", "选择电影："))
        for index, movie in enumerate(movie_list):
            self.comboBox.setItemText(index, _translate('Form', movie.get('name')))
        self.pushButton.setText(_translate("Form", "分析"))
        self.commentNum.setText(_translate("Form", "主要城市评论数及平均分"))
        self.viewCommentNum.setText(_translate("Form", "查看"))
        self.hotMap.setText(_translate("Form", "                 热力图"))
        self.viewHotMap.setText(_translate("Form", "查看"))
        self.wordCloud.setText(_translate("Form", "                   词云"))
        self.viewWordCloud.setText(_translate("Form", "查看"))
        # 电影选择事件
        self.comboBox.activated[str].connect(self.item_change)
        # 分析功能
        self.pushButton.clicked.connect(self.analyze)
        # 判断是否被分析过
        if not os.path.exists(self.default_dir + self.movie_name):
            self.pushButton.setText('分析')
            self.hide()
        else:
            self.pushButton.setText('重新分析')
            self.show()
            self.button_click()

    # 电影选择处理方法
    def item_change(self, text):
        for movie in movie_list:
            # 定位下拉菜单选择的电影
            if text.__eq__(movie.get('name')):
                # 判断是否被分析过
                if not os.path.exists(self.default_dir + text):
                    self.pushButton.setText('分析')
                    self.hide()
                else:
                    self.pushButton.setText('重新分析')
                    self.movie_name = movie.get('name')
                    self.movie_id = movie.get('id')
                    self.show()
                    self.button_click()

    def button_click(self):
        """
        操作查看按钮
        """
        self.viewCommentNum.clicked.connect(self.view_main_city)
        self.viewHotMap.clicked.connect(self.view_hot_map)
        self.viewWordCloud.clicked.connect(self.view_word_cloud)

    def view_main_city(self):
        """
        主要城市评论数及平均分查看按钮触发事件
        """
        self.hot_win.show_hot_map(self.movie_name, index=0)
        self.hot_win.show()

    def view_hot_map(self):
        """
        全国热力图查看按钮触发事件
        """
        self.hot_win.show_hot_map(self.movie_name, index=1)
        self.hot_win.show()

    def view_word_cloud(self):
        """
        词云查看按钮触发事件
        """
        self.word_win.show_word_cloud(self.movie_name)
        self.word_win.show()

    def analyze(self):
        """
        分析按钮触发事件
        """
        # 定位当前选定的电影
        for index, movie in enumerate(movie_list):
            if index == self.comboBox.currentIndex():
                self.movie_name = movie.get('name')
                self.movie_id = movie.get('id')
                self.crawl_data()
                break
        self.show()
        self.pushButton.setText('重新分析')
        self.button_click()

    def crawl_data(self):
        """
        爬取影评数据, 并进行预处理
        """
        # 创建影评分析结果存放目录
        save_dir = self.default_dir + self.movie_name + '/'
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        # 需要存储的信息列
        col_list = ['time', 'score', 'cityName', 'content', 'nickName']
        frame = pd.DataFrame(columns=col_list)
        # 通过URL获取影评数据
        url = 'http://m.maoyan.com/mmdb/comments/movie/' + self.movie_id + '.json'
        json_data = get_json_data(url)  # keys: 'cmts', 'hcmts', 'total'
        comments = json_data.get('cmts')
        high_comments = json_data.get('hcmts')

        # 筛选需要的信息
        list1 = list(map(lambda x: dict(filter(lambda it: it[0] in col_list, x.items())), comments))
        list2 = list(map(lambda x: dict(filter(lambda it: it[0] in col_list, x.items())), high_comments))
        list1.extend(list2)
        frame = frame.append(list1, ignore_index=True)
        # 去重复数据，并重新建立索引
        frame = frame.drop_duplicates().reset_index()
        # 影评保存 csv 文件
        frame.to_csv(save_dir + self.movie_name + '.csv', index=True, header=True, encoding='utf_8_sig')
        frame_group = frame.groupby('cityName')
        # 通过聚合函数求平均分，以及评论总数
        frame_agg = frame_group['score'].agg(['mean', 'count'])
        # 重新建立索引，因为 group by 之后结构已经变了
        frame_agg.reset_index(inplace=True)
        # 平均分保留2位小数
        frame_agg['mean'] = frame_agg['mean'].apply(lambda x: round(x, 2))
        # 生成全国热力图和主要城市评论数及平均分
        self.gen_hot_map(save_dir, frame_agg)
        # 生成词云图
        self.gen_word_cloud(save_dir, ' '.join(frame['content']))

    def gen_hot_map(self, save_dir, frame):
        """
        生成全国热力图和主要城市评论数及平均分
        :param save_dir: 结果的保存目录
        :param frame: 用来操作的数据, DataFrame
        """
        geo_map = Geo('《' + self.movie_name + '》 全国热力图',
                      title_color="#fff",
                      title_pos="center", width=1200,
                      height=600, background_color='#404a59')
        while True:
            try:
                geo_map.add("", attr=frame['cityName'], value=frame['count'], type="heatmap",
                            visual_range=[0, 50], visual_text_color="#fff",
                            symbol_size=15, is_visualmap=True, is_roam=False)
                break
            except ValueError as e:
                # 去除不支持的城市名
                city_name = str(e).split("No coordinate is specified for ")[1]
                frame = frame[frame['cityName'] != city_name]

        # 生成全国热力图html文件
        geo_map.render(save_dir + self.movie_name + '全国热力图.html')

        # 取前30个主要城市
        main_city = frame.sort_values('count', ascending=False)[:30]
        # 以折线图画主要城市评分
        line = Line("主要城市评分")
        line.add("城市", x_axis=main_city['cityName'], y_axis=main_city['mean'], is_stack=True,
                 xaxis_rotate=30, yaxis_min=0, mark_point=['min', 'max'], xaxis_interval=0,
                 line_color='lightblue', line_width=4, mark_point_textcolor='black',
                 mark_point_color='lightblue', is_splitline_show=False)
        # 以柱状图画主要城市评分
        bar = Bar("主要城市评论数")
        bar.add("城市", x_axis=main_city['cityName'], y_axis=main_city['count'], is_stack=True,
                xaxis_rotate=30, yaxis_min=0, xaxis_interval=0, is_splitline_show=False)
        # 叠加画在同一个图上
        overlap = Overlap()
        overlap.add(bar)
        overlap.add(line, yaxis_index=1, is_add_yaxis=True)
        # 生成主要城市评论数及平均分html文件
        overlap.render(save_dir + self.movie_name + '主要城市评论数及平均分.html')

    def gen_word_cloud(self, save_dir, contents):
        """
        先使用jieba分词, 再使用wordcloud生成词云图
        :param save_dir: 词云图保存目录
        :param contents: 要分析的文本
        """
        words_generator = jieba.cut_for_search(contents)
        words_list = list(filter(lambda x: len(x) > 1, words_generator))
        # 解析词云背景图片
        back_color = imageio.imread('../resource/background.jpg')
        word_cloud = WordCloud(
            background_color='white',  # 背景颜色
            max_words=200,  # 最大词数
            mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
            max_font_size=300,  # 显示字体的最大值
            font_path="../resource/STFANGSO.ttf",  # 字体
            random_state=42,  # 为每个词返回一个PIL颜色
        )
        words_count = collections.Counter(words_list)
        word_cloud.generate_from_frequencies(words_count)
        # 基于彩色图像生成相应彩色
        image_colors = ImageColorGenerator(back_color)
        # 绘制词云
        plt.figure()
        plt.imshow(word_cloud.recolor(color_func=image_colors))
        # 去掉坐标轴
        plt.axis('off')
        # 保存词云图片
        word_cloud.to_file(save_dir + self.movie_name + '词云.png')
