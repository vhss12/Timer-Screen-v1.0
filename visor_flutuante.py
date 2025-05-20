from PyQt5 import QtWidgets, QtCore, QtGui
import sys

class FloatingTimer(QtWidgets.QWidget):
    def __init__(self, time_str="00:00"):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.label = QtWidgets.QLabel(time_str, self)
        self.font_size = 80
        self.timeout_font_size = 45  # Tamanho da fonte para "TEMPO ESGOTADO"
        self.font_family = "Segoe UI"
        self.font_weight = QtGui.QFont.Bold
        font = QtGui.QFont(self.font_family, self.font_size, self.font_weight)
        self.label.setFont(font)
        self.label.setStyleSheet("color: black;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.resize(self.label.sizeHint())
        self._drag_pos = None

    def set_time(self, time_str):
        # Usa um tamanho de fonte menor para "TEMPO ESGOTADO"
        if time_str == "TEMPO ESGOTADO":
            font = QtGui.QFont(self.font_family, self.timeout_font_size, self.font_weight)
        else:
            font = QtGui.QFont(self.font_family, self.font_size, self.font_weight)
        self.label.setFont(font)
        self.label.setText(time_str)

    def increase_font_size(self):
        self.font_size += 10
        self.set_time(self.label.text())

    def decrease_font_size(self):
        if self.font_size > 20:
            self.font_size -= 10
            self.set_time(self.label.text())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def set_color(self, color):
        allowed = {"white", "red", "green", "black", "yellow"}
        if color not in allowed:
            color = "black"
        self.label.setStyleSheet(f"color: {color};")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    visor = FloatingTimer("12:34")
    visor.show()
    visor.set_color("red")     # vermelho
    visor.set_color("white")   # branco
    visor.set_color("green")   # verde
    visor.set_color("black")   # preto
    visor.set_color("yellow")  # amarelo
    sys.exit(app.exec_()) 