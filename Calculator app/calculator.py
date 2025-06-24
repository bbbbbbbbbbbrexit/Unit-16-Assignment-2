import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basic Calculator")
        self.setFixedSize(300, 400)

        self.createUI()

    def createUI(self):
        # Set up the main layout
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # Display for user input and results
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px;")
        mainLayout.addWidget(self.display)

        # Sets up button grid layout
        grid = QGridLayout()
        mainLayout.addLayout(grid)

        # Define their position
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0, 1, 4)
        ]

        # Make the buttons dynamically and add to the grid 
        for item in buttons:
            label = item[0]
            row = item[1]
            col = item[2]
            rowspan = item[3] if len(item) > 3 else 1
            colspan = item[4] if len(item) > 4 else 1

            btn = QPushButton(label)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet("font-size: 18px;")
            grid.addWidget(btn, row, col, rowspan, colspan)
            
            btn.clicked.connect(lambda checked, text=label: self.on_button_click(text))


    def on_button_click(self, text):
        # Clear the display
        if text == 'C':
            self.display.clear()
            
        # Evaluate the expression
        elif text == '=':
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except Exception:
                self.display.setText("Error")
                
        # Add the button to the display
        else:
            self.display.setText(self.display.text() + text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec_())
