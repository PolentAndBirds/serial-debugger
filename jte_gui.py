
import customtkinter as ctk
import serial.tools.list_ports
from jte_protocol import JTEProtocol
import threading
import time

class VariableRow(ctk.CTkFrame):
    def __init__(self, master, var_data, on_modify, **kwargs):
        super().__init__(master, **kwargs)
        self.var_data = var_data
        self.on_modify = on_modify
        
        # Name Label
        self.name_label = ctk.CTkLabel(self, text=var_data['name'], width=200, anchor="w", font=ctk.CTkFont(weight="bold" if var_data['step_type'] == '0' else "normal"))
        self.name_label.pack(side="left", padx=10, pady=5)
        
        # Value Label
        self.value_label = ctk.CTkLabel(self, text="--", width=200, anchor="e")
        self.value_label.pack(side="left", padx=10, pady=5)
        
        # Buttons if modifiable
        if var_data['step_type'] in ['1', '2']:
            self.min_btn = ctk.CTkButton(self, text="-", width=30, command=lambda: self.on_modify(var_data['index'], '-'))
            self.min_btn.pack(side="right", padx=2)
            
            self.plus_btn = ctk.CTkButton(self, text="+", width=30, command=lambda: self.on_modify(var_data['index'], '+'))
            self.plus_btn.pack(side="right", padx=2)
            
            self.dmin_btn = ctk.CTkButton(self, text="--", width=40, command=lambda: self.on_modify(var_data['index'], '/'))
            self.dmin_btn.pack(side="right", padx=2)
            
            self.dplus_btn = ctk.CTkButton(self, text="++", width=40, command=lambda: self.on_modify(var_data['index'], '*'))
            self.dplus_btn.pack(side="right", padx=2)

    def update_value(self, new_value):
        try:
            if self.winfo_exists():
                self.value_label.configure(text=new_value)
        except:
            pass

class JTEApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JTE Serial Debugger")
        self.geometry("1200x800")
        
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode (placeholder for now)
        # self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(26, 26))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  JTE Interface", 
                                                  compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.pack(pady=(20, 5))
        
        self.version_label = ctk.CTkLabel(self.navigation_frame, text="Disconnesso", font=ctk.CTkFont(size=10))
        self.version_label.pack(pady=(0, 20))

        self.port_var = ctk.StringVar(value="Seleziona Porta")
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu = ctk.CTkOptionMenu(self.navigation_frame, variable=self.port_var, 
                                          values=ports if ports else ["Nessuna Porta"],
                                          command=self.connect_serial)
        self.port_menu.pack(pady=10, padx=10)

        self.btn_refresh_ports = ctk.CTkButton(self.navigation_frame, text="Aggiorna Porte", command=self.refresh_ports)
        self.btn_refresh_ports.pack(pady=5, padx=10)

        self.btn_reset = ctk.CTkButton(self.navigation_frame, text="Reset Board", 
                                      fg_color="#A02020", hover_color="#801010",
                                      command=self.perform_reset)
        self.btn_reset.pack(pady=5, padx=10)

        self.table_buttons = []
        self.table_btns_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        self.table_btns_frame.pack(fill="both", expand=True)

        # create home frame
        self.home_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        
        self.protocol = None
        self.running = False
        self.var_rows = {} # index -> VariableRow
        self.current_table_idx = -1

    def refresh_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu.configure(values=ports if ports else ["Nessuna Porta"])

    def connect_serial(self, port):
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
            threading.Thread(target=self.comm_thread, daemon=True).start()
            
            # Mostra subito le tabelle caricate durante init_comm
            self.after(100, self.update_table_buttons)
            
        except Exception as e:
            self.version_label.configure(text=f"Errore: {str(e)}", text_color="red")
            print(f"Error connecting: {e}")

    def select_table(self, idx):
        if not self.protocol: return
        # Feedback immediato: svuota la lista e mostra caricamento
        self.var_rows = {} # Svuota i riferimenti prima di distruggere i widget
        for child in self.home_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(self.home_frame, text="Caricamento variabili...").pack(pady=20)
        
        self.protocol.select_table(idx)
        self.update_table_buttons() # Aggiorna i colori dei pulsanti

    def perform_reset(self):
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
        if self.protocol:
            self.protocol.modify_var(idx, action)

    def comm_thread(self):
        last_request_time = 0
        last_values_time = 0
        waiting_for_values = False
        
        while self.running:
            try:
                if self.protocol:
                    # Legge tutti i pacchetti pendenti nel buffer
                    res = self.protocol.sync()
                    
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
                    
                    # 1. Gestione WAKE UP (se siamo stati inattivi per quasi 3 secondi)
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
                        
                time.sleep(0.01) # Ciclo veloce per svuoto buffer
            except Exception as e:
                print(f"Comm error: {e}")
                break

    def update_table_buttons(self):
        if not self.protocol: return
        for btn in self.table_buttons:
            btn.destroy()
        self.table_buttons = []
        for table in self.protocol.tables:
            is_active = (table['index'] == self.protocol.current_table_index)
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
        if not self.protocol: return
        # Refresh UI
        for child in self.home_frame.winfo_children():
            child.destroy()
        
        self.var_rows = {}
        for var in self.protocol.variables:
            row = VariableRow(self.home_frame, var, self.modify_variable, fg_color="transparent")
            row.pack(fill="x", padx=5, pady=1)
            self.var_rows[var['index']] = row

    def update_ui_values(self):
        if not self.protocol: return
        for var in self.protocol.variables:
            row = self.var_rows.get(var['index'])
            if row:
                row.update_value(var['value'])

if __name__ == "__main__":
    app = JTEApp()
    app.mainloop()
