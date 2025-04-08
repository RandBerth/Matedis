if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon  # QIcon debe ser importado desde PyQt6.QtGui

    from view.MainView import MainView
    from controller.OutlawController import OutlawController
    
    app = QApplication(sys.argv)  # QApplication sigue siendo de QtWidgets
    main = MainView(OutlawController())
    main.show()
    sys.exit(app.exec())  # En PyQt6, se usa exec() en lugar de exec_()
