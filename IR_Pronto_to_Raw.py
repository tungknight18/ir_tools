import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMimeData

class PlainTextEdit(QtWidgets.QTextEdit):
    def insertFromMimeData(self, source: QMimeData):
        """Ép chỉ nhận plain text khi paste vào ô nhập liệu"""
        if source.hasText():
            self.insertPlainText(source.text())
            
def pronto_to_raw(pronto_str):
    """
    Chuyển đổi Pronto code (chuỗi hex, các token cách nhau bởi khoảng trắng)
    sang IR raw code dạng dãy số thời gian (micro giây) xen kẽ giữa pulse (dương)
    và space (âm).

    Quy trình:
      1. Tách các token và chuyển sang số nguyên.
      2. Kiểm tra định dạng: chỉ hỗ trợ khi token đầu tiên là 0000.
      3. Lấy frequency code từ token thứ 2 và tính đơn vị thời gian:
             unit = frequency_code * 0.241246   (micro giây)
      4. Bỏ qua 4 token đầu và lấy các token còn lại làm chuỗi burst.
      5. Với mỗi token của burst, tính thời gian tương ứng và gán dấu:
             - Các giá trị ở vị trí chẵn (0, 2, …) là pulse (dương).
             - Các giá trị ở vị trí lẽ (1, 3, …) là khoảng cách (space, âm).
      6. Định dạng kết quả hiển thị dãy số trên nhiều dòng.
    """
    tokens = pronto_str.split()
    if not tokens:
        return "Input rỗng."
    try:
        # Chuyển các token hex sang số nguyên
        values = [int(token, 16) for token in tokens]
    except Exception as e:
        return f"Lỗi khi chuyển đổi giá trị hex: {e}"
    
    if values[0] != 0:
        return "Chỉ hỗ trợ Pronto code định dạng 0000."
    
    freq_code = values[1]
    if freq_code == 0:
        return "Mã frequency bằng 0, không thể tính đơn vị thời gian."
    else:
        freq = 1000000/(freq_code *0.241246)
    result = f"Tần số: \n{freq:.0f}\n"
    # Tính đơn vị thời gian (micro giây)
    unit = freq_code * 0.241246

    # Lấy dãy burst (bỏ qua 4 token đầu)
    burst_sequence = values[4:]
    if len(burst_sequence) == 0:
        return "Không tìm thấy burst data trong Pronto code."

    raw_durations = []
    for index, token in enumerate(burst_sequence):
        # Tính thời gian thực (micro giây)
        duration = token * unit
        # Gán dấu: pulse (các token ở vị trí chẵn) dương, space (vị trí lẽ) âm.
        if index % 2 == 1:
            duration = -duration
        raw_durations.append(round(duration))
    
    # Tạo chuỗi kết quả: các giá trị được cách nhau bởi dấu cách
    raw_code_str = ", ".join(str(x) for x in raw_durations)
    result += f"Raw code:\n[{raw_code_str}]"
    return result

# --- Giao diện PyQt5 ---
class ConverterWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("IR Pronto to Raw Code Converter")
        self.resize(500, 400)
        
        layout = QtWidgets.QVBoxLayout()
        
        # Label và ô nhập Pronto code
        self.input_label = QtWidgets.QLabel("Nhập/Paste Pronto Code:")
        layout.addWidget(self.input_label)
        
        # Định dạng text 
        self.input_text = PlainTextEdit()
        layout.addWidget(self.input_text)
        
        # Nút Convert
        self.convert_button = QtWidgets.QPushButton("Convert")
        layout.addWidget(self.convert_button)
        
        # Label và ô hiển thị kết quả Raw code
        self.output_label = QtWidgets.QLabel("Kết quả Raw Code:")
        layout.addWidget(self.output_label)
        
        self.output_text = QtWidgets.QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        self.setLayout(layout)
        
        # Kết nối sự kiện click nút Convert
        self.convert_button.clicked.connect(self.convert_code)
        
    def convert_code(self):
        pronto_str = self.input_text.toPlainText()
        raw_code_result = pronto_to_raw(pronto_str)
        self.output_text.setPlainText(raw_code_result)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec_())