# app.py
# ref https://freeprog.tistory.com/333
import sys
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (
  QApplication, QWidget, QMainWindow, QDesktopWidget, QDialog, QAction, qApp,
  QPushButton, QToolTip, QLabel, QLineEdit, QComboBox, QMessageBox, QRadioButton,
  QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QCheckBox, QScrollArea,
  QSizePolicy, QHeaderView,
  QTableWidget, QAbstractItemView, QTableWidgetItem, QTableView, QAbstractScrollArea,
  QStyleFactory
)
from PyQt5.QtGui import QIcon, QFont

# 테이블 위젯 설정
class TableWidget(QWidget):
  def __init__(self, parent=None):
    super(QWidget, self).__init__(parent)
    
    self.parent = parent
    
    self.init_ui()
    
  def init_ui(self):
    self.layout = QGridLayout()
    
    self.columns = [
      { "label": "순번", "tooltip":"순번", "align": Qt.AlignCenter },
      { "label": "이름", "align": Qt.AlignCenter },
      { "label": "금액", "align": Qt.AlignRight, "bg": Qt.yellow },
      { "label": "비고", "align": Qt.AlignLeft, "bg": Qt.red }
    ]
    self.column_labels = [ column["label"] for column in self.columns ]
    
    self.defaultColumnCount = len(self.columns)
    self.defaultRowCount = 3
    
    self.make_table()
    self.make_header()
    self.make_controller()
    
    self.setLayout(self.layout)
    
  def make_table(self):
    ### 테이블 생성
    self.table = QTableWidget(self.parent)
    
    ### 테이블 크기
    # Column 갯수
    self.table.setColumnCount(self.defaultColumnCount)
    # Row 갯수
    self.table.setRowCount(self.defaultRowCount)
    
    ### 선택 단위
    # Row 단위
    #self.table.setSelectionBehavior(QTableView.SelectRows)
    # Column 단위
    # self.table.setSelectionBehavior(QAbstractItemView.SelectColumns)
    # Cell 단위
    self.table.setSelectionMode(QAbstractItemView.SingleSelection)
    
    
    ### 다중 선택 모드
    # drag, Ctrl, Shift 키로 다중 선택 가능. 
    #self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
    # self.table.setSelectionMode(QAbstractItemView.MultiSelection)
    # self.table.setSelectionMode(QAbstractItemView.NoSelection) # 선택 불능. 
    # self.table.setSelectionMode(QAbstractItemView.SingleSelection) # 다중 선택 불가능. 
    # self.table.setSelectionMode(QAbstractItemView.ContiguousSelection)

    
    ### 사이즈 설정
    # 콘텐츠에 맞게 설정
    #self.table.resizeColumnsToContents()
    # 테이블에 맞게 설정
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    ### 기타 설정
    self.table.setShowGrid(True)
    
    self.layout.addWidget(self.table, 0, 0)
    
  def make_header(self):
    ### 헤더 설정
    # 헤더명 설정
    self.table.setHorizontalHeaderLabels(self.column_labels)
    
    # 헤더 옵션 설정
    for idx, column in enumerate(self.columns):
      header = self.table.horizontalHeaderItem(idx)
    
      if "tooltip" in column:
        header.setToolTip(column["tooltip"])
      
      if "align" in column:
        header.setTextAlignment(column["align"])
        
      if "bg" in column:
        header.setBackground(column["bg"])
    
  def make_controller(self):
    vbox = QVBoxLayout()
  
    ### Row Control
    row_gbox = QGroupBox("Rows")
    row_gbox_layout = QGridLayout()
    
    btn_add_row_first = QPushButton("첫행에 삽입")
    btn_add_row_first.clicked.connect(lambda flag: self.table.insertRow(0))
    
    btn_add_row_last = QPushButton("마지막행에 삽입")
    btn_add_row_last.clicked.connect(lambda flag: self.table.setRowCount(self.table.rowCount()+1))
    
    row_gbox_layout.addWidget(btn_add_row_first, 0, 0)
    row_gbox_layout.addWidget(btn_add_row_last, 0, 1)
    
    row_gbox.setLayout(row_gbox_layout)
    
        
    ### Columns Control
    col_gbox = QGroupBox("Columns")
    col_gbox_layout = QGridLayout()
    
    btn_add_col_first = QPushButton("첫열에 삽입")
    btn_add_col_first.clicked.connect(lambda flag: self.table.insertColumn(0))
    
    btn_add_col_last = QPushButton("마지막열에 삽입")
    btn_add_col_last.clicked.connect(lambda flag: self.table.setColumnCount(self.table.columnCount()+1))
    
    col_gbox_layout.addWidget(btn_add_col_first, 0, 0)
    col_gbox_layout.addWidget(btn_add_col_last, 0, 1)
    
    col_gbox.setLayout(col_gbox_layout)
    
    
    ### Selection Mode Control
    mode_gbox = QGroupBox("Selection Mode")
    mode_gbox_layout = QHBoxLayout()
    
    selection_mode = self.table.selectionBehavior()
    
    radio_rows_mode = QRadioButton("rows")
    radio_rows_mode.setObjectName("rows")
    radio_rows_mode.setChecked(selection_mode == QTableView.SelectRows)
    
    radio_cols_mode = QRadioButton("cols")
    radio_cols_mode.setObjectName("cols")
    radio_rows_mode.setChecked(selection_mode == QAbstractItemView.SelectColumns)
    
    radio_cell_mode = QRadioButton("cell")
    radio_cell_mode.setObjectName("cell")
    radio_rows_mode.setChecked(selection_mode == QAbstractItemView.SelectItems)
    
    
    @pyqtSlot(bool)
    def checkedSelectioinMode(flag):
      radio = self.sender()
      radioName = radio.objectName()
      
      if radio.isChecked():
        if radioName == "rows":
          print("[SELECTION_MODE][ROWS]")
          self.table.setSelectionBehavior(QTableView.SelectRows)
        elif radioName == "cols":
          print("[SELECTION_MODE][COLS]")
          self.table.setSelectionBehavior(QAbstractItemView.SelectColumns)
        elif radioName == "cell":
          print("[SELECTION_MODE][CELL]")
          self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
    
    radio_rows_mode.clicked.connect( checkedSelectioinMode )
    radio_cols_mode.clicked.connect( checkedSelectioinMode )
    radio_cell_mode.clicked.connect( checkedSelectioinMode )
    
    mode_gbox_layout.addWidget(radio_rows_mode)
    mode_gbox_layout.addWidget(radio_cols_mode)
    mode_gbox_layout.addWidget(radio_cell_mode)
    
    mode_gbox.setLayout(mode_gbox_layout)
    
    
    ### Show Grid
    show_grid_gbox = QGroupBox("Show Grid")
    show_grid_gbox_layout = QHBoxLayout()
    
    chkbox_show_grid = QCheckBox("Show")
    chkbox_show_grid.setChecked(self.table.showGrid() == True)
    
    @pyqtSlot(bool)
    def checkedShowGrid(flag):
      chkbox = self.sender()
      chkboxName = chkbox.objectName()
      
      print(chkboxName, chkbox.isChecked())
      
      self.table.setShowGrid(chkbox.isChecked())
      
    chkbox_show_grid.stateChanged.connect( checkedShowGrid )
    
    show_grid_gbox_layout.addWidget(chkbox_show_grid)
    
    show_grid_gbox.setLayout(show_grid_gbox_layout)
    
    
    ### Layout 설정
    vbox.addWidget(row_gbox)
    vbox.addWidget(col_gbox)
    vbox.addWidget(mode_gbox)
    vbox.addWidget(show_grid_gbox)
    
    scroll_gbox = QGroupBox("Scroll")
    scroll_gbox.setLayout(vbox)
    
    scroll = QScrollArea()
    scroll.setWidget(scroll_gbox)
    scroll.setWidgetResizable(True)
    scroll.setFixedHeight(200)
    
    self.layout.addWidget( scroll, 1, 0 )

  def resizeEvent(self, size):
    pass

    
# 팝업 설정
class MyDialog(QDialog):
  def __init__(self, parent=None, title="Sub Window", **kwargs):
    super(QDialog, self).__init__(parent)
    
    self.parent = parent
    self.title = title
    self.posX = int(kwargs.get("posX")) if "posX" in kwargs else 0
    self.posY = int(kwargs.get("posY")) if "posY" in kwargs else 0
    self.width = int(kwargs.get("width")) if "width" in kwargs else 300
    self.height = int(kwargs.get("height")) if "height" in kwargs else 200
    
    self.main_layout = QGridLayout()
    self.setLayout(self.main_layout)
    
    self.init_ui()
    
  def init_ui(self):
    self.init_window()
    self.init_layout()
    
  def init_window(self):
    # 제목 설정
    self.setWindowTitle(self.title)
    # 아이콘 설정
    self.setWindowIcon(QIcon("./icons/dochi.png"))
    # 크기 및 위치 설정
    self.setGeometry(self.posX, self.posY, self.width, self.height)
  
  def init_layout(self):
    layout = QGridLayout()
  
    edit = QLineEdit()
    font = edit.font()
    font.setPointSize(14)
    edit.setFont(font)
    self.edit = edit
    
    btn_submit = QPushButton("확인")
    btn_submit.clicked.connect(self.accept)

    btn_cancle = QPushButton("취소")
    btn_cancle.clicked.connect(self.reject)
    
    layout.addWidget(edit, 0, 0, 1, 4)
    layout.setRowStretch(1, 0)
    
    layout.addWidget(btn_submit, 2, 0)
    layout.setColumnStretch(2, 0)
    layout.addWidget(btn_cancle, 2, 3)
    
    self.main_layout.addLayout(layout, 0, 0)
    
    

# 위젯 설정
class MyWidget(QWidget):
  def __init__(self, parent=None):        
    super(QWidget, self).__init__(parent)
    
    self.parent = parent
    
    self.init_ui()
    
  def init_ui(self):
    self.main_layout = QGridLayout(self)
    
    self.setInput("입력창1", 0, 0)
    self.setInput("입력창2", 0, 1)
    self.setComoboBox("입력창3", 1, 0, 1, 2)
    self.setTable(2, 0, 1, 2)
    self.setModalButton("Modal", 3, 0, 1, 2)
    
    self.setLayout(self.main_layout)
    
  # Input 설정
  def setInput(self, text, row, col, rowSpan=1, colSpan=1):
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
    
    hbox.addWidget(label)
    hbox.addStretch(3)
    hbox.addWidget(line_edit)
    
    self.main_layout.addLayout(hbox, row, col, rowSpan, colSpan)
    
  # Combo 설정
  def setComoboBox(self, text, row, col, rowSpan=1, colSpan=1):
    hbox = QHBoxLayout()
    
    label = QLabel(text)
    outout_label = QLabel()
  
    cb = QComboBox(self)
    cb.addItem("Option1")
    cb.addItem("Option2")
    cb.addItem("Option3")
    cb.addItem("Option4")
    
    hbox.addWidget(label)
    hbox.addWidget(cb)
    hbox.addWidget(outout_label)
    
    @pyqtSlot(str)
    def outputMessage(msg):
      outout_label.setText(msg)
      outout_label.adjustSize()
        
    @pyqtSlot(str)
    def showMessage(msg):
      QMessageBox.information(self, '알림', msg)

    cb.activated[str].connect(outputMessage)
    cb.currentTextChanged.connect(showMessage)
    
    self.main_layout.addLayout(hbox, row, col, rowSpan, colSpan)
    
      
  # Modal 설정
  def setModalButton(self, text, row, col, rowSpan=1, colSpan=1):
    hbox = QHBoxLayout()
    
    label = QLabel(text)
    modal_text = QLabel()
    
    @pyqtSlot(bool)
    def setText(flag):
      dialog = MyDialog(self, widgh=100, height=50)
      modal = dialog.exec_()

      if modal:
        modal_text.setText( dialog.edit.text() )
        modal_text.adjustSize()
      
    button = QPushButton("열기")
    button.clicked.connect( setText )
    
    hbox.addWidget(label)
    hbox.addWidget(modal_text)
    hbox.addWidget(button)

    self.main_layout.addLayout(hbox, row, col, rowSpan, colSpan)
    
  # Table 설정
  def setTable(self, row, col, rowSpan=1, colSpan=1):
    hbox = QHBoxLayout()
    
    widget = QWidget(self)
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    table = TableWidget(widget)
    
    hbox.addWidget(widget)
    
    self.main_layout.addLayout(hbox, row, col, rowSpan, colSpan)
    

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
    self.init_ui()
    
  # 초기 설정
  def init_ui(self):
    self.init_window()
    self.init_tooltip()
    self.init_status_bar()
    self.init_menu_bar()
    self.init_tool_bar()
    self.init_widget()
  
  # Window 설정
  def init_window(self):
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
    
  # 툴팁 설정
  def init_tooltip(self):
    # 툴팁 폰트 설정
    font = QFont("SansSerif", 10)
    message = f"'<b>Window ToolTip</b>' 입니다."
    
    QToolTip.setFont(font)
    self.setToolTip(message)
    
  # 상태바 설정
  def init_status_bar(self):
    statusBar = self.statusBar()
    statusBar.showMessage("Ready")
  
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
    exit_action.setShortcut("Alt+W")
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
  app.setStyle(QStyleFactory.create('Fusion'))
  win = MyWindow("메인 윈도우", posX=100, posY=400, width=300, height=500)
  win.show()
  
  sys.exit( app.exec() )