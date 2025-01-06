#texto_a_voz
#1.5.5

#importaciones de librerias

from gtts import gTTS
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog, font
import tkinter.font as tkFont
import os
import pygame
from deep_translator import (
    GoogleTranslator,
)

#
class TextoAVozApp:
    def __init__(self, root):
        #ruta base
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Cargar la fuente latin modern sansquotation
        self.load_custom_font()
        
        pygame.mixer.init()
        self.root = root
        self.root.title("Texto a Voz 1.5.5 / Academia ConquerBlocks / PoliXDev")
        self.root.geometry("1000x700")
        
        # Reemplazar configuración de estilos
        self.style = ttk.Style()
        
        # Configurar voces
        self.available_voices = {
            'Español': 'es',
            'Inglés': 'en'
        }
        
        # Añadir el color de fondo para el área de texto
        self.text_bg_color = '#FFFFFF' #blanco
        
        # Crear widgets
        self.create_widgets()
        
        # Historial de textos
        self.text_history = []
        self.current_history_index = -1
        self.is_playing = False 
#carga de fuente    
    def load_custom_font(self):
        try:
            # Crear las diferentes variantes de la fuente usando latin modern sansquotation
            self.custom_title = tkFont.Font(family="latin modern sansquotation", size=24, weight="bold")
            self.custom_subtitle = tkFont.Font(family="latin modern sansquotation", size=12)
            self.custom_text = tkFont.Font(family="latin modern sansquotation", size=12)
            self.custom_small = tkFont.Font(family="latin modern sansquotation", size=10)
            
        except Exception as e:
            print(f"Error al cargar la fuente latin modern sansquotation: {e}")
            # Fallback a nimbus sans l (similar a Helvetica/Arial) si hay error
            self.custom_title = tkFont.Font(family="nimbus sans l", size=24, weight="bold")
            self.custom_subtitle = tkFont.Font(family="nimbus sans l", size=12)
            self.custom_text = tkFont.Font(family="nimbus sans l", size=12)
            self.custom_small = tkFont.Font(family="nimbus sans l", size=10)

#creacion de widgets
    def create_widgets(self):
        #carga de iconos
        icon_size = (20, 20)  # Tamaño para los iconos
        self.icons = {}
        
        for icon_name in ['open', 'save', 'clear', 'translate', 'play', 'stop']:
            icon = tk.PhotoImage(file=os.path.join(self.base_path, 'icons', f'{icon_name}.png'))
            # Redimensionar el icono
            icon = icon.subsample(int(icon.width() / icon_size[0]), int(icon.height() / icon_size[1]))
            self.icons[icon_name] = icon

        # Frame principal con padding y estilo bootstrap
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título y subtítulo con estilos bootstrap
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        #titulo
        title_label = ttk.Label(title_frame, 
                              text="Convertidor de Texto a Voz",
                              font=self.custom_title,
                              bootstyle="primary")
        title_label.pack()
        #subtitulo
        subtitle_label = ttk.Label(title_frame,
                                 text="Convierte cualquier texto a voz natural",
                                 font=self.custom_subtitle,
                                 bootstyle="secondary")
        subtitle_label.pack(pady=(5, 0))

        # Barra de herramientas con botones bootstrap
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Definir los botones de la barra de herramientas con sus iconos
        toolbar_buttons = [
            ("Abrir Texto", self.load_text, 'open'),
            ("Guardar Audio", self.save_audio, 'save'),
            ("Limpiar", self.clear_text, 'clear'),
            ("Traducir Texto", self.translate_current_text, 'translate')
        ]
        #botones de la barra de herramientas
        for text, command, icon_name in toolbar_buttons:
            btn = ttk.Button(toolbar_frame, 
                            text=f" {text}", 
                            command=command,
                            image=self.icons[icon_name],
                            compound='left',
                            bootstyle="info-outline")
            btn.pack(side=tk.LEFT, padx=5)

        # Área de texto con marco bootstrap
        text_frame = ttk.Labelframe(main_frame, 
                                  text="Texto a convertir", 
                                  padding=15,
                                  bootstyle="primary")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        #area de texto
        self.text_area = tk.Text(text_frame, 
                                height=15,
                                width=60,
                                font=self.custom_text,
                                wrap=tk.WORD,
                                undo=True,
                                bg=self.text_bg_color,
                                relief='solid',
                                padx=10,
                                pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        #panel de controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        #panel de controles izquierdos
        left_controls = ttk.Frame(controls_frame)
        left_controls.pack(side=tk.LEFT)
        
        #selector de voces  
        voice_frame = ttk.Labelframe(left_controls, 
                                   text="Idioma y voz",
                                   bootstyle="info")
        voice_frame.pack(side=tk.LEFT, padx=5)
        
        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(voice_frame, 
                                      textvariable=self.voice_var,
                                      width=20,
                                      state='readonly',
                                      font=('Helvetica', 10))
        self.voice_combo['values'] = list(self.available_voices.keys())
        self.voice_combo.set(list(self.available_voices.keys())[0])
        self.voice_combo.pack(padx=10, pady=5)

        # Botón de reproducción con estilo bootstrap
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(side=tk.RIGHT, padx=10)
        #boton de reproducir
        self.play_button = ttk.Button(buttons_frame, 
                                    text=" Reproducir", 
                                    command=self.speak_text,
                                    image=self.icons['play'],
                                    compound='left',
                                    bootstyle="success")
        self.play_button.pack(side=tk.LEFT, padx=2)
        #boton de detener
        self.stop_button = ttk.Button(buttons_frame,
                                    text=" Detener",
                                    command=self.stop_audio,
                                    image=self.icons['stop'],
                                    compound='left',
                                    bootstyle="danger",
                                    state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=2)

        #contador de caracteres y estado
        self.char_count_label = ttk.Label(main_frame, 
                                        text="Caracteres: 0",
                                        font=self.custom_small,
                                        bootstyle="secondary")
        self.char_count_label.pack(pady=5)
        #estado
        self.status_label = ttk.Label(main_frame,
                                    text="Listo",
                                    font=self.custom_small,
                                    bootstyle="secondary")
        self.status_label.pack(pady=5)
        
        # Vincular eventos
        self.text_area.bind('<KeyRelease>', self.update_char_count)
        self.text_area.bind('<Control-z>', self.undo_text)
        self.text_area.bind('<Control-y>', self.redo_text)

    #contador de caracteres
    def update_char_count(self, event=None):
        count = len(self.text_area.get("1.0", tk.END).strip())
        self.char_count_label.config(text=f"Caracteres: {count}")
        
    #cargar texto
    def load_text(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", file.read())
                self.update_char_count()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    #guardar audio
    def save_audio(self):
        texto = self.text_area.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "No hay texto para convertir")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("Archivos MP3", "*.mp3")])
        
        if file_path:
            try:
                self.play_button.configure(state='disabled')
                self.play_button['text'] = "Guardando..."
                self.root.update()
                
                # Obtener el código de idioma completo
                lang_code = self.available_voices[self.voice_var.get()]
                tts = gTTS(text=texto, lang=lang_code)
                tts.save(file_path)
                #mensaje de exito
                messagebox.showinfo("Éxito", "Audio guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el audio: {str(e)}")
            finally:
                self.play_button.configure(state='normal')
                self.play_button['text'] = "Reproducir"

    #limpiar texto
    def clear_text(self):
        if messagebox.askyesno("Confirmar", "¿Deseas borrar todo el texto?"):
            self.text_area.delete("1.0", tk.END)
            self.update_char_count()
    #deshacer texto
    def undo_text(self, event=None):
        try:
            self.text_area.edit_undo()
            self.update_char_count()
        except tk.TclError:
            pass
        return "break"
    #rehacer texto
    def redo_text(self, event=None):
        try:
            self.text_area.edit_redo()
            self.update_char_count()
        except tk.TclError:
            pass
        return "break"

    def translate_text(self, text, target_lang):
        try:
            #traducir texto
            translator = GoogleTranslator(source='auto', target=target_lang)
            translated_text = translator.translate(text)
            #mensaje de exito
            if translated_text:
                print(f"Texto traducido: {translated_text}")  # Mensaje de depuración
                return translated_text
            else:
                raise ValueError("No se pudo traducir el texto")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al traducir el texto: {str(e)}")
            return text
    #reproducir texto
    def speak_text(self):
        texto = self.text_area.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor, introduce algún texto")
            return

        try:
            self.is_playing = True
            self.play_button.configure(state='disabled')
            self.stop_button.configure(state='normal')
            self.status_label.configure(text="Procesando audio...")
            self.root.update()
            #obtener idioma
            lang_code = self.available_voices[self.voice_var.get()]
            #ruta de salida
            output_path = "output.mp3"
            #convertir texto a audio
            tts = gTTS(text=texto, lang=lang_code)
            tts.save(output_path)
            #mensaje de exito
            self.status_label.configure(text="Reproduciendo audio...")
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()
            
            # Configurar un evento para cuando termine la reproducción
            self.root.after(100, self.check_audio_finished)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el texto: {str(e)}")
            self.cleanup()
    #verificar si el audio ha terminado de reproducirse
    def check_audio_finished(self):
        """Verifica si el audio ha terminado de reproducirse"""
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.cleanup()
        elif self.is_playing:
            self.root.after(100, self.check_audio_finished)

    def stop_audio(self):
        """Detiene la reproducción del audio"""
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.cleanup()
    #limpiar recursos
    def cleanup(self):
        """Limpia los recursos y actualiza la interfaz"""
        self.is_playing = False
        self.play_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.status_label.configure(text="Listo")
        
        # Eliminar el archivo temporal
        if os.path.exists("output.mp3"):
            try:
                os.remove("output.mp3")
            except:
                pass
    #traducir texto
    def translate_current_text(self):
        texto = self.text_area.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "No hay texto para traducir")
            return
        
        #deshabilitar controles durante la traduccion
        self.play_button.configure(state='disabled')
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.configure(state='disabled')
        
        try:
            self.status_label.configure(text="Traduciendo...")
            self.root.update()
            
            # Determinar el idioma de destino
            lang_code = self.available_voices[self.voice_var.get()]
            target_lang = 'en' if lang_code == 'es' else 'es'
            print(f"Traduciendo de {lang_code} a {target_lang}") 
            
            translated_text = self.translate_text(texto, target_lang)   
            
            if translated_text and translated_text != texto:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", translated_text)
                self.update_char_count()
                self.status_label.configure(text="Traducción completada")
            else:
                self.status_label.configure(text="No se pudo traducir el texto")
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la traducción: {str(e)}")
            self.status_label.configure(text="Error en la traducción")
        finally:
            # Rehabilitar controles
            self.play_button.configure(state='normal')
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Button):
                    widget.configure(state='normal')
            self.root.update()

if __name__ == "__main__":
    root = ttk.Window(themename="solar")  # tema solar
    app = TextoAVozApp(root)
    root.mainloop()


