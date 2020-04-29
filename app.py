# app.py
import sys
from PyQt5.QtWidgets import (
  QApplication, QWidget, QMainWindow, QDesktopWidget, 
  QAction, qApp,
  QPushButton, QToolTip,
  QLabel, QLineEdit, QComboBox,
  QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QIcon, QFont

# 위젯 설정
class MyWidget(QWidget):
  def __init__(self, parent):        
    super(QWidget, self).__init__(parent)
    
    self.layout = QGridLayout(self)
    
    self.setInput("입력창1", 0, 0)
    self.setInput("입력창2", 0, 1)
    self.setComoboBox("입력창3", 1, 1)
    
    self.setLayout(self.layout)
    
  # 박스 설정
  def setInput(self, text, row, col):
    hbox = QHBoxLayout()
  
    # 라벨 생성
    label = QLabel(text)

    # 라벨 스타일 설정
    label.setStyleSheet('''
      color: red;
      border-style: solid;
      border-width: 2px;
      border-color: #FA8072;
      border-radius: 3px
    ''')
    
    # 입력창 생성
    line_edit = QLineEdit()
    
    hbox.addStretch(3)
    hbox.addWidget(label)
    hbox.addWidget(line_edit)
    hbox.addStretch(3)
    
    self.layout.addLayout(hbox, row, col)
    
  # 박스 설정
  def setComoboBox(self, text, row, col):
    hbox = QHBoxLayout()
    
    label = QLabel(text)
    
    text_label = QLabel()
  
    cb = QComboBox(self)
    cb.addItem("Option1")
    cb.addItem("Option2")
    cb.addItem("Option3")
    cb.addItem("Option4")
    
    hbox.addWidget(text_label)
    hbox.addWidget(label)
    hbox.addWidget(cb)
  
    def onActivated(_label):
      def setText(_text):
        _label.setText(_text)
        _label.adjustSize()
      return setText

    cb.activated[str].connect(onActivated(text_label))
    
    self.layout.addLayout(hbox, row, col)


class MyWindow(QMainWindow):
  def __init__(self, title="Window", **kwargs):
    super(QMainWindow, self).__init__()
    
    # 상태값 설정
    self.title = title
    self.posX = int(kwargs.get("posX")) if "posX" in kwargs else 0
    self.posY = int(kwargs.get("posY")) if "posY" in kwargs else 0
    self.width = int(kwargs.get("width")) if "width" in kwargs else 300
    self.height = int(kwargs.get("height")) if "height" in kwargs else 200
    
    # 초기 설정
    self.init()
    
  # 초기 설정
  def init(self):
    self.init_ui()
    self.init_tooltip()
    self.init_status_bar()
    self.init_menu_bar()
    self.init_tool_bar()
    self.init_widget()
  
  # UI 설정
  def init_ui(self):
    # 제목 설정
    self.setWindowTitle(self.title)
    # 아이콘 설정
    self.setWindowIcon(QIcon("./icons/dochi.png"))
    # 크기 및 위치 설정
    #self.resize(self.width, self.height)
    self.setGeometry(self.posX, self.posY, self.width, self.height)    
    
    # 가운데 정렬
    frame_geo = self.frameGeometry()
    desktop_center = QDesktopWidget().availableGeometry().center()
    frame_geo.moveCenter(desktop_center)
    self.move(frame_geo.topLeft())
    
  # 상태바 설정
  def init_status_bar(self):
    statusBar = self.statusBar()
    statusBar.showMessage("Ready")
    
  # 툴팁 설정
  def init_tooltip(self):
    # 툴팁 폰트 설정
    font = QFont("SansSerif", 10)
    message = f"'<b>Window ToolTip</b>' 입니다."
    
    QToolTip.setFont(font)
    self.setToolTip(message)
  
  # 메뉴바 설정
  def init_menu_bar(self):
    menubar = self.menuBar()
    menubar.setNativeMenuBar(False)
    
    # 기능 설정
    exit_action = QAction(QIcon("./icons/exit.png"), "종료", self)
    exit_action.setShortcut("Alt+Q")
    exit_action.setStatusTip("Window를 종료합니다.")
    exit_action.triggered.connect(qApp.quit)
    
    # 메뉴 추가
    filemenu = menubar.addMenu('File')
    filemenu.addAction(exit_action)
    
  # 툴바 설정
  def init_tool_bar(self):
    # 기능 설정
    exit_action = QAction(QIcon("./icons/exit.png"), "종료", self)
    exit_action.setShortcut("Alt+Q")
    exit_action.setStatusTip("Window를 종료합니다.")
    exit_action.triggered.connect(qApp.quit)
    
    # 툴바 추가
    self.toolbar = self.addToolBar('종료')
    self.toolbar.addAction(exit_action)
    
  # 위젯 설정
  def init_widget(self):
    self.main_widget = MyWidget(self)
    self.setCentralWidget(self.main_widget)
    

if __name__ == '__main__':
  app = QApplication( sys.argv )
  
  win = MyWindow("메인 윈도우", posX=100, posY=400, width=300, height=200)
  win.show()
  
  sys.exit( app.exec() )