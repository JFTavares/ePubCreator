from PyQt4 import QtGui, QtCore

from epubcreator.epubbase import ebook_metadata
from epubcreator.gui.forms import metadata_tab_manager_widget_ui
from epubcreator.gui import metadata_tabs


class MetadataTabManager(QtGui.QWidget, metadata_tab_manager_widget_ui.Ui_MetadataTabManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Contiene un tag 'img' cuyo atributo 'src' es una imagen de un ícono de error.
        self._errorImgTag = self._getErrorImgTag()

    def getEbookMetadata(self):
        """
        Retorna los metadatos ingresados por el usuario.

        @return: un objeto Metadata si no hubo errores, sino None.
        """
        metadata = ebook_metadata.Metadata()

        if self._populateBasicMetadata(metadata) and self._populateAdditionalMetadata(metadata):
            return metadata
        else:
            return None

    def _populateBasicMetadata(self, metadata):
        isValid = True

        metadata.coverImage = self.basicMetadata.getCoverImage()
        metadata.title = self.basicMetadata.getTitle()
        metadata.language = self.basicMetadata.getLanguageCode()
        metadata.bookId = self.basicMetadata.getBookId()
        metadata.subtitle = self.basicMetadata.getSubtitle()
        metadata.synopsis = self.basicMetadata.getSynopsis()
        metadata.coverModification = self.basicMetadata.getCoverModification()
        metadata.coverDesigner = self.basicMetadata.getCoverDesigner()

        for author in self.basicMetadata.getAuthors():
            metadata.authors.append(author)

        return isValid

    def _populateAdditionalMetadata(self, metadata):
        isValid = True

        metadata.dedication = self.additionalMetadata.getDedication()
        metadata.originalTitle = self.additionalMetadata.getOriginalTitle()

        try:
            metadata.publicationDate = self.additionalMetadata.getPublicationDate()
        except metadata_tabs.ValidationException as e:
            self._showError(e.error, e.description, e.tab, e.widget)
            isValid = False

        try:
            collection = self.additionalMetadata.getCollection()
            metadata.collectionName = collection[0]
            metadata.subCollectionName = collection[1]
            metadata.collectionVolume = collection[2]
        except metadata_tabs.ValidationException as e:
            self._showError(e.error, e.description, e.tab, e.widget)
            isValid = False

        for translator in self.additionalMetadata.getTranslators():
            metadata.translators.append(translator)

        for ilustrator in self.additionalMetadata.getIlustrators():
            metadata.ilustrators.append(ilustrator)

        for genre in self.additionalMetadata.getGenres():
            metadata.genres.append(genre)

        return isValid

    def _showError(self, error, description, tab, widget):
        toolTipMsg = ('<p>{0} <b> {1}</b></p><p style="margin-left: 0.5em;">{2}</p>'.format(self._errorImgTag, error, description))
        toolTipPos = widget.mapToGlobal(QtCore.QPoint(0, 0))

        self.metadataTabManager.setCurrentWidget(tab)
        widget.setFocus()

        QtGui.QToolTip.showText(toolTipPos, toolTipMsg)

    def _getErrorImgTag(self):
        """
        Retorna un tag 'img' cuyo source es el ícono de error y depende del sistema operativo.

        @return: un string con el tag img (cuyo atributo 'src' es la imagen codificada en base64).
        """
        # Html permite poner en 'src' datos codificados en base64. Esto me permite cargar a mí el ícono de error
        # estándar para cada operativo. Sino lo que tengo que hacer es meter algún ícono de error genérico en un
        # archivo de recurso y cargarlo.
        errorIcon = self.style().standardIcon(QtGui.QStyle.SP_MessageBoxCritical)

        ba = QtCore.QByteArray()
        buffer = QtCore.QBuffer(ba)
        buffer.open(QtCore.QIODevice.WriteOnly)
        errorIcon.pixmap(QtCore.QSize(24, 24)).save(buffer, "PNG")
        imgTag = '<img src="data:image/png;base64,{0}"/>'.format(bytes(buffer.data().toBase64()).decode("utf-8"))
        buffer.close()

        return imgTag