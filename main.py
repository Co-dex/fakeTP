import os
import sys
from PySide2 import QtWidgets, QtCore, QtGui


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 隐藏任务栏|去掉边框|顶层显示
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.X11BypassWindowManagerHint |
                            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)


        self.progress = 18
        self.setWindowOpacity(0)
        # 窗口显示flag
        self.isShow = False
        self.pix = QtGui.QBitmap(self.resource_path(r'res\image\mask.png'))
        self.resize(self.pix.size())
        # 设置掩膜,窗口就是掩膜的形状
        self.setMask(self.pix)
        # 设置窗口为透明
        # 初始化计时器
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateProgress)
        # 初始化进度条
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setFixedWidth(200)
        self.progressBar.setFixedHeight(32)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.progressBar)
        self.progressBar.move(115, 50)
        self.progressBar.setValue(18)
        self.progressBar.setFormat('安全防护启动中')
        # 载入进度条样式 最低圆形进度为 16
        with open(self.resource_path(r'res\progressBar.qss'), 'r', encoding='utf8') as style:
            self.setStyleSheet(style.read())

        # 动画
        self.animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.animation.finished.connect(self.onAnimationEnd)
        self.animation.setDuration(1000)

    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(-8, 0, self.pix.width() + 15, self.pix.height(),
                           QtGui.QPixmap(self.resource_path(r'res\image\bg.png')))

    def startAnimate(self):
        self.timer.start(450)  # 间隔 500ms
        # 开始动画
        if not self.isShow:
            self.isShow = True
            self.animation.stop()  # 先停止之前的动画,重新开始
            self.animation.setStartValue(0.0)
            self.animation.setEndValue(1.0)
            self.animation.start()

    def updateProgress(self, event=None):
        # print(self.progress)
        if self.progress <= 100:
            self.progress = self.progress * 1.25
            if self.progress > 100:
                self.progress = 100
                self.progressBar.setValue(self.progress)
                self.progress = 101
            else:
                self.progressBar.setValue(self.progress)
        else:
            # TODO run new exe
            # 关闭动画
            self.isShow = False
            self.timer.stop()
            self.animation.stop()
            self.animation.setStartValue(1.0)
            self.animation.setEndValue(0.0)
            self.animation.start()

    def onAnimationEnd(self):
        # 动画结束
        print("onAnimationEnd isShow", self.isShow)

        if not self.isShow:
            print("onAnimationEnd close()")
            # 自定义你想启动的文件 参考QProcess文档
            target = QtCore.QProcess()
            target.setProgram("msinfo32")
            target.startDetached()
            QtWidgets.QApplication.quit()

    def show(self):
        super().show()
        self.startAnimate()

    def resource_path(self, relative_path):
        if getattr(sys, 'frozen', False):  # 是否Bundle Resource
            base_path = sys._MEIPASS
        else:
            # base_path = os.path.abspath(".")
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    form = Window()
    screen = app.primaryScreen().availableSize()
    form.move(screen.width() - 400, screen.height() - 150)
    form.show()
    sys.exit(app.exec_())
