import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.alert_icon = QIcon('.\\icons\\icon.ico')  # Путь к иконке для alert

    def javaScriptAlert(self, securityOrigin, msg):
        alert = QMessageBox()
        alert.setWindowTitle('JavaScript')
        alert.setText(msg)
        alert.setIcon(QMessageBox.Information)
        alert.setWindowIcon(self.alert_icon)
        alert.exec_()

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WebEngine5')
        self.setGeometry(200, 200, 1200, 800)
        
        self.browser = QWebEngineView()
        self.browser.setPage(CustomWebEnginePage(self.browser))
        self.browser.page().titleChanged.connect(self.update_title)
        self.browser.page().loadFinished.connect(self.on_load_finished)
        
        self.reload_button = QPushButton('Reload', self)
        self.reload_button.clicked.connect(self.browser.reload)
        
        self.fullscreen_button = QPushButton('F11', self)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        self.site_label = QLabel('', self)

        layout = QVBoxLayout()
        layout.addWidget(self.reload_button)
        layout.addWidget(self.fullscreen_button)
        layout.addWidget(self.site_label)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(self.browser)
        
        # Проверяем, есть ли ссылка в аргументах командной строки
        if len(sys.argv) > 1:
            self.load_url_or_file(sys.argv[1])  # Загружаем ссылку или локальный файл, переданный через аргументы командной строки
        else:
            self.browser.setUrl(QUrl(''))  # Иначе загружаем пустую страницу по умолчанию

        self.addToolBar(Qt.TopToolBarArea, self.create_toolbar())
        
        self.set_taskbar_icon()  # Устанавливаем иконку в панели задач
        
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def create_toolbar(self):
        toolbar = self.addToolBar("Toolbar")
        toolbar.addWidget(self.reload_button)
        toolbar.addWidget(self.fullscreen_button)
        toolbar.addWidget(self.site_label)
        return toolbar

    def update_site_label(self, url):
        self.site_label.setText(url.toString())
    
    def set_taskbar_icon(self):
        taskbar_icon = QIcon('.\\icons\\icon.ico')  # Путь к вашей иконке
        self.setWindowIcon(taskbar_icon)
        # Дополнительная строка для изменения иконки в панели задач
        if hasattr(sys, 'frozen'):
            self.app_id = 'WebEngine5.KixtTeam.Ru'  # Идентификатор вашего приложения
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.app_id)

    def load_url_or_file(self, path):
        if os.path.isfile(path):  # Проверка, является ли путь к локальным файлом
            local_url = QUrl.fromLocalFile(path)
            self.browser.setUrl(local_url)
        else:  # Иначе считаем, что это веб-ресурс
            self.browser.setUrl(QUrl(path))
    

    def on_load_finished(self, success):
        if not success:
            self.browser.setHtml('<h1>404 - Page Not Found</h1><p>The page could not be loaded.</p>')

    def update_title(self, title):
        self.setWindowTitle(f'WebEngine5 - {title}')

app = QApplication(sys.argv)
window = Browser()
window.show()
sys.exit(app.exec_())
