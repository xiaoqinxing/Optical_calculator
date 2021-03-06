from ui.help_window import Ui_HelpWindow
from ui.customwidget import SubWindow


class HelpDoc(SubWindow):

    def __init__(self, name='HelpDoc', parent=None):
        super().__init__(name, parent, Ui_HelpWindow())
        with open("Readme.md", "r", encoding="utf-8") as input_file:
            text = input_file.read()
        self.ui.textBrowser.setMarkdown(text)
