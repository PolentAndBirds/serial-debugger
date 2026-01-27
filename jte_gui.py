
import customtkinter as ctk # CustomTkinter è una libreria basata su Tkinter con un'estetica moderna
import serial.tools.list_ports
from jte_protocol import JTEProtocol
from tcp_serial_bridge import TCPSerialBridge
import threading
import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

"""
CONCETTI BASE DI TKINTER / CUSTOMTKINTER:
1. Widget: Sono gli elementi dell'interfaccia (pulsanti, etichette, riquadri).
2. Frame: Sono contenitori usati per raggruppare e organizzare altri widget.
3. Layout Managers: Metodi per posizionare i widget:
   - pack(): Impila i widget uno dopo l'altro (sopra, sotto, destra, sinistra).
   - grid(): Dispone i widget in una tabella (righe e colonne).
4. Mainloop: Il ciclo infinito che mantiene l'app aperta e in ascolto di eventi (click, tastiera).
5. Threading: In una GUI, le operazioni lunghe (come leggere la seriale) devono stare in un 
   thread separato, altrimenti l'interfaccia "si blocca" e smette di rispondere.
"""

class VariableRow(ctk.CTkFrame):
    """
    Rappresenta una singola riga nell'interfaccia per una variabile.
    """
    def __init__(self, master, var_data, on_modify, on_plot_toggle, is_plotted=False, **kwargs):
        super().__init__(master, **kwargs)
        self.var_data = var_data
        self.on_modify = on_modify
        self.on_plot_toggle = on_plot_toggle
        self.plot_cb_visible = False # Traccia se la checkbox è visualizzata
        
        # Etichetta Nome: anchor="w" allinea il testo a sinistra (West)
        # Font in grassetto se la variabile è di tipo '0' (presumibilmente un titolo o costante)
        self.name_label = ctk.CTkLabel(self, text=var_data['name'], width=300, anchor="w", 
                                      font=ctk.CTkFont(weight="bold" if var_data['step_type'] == '0' else "normal"))
        self.name_label.pack(side="left", padx=10, pady=1)
        
        # Etichetta Valore: anchor="e" allinea il testo a destra (East)
        self.value_label = ctk.CTkLabel(self, text="--", width=200, anchor="e")
        self.value_label.pack(side="left", padx=10, pady=1)
        
        # Se la variabile è modificabile (step_type '1' o '2'), aggiunge i pulsanti di controllo
        if var_data['step_type'] in ['1', '2']:
            # I pulsanti usano "lambda" per passare argomenti alla funzione on_modify senza eseguirla subito
            self.min_btn = ctk.CTkButton(self, text="-", width=30, command=lambda: self.on_modify(var_data['index'], '-'))
            self.min_btn.pack(side="right", padx=2)
            
            self.plus_btn = ctk.CTkButton(self, text="+", width=30, command=lambda: self.on_modify(var_data['index'], '+'))
            self.plus_btn.pack(side="right", padx=2)
            
            self.dmin_btn = ctk.CTkButton(self, text="--", width=40, command=lambda: self.on_modify(var_data['index'], '/'))
            self.dmin_btn.pack(side="right", padx=2)
            
            self.dplus_btn = ctk.CTkButton(self, text="++", width=40, command=lambda: self.on_modify(var_data['index'], '*'))
            self.dplus_btn.pack(side="right", padx=2)

        # Checkbox per il plotting (inizialmente nascosto o visibile in base al tipo/stato)
        self.plot_cb = ctk.CTkCheckBox(self, text="Plot", width=40, 
                                      command=lambda: self.on_plot_toggle(var_data['index'], self.plot_cb.get()))
        
        # Se la variabile era già monitorata o è di tipo modificabile (sicuramente ha un valore), la mostriamo
        # Per le variabili di tipo '0', la checkbox è visibile solo se già monitorata.
        # Per le variabili di tipo '1' o '2', è sempre visibile.
        if is_plotted or var_data['step_type'] in ['1', '2']:
            if is_plotted:
                self.plot_cb.select()
            self._show_plot_checkbox()

    def _show_plot_checkbox(self):
        """Rende visibile la checkbox del grafico se non lo è già."""
        if not self.plot_cb_visible:
            self.plot_cb.pack(side="right", padx=10)
            self.plot_cb_visible = True

    def update_value(self, new_value):
        """Aggiorna il testo visualizzato nell'etichetta del valore."""
        try:
            if self.winfo_exists(): # Verifica che il widget non sia stato distrutto
                self.value_label.configure(text=new_value)
                
                # Se la checkbox non è ancora visibile, proviamo a capire se è una variabile numerica
                if not self.plot_cb_visible and new_value.strip() and new_value != "--":
                    try:
                        # Rimuove simboli non numerici per il test di conversione
                        clean_val = "".join(c for c in new_value if c.isdigit() or c in '.-')
                        if clean_val:
                            float(clean_val)
                            self._show_plot_checkbox()
                    except:
                        pass
        except:
            pass

class JTEApp(ctk.CTk):
    """
    Classe principale dell'applicazione. Eredita da CTk (la finestra principale).
    """
    def __init__(self):
        super().__init__()

        self.title("JTE Serial Debugger")
        self.geometry("1400x900") # Leggermente più grande per il plot
        
        # Configurazione della griglia: la riga 1 ospita il plot
        self.grid_rowconfigure(0, weight=3) # Variabili
        self.grid_rowconfigure(1, weight=2) # Plot
        self.grid_columnconfigure(1, weight=1)

        # Frame di navigazione laterale (Sidebar)
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew") # sticky="nsew" fa sì che occupi tutta l'altezza
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  JTE Interface", 
                                                  compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.pack(pady=(20, 5))
        
        # Etichetta per mostrare la versione o lo stato della connessione
        self.version_label = ctk.CTkLabel(self.navigation_frame, text="Not connected", font=ctk.CTkFont(size=10))
        self.version_label.pack(pady=(0, 20))

        # Variabile Tkinter per gestire la selezione del menu a tendina
        self.port_var = ctk.StringVar(value="Serial port")
        ports = [p.device for p in serial.tools.list_ports.comports()]
        
        # Menu a tendina per le porte seriali
        self.port_menu = ctk.CTkOptionMenu(self.navigation_frame, variable=self.port_var, 
                                          values=ports if ports else ["Nessuna Porta"],
                                          command=self.connect_serial)
        self.port_menu.pack(pady=10, padx=10)

        self.btn_refresh_ports = ctk.CTkButton(self.navigation_frame, text="Refresh", command=self.refresh_ports)
        self.btn_refresh_ports.pack(pady=5, padx=10)

        # Pulsante di Reset fisico (Hard Reset)
        self.btn_reset = ctk.CTkButton(self.navigation_frame, text="Reset", 
                                      fg_color="#A02020", hover_color="#801010",
                                      command=self.perform_reset)
        self.btn_reset.pack(pady=5, padx=10)

        # Pulsante Disconnetti
        self.btn_disconnect = ctk.CTkButton(self.navigation_frame, text="Close Connection", 
                                           fg_color="#444444", hover_color="#333333",
                                           command=self.disconnect)
        self.btn_disconnect.pack(pady=5, padx=10)

        # Sezione TCP per ESP32 WiFi
        ctk.CTkLabel(self.navigation_frame, text="WiFi Bridge", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 0))
        self.tcp_ip_var = ctk.StringVar(value="192.168.1.15") # Valore di default indicativo
        self.tcp_entry = ctk.CTkEntry(self.navigation_frame, textvariable=self.tcp_ip_var, placeholder_text="IP ESP32")
        self.tcp_entry.pack(pady=5, padx=10)
        
        self.btn_connect_tcp = ctk.CTkButton(self.navigation_frame, text="Connect WiFi Bridge", 
                                            command=lambda: self.connect_serial(self.tcp_ip_var.get(), is_tcp=True))
        self.btn_connect_tcp.pack(pady=5, padx=10)

        self.table_buttons = [] # Lista per tenere traccia dei pulsanti delle tabelle creati dinamicamente
        self.table_btns_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        self.table_btns_frame.pack(fill="both", expand=True)

        # Frame principale con scroll (per le variabili)
        self.home_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew")

        self.jte_comm = None
        self.running = False
        self.var_rows = {} # Dizionario per mappare l'indice della variabile al suo widget VariableRow
        self.current_table_idx = -1
        
        # Dati per il plotting
        self.plot_data = {} # idx -> deque dei valori
        self.plot_max_reached = {} # idx -> valore massimo storico per normalizzazione
        self.plotted_indices = set()
        self.max_points = 200 # Lunghezza dell'asse X (punti visibili)

        # Area Plot (Oscilloscopio)
        self.plot_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        self.plot_container.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        self.init_plot()
        
        # Gestisce la chiusura pulita dell'applicazione
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def refresh_ports(self):
        """Rileva le porte seriali disponibili e aggiorna il menu."""
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu.configure(values=ports if ports else ["Nessuna Porta"])

    def connect_serial(self, port, is_tcp=False):
        """Inizializza la comunicazione (seriale o TCP) sulla porta selezionata."""
        if port == "Nessuna Porta" or not port: return
        self.disconnect()
        
        try:
            self.version_label.configure(text=f"Connessione {'TCP' if is_tcp else 'Seriale'}...", text_color="orange")
            
            if is_tcp:
                # Crea il bridge TCP
                bridge = TCPSerialBridge(port, port=9000)
                if not bridge.open():
                    raise Exception(f"Impossibile connettersi a {port}:9000")
                self.jte_comm = JTEProtocol(bridge)
            else:
                self.jte_comm = JTEProtocol(port)
                
            self.jte_comm.init_comm()
            
            self.running = True
            # Avvia il thread di comunicazione separato per non bloccare la GUI
            threading.Thread(target=self.comm_thread, daemon=True).start()
            
            # Mostra subito le tabelle caricate durante init_comm
            if self.winfo_exists():
                self.after(100, self.update_table_buttons)
            
        except Exception as e:
            self.version_label.configure(text=f"Errore: {str(e)}", text_color="red")
            print(f"Error connecting: {e}")

    def disconnect(self):
        """Chiude la comunicazione attuale e pulisce l'interfaccia."""
        self.running = False
        if self.jte_comm:
            self.jte_comm.close()
            self.jte_comm = None
        
        # Pulisce l'interfaccia
        self.version_label.configure(text="Disconnesso", text_color="gray")
        self.current_table_idx = -1
        self.table_buttons = []
        for child in self.table_btns_frame.winfo_children():
            child.destroy()
        for child in self.home_frame.winfo_children():
            child.destroy()
        self.var_rows = {}
        self.clear_plot_data()

    def select_table(self, idx):
        """Comanda al protocollo di cambiare tabella e pulisce l'interfaccia."""
        if not self.jte_comm: return
        self.var_rows = {}
        # Distrugge tutti i widget figli del frame home per pulire lo schermo
        for child in self.home_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(self.home_frame, text="Caricamento variabili...").pack(pady=20)
        
        self.jte_comm.select_table(idx)
        self.update_table_buttons() # Aggiorna i colori dei pulsanti
        self.clear_plot_data() # ripulisce i dati nel plot

    def perform_reset(self):
        """Esegue il reset hardware e pulisce l'interfaccia."""
        if not self.jte_comm: return
        self.version_label.configure(text="Reset in corso...", text_color="orange")
        # Svuota l'interfaccia
        for child in self.home_frame.winfo_children():
            child.destroy()
        self.var_rows = {}
        
        # Esegue reset tramite protocollo
        self.jte_comm.hard_reset()
        
        # Aggiorna la lista tabelle (che potrebbero essere cambiate o ricaricate)
        self.update_table_buttons()
        self.clear_plot_data()

    def init_plot(self):
        """Inizializza la figura Matplotlib inserendola nel contenitore Tkinter."""
        self.fig, self.ax = plt.subplots(figsize=(5, 2), dpi=100)
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax.set_facecolor('#0d0d0d')
        self.ax.tick_params(colors='gray', labelsize=8)
        self.ax.grid(color='#333333', linestyle='--', alpha=0.5)
        self.ax.set_ylim(-0.1, 1.1) # Normalizzato 0-1 (con piccolo margine)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Loop di aggiornamento grafico
        self.update_plot_loop()

    def toggle_plot_variable(self, idx, is_active):
        """Attiva/Disattiva il monitoraggio di una variabile nel grafico."""
        if is_active:
            self.plotted_indices.add(idx)
            if idx not in self.plot_data:
                self.plot_data[idx] = deque([0.0] * self.max_points, maxlen=self.max_points)  
                self.plot_max_reached[idx] = 1.0 # Default iniziale
        else:
            if idx in self.plotted_indices:
                self.plotted_indices.remove(idx)

    def clear_plot_data(self):
        """Resetta i dati accumulati nel grafico e pulisce l'area visiva."""
        self.plot_data = {}
        self.plot_max_reached = {}
        self.plotted_indices.clear()
        
        # Pulisce visivamente il grafico immediatamente
        self.ax.clear()
        self.ax.set_facecolor('#0d0d0d')
        self.ax.grid(color='#333333', linestyle='--', alpha=0.5)
        self.ax.set_ylim(-0.05, 1.05)
        self.canvas.draw_idle()

    def update_plot_loop(self):
        """Aggiorna il grafico periodicamente."""
        if not self.winfo_exists():
            return

        if self.running and self.plotted_indices:
            self.ax.clear()
            self.ax.set_facecolor('#0d0d0d')
            self.ax.grid(color='#333333', linestyle='--', alpha=0.5)
            self.ax.set_ylim(-0.05, 1.05)
            
            for idx in self.plotted_indices:
                data = list(self.plot_data.get(idx, [0.0]))
                m = self.plot_max_reached.get(idx, 1.0)
                if m == 0: m = 1.0
                norm_data = [v / m for v in data]
                
                var_name = "Var " + str(idx)
                for v in self.jte_comm.variables:
                    if v['index'] == idx:
                        var_name = v['name']
                        break
                
                self.ax.plot(norm_data, label=f"{var_name} (max:{m})")
            
            if self.plotted_indices:
                self.ax.legend(loc="upper left", fontsize=8, facecolor='#1a1a1a', labelcolor='white')
            
            self.canvas.draw_idle()
            
        # Schedula il prossimo aggiornamento finché la finestra esiste
        if self.winfo_exists():
            self.after(50, self.update_plot_loop)

    def on_closing(self):
        """Gestisce la chiusura sicura dell'applicazione."""
        self.running = False
        if self.jte_comm:
            self.jte_comm.close()
        
        # Ferma il mainloop e distrugge la finestra
        self.quit()
        try:
            self.destroy()
        except:
            pass

    def modify_variable(self, idx, action):
        """Invia un comando di modifica variabile tramite il protocollo."""
        if self.jte_comm:
            self.jte_comm.modify_var(idx, action)

    def comm_thread(self):
        """
        Thread dedicato alla comunicazione seriale.
        Cicla continuamente per leggere dati e richiedere aggiornamenti.
        """
        last_request_time = 0
        last_values_time = 0
        waiting_for_values = False
        
        while self.running:
            try:
                if self.jte_comm:
                    # Legge pacchetti in arrivo
                    res = self.jte_comm.sync()
                    
                    if not self.running: break
                    
                    # Usa self.after(0, ...) per chiedere alla GUI principale di eseguire aggiornamenti
                    # Questo perché Tkinter non è thread-safe: solo il thread principale può toccare i widget.
                    if res == "TABLES_LOADED":
                        if self.jte_comm.tables:
                            print("Auto-selezione Tabella 0...")
                            self.after(0, lambda: self.select_table(0))
                    elif res == "TABLE_UPDATED":
                        self.after(0, self.rebuild_ui)
                        waiting_for_values = False # Reset stato dopo cambio tabella
                    elif res == "VALUES_UPDATED":
                         self.after(0, self.update_ui_values)
                         last_values_time = time.time()
                         waiting_for_values = False # Segnala che abbiamo finito di ricevere
                    elif res == "NEW_TABLE":
                        self.after(0, self.update_table_buttons)
                    elif res == "VERSION_UPDATED":
                        self.after(0, self.update_table_buttons)
                    
                    now = time.time()
                    time_since_last_tx = now - self.jte_comm.last_tx_time
                    
                    # Logica di Keep-Alive e Polling
                    if time_since_last_tx > 2.8:
                        self.jte_comm.wake_up()
                        waiting_for_values = False
                        
                    # 2. Richiesta valori SEQUENZIALE (Chain-polling)
                    elif (self.jte_comm.current_table_index != -1 and not self.jte_comm.is_loading):
                        # Condizioni per nuovo invio:
                        # - Non stiamo già aspettando una risposta (waiting_for_values è False)
                        # - OPPURE è passato troppo tempo dall'ultima richiesta (timeout 1s per sicurezza)
                        # - E sono passati almeno 50ms dall'ultima ricezione completa
                        timeout_per_sicurezza = (now - last_request_time > 1.0)
                        ritardo_post_ricezione = (now - last_values_time > 0.05)
                        
                        if (not waiting_for_values or timeout_per_sicurezza) and ritardo_post_ricezione:
                            self.jte_comm.request_values()
                            last_request_time = now
                            waiting_for_values = True
                        
                    # 3. KEEP ALIVE (se non siamo in una tabella)
                    elif self.jte_comm.current_table_index == -1 and time_since_last_tx > 1.5:
                        self.jte_comm.request_values()
                        
                time.sleep(0.01) # Piccola pausa per non saturare la CPU
            except Exception as e:
                print(f"Comm error: {e}")
                break

    def update_table_buttons(self):
        """Crea dinamicamente i pulsanti per le tabelle nella barra laterale."""
        if not self.jte_comm or not self.winfo_exists(): return
        for btn in self.table_buttons:
            btn.destroy()
        self.table_buttons = []
        for table in self.jte_comm.tables:
            is_active = (table['index'] == self.jte_comm.current_table_index)
            # Creazione pulsante con colori diversi se attivo
            btn = ctk.CTkButton(self.table_btns_frame, text=table['name'], 
                                fg_color="gray30" if is_active else "transparent",
                                text_color=("gray10", "gray90") if not is_active else "white",
                                hover_color=("gray70", "gray30"), anchor="w",
                                command=lambda t=table: self.select_table(t['index']))
            btn.pack(fill="x", padx=10, pady=2)
            self.table_buttons.append(btn)
        
        if self.jte_comm.version:
            self.version_label.configure(text=f"Ver: {self.jte_comm.version}", text_color="green")

    def rebuild_ui(self):
        """Costruisce integralmente la lista di widget per le variabili della tabella corrente."""
        if not self.jte_comm or not self.winfo_exists(): return                                # Se non c'è protocollo, non fare nulla
        # Refresh UI
        for child in self.home_frame.winfo_children():              # Rimuove tutti i widget figli
            child.destroy()
        
        self.var_rows = {}                                          # Reset del dizionario delle righe
        for var in self.jte_comm.variables:                         # Per ogni variabile nella tabella corrente
            is_plotted = var['index'] in self.plotted_indices
            row = VariableRow(self.home_frame, var, self.modify_variable, self.toggle_plot_variable, 
                             is_plotted=is_plotted, fg_color="transparent") # Crea un widget VariableRow per ogni variabile ricevuta
            row.pack(fill="x", padx=5, pady=0)                      # Aggiunge la riga al frame
            self.var_rows[var['index']] = row                       # Aggiunge la riga al dizionario
            
            # Aggiunge una sottile linea di separazione (bordo) tra le righe
            separator = ctk.CTkFrame(self.home_frame, height=2, fg_color="gray25", border_width=0)# Crea un frame per la linea di separazione
            separator.pack(fill="x", padx=20, pady=(0, 2))           # Aggiunge la linea di separazione al frame

    def update_ui_values(self):
        """Aggiorna solo i valori numerici nell'interfaccia senza ricostruirla."""
        if not self.jte_comm or not self.winfo_exists(): return                                # Se non c'è protocollo, non fare nulla
        for var in self.jte_comm.variables:                         # Per ogni variabile nella tabella corrente
            idx = var['index']
            val_str = var['value']
            
            # Aggiorna widget
            row = self.var_rows.get(idx)
            if row:
                row.update_value(val_str)
            
            # Accumula dati per il plot se attivo
            if idx in self.plotted_indices:
                try:
                    # Rimuove eventuali unità o simboli spuri per convertire in float
                    clean_val = "".join(c for c in val_str if c.isdigit() or c in '.-')
                    v = float(clean_val)
                    if idx not in self.plot_data:
                        self.plot_data[idx] = deque([0.0] * self.max_points, maxlen=self.max_points)
                        self.plot_max_reached[idx] = abs(v) if abs(v) > 0 else 1.0
                    
                    self.plot_data[idx].append(v)
                    # Aggiorna il massimo relativo (in valore assoluto per gestire negativi)
                    self.plot_max_reached[idx] = max(self.plot_max_reached[idx], abs(v))
                except (ValueError, TypeError):
                    pass

if __name__ == "__main__":
    # Avvio dell'applicazione
    app = JTEApp()
    app.mainloop() # Questo blocca l'esecuzione qui finché la finestra non viene chiusa
