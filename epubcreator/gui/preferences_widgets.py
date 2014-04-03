import platform

from PyQt4 import QtGui, QtCore

from epubcreator.gui.forms import preferences_general_widget_ui, preferences_docx_widget_ui
from epubcreator.gui.misc import settings_store, utils
from epubcreator.converters.docx import docx_converter


class PreferencesAbstract(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def saveSettings(self):
        raise NotImplemented


class GeneralPreferences(PreferencesAbstract, preferences_general_widget_ui.Ui_GeneralPreferences):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.changeSigilPathButton.clicked.connect(self._changeSigilPath)

        self._loadSettings()

    def saveSettings(self):
        settings = settings_store.SettingsStore()

        settings.editor = self.editorInput.text().strip()
        settings.sigilPath = self.sigilPathInput.text().strip()

    def _loadSettings(self):
        settings = settings_store.SettingsStore()

        self.editorInput.setText(settings.editor)
        self.sigilPathInput.setText(settings.sigilPath)

    def _changeSigilPath(self):
        dialogFilter = "Sigil (sigil.exe)"

        if platform.system() == "Linux":
            dialogFilter = "Sigil (sigil)"
        elif platform.system() == "Darwin":
            dialogFilter = "Sigil (Sigil.app)"

        fileName = QtGui.QFileDialog.getOpenFileName(self, "", "", dialogFilter)
        if fileName:
            self.sigilPathInput.setText(fileName)


class DocxPreferences(PreferencesAbstract, preferences_docx_widget_ui.Ui_DocxPreferences):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._extendUi()

        self._loadSettings()

    def saveSettings(self):
        settings = settings_store.SettingsStore()

        settings.docxIgnoreEmptyParagraphs = self.ignoreEmptyParagraphsInput.isChecked()

    def _loadSettings(self):
        settings = settings_store.SettingsStore()

        self.ignoreEmptyParagraphsInput.setCheckState(QtCore.Qt.Checked if settings.docxIgnoreEmptyParagraphs else QtCore.Qt.Unchecked)

    def _extendUi(self):
        self.ignoreEmptyParagraphsInput.setToolTip(utils.insertNewLines(docx_converter.DocxConverter.getOptionDescription("ignoreEmptyParagraphs")))