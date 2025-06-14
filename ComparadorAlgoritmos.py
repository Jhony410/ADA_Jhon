import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import time
import random
import re
import string

class ComparadorAlgoritmos:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Algoritmos - UNA Puno")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="COMPARADOR DE ALGORITMOS", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame, text="Universidad Nacional del Altiplano - Análisis y Diseño de Algoritmos", 
                                 font=('Arial', 10), fg='#ecf0f1', bg='#2c3e50')
        subtitle_label.pack()
        
        # Frame principal con pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Pestaña de búsqueda
        search_frame = ttk.Frame(notebook)
        notebook.add(search_frame, text="Algoritmos de Búsqueda")
        self.setup_search_tab(search_frame)
        
        # Pestaña de ordenamiento
        sort_frame = ttk.Frame(notebook)
        notebook.add(sort_frame, text="Algoritmos de Ordenamiento")
        self.setup_sort_tab(sort_frame)
        
        # Pestaña de búsqueda textual
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text="Búsqueda Textual")
        self.setup_text_tab(text_frame)
    
    def setup_search_tab(self, parent):
        # Frame de configuración para búsqueda
        config_frame = tk.LabelFrame(parent, text="Configuración de Pruebas - Búsqueda", padx=15, pady=15)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Entrada para datos de búsqueda
        tk.Label(config_frame, text="Datos para búsqueda (separados por comas):", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.search_data_entry = tk.Entry(config_frame, font=('Arial', 9), width=80)
        # Datos del informe
        search_data = "87,14,52,91,33,28,64,19,75,41,5,96,23,60,37,82,11,49,68,3,99,45,72,7,55,84,26,63,12,78,31,58,94,21,70,9,43,80,16,66"
        self.search_data_entry.insert(0, search_data)
        self.search_data_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Elemento a buscar
        search_frame = tk.Frame(config_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Elemento a buscar:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.search_target_entry = tk.Entry(search_frame, font=('Arial', 10), width=10)
        self.search_target_entry.insert(0, "45")
        self.search_target_entry.pack(side=tk.LEFT, padx=(10, 20))
        
        tk.Button(search_frame, text="Ejecutar Pruebas de Búsqueda", 
                 command=self.probar_busqueda, bg='#27ae60', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        # Frame para gráfico
        self.search_plot_frame = tk.Frame(parent)
        self.search_plot_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def setup_sort_tab(self, parent):
        # Frame de configuración para ordenamiento
        config_frame = tk.LabelFrame(parent, text="Configuración de Pruebas - Ordenamiento", padx=15, pady=15)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Entrada para datos de ordenamiento
        tk.Label(config_frame, text="Datos para ordenamiento (separados por comas):", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.sort_data_entry = tk.Entry(config_frame, font=('Arial', 9), width=80)
        # Datos del informe
        sort_data = "87,14,52,91,33,28,64,19,75,41,5,96,23,60,37,82,11,49,68,3,99,45,72,7,55,84,26,63,12,78,31,58,94,21,70,9,43,80,16,66"
        self.sort_data_entry.insert(0, sort_data)
        self.sort_data_entry.pack(fill=tk.X, pady=(5, 10))
        
        tk.Button(config_frame, text="Ejecutar Pruebas de Ordenamiento", 
                 command=self.probar_ordenamiento, bg='#f39c12', fg='white',
                 font=('Arial', 10, 'bold')).pack()
        
        # Frame para gráfico
        self.sort_plot_frame = tk.Frame(parent)
        self.sort_plot_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def setup_text_tab(self, parent):
        # Frame de configuración para búsqueda textual
        config_frame = tk.LabelFrame(parent, text="Configuración de Pruebas - Búsqueda Textual", padx=15, pady=15)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Entrada para datos textuales
        tk.Label(config_frame, text="Datos textuales (texto base que se repetirá):", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.text_data_entry = tk.Entry(config_frame, font=('Arial', 9), width=80)
        # MODIFICACIÓN: Texto base más largo y realista
        text_data = "El rápido zorro marrón salta sobre el perro perezoso. Esta es una frase de prueba, repetitiva para hacer un texto más largo y poder observar el rendimiento. La eficiencia es clave. Este texto se va a concatenar para generar mayores tamaños de dataset. Consideramos la importancia de los algoritmos y su impacto. Un buen algoritmo ahorra tiempo y recursos. El análisis de rendimiento es vital. "
        self.text_data_entry.insert(0, text_data)
        self.text_data_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Configuración de búsqueda
        search_frame = tk.Frame(config_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Texto/carácter a buscar:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.text_target_entry = tk.Entry(search_frame, font=('Arial', 10), width=15)
        # MODIFICACIÓN: Palabra más larga para buscar
        self.text_target_entry.insert(0, "rendimiento")
        self.text_target_entry.pack(side=tk.LEFT, padx=(10, 20))
        
        tk.Button(search_frame, text="Ejecutar Búsqueda Textual", 
                 command=self.probar_busqueda_textual, bg='#9b59b6', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        # Frame para gráfico
        self.text_plot_frame = tk.Frame(parent)
        self.text_plot_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def medir_tiempo(self, funcion, *args):
        """Medir tiempo de ejecución de una función"""
        # Calentamiento
        for _ in range(2):
            try:
                funcion(*args)
            except:
                pass
        
        # Medición real (promedio de 5 ejecuciones para mayor precisión)
        tiempos = []
        for _ in range(5):
            inicio = time.time()
            try:
                resultado = funcion(*args)
            except:
                resultado = None
            fin = time.time()
            tiempos.append(fin - inicio)
        
        return sum(tiempos) / len(tiempos)
    
    # Algoritmos de búsqueda
    def busqueda_lineal(self, lista, objetivo):
        for i, valor in enumerate(lista):
            if valor == objetivo:
                return i
        return -1
    
    def busqueda_binaria(self, lista, objetivo):
        lista_ordenada = sorted(lista)
        izquierda, derecha = 0, len(lista_ordenada) - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if lista_ordenada[medio] == objetivo:
                return medio
            elif lista_ordenada[medio] < objetivo:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return -1
    
    # Algoritmos de ordenamiento
    def ordenamiento_burbuja(self, lista):
        n = len(lista)
        lista_copia = lista.copy()
        for i in range(n):
            for j in range(0, n-i-1):
                if lista_copia[j] > lista_copia[j+1]:
                    lista_copia[j], lista_copia[j+1] = lista_copia[j+1], lista_copia[j]
        return lista_copia
    
    def quicksort(self, lista):
        if len(lista) <= 1:
            return lista
        else:
            pivote = lista[0]
            menores = [x for x in lista[1:] if x <= pivote]
            mayores = [x for x in lista[1:] if x > pivote]
            return self.quicksort(menores) + [pivote] + self.quicksort(mayores)
    
    def ordenamiento_seleccion(self, lista):
        lista_copia = lista.copy()
        n = len(lista_copia)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if lista_copia[j] < lista_copia[min_idx]:
                    min_idx = j
            lista_copia[i], lista_copia[min_idx] = lista_copia[min_idx], lista_copia[i]
        return lista_copia
    
    def ordenamiento_insercion(self, lista):
        lista_copia = lista.copy()
        for i in range(1, len(lista_copia)):
            key = lista_copia[i]
            j = i - 1
            while j >= 0 and key < lista_copia[j]:
                lista_copia[j + 1] = lista_copia[j]
                j -= 1
            lista_copia[j + 1] = key
        return lista_copia
    
    # Algoritmos de búsqueda textual
    def busqueda_in(self, texto, palabra):
        return palabra in texto
    
    def busqueda_regex(self, texto, palabra):
        return re.search(palabra, texto) is not None
    
    def busqueda_fuerza_bruta(self, texto, palabra):
        for i in range(len(texto) - len(palabra) + 1):
            if texto[i:i + len(palabra)] == palabra:
                return True
        return False
    
    def generar_tamaños_crecientes(self, datos_base, max_multiplier=50):
        """Generar diferentes tamaños de datasets basados en los datos originales"""
        tamaños = []
        datasets = []
        
        # Tamaños: 1x, 2x, 5x, 10x, 20x, 50x del tamaño original
        multipliers = [1, 2, 5, 10, 20, max_multiplier]
        
        for mult in multipliers:
            nuevo_tamaño = len(datos_base) * mult
            tamaños.append(nuevo_tamaño)
            
            # Crear dataset más grande repitiendo y mezclando los datos base
            nuevo_dataset = []
            for _ in range(mult):
                datos_mezclados = datos_base.copy()
                random.shuffle(datos_mezclados)
                nuevo_dataset.extend(datos_mezclados)
            
            datasets.append(nuevo_dataset)
        
        return tamaños, datasets
    
    def probar_busqueda(self):
        """Probar algoritmos de búsqueda"""
        try:
            # Obtener datos de entrada
            datos_texto = self.search_data_entry.get().strip()
            objetivo_texto = self.search_target_entry.get().strip()
            
            if not datos_texto or not objetivo_texto:
                messagebox.showwarning("Advertencia", "Ingrese datos y elemento a buscar.")
                return
            
            datos_base = [int(x.strip()) for x in datos_texto.split(',')]
            objetivo = int(objetivo_texto)
            
            # Generar diferentes tamaños
            tamaños, datasets = self.generar_tamaños_crecientes(datos_base)
            
            tiempos_busqueda = {
                'Búsqueda Lineal': [],
                'Búsqueda Binaria': []
            }
            
            for i, datos in enumerate(datasets):
                tamaño = tamaños[i]
                
                # Asegurar que el objetivo esté en los datos
                if objetivo not in datos:
                    datos.append(objetivo)
                
                # Búsqueda lineal
                tiempo_lineal = self.medir_tiempo(self.busqueda_lineal, datos, objetivo)
                tiempos_busqueda['Búsqueda Lineal'].append(tiempo_lineal)
                
                # Búsqueda binaria
                tiempo_binaria = self.medir_tiempo(self.busqueda_binaria, datos, objetivo)
                tiempos_busqueda['Búsqueda Binaria'].append(tiempo_binaria)
                
                print(f"Tamaño {tamaño}: Lineal={tiempo_lineal:.6f}s, Binaria={tiempo_binaria:.6f}s")
            
            self.graficar_resultados(tamaños, tiempos_busqueda, 
                                   f"Comparación de Algoritmos de Búsqueda (Objetivo: {objetivo})", 
                                   self.search_plot_frame)
            
        except ValueError:
            messagebox.showerror("Error", "Verifique que los datos sean números válidos.")
    
    def probar_ordenamiento(self):
        """Probar algoritmos de ordenamiento"""
        try:
            # Obtener datos de entrada
            datos_texto = self.sort_data_entry.get().strip()
            
            if not datos_texto:
                messagebox.showwarning("Advertencia", "Ingrese datos para ordenar.")
                return
            
            datos_base = [int(x.strip()) for x in datos_texto.split(',')]
            
            # Generar diferentes tamaños
            tamaños, datasets = self.generar_tamaños_crecientes(datos_base, 30)  # Menor para ordenamiento
            
            tiempos_ordenamiento = {
                'Burbuja': [],
                'Quicksort': [],
                'Selección': [],
                'Inserción': []
            }
            
            for i, datos in enumerate(datasets):
                tamaño = tamaños[i]
                
                # Burbuja
                tiempo_burbuja = self.medir_tiempo(self.ordenamiento_burbuja, datos)
                tiempos_ordenamiento['Burbuja'].append(tiempo_burbuja)
                
                # Quicksort
                tiempo_quicksort = self.medir_tiempo(self.quicksort, datos)
                tiempos_ordenamiento['Quicksort'].append(tiempo_quicksort)
                
                # Selección
                tiempo_seleccion = self.medir_tiempo(self.ordenamiento_seleccion, datos)
                tiempos_ordenamiento['Selección'].append(tiempo_seleccion)
                
                # Inserción
                tiempo_insercion = self.medir_tiempo(self.ordenamiento_insercion, datos)
                tiempos_ordenamiento['Inserción'].append(tiempo_insercion)
                
                print(f"Tamaño {tamaño}: Burbuja={tiempo_burbuja:.6f}s, Quick={tiempo_quicksort:.6f}s, Selec={tiempo_seleccion:.6f}s, Inser={tiempo_insercion:.6f}s")
            
            self.graficar_resultados(tamaños, tiempos_ordenamiento, 
                                   "Comparación de Algoritmos de Ordenamiento", 
                                   self.sort_plot_frame)
            
        except ValueError:
            messagebox.showerror("Error", "Verifique que los datos sean números válidos.")
    
    def probar_busqueda_textual(self):
        """Probar algoritmos de búsqueda textual"""
        try:
            # Obtener datos de entrada
            datos_base_str = self.text_data_entry.get().strip() # Ahora es una cadena completa
            objetivo_texto = self.text_target_entry.get().strip()
            
            if not datos_base_str or not objetivo_texto:
                messagebox.showwarning("Advertencia", "Ingrese datos y texto a buscar.")
                return
            
            # MODIFICACIÓN: Multiplicadores para generar textos MUCHO más grandes
            multipliers = [1, 10, 100, 1000, 5000, 10000] # Para ver diferencias claras
            
            tamaños = []
            textos = []
            
            for mult in multipliers:
                # Crear texto más largo concatenando la cadena base
                texto_completo = datos_base_str * mult
                
                # Asegurar que el objetivo esté en el texto
                if objetivo_texto not in texto_completo:
                    texto_completo += objetivo_texto 

                tamaños.append(len(texto_completo)) # El tamaño es la longitud del texto
                textos.append(texto_completo)
            
            tiempos_textual = {
                'Operador in': [],
                'Expresiones Regulares': [],
                'Fuerza Bruta': []
            }
            
            for i, texto in enumerate(textos):
                tamaño = tamaños[i]
                
                # Operador in
                tiempo_in = self.medir_tiempo(self.busqueda_in, texto, objetivo_texto)
                tiempos_textual['Operador in'].append(tiempo_in)
                
                # Expresiones regulares
                tiempo_regex = self.medir_tiempo(self.busqueda_regex, texto, objetivo_texto)
                tiempos_textual['Expresiones Regulares'].append(tiempo_regex)
                
                # Fuerza bruta
                tiempo_bruta = self.medir_tiempo(self.busqueda_fuerza_bruta, texto, objetivo_texto)
                tiempos_textual['Fuerza Bruta'].append(tiempo_bruta)
                
                print(f"Tamaño {tamaño}: in={tiempo_in:.6f}s, regex={tiempo_regex:.6f}s, bruta={tiempo_bruta:.6f}s")
            
            self.graficar_resultados(tamaños, tiempos_textual, 
                                   f"Comparación de Búsqueda Textual: '{objetivo_texto}'", 
                                   self.text_plot_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda textual: {str(e)}")
    
    def graficar_resultados(self, x, y_dict, titulo, contenedor):
        """Crear gráfico interactivo con matplotlib mejorado"""
        # Limpiar contenedor
        for widget in contenedor.winfo_children():
            widget.destroy()
        
        # Crear figura con mejor configuración
        fig, ax = plt.subplots(figsize=(12, 7))
        fig.patch.set_facecolor('white')
        
        # Plotear líneas con estilos mejorados
        colores = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        marcadores = ['o', 's', '^', 'D', 'v', '<']
        
        for i, (etiqueta, y) in enumerate(y_dict.items()):
            color = colores[i % len(colores)]
            marcador = marcadores[i % len(marcadores)]
            ax.plot(x, y, label=etiqueta, marker=marcador, linewidth=2.5, 
                   markersize=7, color=color, markerfacecolor='white', 
                   markeredgewidth=2, markeredgecolor=color)
        
        # Configurar gráfico con mejor apariencia
        ax.set_title(titulo, fontsize=15, fontweight='bold', pad=25)
        ax.set_xlabel("Tamaño del dataset", fontsize=13, fontweight='bold')
        ax.set_ylabel("Tiempo (segundos)", fontsize=13, fontweight='bold')
        
        # Grid mejorado
        ax.grid(True, linestyle='--', alpha=0.6, color='gray')
        ax.set_axisbelow(True)
        
        # Leyenda mejorada
        legend = ax.legend(loc='upper left', frameon=True, fancybox=True, 
                          shadow=True, fontsize=11, framealpha=0.9)
        legend.get_frame().set_facecolor('white')
        
        # Mejorar apariencia de ejes
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#666666')
        ax.spines['bottom'].set_color('#666666')
        
        # Mejorar ticks
        ax.tick_params(axis='both', which='major', labelsize=10, colors='#333333')
        
        # Crear canvas con navegación mejorada
        canvas = FigureCanvasTkAgg(fig, master=contenedor)
        canvas.draw()
        
        # Barra de herramientas personalizada
        toolbar_frame = tk.Frame(contenedor)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
        # Empaquetar canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar zoom con rueda del mouse
        def zoom_function(event):
            if event.inaxes != ax:
                return
            
            # Factor de zoom
            zoom_factor = 1.2
            if event.button == 'up':
                # Zoom in
                scale_factor = 1 / zoom_factor
            elif event.button == 'down':
                # Zoom out
                scale_factor = zoom_factor
            else:
                return
            
            # Obtener límites actuales
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            
            # Calcular nuevo centro basado en la posición del mouse
            xdata, ydata = event.xdata, event.ydata
            
            # Calcular nuevos límites
            new_width = (xlim[1] - xlim[0]) * scale_factor
            new_height = (ylim[1] - ylim[0]) * scale_factor
            
            relx = (xlim[1] - xdata) / (xlim[1] - xlim[0])
            rely = (ylim[1] - ydata) / (ylim[1] - ylim[0])
            
            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
            
            canvas.draw()
        
        # Conectar evento de scroll
        canvas.mpl_connect('scroll_event', zoom_function)

def main():
    root = tk.Tk()
    app = ComparadorAlgoritmos(root)
    root.mainloop()

if __name__ == "__main__":
    main()
