from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotManager:
    """
    Gestisce la visualizzazione dei grafici in tempo reale con auto-zoom, hover e pausa.
    """
    def __init__(self, master_frame, app_callback):
        self.container = master_frame
        self.app = app_callback
        self.plot_data = {} # idx -> deque dei valori
        self.plot_max_reached = {} # idx -> valore massimo storico
        self.plot_min_reached = {} # idx -> valore minimo storico
        self.plotted_indices = set()
        self.max_points = 200
        self.is_paused = False
        
        self.fig, self.ax = plt.subplots(figsize=(5, 2), dpi=100)
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax.set_facecolor('#0d0d0d')
        self.ax.tick_params(colors='gray', labelsize=8)
        self.ax.grid(color='#333333', linestyle='--', alpha=0.5)
        self.ax.set_ylim(-0.05, 1.05)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Gestione interattività
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        self.last_hover_x = -1
        self.last_hover_info = ""

    def toggle_pause(self):
        """Attiva/disattiva la pausa. Se riprende, pulisce i dati."""
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self.clear_data()
        return self.is_paused

    def toggle_variable(self, idx, is_active):
        if is_active:
            self.plotted_indices.add(idx)
            if idx not in self.plot_data:
                self.plot_data[idx] = deque([0.0] * self.max_points, maxlen=self.max_points)  
                self.plot_max_reached[idx] = -1e12
                self.plot_min_reached[idx] = 1e12
        else:
            if idx in self.plotted_indices:
                self.plotted_indices.remove(idx)

    def clear_data(self):
        self.plot_data = {}
        self.plot_max_reached = {}
        self.plot_min_reached = {}
        self.ax.clear()
        self.ax.set_facecolor('#0d0d0d')
        self.ax.grid(color='#333333', linestyle='--', alpha=0.5)
        self.ax.set_ylim(-0.05, 1.05)
        self.canvas.draw_idle()

    def update_plot(self):
        if not self.app.winfo_exists():
            return

        # Aggiorna il grafico solo se non in pausa e se ci sono dati
        if self.app.running and self.plotted_indices and not self.is_paused:
            self.ax.clear()
            self.ax.set_facecolor('#0d0d0d')
            self.ax.grid(color='#333333', linestyle='--', alpha=0.5)
            self.ax.set_ylim(-0.05, 1.05)
            
            for idx in self.plotted_indices:
                data = list(self.plot_data.get(idx, [0.0]))
                v_max = self.plot_max_reached.get(idx, 1.0)
                v_min = self.plot_min_reached.get(idx, -1.0)
                
                diff = v_max - v_min
                if diff == 0:
                    norm_data = [0.5 for _ in data]
                else:
                    norm_data = [(v - v_min) / diff for v in data]
                
                var_name = f"V{idx}"
                if self.app.jte_comm:
                    for v in self.app.jte_comm.variables:
                        if v['index'] == idx:
                            var_name = v['name']
                            break
                self.ax.plot(norm_data, label=f"{var_name}")
            
            # Info Hover persistente
            if self.last_hover_x >= 0:
                self.ax.axvline(self.last_hover_x, color='white', linestyle='--', alpha=0.3)
                self.ax.set_title(self.last_hover_info, color='#00FF00', fontsize=9, pad=3)

            if self.plotted_indices:
                self.ax.legend(loc="upper left", fontsize=7, facecolor='#1a1a1a', labelcolor='white', ncol=3)
            
            self.canvas.draw_idle()
        
        # Mantieni l'hover funzionante anche in pausa
        elif self.is_paused and self.last_hover_x >= 0:
            # Ridisegna solo l'hover sopra l'ultima immagine statica
            # Nota: ax.clear non viene chiamato qui, quindi dobbiamo stare attenti
            pass

        if self.app.winfo_exists():
            self.app.after(50, self.update_plot)

    def on_mouse_move(self, event):
        if not event.inaxes or not self.plotted_indices:
            self.last_hover_x = -1
            self.last_hover_info = ""
            return

        try:
            x = int(round(event.xdata))
            if 0 <= x < self.max_points:
                hover_info = []
                for idx in self.plotted_indices:
                    data = self.plot_data.get(idx)
                    if data and x < len(data):
                        val = data[x]
                        name = f"V{idx}"
                        if self.app.jte_comm:
                            for v in self.app.jte_comm.variables:
                                if v['index'] == idx:
                                    name = v['name']
                                    break
                        hover_info.append(f"{name}: {val:.2f}")
                
                self.last_hover_x = x
                self.last_hover_info = f"T[{x}]: " + " | ".join(hover_info)
                
                # Se siamo in pausa o non in corsa, aggiorniamo manualmente il titolo per il feedback immediato
                # senza cancellare il grafico sottostante
                self.ax.set_title(self.last_hover_info, color='#00FF00', fontsize=9, pad=3)
                self.canvas.draw_idle()
        except:
            pass

    def add_value(self, idx, value):
        if self.is_paused: return # Non accumula dati in pausa
        
        try:
            clean_val = "".join(c for c in value if c.isdigit() or c in '.-')
            if not clean_val: return
            v = float(clean_val)
            
            if idx not in self.plot_data:
                self.plot_data[idx] = deque([v] * self.max_points, maxlen=self.max_points)
                self.plot_max_reached[idx] = v
                self.plot_min_reached[idx] = v
            
            self.plot_data[idx].append(v)
            self.plot_max_reached[idx] = max(self.plot_max_reached[idx], v)
            self.plot_min_reached[idx] = min(self.plot_min_reached[idx], v)
            
        except:
            pass
