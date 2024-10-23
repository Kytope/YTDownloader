import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
from threading import Thread
import os

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de Videos y Audio")
        self.root.geometry("700x500")
        
        # Variables
        self.url_var = tk.StringVar()
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.video_info = None
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL entrada
        ttk.Label(main_frame, text="URL del Video:").grid(row=0, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Botón de información
        ttk.Button(main_frame, text="Obtener Info", command=self.get_video_info).grid(
            row=1, column=0, columnspan=3, pady=10)
        
        # Frame de información
        self.info_frame = ttk.LabelFrame(main_frame, text="Información del Video", padding="5")
        self.info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Labels para información
        self.title_label = ttk.Label(self.info_frame, text="Título: ", wraplength=600)
        self.title_label.grid(row=0, column=0, sticky=tk.W)
        
        self.duration_label = ttk.Label(self.info_frame, text="Duración: ")
        self.duration_label.grid(row=1, column=0, sticky=tk.W)
        
        # Selector de formato
        ttk.Label(main_frame, text="Seleccionar Formato:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.format_combo = ttk.Combobox(main_frame, state="readonly", width=57)
        self.format_combo.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Selector de directorio
        ttk.Button(main_frame, text="Directorio de descarga", command=self.select_directory).grid(
            row=4, column=0, sticky=tk.W, pady=5)
        self.dir_label = ttk.Label(main_frame, text=self.download_path, wraplength=400)
        self.dir_label.grid(row=4, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, length=500, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=6, column=0, columnspan=3, sticky=tk.W)
        
        # Botones de descarga
        ttk.Button(main_frame, text="Descargar Video", command=lambda: self.start_download('video')).grid(
            row=7, column=0, pady=5)
        ttk.Button(main_frame, text="Descargar Audio", command=lambda: self.start_download('audio')).grid(
            row=7, column=1, pady=5)
            
    def select_directory(self):
        dir_path = filedialog.askdirectory(initialdir=self.download_path)
        if dir_path:
            self.download_path = dir_path
            self.dir_label.config(text=self.download_path)
    
    def format_duration(self, duration):
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def get_video_info(self):
        try:
            url = self.url_var.get()
            if not url:
                messagebox.showerror("Error", "Por favor ingrese una URL")
                return
            
            self.status_label.config(text="Obteniendo información del video...")
            self.root.update()
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.video_info = ydl.extract_info(url, download=False)
                
                # Actualizar información
                self.title_label.config(text=f"Título: {self.video_info['title']}")
                duration = self.format_duration(self.video_info['duration'])
                self.duration_label.config(text=f"Duración: {duration}")
                
                # Preparar formatos disponibles
                formats = []
                for f in self.video_info['formats']:
                    if f.get('height'):  # Video formats
                        formats.append(f"{f['height']}p - {f['ext']} ({f.get('format_note', 'N/A')})")
                
                self.format_combo['values'] = formats
                if formats:
                    self.format_combo.set(formats[0])
                
                self.status_label.config(text="Información obtenida correctamente")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener información: {str(e)}")
            self.status_label.config(text="Error al obtener información")
            
    def download_progress_hook(self, d):
        if d['status'] == 'downloading':
            # Actualizar progreso
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total_bytes:
                downloaded = d.get('downloaded_bytes', 0)
                progress = (downloaded / total_bytes) * 100
                self.progress['value'] = progress
                
                # Actualizar status
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / 1024 / 1024
                    self.status_label.config(text=f"Descargando: {progress:.1f}% ({speed_mb:.1f} MB/s)")
                else:
                    self.status_label.config(text=f"Descargando: {progress:.1f}%")
                
                self.root.update()
        
        elif d['status'] == 'finished':
            self.status_label.config(text="Descarga completada. Procesando...")
            self.root.update()
            
    def download_video(self, type='video'):
        try:
            if not self.video_info:
                messagebox.showerror("Error", "Primero obtenga la información del video")
                return
                
            url = self.url_var.get()
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.download_progress_hook],
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            }
            
            if type == 'audio':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                # Obtener formato seleccionado
                selected = self.format_combo.get()
                height = selected.split('p')[0]
                ydl_opts.update({
                    'format': f'bestvideo[height={height}]+bestaudio/best[height<={height}]',
                })
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.progress['value'] = 100
            self.status_label.config(text="Descarga completada exitosamente!")
            messagebox.showinfo("Éxito", "Descarga completada!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la descarga: {str(e)}")
            self.status_label.config(text="Error en la descarga")
        finally:
            self.progress['value'] = 0
            
    def start_download(self, type):
        Thread(target=lambda: self.download_video(type)).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloader(root)
    root.mainloop()