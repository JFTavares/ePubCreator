import zipfile
import os

from lxml import etree

from epubcreator.pyepub.pyepubreader import opf, toc


class EpubReader:
    """ Simple clase para leer el contenido de un epub, que la hice con el
        único de propósito de usarla para los unittests, por ahora. """

    def __init__(self, fileInput):
        """
        Abre un epub.

        @param fileInput: el path del epub a abrir, o un objeto de tipo file.
        """
        self._epub = zipfile.ZipFile(fileInput, "r")

        pathToOpf = self._getPathToOpf()
        # En el directorio donde esté ubicado content.opf, es donde se encuentran
        # el resto de los archivos.
        self._rootDir = os.path.split(pathToOpf)[0]
        self._opf = opf.Opf(self._epub.open(pathToOpf))

        # No puedo hacer un os.path.join, porque imperiosamente necesito usar esta barra: "/" y
        # no esta "\".
        self._toc = toc.Toc(self._epub.open("/".join(("OEBPS", self._opf.getPathToToc()))))

    def getHtmlFileNamesReadingOrder(self):
        """
        Retorna los htmls en orden de lectura (según el playorder).

        @return: una lista de strings con el nombre de cada html.
        """
        return self._opf.getSpineItems()

    def getNamelist(self):
        return [os.path.split(f)[1] for f in self._epub.namelist()]

    def hasFile(self, fileName):
        return any(fileName in x for x in self.getNamelist())

    def getFullPathToFile(self, fileName):
        return next((f for f in self._epub.namelist() if f.endswith("/" + fileName)), None)

    def getAuthors(self):
        return self._opf.getAuthors()

    def getTranslators(self):
        return self._opf.getTranslators()

    def getIlustrators(self):
        return self._opf.getIlustrators()

    def getCalibreSerie(self):
        """
        Retorna la serie, especificada en el formato de calibre.

        @return: una tupla de strings: el primer elemento es el nombre de la serie, y el segundo el índice.
        """
        return self._opf.getCalibreSerie()

    def getTitles(self):
        return self._toc.getTitles()

    def getDescription(self):
        return self._opf.getDescription()

    def getTitle(self):
        return self._opf.getTitle()

    def getLanguage(self):
        return self._opf.getLanguage()

    def getModificationDate(self):
        return self._opf.getModificationDate()

    def getPublicationDate(self):
        return self._opf.getPublicationDate()

    def getPublisher(self):
        return self._opf.getPublisher()

    def getSubject(self):
        return self._opf.getSubject()

    def open(self, name):
        return self._epub.open(name)

    def read(self, name):
        return self._epub.read(name)

    def _getPathToOpf(self):
        container = etree.parse(self._epub.open("META-INF/container.xml"))
        return container.xpath("/inf:container/inf:rootfiles/inf:rootfile/@full-path",
                               namespaces={"inf": "urn:oasis:names:tc:opendocument:xmlns:container"})[0]

    def close(self):
        self._epub.close()