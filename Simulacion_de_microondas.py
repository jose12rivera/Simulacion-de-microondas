import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime

class MicroondasMultifuncional:
    def __init__(self, root):
        self.root = root
        self.root.title("Microondas Multifuncional 3000")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Variables del sistema
        self.combustible_actual = tk.StringVar(value="Energía Eléctrica")
        self.alimento_actual = tk.StringVar(value="Pollo")
        self.potencia = tk.IntVar(value=50)
        self.tiempo_coccion = 0
        self.kcal_consumidas = 0
        self.estado = "Apagado"
        self.cocinando = False
        
        # Historial
        self.historial_tiempo = []
        self.historial_kcal = []
        self.historial_combustibles = {
            "Energía Eléctrica": 0, 
            "Madera": 0, 
            "Hojas Secas": 0, 
            "Combustible (Gasolina)": 0
        }
        
        # Consumo de kcal por minuto según combustible
        self.consumo_combustible = {
            "Energía Eléctrica": 2.5,
            "Madera": 4.0,
            "Hojas Secas": 3.0,
            "Combustible (Gasolina)": 5.5
        }
        
        # Tiempo de cocción base por alimento (minutos) a potencia 100%
        self.tiempo_base_alimento = {
            "Pollo": 25,
            "Pavo": 45,
            "Res": 35
        }
        
        # Emojis de combustible
        self.emojis_combustible = {
            "Energía Eléctrica": "⚡",
            "Madera": "🪵",
            "Hojas Secas": "🍂",
            "Combustible (Gasolina)": "⛽"
        }
        
        self.crear_interfaz()
        self.actualizar_tiempo_estimado()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === TÍTULO PRINCIPAL ===
        titulo_frame = tk.Frame(main_frame, bg='#ff6b35', height=80)
        titulo_frame.pack(fill=tk.X, padx=20, pady=(20,10))
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="🔥 MICROONDAS MULTIFUNCIONAL 3000 🔥", 
                font=('Arial', 28, 'bold'), bg='#ff6b35', fg='white').pack(expand=True)
        
        # Container para panel central y lateral
        content_frame = tk.Frame(main_frame, bg='#1a1a1a')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # === PANEL IZQUIERDO - DISEÑO DEL MICROONDAS ===
        left_panel = tk.Frame(content_frame, bg='#2d2d2d', relief=tk.RAISED, bd=5)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
        
        self.crear_microondas(left_panel)
        
        # === PANEL DERECHO - CONTROLES Y GRÁFICOS ===
        right_panel = tk.Frame(content_frame, bg='#2d2d2d', relief=tk.RAISED, bd=5)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.crear_controles(right_panel)
        
    def crear_microondas(self, parent):
        # Frame del microondas
        microondas_frame = tk.Frame(parent, bg='#2d2d2d')
        microondas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # === CUERPO DEL MICROONDAS ===
        cuerpo_frame = tk.Frame(microondas_frame, bg='#4a4a4a', relief=tk.RIDGE, bd=8)
        cuerpo_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ventana/Display
        ventana_frame = tk.Frame(cuerpo_frame, bg='#1a1a1a', relief=tk.SUNKEN, bd=5)
        ventana_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas para la ventana del microondas
        self.canvas = tk.Canvas(ventana_frame, bg='#000000', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display de estado dentro de la ventana
        self.display_estado = tk.Label(self.canvas, text="APAGADO", 
                                       font=('Arial', 24, 'bold'), 
                                       bg='#000000', fg='#ff0000')
        self.canvas.create_window(350, 50, window=self.display_estado)
        
        # Plato giratorio
        self.plato_angulo = 0
        self.plato_id = self.canvas.create_oval(200, 150, 500, 450, 
                                                fill='#666666', outline='#999999', width=3)
        
        # Alimento en el plato
        self.alimento_id = self.canvas.create_text(350, 300, text="🍗", 
                                                   font=('Arial', 80), fill='white')
        
        # Panel de control inferior
        panel_control = tk.Frame(cuerpo_frame, bg='#3d3d3d', height=150)
        panel_control.pack(fill=tk.X, padx=20, pady=(0,20))
        panel_control.pack_propagate(False)
        
        # Display LCD
        lcd_frame = tk.Frame(panel_control, bg='#00ff00', relief=tk.SUNKEN, bd=3)
        lcd_frame.pack(pady=10, padx=20)
        
        display_container = tk.Frame(lcd_frame, bg='#003300')
        display_container.pack(padx=5, pady=5)
        
        self.lcd_tiempo = tk.Label(display_container, text="00:00", 
                                   font=('Digital-7', 36, 'bold'), 
                                   bg='#003300', fg='#00ff00', width=10)
        self.lcd_tiempo.pack(side=tk.LEFT, padx=5)
        
        self.lcd_kcal = tk.Label(display_container, text="0 kcal/h", 
                                font=('Arial', 14, 'bold'), 
                                bg='#003300', fg='#ffff00')
        self.lcd_kcal.pack(side=tk.LEFT, padx=10)
        
        # Indicador de combustible
        self.combustible_indicator = tk.Label(panel_control, text="⚡ Energía Eléctrica", 
                                             font=('Arial', 12, 'bold'), 
                                             bg='#3d3d3d', fg='#00ffff')
        self.combustible_indicator.pack()
        
    def crear_controles(self, parent):
        # Notebook para organizar controles
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Estilo para el notebook
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))
        
        # === TAB 1: CONFIGURACIÓN ===
        config_tab = tk.Frame(notebook, bg='#2d2d2d')
        notebook.add(config_tab, text='⚙️ Configuración')
        
        # Scrollbar para config_tab
        canvas_config = tk.Canvas(config_tab, bg='#2d2d2d', highlightthickness=0)
        scrollbar = tk.Scrollbar(config_tab, orient="vertical", command=canvas_config.yview)
        scrollable_config = tk.Frame(canvas_config, bg='#2d2d2d')
        
        scrollable_config.bind(
            "<Configure>",
            lambda e: canvas_config.configure(scrollregion=canvas_config.bbox("all"))
        )
        
        canvas_config.create_window((0, 0), window=scrollable_config, anchor="nw")
        canvas_config.configure(yscrollcommand=scrollbar.set)
        
        canvas_config.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Combustible
        combustible_frame = tk.LabelFrame(scrollable_config, text="🔥 Tipo de Combustible", 
                                         font=('Arial', 13, 'bold'), bg='#3d3d3d', 
                                         fg='#ffffff', padx=15, pady=15)
        combustible_frame.pack(fill=tk.X, padx=15, pady=10)
        
        combustibles = [
            ("⚡ Energía Eléctrica", "Energía Eléctrica", "#ffeb3b"),
            ("🪵 Madera", "Madera", "#ff9800"),
            ("🍂 Hojas Secas", "Hojas Secas", "#8bc34a"),
            ("⛽ Combustible (Gasolina)", "Combustible (Gasolina)", "#f44336")
        ]
        
        for texto, valor, color in combustibles:
            rb = tk.Radiobutton(combustible_frame, text=texto, 
                              variable=self.combustible_actual, value=valor,
                              bg='#3d3d3d', fg=color, selectcolor='#1a1a1a',
                              font=('Arial', 11, 'bold'), 
                              activebackground='#3d3d3d', activeforeground='white',
                              command=self.actualizar_combustible)
            rb.pack(anchor=tk.W, pady=5, padx=10)
        
        # Alimento
        alimento_frame = tk.LabelFrame(scrollable_config, text="🍖 Tipo de Alimento", 
                                      font=('Arial', 13, 'bold'), bg='#3d3d3d', 
                                      fg='#ffffff', padx=15, pady=15)
        alimento_frame.pack(fill=tk.X, padx=15, pady=10)
        
        alimentos = [
            ("🍗 Pollo", "Pollo"),
            ("🦃 Pavo", "Pavo"),
            ("🥩 Res", "Res")
        ]
        
        for texto, valor in alimentos:
            rb = tk.Radiobutton(alimento_frame, text=texto, 
                              variable=self.alimento_actual, value=valor,
                              bg='#3d3d3d', fg='#ffffff', selectcolor='#1a1a1a',
                              font=('Arial', 11), 
                              activebackground='#3d3d3d', activeforeground='white',
                              command=self.actualizar_alimento)
            rb.pack(anchor=tk.W, pady=5, padx=10)
        
        # Tiempo estimado de cocción
        tiempo_frame = tk.LabelFrame(scrollable_config, text="⏱️ Tiempo Estimado", 
                                    font=('Arial', 13, 'bold'), bg='#3d3d3d', 
                                    fg='#ffffff', padx=15, pady=15)
        tiempo_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.tiempo_estimado_label = tk.Label(tiempo_frame, 
                                             text="Tiempo estimado: 25 minutos",
                                             font=('Arial', 12, 'bold'),
                                             bg='#3d3d3d', fg='#00ff00')
        self.tiempo_estimado_label.pack(pady=5)
        
        self.consumo_estimado_label = tk.Label(tiempo_frame,
                                              text="Consumo estimado: 0 kcal",
                                              font=('Arial', 11),
                                              bg='#3d3d3d', fg='#ffff00')
        self.consumo_estimado_label.pack(pady=2)
        
        # Potencia con dial circular
        potencia_frame = tk.LabelFrame(scrollable_config, text="🎚️ Control de Potencia", 
                                      font=('Arial', 13, 'bold'), bg='#3d3d3d', 
                                      fg='#ffffff', padx=15, pady=15)
        potencia_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Canvas para el dial
        dial_canvas = tk.Canvas(potencia_frame, width=200, height=200, 
                               bg='#2d2d2d', highlightthickness=0)
        dial_canvas.pack(pady=10)
        
        # Dibujar círculo del dial
        dial_canvas.create_oval(20, 20, 180, 180, outline='#666666', width=3)
        
        # Marcas del dial
        for i in range(0, 101, 10):
            angle = math.radians(225 - (i * 2.7))
            x1 = 100 + 70 * math.cos(angle)
            y1 = 100 - 70 * math.sin(angle)
            x2 = 100 + 60 * math.cos(angle)
            y2 = 100 - 60 * math.sin(angle)
            dial_canvas.create_line(x1, y1, x2, y2, fill='#999999', width=2)
            
            # Números
            x3 = 100 + 50 * math.cos(angle)
            y3 = 100 - 50 * math.sin(angle)
            dial_canvas.create_text(x3, y3, text=str(i), fill='white', font=('Arial', 8))
        
        # Indicador del dial
        self.dial_line = dial_canvas.create_line(100, 100, 100, 40, 
                                                 fill='#ff6b35', width=4)
        self.dial_center = dial_canvas.create_oval(90, 90, 110, 110, 
                                                   fill='#ff6b35', outline='white')
        
        self.potencia_label = tk.Label(potencia_frame, text="50%", 
                                      font=('Arial', 24, 'bold'),
                                      bg='#3d3d3d', fg='#ff6b35')
        self.potencia_label.pack(pady=5)
        
        self.potencia_scale = tk.Scale(potencia_frame, from_=10, to=100, 
                                      orient=tk.HORIZONTAL, variable=self.potencia,
                                      command=self.actualizar_potencia,
                                      bg='#2d2d2d', fg='#ffffff', 
                                      troughcolor='#ff6b35', highlightthickness=0, 
                                      length=300, width=20)
        self.potencia_scale.pack(pady=10)
        
        self.dial_canvas = dial_canvas
        self.actualizar_dial()
        
        # Botones de control
        botones_frame = tk.Frame(scrollable_config, bg='#2d2d2d')
        botones_frame.pack(fill=tk.X, padx=15, pady=20)
        
        self.btn_iniciar = tk.Button(botones_frame, text="▶ INICIAR COCCIÓN", 
                                     command=self.iniciar_coccion,
                                     bg='#4caf50', fg='white', 
                                     font=('Arial', 14, 'bold'),
                                     relief=tk.RAISED, bd=4, 
                                     activebackground='#45a049',
                                     cursor='hand2', height=2)
        self.btn_iniciar.pack(fill=tk.X, pady=5)
        
        self.btn_detener = tk.Button(botones_frame, text="⏹ DETENER", 
                                     command=self.detener_coccion,
                                     bg='#f44336', fg='white', 
                                     font=('Arial', 14, 'bold'),
                                     relief=tk.RAISED, bd=4, 
                                     activebackground='#da190b',
                                     state=tk.DISABLED, cursor='hand2', height=2)
        self.btn_detener.pack(fill=tk.X, pady=5)
        
        tk.Button(botones_frame, text="🔄 REINICIAR SISTEMA", 
                 command=self.reiniciar,
                 bg='#2196f3', fg='white', 
                 font=('Arial', 14, 'bold'),
                 relief=tk.RAISED, bd=4, 
                 activebackground='#0b7dda',
                 cursor='hand2', height=2).pack(fill=tk.X, pady=5)
        
        # === TAB 2: ESTADÍSTICAS ===
        stats_tab = tk.Frame(notebook, bg='#2d2d2d')
        notebook.add(stats_tab, text='📊 Estadísticas')
        
        # Crear sistema de scroll para estadísticas
        stats_container = tk.Frame(stats_tab, bg='#2d2d2d')
        stats_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar para estadísticas
        canvas_stats = tk.Canvas(stats_container, bg='#1a1a1a', highlightthickness=0)
        scrollbar_stats = tk.Scrollbar(stats_container, orient="vertical", command=canvas_stats.yview)
        
        # Frame scrollable dentro del canvas
        self.scrollable_stats = tk.Frame(canvas_stats, bg='#1a1a1a')
        
        self.scrollable_stats.bind(
            "<Configure>",
            lambda e: canvas_stats.configure(scrollregion=canvas_stats.bbox("all"))
        )
        
        canvas_stats.create_window((0, 0), window=self.scrollable_stats, anchor="nw")
        canvas_stats.configure(yscrollcommand=scrollbar_stats.set)
        
        # Empaquetar canvas y scrollbar
        canvas_stats.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar_stats.pack(side="right", fill="y")
        
        # Canvas para gráficos dentro del frame scrollable
        self.stats_canvas = tk.Canvas(self.scrollable_stats, bg='#1a1a1a', highlightthickness=0,
                                     width=800, height=1200)
        self.stats_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === TAB 3: INFORMACIÓN ===
        info_tab = tk.Frame(notebook, bg='#2d2d2d')
        notebook.add(info_tab, text='ℹ️ Información')
        
        info_text = tk.Text(info_tab, bg='#1a1a1a', fg='#ffffff', 
                           font=('Arial', 11), wrap=tk.WORD, 
                           relief=tk.FLAT, padx=20, pady=20)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info_content = """
=========================================================
==       MICROONDAS MULTIFUNCIONAL 3000 - MANUAL         ==
=========================================================
🔥 COMBUSTIBLES DISPONIBLES:
=========================================================
⚡ Energía Eléctrica: 2.5 kcal/min por minuto
   • Limpio y eficiente
   • Ideal para uso doméstico
   • Control preciso de temperatura

🪵 Madera: 4.0 kcal/min por minuto
   • Mayor potencia calorífica
   • Sabor ahumado natural
   • Requiere ventilación adecuada

🍂 Hojas Secas: 3.0 kcal/min por minuto
   • Opción ecológica
   • Combustión rápida
   • Bajo costo operativo

⛽ Combustible (Gasolina): 5.5 kcal/min por minuto
   • Máxima potencia
   • Calentamiento ultra-rápido
   • Uso industrial

=========================================================
🍖 ALIMENTOS Y TIEMPOS BASE (100% potencia):
=========================================================
🍗 Pollo: 25 minutos
🦃 Pavo: 45 minutos  
🥩 Res: 35 minutos

=========================================================
⚙️ CÁLCULOS DINÁMICOS:
=========================================================
• Tiempo Ajustado = Tiempo Base × (100 / Potencia)
• Consumo por minuto = Consumo Combustible × (Potencia/100)
• El tiempo y consumo se actualizan automáticamente
=========================================================
"""
        
        info_text.insert('1.0', info_content)
        info_text.config(state=tk.DISABLED)
        
    def calcular_tiempo_ajustado(self):
        """Calcula el tiempo de cocción ajustado según la potencia"""
        tiempo_base = self.tiempo_base_alimento[self.alimento_actual.get()]
        potencia = self.potencia.get()
        
        # A mayor potencia, menor tiempo (relación inversa)
        if potencia > 0:
            tiempo_ajustado = tiempo_base * (100 / potencia)
            return max(1, int(tiempo_ajustado))
        return tiempo_base
    
    def calcular_consumo_estimado(self):
        """Calcula el consumo total estimado"""
        tiempo_estimado = self.calcular_tiempo_ajustado()
        consumo_minuto = self.consumo_combustible[self.combustible_actual.get()]
        potencia = self.potencia.get() / 100.0
        
        consumo_total = consumo_minuto * potencia * tiempo_estimado
        return consumo_total
    
    def actualizar_tiempo_estimado(self):
        """Actualiza las etiquetas de tiempo y consumo estimado"""
        if not self.cocinando:
            tiempo_ajustado = self.calcular_tiempo_ajustado()
            consumo_estimado = self.calcular_consumo_estimado()
            
            self.tiempo_estimado_label.config(
                text=f"Tiempo estimado: {tiempo_ajustado} minutos"
            )
            self.consumo_estimado_label.config(
                text=f"Consumo estimado: {consumo_estimado:.1f} kcal"
            )
        
    def actualizar_dial(self):
        potencia_val = self.potencia.get()
        angle = math.radians(225 - (potencia_val * 2.7))
        x = 100 + 60 * math.cos(angle)
        y = 100 - 60 * math.sin(angle)
        self.dial_canvas.coords(self.dial_line, 100, 100, x, y)
        
    def actualizar_potencia(self, valor):
        self.potencia_label.config(text=f"{valor}%")
        self.actualizar_dial()
        self.actualizar_tiempo_estimado()
        
    def actualizar_combustible(self):
        combustible = self.combustible_actual.get()
        emoji = self.emojis_combustible[combustible]
        self.combustible_indicator.config(text=f"{emoji} {combustible}")
        self.actualizar_tiempo_estimado()
        
    def actualizar_alimento(self):
        emojis = {"Pollo": "🍗", "Pavo": "🦃", "Res": "🥩"}
        self.canvas.itemconfig(self.alimento_id, text=emojis[self.alimento_actual.get()])
        self.actualizar_tiempo_estimado()
        
    def iniciar_coccion(self):
        self.cocinando = True
        self.estado = "Cocinando"
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)
        self.display_estado.config(text="COCINANDO", fg='#00ff00')
        
        # Obtener tiempo objetivo ajustado
        self.tiempo_objetivo = self.calcular_tiempo_ajustado()
        self.tiempo_transcurrido = 0
        
        self.cocinar()
        self.girar_plato()
        
    def cocinar(self):
        if self.cocinando:
            self.tiempo_transcurrido += 1
            
            # Calcular kcal por minuto actual
            consumo_base = self.consumo_combustible[self.combustible_actual.get()]
            factor_potencia = self.potencia.get() / 100.0
            kcal_minuto = consumo_base * factor_potencia
            self.kcal_consumidas += kcal_minuto
            
            # Actualizar historial
            self.historial_tiempo.append(self.tiempo_transcurrido)
            self.historial_kcal.append(self.kcal_consumidas)
            self.historial_combustibles[self.combustible_actual.get()] += kcal_minuto
            
            # Actualizar displays
            minutos = self.tiempo_transcurrido
            segundos = 0
            self.lcd_tiempo.config(text=f"{minutos:02d}:{segundos:02d}")
            self.lcd_kcal.config(text=f"{self.kcal_consumidas:.1f} kcal")
            
            # Actualizar estadísticas
            self.dibujar_estadisticas()
            
            # Verificar si terminó
            if self.tiempo_transcurrido >= self.tiempo_objetivo:
                self.terminar_coccion()
                return
            
            self.root.after(1000, self.cocinar)
            
    def girar_plato(self):
        if self.cocinando:
            self.plato_angulo = (self.plato_angulo + 10) % 360
            # Rotar el alimento
            angle_rad = math.radians(self.plato_angulo)
            offset = 30
            x = 350 + offset * math.cos(angle_rad)
            y = 300 + offset * math.sin(angle_rad)
            self.canvas.coords(self.alimento_id, x, y)
            self.root.after(100, self.girar_plato)
            
    def detener_coccion(self):
        self.cocinando = False
        self.estado = "Detenido"
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)
        self.display_estado.config(text="PAUSADO", fg='#ffff00')
        
    def terminar_coccion(self):
        self.cocinando = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)
        self.display_estado.config(text="LISTO", fg='#00ff00')
        
        messagebox.showinfo(
            "¡Cocción Completa! 🎉",
            f"===============================================\n"
            f"   ¡Tu {self.alimento_actual.get()} está listo!\n"
            f"===============================================\n\n"
            f"⏱️  Tiempo total: {self.tiempo_transcurrido} minutos\n"
            f"🔥 Combustible: {self.combustible_actual.get()}\n"
            f"⚡ Potencia: {self.potencia.get()}%\n"
            f"📊 Consumo: {self.kcal_consumidas:.1f} kcal\n\n"
            f"¡Buen provecho! 🍽️"
        )
        
    def reiniciar(self):
        self.cocinando = False
        self.estado = "Apagado"
        self.tiempo_transcurrido = 0
        self.kcal_consumidas = 0
        self.historial_tiempo = []
        self.historial_kcal = []
        self.historial_combustibles = {k: 0 for k in self.historial_combustibles}
        
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)
        self.display_estado.config(text="APAGADO", fg='#ff0000')
        self.lcd_tiempo.config(text="00:00")
        self.lcd_kcal.config(text="0 kcal/h")
        
        self.actualizar_tiempo_estimado()
        self.dibujar_estadisticas()
        
    def dibujar_estadisticas(self):
        self.stats_canvas.delete("all")
        w = 800
        h = 1200

        # Título
        self.stats_canvas.create_text(w//2, 30, text="📊 ANÁLISIS ENERGÉTICO EN TIEMPO REAL", 
                                     font=('Arial', 16, 'bold'), fill='#ffffff')
        
        # Gráfico de línea - Consumo en el tiempo
        if self.historial_tiempo:
            # Marco del gráfico
            x0, y0 = 50, 80
            x1, y1 = w - 50, 280
            self.stats_canvas.create_rectangle(x0, y0, x1, y1, outline='#666666', width=2)
            self.stats_canvas.create_text((x0+x1)//2, y0-10, 
                                         text="Consumo kcal en el Tiempo", 
                                         font=('Arial', 12, 'bold'), fill='#00ff00')
            
            # Dibujar línea
            max_kcal = max(self.historial_kcal) if self.historial_kcal else 1
            max_tiempo = max(self.historial_tiempo) if self.historial_tiempo else 1
            
            points = []
            for i, (t, k) in enumerate(zip(self.historial_tiempo, self.historial_kcal)):
                x = x0 + (t / max_tiempo) * (x1 - x0)
                y = y1 - (k / max_kcal) * (y1 - y0)
                points.extend([x, y])
                
                # Puntos
                self.stats_canvas.create_oval(x-3, y-3, x+3, y+3, fill='#00ff00', outline='white')
            
            # Dibujar línea conectando puntos
            if len(points) >= 4:
                self.stats_canvas.create_line(points, fill='#00ff00', width=3, smooth=True)
            
            # Etiquetas de ejes
            self.stats_canvas.create_text(x0-30, y1, text="0", fill='white', font=('Arial', 9))
            self.stats_canvas.create_text(x0-30, y0, text=f"{max_kcal:.1f}", fill='white', font=('Arial', 9))
            self.stats_canvas.create_text(x0, y1+15, text="0", fill='white', font=('Arial', 9))
            self.stats_canvas.create_text(x1, y1+15, text=f"{int(max_tiempo)}", fill='white', font=('Arial', 9))
            self.stats_canvas.create_text(x0-40, (y0+y1)//2, text="kcal", fill='white', font=('Arial', 9))
            self.stats_canvas.create_text((x0+x1)//2, y1+30, text="Tiempo (min)", fill='white', font=('Arial', 9))

        # Información actual
        y_info = 320
        info_text = f"⚙️ CONFIGURACIÓN ACTUAL:\n"
        info_text += f"🍖 Alimento: {self.alimento_actual.get()}\n"
        info_text += f"🔥 Combustible: {self.combustible_actual.get()}\n"
        info_text += f"⚡ Potencia: {self.potencia.get()}%\n"
        info_text += f"⏱️ Tiempo estimado: {self.calcular_tiempo_ajustado()} min\n"
        info_text += f"📊 Consumo estimado: {self.calcular_consumo_estimado():.1f} kcal"
        
        self.stats_canvas.create_text(w//2, y_info, text=info_text,
                                     font=('Arial', 11, 'bold'), fill='#ffff00',
                                     justify=tk.CENTER)

# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MicroondasMultifuncional(root)
    root.mainloop()