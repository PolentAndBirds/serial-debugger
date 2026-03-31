from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotManager:
    """
    Gestisce la visualizzazione dei grafici in tempo reale con auto-zoom (Min-Max scaling).
    """
    def __init__(self, master_frame, app_callback):
        self.container = master_frame
        self.app = app_callback
        self.plot_data = {} # idx -> deque dei valori
        self.plot_max_reached = {} # idx -> valore massimo storico
        self.plot_min_reached = {} # idx -> valore minimo storico
        self.plotted_indices = set()
        self.max_points = 200
        
        self.fig, self.ax = plt.subplots(figsize=(5, 2), dpi=100)
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax.set_facecolor('#0d0d0d')
        self.ax.tick_params(colors='gray', labelsize=8)
        self.ax.grid(color='#333333', linestyle='--', alpha=0.5)
        self.ax.set_ylim(-0.05, 1.05)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def toggle_variable(self, idx, is_active):
        if is_active:
            self.plotted_indices.add(idx)
            if idx not in self.plot_data:
                self.plot_data[idx] = deque([0.0] * self.max_points, maxlen=self.max_points)  
                self.plot_max_reached[idx] = -1e12 # Placeholder molto piccolo
                self.plot_min_reached[idx] = 1e12  # Placeholder molto grande
        else:
            if idx in self.plotted_indices:
                self.plotted_indices.remove(idx)

    def clear_data(self):
        self.plot_data = {}
        self.plot_max_reached = {}
        self.plot_min_reached = {}
        self.plotted_indices.clear()
        self.ax.clear()
        self.ax.set_facecolor('#0d0d0d')
        self.ax.grid(color='#333333', linestyle='--', alpha=0.5)
        self.ax.set_ylim(-0.05, 1.05)
        self.canvas.draw_idle()

    def update_plot(self):
        if not self.app.winfo_exists():
            return

        if self.app.running and self.plotted_indices:
            self.ax.clear()
            self.ax.set_facecolor('#0d0d0d')
            self.ax.grid(color='#333333', linestyle='--', alpha=0.5)
            self.ax.set_ylim(-0.05, 1.05)
            
            for idx in self.plotted_indices:
                data = list(self.plot_data.get(idx, [0.0]))
                v_max = self.plot_max_reached.get(idx, 1.0)
                v_min = self.plot_min_reached.get(idx, -1.0)
                
                # Calcola delta per normalizzazione
                diff = v_max - v_min
                if diff == 0:
                    norm_data = [0.5 for _ in data] # Mostra linea centrale se valore è costante
                else:
                    # Scaling 0.0 - 1.0
                    norm_data = [(v - v_min) / diff for v in data]
                
                var_name = f"Var {idx}"
                if self.app.jte_comm:
                    for v in self.app.jte_comm.variables:
                        if v['index'] == idx:
                            var_name = v['name']
                            break
                
                self.ax.plot(norm_data, label=f"{var_name} [{v_min:.1f} .. {v_max:.1f}]")
            
            if self.plotted_indices:
                self.ax.legend(loc="upper left", fontsize=8, facecolor='#1a1a1a', labelcolor='white')
            
            self.canvas.draw_idle()
        
        # Schedula il prossimo aggiornamento
        if self.app.winfo_exists():
            self.app.after(50, self.update_plot)

    def add_value(self, idx, value):
        try:
            # Pulisci la stringa da eventuali caratteri non numerici
            clean_val = "".join(c for c in value if c.isdigit() or c in '.-')
            if not clean_val: return
            v = float(clean_val)
            
            if idx not in self.plot_data:
                self.plot_data[idx] = deque([v] * self.max_points, maxlen=self.max_points)
                self.plot_max_reached[idx] = v
                self.plot_min_reached[idx] = v
            
            self.plot_data[idx].append(v)
            
            # Aggiorna i limiti storici per l'auto-zoom
            self.plot_max_reached[idx] = max(self.plot_max_reached[idx], v)
            self.plot_min_reached[idx] = min(self.plot_min_reached[idx], v)
            
        except Exception as e:
            pass
