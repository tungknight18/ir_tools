import sys
import re
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import QMimeData

class PlainTextEdit(QtWidgets.QTextEdit):
    def insertFromMimeData(self, source: QMimeData):
        """Ép chỉ nhận plain text khi paste vào ô nhập liệu"""
        if source.hasText():
            self.insertPlainText(source.text())

def parse_list(input_str):
    """Chuyển đổi chuỗi nhập vào thành danh sách số nguyên, hỗ trợ cả raw và Pronto hex."""
    input_str = re.sub(r'\s+', ' ', input_str).strip()
    try:
        if ',' in input_str or '\n' in input_str:
            # Xử lý mã raw (có dấu phẩy hoặc xuống dòng)
            return list(map(int, input_str.replace('\n', ',').split(',')))
        else:
            # Xử lý mã Pronto hex (các giá trị hex cách nhau bởi khoảng trắng)
            return [int(x, 16) for x in input_str.split(' ')]    
    except ValueError:
        return None

class ListComparator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("So sánh hai danh sách")
        self.setGeometry(100, 100, 500, 400)
        
        layout = QVBoxLayout()
        
        self.label_tolerance = QLabel("Sai số:")
        layout.addWidget(self.label_tolerance)
        
        self.entry_tolerance = QLineEdit()
        self.entry_tolerance.setText("0.15")
        layout.addWidget(self.entry_tolerance)
        
        self.label_list1 = QLabel("Danh sách 1:")
        layout.addWidget(self.label_list1)        

        self.entry_list1 = PlainTextEdit()
        self.entry_list1.setPlaceholderText("Nhập danh sách số, cách nhau bởi dấu phẩy hoặc xuống dòng")
        layout.addWidget(self.entry_list1)
        
        self.label_list2 = QLabel("Danh sách 2:")
        layout.addWidget(self.label_list2)
        
        self.entry_list2 = PlainTextEdit()
        self.entry_list2.setPlaceholderText("Nhập danh sách số, cách nhau bởi dấu phẩy hoặc xuống dòng")
        layout.addWidget(self.entry_list2)
        

        self.compare_button = QPushButton("So sánh")
        self.compare_button.clicked.connect(self.compare_lists)
        layout.addWidget(self.compare_button)
        
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)
    
    def compare_lists(self):
        list1 = parse_list(self.entry_list1.toPlainText())
        list2 = parse_list(self.entry_list2.toPlainText())

        if list1 is None and list2 is None:
            self.result_label.setText("Danh sách 1 và 2 không hợp lệ!")
            self.result_label.setStyleSheet("color: red;")
            return
        elif list1 is None and list2 is not None:
            self.result_label.setText("Danh sách 1 không hợp lệ!")
            self.result_label.setStyleSheet("color: red;")
            return
        elif list1 is not None and list2 is None:
            self.result_label.setText("Danh sách 2 không hợp lệ!")
            self.result_label.setStyleSheet("color: red;")
            return
        
        try:
            tolerance = float(self.entry_tolerance.text())
        except ValueError:
            self.result_label.setText("Sai số phải là một số hợp lệ.")
            self.result_label.setStyleSheet("color: red;")
            return
        
        if len(list1) != len(list2):
            self.result_label.setText("Không khớp (Chiều dài mảng không bằng nhau)")
            self.result_label.setStyleSheet("color: red;")
            return
        
        for i in range(len(list1)):
            temp = max(abs(list1[i]), abs(list2[i]))
            if abs(list1[i] - list2[i]) > tolerance * temp:
                self.result_label.setText("Không khớp")
                self.result_label.setStyleSheet("color: red;")
                return
        
        self.result_label.setText("Khớp")
        self.result_label.setStyleSheet("color: green;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ListComparator()
    window.show()
    sys.exit(app.exec_())
