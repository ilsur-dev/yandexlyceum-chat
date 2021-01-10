import sys
from PyQt5.QtWidgets import QApplication
from wrapper import WebsocketWrapper
import logging

FORMAT = '[%(asctime)-15s] [%(levelname)s] - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ws = WebsocketWrapper()
    sys.exit(app.exec_())