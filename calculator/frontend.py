import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from .ui.ui_home_page import Ui_Calculator
from .backend import CalculatorEngine

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Calculator()
        self.ui.setupUi(self)
        
        # Initialize calculator engine
        self.calc_engine = CalculatorEngine()
        
        # Connect button signals to slots
        self.connect_buttons()
        
        # Set window properties
        self.setWindowTitle("Calculator")
        self.setFixedSize(400, 600)  # Make it a bit taller for the extra button
        
    def connect_buttons(self):
        """Connect all button signals to their respective slots"""
        
        # Number buttons
        self.ui.btn_0.clicked.connect(lambda: self.number_clicked('0'))
        self.ui.btn_1.clicked.connect(lambda: self.number_clicked('1'))
        self.ui.btn_2.clicked.connect(lambda: self.number_clicked('2'))
        self.ui.btn_3.clicked.connect(lambda: self.number_clicked('3'))
        self.ui.btn_4.clicked.connect(lambda: self.number_clicked('4'))
        self.ui.btn_5.clicked.connect(lambda: self.number_clicked('5'))
        self.ui.btn_6.clicked.connect(lambda: self.number_clicked('6'))
        self.ui.btn_7.clicked.connect(lambda: self.number_clicked('7'))
        self.ui.btn_8.clicked.connect(lambda: self.number_clicked('8'))
        self.ui.btn_9.clicked.connect(lambda: self.number_clicked('9'))
        
        # Operation buttons
        self.ui.btn_add.clicked.connect(lambda: self.operation_clicked('+'))
        self.ui.btn_subtract.clicked.connect(lambda: self.operation_clicked('-'))
        self.ui.btn_multiply.clicked.connect(lambda: self.operation_clicked('*'))
        self.ui.btn_divide.clicked.connect(lambda: self.operation_clicked('/'))
        
        # Function buttons
        self.ui.btn_equals.clicked.connect(self.equals_clicked)
        self.ui.btn_clear.clicked.connect(self.clear_clicked)
        self.ui.btn_decimal.clicked.connect(self.decimal_clicked)
        self.ui.btn_toggle_sign.clicked.connect(self.toggle_sign_clicked)
        self.ui.btn_percentage.clicked.connect(self.percentage_clicked)
        self.ui.btn_square.clicked.connect(self.square_clicked)
        
        # Enable keyboard input
        self.setFocusPolicy(Qt.StrongFocus)
        
    def keyPressEvent(self, event):
        """Handle keyboard input"""
        key = event.key()
        
        # Number keys
        if Qt.Key_0 <= key <= Qt.Key_9:
            digit = str(key - Qt.Key_0)
            self.number_clicked(digit)
        
        # Operation keys
        elif key == Qt.Key_Plus:
            self.operation_clicked('+')
        elif key == Qt.Key_Minus:
            self.operation_clicked('-')
        elif key == Qt.Key_Asterisk:
            self.operation_clicked('*')
        elif key == Qt.Key_Slash:
            self.operation_clicked('/')
        
        # Function keys
        elif key in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Equal):
            self.equals_clicked()
        elif key == Qt.Key_Period:
            self.decimal_clicked()
        elif key in (Qt.Key_Escape, Qt.Key_C):
            self.clear_clicked()
        elif key == Qt.Key_Backspace:
            self.backspace_clicked()
            
        super().keyPressEvent(event)
    
    def number_clicked(self, digit):
        """Handle number button clicks"""
        display_text = self.calc_engine.add_digit(digit)
        self.update_display(display_text)
    
    def operation_clicked(self, operation):
        """Handle operation button clicks"""
        # Convert display symbols to internal operators
        op_map = {'+': '+', '-': '-', '×': '*', '÷': '/'}
        internal_op = op_map.get(operation, operation)
        
        result = self.calc_engine.set_operation(internal_op)
        if result is not None:
            self.update_display(result)
    
    def equals_clicked(self):
        """Handle equals button click"""
        result = self.calc_engine.calculate()
        if result is not None:
            if result == "Error":
                self.update_display("Error")
                self.calc_engine.clear()
            else:
                display_text = self.calc_engine.format_number(result)
                self.update_display(display_text)
    
    def clear_clicked(self):
        """Handle clear button click"""
        result = self.calc_engine.clear()
        self.update_display(result)
    
    def decimal_clicked(self):
        """Handle decimal button click"""
        display_text = self.calc_engine.add_decimal()
        self.update_display(display_text)
    
    def toggle_sign_clicked(self):
        """Handle toggle sign button click"""
        current_display = self.ui.display.text()
        result = self.calc_engine.toggle_sign(current_display)
        self.update_display(result)
    
    def percentage_clicked(self):
        """Handle percentage button click"""
        current_display = self.ui.display.text()
        result = self.calc_engine.calculate_percentage(current_display)
        self.update_display(result)
    
    def square_clicked(self):
        """Handle square button click"""
        current_display = self.ui.display.text()
        result = self.calc_engine.calculate_square(current_display)
        self.update_display(result)
    
    def backspace_clicked(self):
        """Handle backspace functionality"""
        current_text = self.ui.display.text()
        
        if current_text == "Error" or self.calc_engine.just_calculated:
            self.clear_clicked()
            return
            
        if len(current_text) > 1:
            new_text = current_text[:-1]
            if new_text.endswith('.'):
                self.calc_engine.has_decimal = False
        else:
            new_text = "0"
            
        self.calc_engine.current_input = new_text if new_text != "0" else ""
        self.update_display(new_text)
    
    def update_display(self, text):
        """Update the calculator display"""
        # Limit display length to prevent overflow
        if len(str(text)) > 15:
            if text == "Error":
                self.ui.display.setText("Error")
            else:
                # Scientific notation for very large numbers
                try:
                    num = float(text)
                    self.ui.display.setText(f"{num:.6e}")
                except:
                    self.ui.display.setText("Error")
        else:
            self.ui.display.setText(str(text))

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Calculator")
    app.setApplicationVersion("1.0")
    
    # Create and show calculator
    calculator = CalculatorApp()
    calculator.show()
    
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Calculator closed.')

if __name__ == '__main__':
    main()