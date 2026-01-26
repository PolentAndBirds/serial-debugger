
import customtkinter as ctk # CustomTkinter è una libreria basata su Tkinter con un'estetica moderna
import serial.tools.list_ports
from jte_protocol import JTEProtocol
import threading
import time

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
    Eredita da CTkFrame, quindi è un contenitore che al suo interno ha etichette e pulsanti.
    """
    def __init__(self, master, var_data, on_modify, **kwargs):
        super().__init__(master, **kwargs)
        self.var_data = var_data
        self.on_modify = on_modify # Funzione da chiamare quando si preme un pulsante
        
        # Etichetta Nome: anchor="w" allinea il testo a sinistra (West)
        # Font in grassetto se la variabile è di tipo '0' (presumibilmente un titolo o costante)
        self.name_label = ctk.CTkLabel(self, text=var_data['name'], width=200, anchor="w", 
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

    def update_value(self, new_value):
        """Aggiorna il testo visualizzato nell'etichetta del valore."""
        try:
            if self.winfo_exists(): # Verifica che il widget non sia stato distrutto
                self.value_label.configure(text=new_value)
        except:
            pass

class JTEApp(ctk.CTk):
    """
    Classe principale dell'applicazione. Eredita da CTk (la finestra principale).
    """
    def __init__(self):
        super().__init__()

        self.title("JTE Serial Debugger")
        self.geometry("1200x800")
        
        # Configurazione della griglia: la colonna 1 (destra) si espanderà per occupare lo spazio
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Frame di navigazione laterale (Sidebar)
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew") # sticky="nsew" fa sì che occupi tutta l'altezza
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  JTE Interface", 
                                                  compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.pack(pady=(20, 5))
        
        # Etichetta per mostrare la versione o lo stato della connessione
        self.version_label = ctk.CTkLabel(self.navigation_frame, text="Disconnesso", font=ctk.CTkFont(size=10))
        self.version_label.pack(pady=(0, 20))

        # Variabile Tkinter per gestire la selezione del menu a tendina
        self.port_var = ctk.StringVar(value="Seleziona Porta")
        ports = [p.device for p in serial.tools.list_ports.comports()]
        
        # Menu a tendina per le porte seriali
        self.port_menu = ctk.CTkOptionMenu(self.navigation_frame, variable=self.port_var, 
                                          values=ports if ports else ["Nessuna Porta"],
                                          command=self.connect_serial)
        self.port_menu.pack(pady=10, padx=10)

        self.btn_refresh_ports = ctk.CTkButton(self.navigation_frame, text="Aggiorna Porte", command=self.refresh_ports)
        self.btn_refresh_ports.pack(pady=5, padx=10)

        # Pulsante di Reset fisico (Hard Reset)
        self.btn_reset = ctk.CTkButton(self.navigation_frame, text="Reset Board", 
                                      fg_color="#A02020", hover_color="#801010",
                                      command=self.perform_reset)
        self.btn_reset.pack(pady=5, padx=10)

        self.table_buttons = [] # Lista per tenere traccia dei pulsanti delle tabelle creati dinamicamente
        self.table_btns_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        self.table_btns_frame.pack(fill="both", expand=True)

        # Frame principale con scroll (per le variabili)
        self.home_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        
        self.protocol = None
        self.running = False
        self.var_rows = {} # Dizionario per mappare l'indice della variabile al suo widget VariableRow
        self.current_table_idx = -1

    def refresh_ports(self):
        """Rileva le porte seriali disponibili e aggiorna il menu."""
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu.configure(values=ports if ports else ["Nessuna Porta"])

    def connect_serial(self, port):
        """Inizializza la comunicazione seriale sulla porta selezionata."""
        if port == "Nessuna Porta": return
        if self.protocol:
            self.running = False
            time.sleep(0.2)
            self.protocol.close()
            
        try:
            self.version_label.configure(text="Connessione in corso...", text_color="orange")
            self.protocol = JTEProtocol(port)
            self.protocol.init_comm()
            
            self.running = True
            # Avvia il thread di comunicazione separato per non bloccare la GUI
            threading.Thread(target=self.comm_thread, daemon=True).start()
            
            # Mostra subito le tabelle caricate durante init_comm
            self.after(100, self.update_table_buttons)
            
        except Exception as e:
            self.version_label.configure(text=f"Errore: {str(e)}", text_color="red")
            print(f"Error connecting: {e}")

    def select_table(self, idx):
        """Comanda al protocollo di cambiare tabella e pulisce l'interfaccia."""
        if not self.protocol: return
        self.var_rows = {}
        # Distrugge tutti i widget figli del frame home per pulire lo schermo
        for child in self.home_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(self.home_frame, text="Caricamento variabili...").pack(pady=20)
        
        self.protocol.select_table(idx)
        self.update_table_buttons() # Aggiorna i colori dei pulsanti

    def perform_reset(self):
        """Esegue il reset hardware e pulisce l'interfaccia."""
        if not self.protocol: return
        self.version_label.configure(text="Reset in corso...", text_color="orange")
        # Svuota l'interfaccia
        for child in self.home_frame.winfo_children():
            child.destroy()
        self.var_rows = {}
        
        # Esegue reset tramite protocollo
        self.protocol.hard_reset()
        
        # Aggiorna la lista tabelle (che potrebbero essere cambiate o ricaricate)
        self.update_table_buttons()

    def modify_variable(self, idx, action):
        """Invia un comando di modifica variabile tramite il protocollo."""
        if self.protocol:
            self.protocol.modify_var(idx, action)

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
                if self.protocol:
                    # Legge pacchetti in arrivo
                    res = self.protocol.sync()
                    
                    # Usa self.after(0, ...) per chiedere alla GUI principale di eseguire aggiornamenti
                    # Questo perché Tkinter non è thread-safe: solo il thread principale può toccare i widget.
                    if res == "TABLES_LOADED":
                        if self.protocol.tables:
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
                    time_since_last_tx = now - self.protocol.last_tx_time
                    
                    # Logica di Keep-Alive e Polling
                    if time_since_last_tx > 2.8:
                        self.protocol.wake_up()
                        waiting_for_values = False
                        
                    # 2. Richiesta valori SEQUENZIALE (Chain-polling)
                    elif (self.protocol.current_table_index != -1 and not self.protocol.is_loading):
                        # Condizioni per nuovo invio:
                        # - Non stiamo già aspettando una risposta (waiting_for_values è False)
                        # - OPPURE è passato troppo tempo dall'ultima richiesta (timeout 1s per sicurezza)
                        # - E sono passati almeno 50ms dall'ultima ricezione completa
                        timeout_per_sicurezza = (now - last_request_time > 1.0)
                        ritardo_post_ricezione = (now - last_values_time > 0.05)
                        
                        if (not waiting_for_values or timeout_per_sicurezza) and ritardo_post_ricezione:
                            self.protocol.request_values()
                            last_request_time = now
                            waiting_for_values = True
                        
                    # 3. KEEP ALIVE (se non siamo in una tabella)
                    elif self.protocol.current_table_index == -1 and time_since_last_tx > 1.5:
                        self.protocol.request_values()
                        
                time.sleep(0.01) # Piccola pausa per non saturare la CPU
            except Exception as e:
                print(f"Comm error: {e}")
                break

    def update_table_buttons(self):
        """Crea dinamicamente i pulsanti per le tabelle nella barra laterale."""
        if not self.protocol: return
        for btn in self.table_buttons:
            btn.destroy()
        self.table_buttons = []
        for table in self.protocol.tables:
            is_active = (table['index'] == self.protocol.current_table_index)
            # Creazione pulsante con colori diversi se attivo
            btn = ctk.CTkButton(self.table_btns_frame, text=table['name'], 
                                fg_color="gray30" if is_active else "transparent",
                                text_color=("gray10", "gray90") if not is_active else "white",
                                hover_color=("gray70", "gray30"), anchor="w",
                                command=lambda t=table: self.select_table(t['index']))
            btn.pack(fill="x", padx=10, pady=2)
            self.table_buttons.append(btn)
        
        if self.protocol.version:
            self.version_label.configure(text=f"Ver: {self.protocol.version}", text_color="green")

    def rebuild_ui(self):
        """Costruisce integralmente la lista di widget per le variabili della tabella corrente."""
        if not self.protocol: return                                # Se non c'è protocollo, non fare nulla
        # Refresh UI
        for child in self.home_frame.winfo_children():              # Rimuove tutti i widget figli
            child.destroy()
        
        self.var_rows = {}                                          # Reset del dizionario delle righe
        for var in self.protocol.variables:                         # Per ogni variabile nella tabella corrente
            row = VariableRow(self.home_frame, var, self.modify_variable, fg_color="transparent") # Crea un widget VariableRow per ogni variabile ricevuta
            row.pack(fill="x", padx=5, pady=0)                      # Aggiunge la riga al frame
            self.var_rows[var['index']] = row                       # Aggiunge la riga al dizionario
            
            # Aggiunge una sottile linea di separazione (bordo) tra le righe
            separator = ctk.CTkFrame(self.home_frame, height=2, fg_color="gray25", border_width=0)# Crea un frame per la linea di separazione
            separator.pack(fill="x", padx=20, pady=(0, 2))           # Aggiunge la linea di separazione al frame

    def update_ui_values(self):
        """Aggiorna solo i valori numerici nell'interfaccia senza ricostruirla."""
        if not self.protocol: return                                # Se non c'è protocollo, non fare nulla
        for var in self.protocol.variables:                         # Per ogni variabile nella tabella corrente
            row = self.var_rows.get(var['index'])                   # Ottiene la riga corrispondente all'indice della variabile
            if row:                                                 # Se la riga esiste
                row.update_value(var['value'])                      # Aggiorna il valore della riga

if __name__ == "__main__":
    # Avvio dell'applicazione
    app = JTEApp()
    app.mainloop() # Questo blocca l'esecuzione qui finché la finestra non viene chiusa
