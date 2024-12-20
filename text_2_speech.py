from newspaper import Article
from gtts import gTTS
from nltk.tokenize import sent_tokenize
import nltk
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLineEdit, QLabel, QMessageBox)
import sys

class VentanaTextoAVoz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertidor de Artículo a Audio")
        self.setGeometry(100, 100, 400, 200)
        
        # Widget y layout principal
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)
        layout = QVBoxLayout()
        
        # Elementos de la interfaz
        self.label_url = QLabel("URL del artículo:")
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("Introduce la URL del artículo")
        
        self.label_archivo = QLabel("Nombre del archivo:")
        self.input_archivo = QLineEdit()
        self.input_archivo.setPlaceholderText("articulo.mp3")
        
        self.boton_convertir = QPushButton("Convertir a Audio")
        self.boton_convertir.clicked.connect(self.convertir_articulo)
        
        # Añadir elementos al layout
        layout.addWidget(self.label_url)
        layout.addWidget(self.input_url)
        layout.addWidget(self.label_archivo)
        layout.addWidget(self.input_archivo)
        layout.addWidget(self.boton_convertir)
        
        widget_principal.setLayout(layout)

    def convertir_articulo(self):
        url = self.input_url.text()
        nombre_archivo = self.input_archivo.text()
        
        if not url:
            QMessageBox.warning(self, "Error", "Por favor, introduce una URL")
            return
            
        if not nombre_archivo:
            nombre_archivo = "articulo.mp3"
            
        # Validar URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url.lstrip('/:')
        
        # Intentar convertir el artículo
        if articulo_a_audio(url, nombre_archivo):
            QMessageBox.information(self, "Éxito", f"Archivo guardado como: {nombre_archivo}")
        else:
            QMessageBox.critical(self, "Error", "No se pudo procesar el artículo")

def articulo_a_audio(url, nombre_archivo="articulo.mp3"):
    try:
        # Descargar y parsear el artículo
        articulo = Article(url)
        articulo.download()
        articulo.parse()
        
        # Extraer el texto del artículo
        texto = articulo.text
        
        # Dividir el texto en oraciones para mejor procesamiento
        oraciones = sent_tokenize(texto)
        texto_con_pausas = '. '.join(oraciones)
        
        # Convertir el texto a audio
        tts = gTTS(text=texto_con_pausas, lang='es')
        
        # Guardar el archivo de audio
        tts.save(nombre_archivo)
        
        return True
        
    except Exception as e:
        print(f"Error al procesar el artículo: {str(e)}")
        return False

# Ejemplo de uso
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaTextoAVoz()
    ventana.show()
    sys.exit(app.exec_())
