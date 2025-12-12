"""
This file starts the program and opens the window
"""
import sys
from PyQt6.QtWidgets import QApplication
from logic import *

def main():
    """
    runs the app and shows the window

    """
    app = QApplication(sys.argv)
    window = VoteWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()