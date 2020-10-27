from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QColor, QPalette, QBrush, QPixmap, QRadialGradient, QCursor
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtWidgets import QWidget
from game import Gomoku
import os
import QssTools
from dinglinghui.search_level1 import ChessAI as level1
from dinglinghui.search_level2 import ChessAI as level2
from dinglinghui.search_level3 import ChessAI as level3
from dinglinghui.Macro import MAP_ENTRY_TYPE, HEIGHT


class CornerWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setFixedSize(30, 30)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.red, 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, 8, 0, 0)
        qp.drawLine(0, 0, 8, 0)
        qp.drawLine(22, 0, 28, 0)
        qp.drawLine(28, 0, 28, 8)
        qp.drawLine(28, 22, 28, 28)
        qp.drawLine(28, 28, 20, 28)
        qp.drawLine(8, 28, 0, 28)
        qp.drawLine(0, 28, 0, 22)


class GomokuWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()  # 初始化游戏界面
        self.g = Gomoku()  # 初始化游戏内容

        self.last_pos = (-1, -1)
        self.res = 0  # 记录哪边获得了胜利
        self.operate_status = 0  # 游戏操作状态。0为游戏中（可操作），1为游戏结束闪烁过程中（不可操作）

    def init_ui(self):
        """初始化游戏界面"""
        # 1. 确定游戏界面的标题，大小和背景颜色
        self.setObjectName('MainWindow')
        self.setWindowTitle('五子棋')
        self.setFixedSize(650, 650)

        # 使用调色板功能
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap(os.path.join(os.getcwd(), 'src', 'imgs', 'muzm.jpg'))))
        self.setPalette(palette)

        # # 2. 设置鼠标光标样式
        # # 2.1 创建光标的图像，参数为光标的相对位置（本文将光标存在工程目录的Cursor_png文件夹下）
        # pixmap = QPixmap(os.path.join(os.getcwd(), 'src', 'imgs', 'cursor.png'))
        # # 2.2 将光标对象传入鼠标对象中
        # cursor = QCursor(pixmap, 0, 0)
        # # 2.3 设置控件的光标
        # self.setCursor(cursor)

        # 2. 开启鼠标位置的追踪。并在鼠标位置移动时，使用特殊符号标记当前的位置
        self.setMouseTracking(True)
        # 3. 鼠标位置移动时，对鼠标位置的特殊标记
        self.corner_widget = CornerWidget(self)
        self.corner_widget.repaint()
        self.corner_widget.hide()
        # 4. 游戏结束时闪烁的定时器
        self.end_timer = QTimer(self)
        self.end_timer.timeout.connect(self.end_flash)
        self.flash_cnt = 0  # 游戏结束之前闪烁了多少次
        self.flash_pieces = ((-1, -1),)  # 哪些棋子需要闪烁
        # 5.QSS美化
        QssTools.SetQss(os.path.join(os.getcwd(), 'src', 'qss', 'ThreeStateStyle.qss'), self)
        # 6. 显示初始化的游戏界面
        self.show()

    def paintEvent(self, e):
        """绘制游戏内容"""

        def draw_map():
            """绘制棋盘"""
            qp.setPen(QPen(QColor(255, 255, 255), 2, Qt.SolidLine))  # 棋盘的颜色为黑色
            # 绘制横线
            for x in range(15):
                qp.drawLine(40 * (x + 1), 40, 40 * (x + 1), 600)
            # 绘制竖线
            for y in range(15):
                qp.drawLine(40, 40 * (y + 1), 600, 40 * (y + 1))
            # 绘制棋盘中的黑点
            qp.setBrush(QColor(0, 0, 0))
            key_points = [(4, 4), (12, 4), (4, 12), (12, 12), (8, 8)]
            for t in key_points:
                qp.drawEllipse(QPoint(40 * t[0], 40 * t[1]), 5, 5)

        def draw_pieces():
            """绘制棋子"""
            # 绘制黑棋子
            qp.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            for x in range(15):
                for y in range(15):
                    if self.g.g_map[x][y] == 1:
                        if self.flash_cnt % 2 == 1 and (x, y) in self.flash_pieces:
                            continue
                        radial = QRadialGradient(40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35)  # 棋子的渐变效果
                        radial.setColorAt(0, QColor(96, 96, 96))
                        radial.setColorAt(1, QColor(0, 0, 0))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(40 * (x + 1), 40 * (y + 1)), 15, 15)
            # 绘制白棋子
            qp.setPen(QPen(QColor(160, 160, 160), 1, Qt.SolidLine))
            for x in range(15):
                for y in range(15):
                    if self.g.g_map[x][y] == 2:
                        if self.flash_cnt % 2 == 1 and (x, y) in self.flash_pieces:
                            continue
                        radial = QRadialGradient(40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35)  # 棋子的渐变效果
                        radial.setColorAt(0, QColor(255, 255, 255))
                        radial.setColorAt(1, QColor(160, 160, 160))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(40 * (x + 1), 40 * (y + 1)), 15, 15)

        if hasattr(self, 'g'):  # 游戏还没开始的话，就不用画了
            qp = QPainter()
            qp.begin(self)
            draw_map()  # 绘制棋盘
            draw_pieces()  # 绘制棋子
            qp.end()

    def mouseMoveEvent(self, e):
        # 1. 首先判断鼠标位置对应棋盘中的哪一个格子
        mouse_x = e.windowPos().x()
        mouse_y = e.windowPos().y()
        if 25 <= mouse_x <= 615 and 25 <= mouse_y <= 615 and (mouse_x % 40 <= 15 or mouse_x % 40 >= 25) and (
                mouse_y % 40 <= 15 or mouse_y % 40 >= 25):
            game_x = int((mouse_x + 15) // 40) - 1
            game_y = int((mouse_y + 15) // 40) - 1
        else:  # 鼠标当前的位置不对应任何一个游戏格子，将其标记为(-1, -1)
            game_x = -1
            game_y = -1

        # 2. 然后判断鼠标位置较前一时刻是否发生了变化
        pos_change = False  # 标记鼠标位置是否发生了变化
        if game_x != self.last_pos[0] or game_y != self.last_pos[1]:
            pos_change = True
        self.last_pos = (game_x, game_y)
        # 3. 最后根据鼠标位置的变化，绘制特殊标记
        if pos_change and game_x != -1:
            self.setCursor(Qt.PointingHandCursor)
        if pos_change and game_x == -1:
            self.setCursor(Qt.ArrowCursor)
        if pos_change and game_x != -1:
            self.corner_widget.move(25 + game_x * 40, 25 + game_y * 40)
            self.corner_widget.show()
        if pos_change and game_x == -1:
            self.corner_widget.hide()

    def mousePressEvent(self, e):
        """根据鼠标的动作，确定落子位置"""

        if not (hasattr(self, 'operate_status') and self.operate_status == 0):
            return
        if e.button() == Qt.LeftButton:
            # 1. 首先判断按下了哪个格子
            mouse_x = e.windowPos().x()
            mouse_y = e.windowPos().y()
            if (mouse_x % 40 <= 15 or mouse_x % 40 >= 25) and (mouse_y % 40 <= 15 or mouse_y % 40 >= 25):
                game_x = int((mouse_x + 15) // 40) - 1
                game_y = int((mouse_y + 15) // 40) - 1
            else:  # 鼠标点击的位置不正确
                return
            self.g.move_1step(game_y, game_x, MAP_ENTRY_TYPE.MAP_PLAYER_ONE)
        """
            # 2. 根据操作结果进行一轮游戏循环
            res, self.flash_pieces = self.g.game_result(show=True)  # 判断游戏结果
            if res != 0:  # 如果游戏结果为“已经结束”，则显示游戏内容，并退出主循环
                self.repaint(0, 0, 650, 650)
                self.game_restart(res)
                return
        """
            # TODO:we should rewrite a function to make the machine play.
            #  需要在完成AI部分代码后，仿照上述部分进行AI落子操作

            # self.repaint(0, 0, 650, 650)  # 在游戏还没有结束的情况下，显示游戏内容，并继续下一轮循环
        #ai1 = level1(HEIGHT)
        #x, y = ai1.findBestChess(self.g.g_map, MAP_ENTRY_TYPE.MAP_PLAYER_TWO)
        #self.g.move_1step(x, y)
        #x, y = ai1.findBestChess(self.g.g_map, MAP_ENTRY_TYPE.MAP_PLAYER_TWO)
        #TODO:xia mian shi diao yong deng ji er de ji qi shi fan.
        ai2 = level1(HEIGHT)
        x, y = ai2.findBestChess(self.g.g_map, MAP_ENTRY_TYPE.MAP_PLAYER_TWO)
        self.g.move_1step(x, y, MAP_ENTRY_TYPE.MAP_PLAYER_TWO)
        #ai3 = level3(HEIGHT)
        #x, y = ai3.findBestChess(self.g.g_map, MAP_ENTRY_TYPE.MAP_PLAYER_TWO)

        #self.g.move_1step(x, y)


        res, self.flash_pieces = self.g.game_result(show=True)  # 判断游戏结果
        if res != 0:  # 如果游戏结果为“已经结束”，则显示游戏内容，并退出主循环
            self.repaint(0, 0, 650, 650)
            self.game_restart(res)
            return
        self.repaint(0, 0, 650, 650)

    def end_flash(self):
        # 游戏结束时的闪烁操作
        if self.flash_cnt <= 5:
            # 执行闪烁
            self.flash_cnt += 1
            self.repaint()
        else:
            # 闪烁完毕，执行重新开始的操作
            self.end_timer.stop()
            # 1. 显示游戏结束的信息
            if self.res == 1:
                QMessageBox.about(self, '游戏结束', '玩家获胜!')
            elif self.res == 2:
                QMessageBox.about(self, '游戏结束', '电脑获胜!')
            elif self.res == 3:
                QMessageBox.about(self, '游戏结束', '平局!')
            # 2. 游戏重新开始的操作
            self.res = 0
            self.operate_status = 0
            self.flash_cnt = 0
            self.g = Gomoku()  # 重新初始化游戏内容
            self.repaint(0, 0, 650, 650)  # 重新绘制游戏界面

    def game_restart(self, res):
        """游戏出现开始"""
        self.res = res  # 标记谁获胜了
        self.operate_status = 1  # 游戏结束时的闪烁过程中，不可操作
        self.end_timer.start(300)  # 开始结束时闪烁的计时器
