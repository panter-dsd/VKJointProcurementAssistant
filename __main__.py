# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'

import sys
import re
from PyQt4 import QtCore, QtGui, QtWebKit

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._web_view = QtWebKit.QWebView(self)
        self._web_view.load(QtCore.QUrl("http://vk.com"))

        self._table = QtGui.QTableView(self)

        self._model = QtGui.QStringListModel(self)
        self._table.setModel(self._model)

        self._text_view = QtGui.QPlainTextEdit(self)

        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(self._table)
        vLayout.addWidget(self._text_view)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._web_view)
        layout.addLayout(vLayout)

        central_widget = QtGui.QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        timer = QtCore.QTimer(self)
        timer.setInterval(100)
        timer.setSingleShot(False)
        timer.timeout.connect(self._update_table)
        timer.start()

    def _update_table(self):
        text = self._web_view.page().currentFrame().toHtml()
        author_re = re.compile("<a href=\".*\" onclick=\"return nav.go\(this, event\)\" class=\"author\">(.*)<\/a>")
        comment_re = re.compile("<div class=\"pv_commtext\">\D*([0123456789]+)\D*<\/div>")

        authors = []

        output_text = []

        sum = 0
        for author_match in author_re.finditer(text):
            authors.append(author_match.group(1))

            comment_match = comment_re.search(text, author_match.end(), author_match.end() + 1024)

            if comment_match:
                for group in comment_match.groups():
                    if (int(group) > 0) and (int(group) < 1000):
                        output_text.append(author_match.group(1) + " " + group)
                        sum += int(group)

        self._model.setStringList(authors)

        output_text.append("======================= {0}".format(sum))
        output_text_str = "\n".join(output_text)

        if output_text_str != self._text_view.toPlainText():
            self._text_view.setPlainText(output_text_str)


app = QtGui.QApplication(sys.argv)
win = MainWindow()
win.show()

sys.exit(app.exec())