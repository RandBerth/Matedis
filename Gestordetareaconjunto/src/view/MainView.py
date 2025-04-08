from view.dialog.Form import Form
from view.dialog.ListAll import ListAll
from view.dialog.About import About
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QMainWindow, QApplication
from PyQt6.QtGui import QPixmap, QScreen

class MainView(QWidget):

    def __init__(self, controller):
        super(MainView, self).__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.resize(350, 504)
        self.setWindowTitle('The Outlaws')

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('../media/bang.jpg'))

        self._center()
        self._create_dialogs()
        self._create_buttons()
        self._create_events()

    def _create_dialogs(self):
        self.form = Form(self.controller, self)
        self.list_all = ListAll(self.controller, self)
        self.about = About(self)

    def _create_buttons(self):
        self.insert_outlaw_button = QPushButton('Insert Outlaw', self)
        self.insert_outlaw_button.setToolTip('Insert a new outlaw.')
        self.insert_outlaw_button.resize(100, 35)
        self.insert_outlaw_button.move(230, 200)

        self.list_all_button = QPushButton('List all', self)
        self.list_all_button.setToolTip('List all the outlaws.')
        self.list_all_button.resize(100, 35)
        self.list_all_button.move(230, 240)

        self.about_button = QPushButton('About', self)
        self.about_button.setToolTip('About this software.')
        self.about_button.resize(100, 35)
        self.about_button.move(230, 280)

    def _create_events(self):
        self.insert_outlaw_button.clicked.connect(self.form.show)
        self.list_all_button.clicked.connect(self.list_all.show)
        self.about_button.clicked.connect(self.about.show)

    def _center(self):
        screen = QApplication.primaryScreen()  # Get the primary screen using QApplication
        screen_geometry = screen.availableGeometry()  # Get the screen's available geometry
        qr = self.frameGeometry()
        cp = screen_geometry.center()  # Center the window based on screen geometry
        qr.moveCenter(cp)
        self.move(qr.topLeft())
