import sys
from importlib import resources

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from . import views

views_files = resources.files(views)


def app():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(views_files / "main.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())


if __name__ == "__main__":
    app()
