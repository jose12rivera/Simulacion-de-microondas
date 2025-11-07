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
        
        # Tiempo de cocción óptimo por alimento (minutos)
        self.tiempo_alimento = {
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
            ("🍗 Pollo (25 min)", "Pollo"),
            ("🦃 Pavo (45 min)", "Pavo"),
            ("🥩 Res (35 min)", "Res")
        ]
        
        for texto, valor in alimentos:
            rb = tk.Radiobutton(alimento_frame, text=texto, 
                              variable=self.alimento_actual, value=valor,
                              bg='#3d3d3d', fg='#ffffff', selectcolor='#1a1a1a',
                              font=('Arial', 11), 
                              activebackground='#3d3d3d', activeforeground='white',
                              command=self.actualizar_alimento)
            rb.pack(anchor=tk.W, pady=5, padx=10)
        
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
                                     width=800, height=1200)  # Altura aumentada para contenido extenso
        self.stats_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === TAB 3: INFORMACIÓN ===
        info_tab = tk.Frame(notebook, bg='#2d2d2d')
        notebook.add(info_tab, text='ℹ️ Información')
        
        info_text = tk.Text(info_tab, bg='#1a1a1a', fg='#ffffff', 
                           font=('Arial', 11), wrap=tk.WORD, 
                           relief=tk.FLAT, padx=20, pady=20)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info_content = """
╔═══════════════════════════════════════════════════════════╗
║        MICROONDAS MULTIFUNCIONAL 3000 - MANUAL           ║
╚═══════════════════════════════════════════════════════════╝

🔥 COMBUSTIBLES DISPONIBLES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Energía Eléctrica: 2.5 kcal/h por minuto
   • Limpio y eficiente
   • Ideal para uso doméstico
   • Control preciso de temperatura

🪵 Madera: 4.0 kcal/h por minuto
   • Mayor potencia calorífica
   • Sabor ahumado natural
   • Requiere ventilación adecuada

🍂 Hojas Secas: 3.0 kcal/h por minuto
   • Opción ecológica
   • Combustión rápida
   • Bajo costo operativo

⛽ Combustible (Gasolina): 5.5 kcal/h por minuto
   • Máxima potencia
   • Calentamiento ultra-rápido
   • Uso industrial

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍖 ALIMENTOS Y TIEMPOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍗 Pollo: 25 minutos
🦃 Pavo: 45 minutos  
🥩 Res: 35 minutos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️ INSTRUCCIONES DE USO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Seleccione el tipo de combustible deseado
2. Elija el alimento a cocinar
3. Ajuste la potencia (10% - 100%)
4. Presione INICIAR COCCIÓN
5. Observe el progreso en tiempo real
6. El sistema le notificará cuando esté listo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 CÁLCULO DE ENERGÍA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

El consumo energético se calcula mediante:

kcal/h = (Consumo base) × (Potencia/100) × 60

Ejemplo:
• Combustible: Madera (4.0 kcal/h por minuto)
• Potencia: 75%
• Resultado: 4.0 × 0.75 × 60 = 180 kcal/h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ ADVERTENCIAS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• No usar combustibles líquidos cerca de llamas abiertas
• Mantener ventilación adecuada con madera u hojas
• No abrir durante la cocción
• Supervisar constantemente el proceso

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TECNOLOGÍA INNOVADORA
Patente pendiente © 2025 Microondas Multifuncional 3000
        """
        
        info_text.insert('1.0', info_content)
        info_text.config(state=tk.DISABLED)
        
    def actualizar_dial(self):
        potencia_val = self.potencia.get()
        angle = math.radians(225 - (potencia_val * 2.7))
        x = 100 + 60 * math.cos(angle)
        y = 100 - 60 * math.sin(angle)
        self.dial_canvas.coords(self.dial_line, 100, 100, x, y)
        
    def actualizar_potencia(self, valor):
        self.potencia_label.config(text=f"{valor}%")
        self.actualizar_dial()
        
    def actualizar_combustible(self):
        combustible = self.combustible_actual.get()
        emoji = self.emojis_combustible[combustible]
        self.combustible_indicator.config(text=f"{emoji} {combustible}")
        
    def actualizar_alimento(self):
        emojis = {"Pollo": "🍗", "Pavo": "🦃", "Res": "🥩"}
        self.canvas.itemconfig(self.alimento_id, text=emojis[self.alimento_actual.get()])
        
    def iniciar_coccion(self):
        self.cocinando = True
        self.estado = "Cocinando"
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)
        self.display_estado.config(text="COCINANDO", fg='#00ff00')
        self.cocinar()
        self.girar_plato()
        
    def cocinar(self):
        if self.cocinando:
            self.tiempo_coccion += 1
            
            # Calcular kcal
            consumo_base = self.consumo_combustible[self.combustible_actual.get()]
            factor_potencia = self.potencia.get() / 100.0
            kcal_minuto = consumo_base * factor_potencia * 60
            self.kcal_consumidas += kcal_minuto
            
            # Actualizar historial
            self.historial_tiempo.append(self.tiempo_coccion)
            self.historial_kcal.append(self.kcal_consumidas)
            self.historial_combustibles[self.combustible_actual.get()] += kcal_minuto
            
            # Actualizar displays
            minutos = self.tiempo_coccion
            self.lcd_tiempo.config(text=f"{minutos:02d}:00")
            self.lcd_kcal.config(text=f"{self.kcal_consumidas:.0f} kcal/h")
            
            # Actualizar estadísticas
            self.dibujar_estadisticas()
            
            # Verificar si terminó
            if self.tiempo_coccion >= self.tiempo_alimento[self.alimento_actual.get()]:
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
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   ¡Tu {self.alimento_actual.get()} está listo!\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"⏱️  Tiempo total: {self.tiempo_coccion} minutos\n"
            f"🔥 Combustible: {self.combustible_actual.get()}\n"
            f"⚡ Potencia: {self.potencia.get()}%\n"
            f"📊 Consumo: {self.kcal_consumidas:.1f} kcal/h\n\n"
            f"¡Buen provecho! 🍽️"
        )
        
    def reiniciar(self):
        self.cocinando = False
        self.estado = "Apagado"
        self.tiempo_coccion = 0
        self.kcal_consumidas = 0
        self.historial_tiempo = []
        self.historial_kcal = []
        self.historial_combustibles = {k: 0 for k in self.historial_combustibles}
        
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)
        self.display_estado.config(text="APAGADO", fg='#ff0000')
        self.lcd_tiempo.config(text="00:00")
        self.lcd_kcal.config(text="0 kcal/h")
        
        self.dibujar_estadisticas()
        
    def dibujar_estadisticas(self):
        self.stats_canvas.delete("all")
        w = 800  # Ancho fijo para el canvas de estadísticas
        h = 1200  # Altura fija para permitir scroll
        
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
                                         text="Consumo kcal/h en el Tiempo", 
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
            self.stats_canvas.create_text(x0-30, y0, text=f"{int(max_kcal)}", fill='white', font=('Arial', 9))
            self.stats_canvas.create_text(x0, y1+15, text="0", fill='white', font=('Arial', 9))
            self.stats_canvas.create_text(x1, y1+15, text=f"{int(max_tiempo)}", fill='white', font=('Arial', 9))
            self.stats_canvas.create_text(x0-30, (y0+y1)//2, text="kcal/h", fill='white', font=('Arial', 9))
            self.stats_canvas.create_text((x0+x1)//2, y1+30, text="Tiempo (min)", fill='white', font=('Arial', 9))
        
        # Gráfico de pastel - Distribución de combustibles
        y_offset = 320
        self.stats_canvas.create_text(w//2, y_offset, 
                                     text="Distribución de Uso por Combustible", 
                                     font=('Arial', 12, 'bold'), fill='#ff6b35')
        
        total = sum(self.historial_combustibles.values())
        if total > 0:
            cx, cy = w//2, y_offset + 120
            radius = 80
            start_angle = 0
            
            colores = {
                "Energía Eléctrica": "#ffeb3b",
                "Madera": "#ff9800", 
                "Hojas Secas": "#8bc34a",
                "Combustible (Gasolina)": "#f44336"
            }
            
            for combustible, valor in self.historial_combustibles.items():
                if valor > 0:
                    extent = (valor / total) * 360
                    self.stats_canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                                                start=start_angle, extent=extent,
                                                fill=colores[combustible], outline='white', width=2)
                    
                    # Etiqueta
                    angle_mid = math.radians(start_angle + extent/2)
                    label_x = cx + (radius + 40) * math.cos(angle_mid)
                    label_y = cy - (radius + 40) * math.sin(angle_mid)
                    porcentaje = (valor / total) * 100
                    
                    self.stats_canvas.create_text(label_x, label_y, 
                                                 text=f"{combustible.split()[0]}\n{porcentaje:.1f}%",
                                                 fill=colores[combustible], 
                                                 font=('Arial', 9, 'bold'))
                    
                    start_angle += extent
        else:
            self.stats_canvas.create_text(w//2, y_offset + 100, 
                                         text="Sin datos - Inicie la cocción", 
                                         fill='#666666', font=('Arial', 11))
        
        # Resumen estadístico
        y_stats = y_offset + 220
        self.stats_canvas.create_rectangle(50, y_stats, w-50, y_stats+80, 
                                          fill='#3d3d3d', outline='#ff6b35', width=2)
        
        self.stats_canvas.create_text(w//2, y_stats+15, 
                                     text="📈 RESUMEN ESTADÍSTICO", 
                                     font=('Arial', 12, 'bold'), fill='#ffffff')
        
        stats_text = f"Tiempo Total: {self.tiempo_coccion} min  |  "
        stats_text += f"Consumo Total: {self.kcal_consumidas:.1f} kcal/h  |  "
        stats_text += f"Potencia Actual: {self.potencia.get()}%"
        
        self.stats_canvas.create_text(w//2, y_stats+45, 
                                     text=stats_text, 
                                     font=('Arial', 10), fill='#00ff00')
        
        # Información adicional extensa
        y_extra = y_stats + 120
        
        # Eficiencia por combustible
        eficiencia_frame = tk.Frame(self.scrollable_stats, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        eficiencia_frame.place(x=50, y=y_extra, width=w-100, height=200)
        
        eficiencia_label = tk.Label(eficiencia_frame, text="📈 EFICIENCIA POR COMBUSTIBLE", 
                                   font=('Arial', 12, 'bold'), bg='#2d2d2d', fg='#ffffff')
        eficiencia_label.pack(pady=10)
        
        # Tabla de eficiencia
        eficiencia_text = tk.Text(eficiencia_frame, bg='#1a1a1a', fg='#ffffff', 
                                 font=('Arial', 10), width=70, height=8, relief=tk.FLAT)
        eficiencia_text.pack(padx=10, pady=10, fill=tk.BOTH)
        
        tabla_content = "Combustible           kcal/min   Eficiencia   Costo Relativo\n"
        tabla_content += "──────────────────────────────────────────────────────────\n"
        tabla_content += "⚡ Energía Eléctrica     2.5       Alta           Medio\n"
        tabla_content += "🪵 Madera                4.0       Media          Bajo\n"
        tabla_content += "🍂 Hojas Secas           3.0       Baja           Muy Bajo\n"
        tabla_content += "⛽ Combustible           5.5       Muy Alta       Alto\n"
        
        eficiencia_text.insert('1.0', tabla_content)
        eficiencia_text.config(state=tk.DISABLED)
        
        # Historial detallado
        y_historial = y_extra + 230
        
        historial_frame = tk.Frame(self.scrollable_stats, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        historial_frame.place(x=50, y=y_historial, width=w-100, height=300)
        
        historial_label = tk.Label(historial_frame, text="📋 HISTORIAL DETALLADO", 
                                  font=('Arial', 12, 'bold'), bg='#2d2d2d', fg='#ffffff')
        historial_label.pack(pady=10)
        
        historial_text = tk.Text(historial_frame, bg='#1a1a1a', fg='#ffffff', 
                                font=('Courier', 9), width=80, height=12, relief=tk.FLAT)
        historial_scroll = tk.Scrollbar(historial_frame, command=historial_text.yview)
        historial_text.configure(yscrollcommand=historial_scroll.set)
        
        historial_text.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)
        historial_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Contenido del historial
        if self.historial_tiempo:
            hist_content = "Minuto   kcal Acumuladas   Combustible Actual\n"
            hist_content += "─────────────────────────────────────────────\n"
            for i, (tiempo, kcal) in enumerate(zip(self.historial_tiempo, self.historial_kcal)):
                hist_content += f"{tiempo:^7} {kcal:^15.1f}   {self.combustible_actual.get()}\n"
        else:
            hist_content = "No hay datos de historial disponibles.\nInicie la cocción para generar datos."
        
        historial_text.insert('1.0', hist_content)
        historial_text.config(state=tk.DISABLED)

# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MicroondasMultifuncional(root)
    root.mainloop()