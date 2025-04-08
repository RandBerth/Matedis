from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel, QGridLayout, QMessageBox
from PyQt6.QtGui import QDoubleValidator
from model.Outlaw import Outlaw

class Form(QDialog):

    def __init__(self, controller=None, parent=None):
        super(Form, self).__init__(parent)
        
        self.controller = controller
        self._create_buttons()
        self._create_lines()
        self._create_grid()
        self._create_events()
        
    def _create_buttons(self):
        self.insert_button = QPushButton('Insert')
        self.insert_button.setToolTip('Insert outlaw.')
        
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setToolTip('Back to main screen.')
        
    def _create_lines(self):
        self.name_edit = QLineEdit()
        self.surname_edit = QLineEdit()
        self.reward_edit = QLineEdit()
        self.reward_edit.setValidator(QDoubleValidator(0.0, 100000.00, 2, self))
        
    def _create_grid(self):
        grid = QGridLayout()
        
        grid.addWidget(QLabel('Name:'), 0, 0)
        grid.addWidget(self.name_edit, 0, 1)
        
        grid.addWidget(QLabel('Surname:'), 1, 0)
        grid.addWidget(self.surname_edit, 1, 1)
        
        grid.addWidget(QLabel('Reward ($):'), 2, 0)
        grid.addWidget(self.reward_edit, 2, 1)
        
        grid.addWidget(self.insert_button, 3, 0)
        grid.addWidget(self.cancel_button, 3, 1)
        
        self.setLayout(grid)
        
    def _create_events(self):
        self.insert_button.clicked.connect(self._insert)
        self.cancel_button.clicked.connect(self.close)
        
    def _insert(self):
        reward = str(self.reward_edit.text())
        
        if reward == '':
            reward = 0.0
        else:
            reward = float(reward)
        
        outlaw = Outlaw(str(self.name_edit.text()), str(self.surname_edit.text()), reward)
        
        if not self.controller.save(outlaw):
            QMessageBox.warning(self, 'WARNING', 'There are blank fields.', QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, 'Success', 'Outlaw saved.', QMessageBox.StandardButton.Ok)
            
        self._clear()
        
    def _clear(self):
        self.name_edit.clear()
        self.surname_edit.clear()
        self.reward_edit.clear()
