
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
import json
import os
import socket
from tkinter import filedialog, messagebox

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
        
        # Etichetta per mostrare la versione o lo stato della connessione
        self.version_label = ctk.CTkLabel(self.navigation_frame, text="Not connected", font=ctk.CTkFont(size=12))
        self.version_label.pack(pady=(0, 10))

        # Variabile Tkinter per gestire la selezione del menu a tendina
        self.port_var = ctk.StringVar(value="Serial port")
        ports = [p.device for p in serial.tools.list_ports.comports()]
        
        # Riga Seriale: Dropdown + Refresh
        serial_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        serial_frame.pack(pady=5, padx=10, fill="x")
        
        self.port_menu = ctk.CTkOptionMenu(serial_frame, variable=self.port_var, 
                                          values=ports if ports else ["Nessuna Porta"],
                                          command=self.connect_serial, width=140)
        self.port_menu.pack(side="left", padx=(0, 5))
        self.port_menu.bind("<Button-1>", lambda e: self.refresh_ports()) # Auto-refresh al click

        self.btn_refresh_ports = ctk.CTkButton(serial_frame, text="🔄", width=30, 
                                              command=self.refresh_ports)
        self.btn_refresh_ports.pack(side="left")

        # Riga Azioni: Reset + Close
        actions_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        actions_frame.pack(pady=5, padx=10, fill="x")
        
        self.btn_reset = ctk.CTkButton(actions_frame, text="⚡ Reset", fg_color="#A02020", 
                                      hover_color="#801010", command=self.perform_reset, width=85)
        self.btn_reset.pack(side="left", padx=(0, 5))

        self.btn_disconnect = ctk.CTkButton(actions_frame, text="🚫 Close", fg_color="#444444", 
                                           hover_color="#333333", command=self.disconnect, width=85)
        self.btn_disconnect.pack(side="left")

        # Carica IP salvati
        self.config_file = "config.json"
        config = self.load_config()
        self.wifi_devices = config.get("wifi_devices", {"192.168.50.100": "Default"})
        
        # Sezione WiFi aggiornata con Dropdown e Scan
        ctk.CTkLabel(self.navigation_frame, text="WiFi Bridge", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 0))
        # Prepariamo la lista per il dropdown: "Nome (IP)"
        self.wifi_display_list = [f"{name} ({ip})" for ip, name in self.wifi_devices.items()]
        self.tcp_device_var = ctk.StringVar(value=self.wifi_display_list[0] if self.wifi_display_list else "")
        
        # Riga WiFi: Dropdown + Scan
        wifi_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        wifi_frame.pack(pady=5, padx=10, fill="x")
        
        self.tcp_menu = ctk.CTkOptionMenu(wifi_frame, variable=self.tcp_device_var, 
                                         values=self.wifi_display_list if self.wifi_display_list else ["No devices"],
                                         command=self.on_connect_wifi_click, width=140)
        self.tcp_menu.pack(side="left", padx=(0, 5))
        self.tcp_menu.bind("<Button-1>", lambda e: self.start_scan()) # Auto-scan al click

        self.btn_scan_tcp = ctk.CTkButton(wifi_frame, text="🔍", width=30, 
                                         fg_color="#1f538d", hover_color="#14375e",
                                         command=self.start_scan)
        self.btn_scan_tcp.pack(side="left")

        self.btn_setup_wifi = ctk.CTkButton(self.navigation_frame, text="⚙️ Setup New Bridge", 
                                           fg_color="#285e28", hover_color="#1e461e",
                                           command=self.open_wifi_setup)
        self.btn_setup_wifi.pack(pady=5, padx=10, fill="x")

        # Sezione Firmware Update
        ctk.CTkLabel(self.navigation_frame, text="Firmware", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0))
        self.hex_path_var = ctk.StringVar(value="")
        self.btn_select_hex = ctk.CTkButton(self.navigation_frame, text="📁 Select HEX", 
                                           fg_color="gray30", command=self.select_hex_file)
        self.btn_select_hex.pack(pady=5, padx=10, fill="x")
        
        self.stm32_model_var = ctk.StringVar(value="F303")
        # Riga Flash: Model + Flash + Format
        flash_row = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        flash_row.pack(pady=5, padx=10, fill="x")
        
        self.stm32_model_menu = ctk.CTkOptionMenu(flash_row, variable=self.stm32_model_var,
                                                 values=["F303", "G474"], width=65)
        self.stm32_model_menu.pack(side="left", padx=(0, 5))
        
        self.btn_flash = ctk.CTkButton(flash_row, text="🚀 Flash", width=55,
                                      fg_color="#A0522D", hover_color="#8B4513",
                                      command=self.start_file_transfer)
        self.btn_flash.pack(side="left", padx=(0, 5))

        self.btn_format = ctk.CTkButton(flash_row, text="🧹 Format", width=55,
                                       fg_color="#555555", hover_color="#333333",
                                       command=self.start_format_spiffs)
        self.btn_format.pack(side="left")

        # Nuova riga per azioni singole: Upload e Flash Only
        single_flash_row = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        single_flash_row.pack(pady=5, padx=10, fill="x")

        self.btn_upload_only = ctk.CTkButton(single_flash_row, text="📤 Upload Only", width=90,
                                            fg_color="#4682B4", hover_color="#36648B",
                                            command=lambda: self.start_file_transfer(mode="upload"))
        self.btn_upload_only.pack(side="left", padx=(0, 5), expand=True, fill="x")

        self.btn_flash_only = ctk.CTkButton(single_flash_row, text="🔥 Flash Only", width=90,
                                           fg_color="#CD5C5C", hover_color="#B22222",
                                           command=lambda: self.start_file_transfer(mode="flash"))
        self.btn_flash_only.pack(side="left", expand=True, fill="x")
        
        # Barra di progresso per il caricamento
        self.progress_bar = ctk.CTkProgressBar(self.navigation_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5, padx=10, fill="x")
        self.progress_label = ctk.CTkLabel(self.navigation_frame, text="Ready", font=ctk.CTkFont(size=10))
        self.progress_label.pack(pady=(0, 10))

        self.table_buttons = [] # Lista per tenere traccia dei pulsanti delle tabelle creati dinamicamente
        self.table_btns_frame = ctk.CTkScrollableFrame(self.navigation_frame, fg_color="transparent", label_text="Tables")
        self.table_btns_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame principale con scroll (per le variabili)
        self.home_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew")

        self.jte_comm = None
        self.running = False
        self.is_suspended = False
        self.connected_ip = None
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

        # Stato iniziale pulsanti
        self.update_action_buttons_state()

    def refresh_ports(self):
        """Rileva le porte seriali disponibili e aggiorna il menu."""
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu.configure(values=ports if ports else ["Nessuna Porta"])

    def on_connect_wifi_click(self, selection):
        # Estrae l'IP dalla stringa "Nome (IP)"
        if "(" in selection and ")" in selection:
            ip = selection.split("(")[1].split(")")[0]
            self.connected_ip = ip
            self.connect_serial(ip, is_tcp=True)

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
            
            self.update_table_buttons()
            
            self.running = True
            # Avvia il thread di comunicazione separato per non bloccare la GUI
            threading.Thread(target=self.comm_thread, daemon=True).start()
            self.update_action_buttons_state()
            
        except Exception as e:
            self.version_label.configure(text=f"Errore: {str(e)}", text_color="red")
            print(f"Error connecting: {e}")
            self.running = False
            self.update_action_buttons_state()

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
        self.update_action_buttons_state()

    def update_action_buttons_state(self, loading=False):
        """Abilita o disabilita i pulsanti in base allo stato della connessione."""
        state = "normal" if self.running and not loading else "disabled"
        self.btn_disconnect.configure(state=state)
        self.btn_flash.configure(state=state)
        self.btn_format.configure(state=state)
        self.btn_reset.configure(state=state)
        if hasattr(self, 'btn_upload_only'):
            self.btn_upload_only.configure(state=state)
        if hasattr(self, 'btn_flash_only'):
            self.btn_flash_only.configure(state=state)

    def pause_bridge(self):
        """Sospende temporaneamente la comunicazione senza pulire la UI."""
        self.is_suspended = True
        if self.jte_comm:
            self.jte_comm.close() # Chiude socket/seriale

    def resume_bridge(self):
        """Riprende la comunicazione precedentemente sospesa."""
        if self.connected_ip:
            self.connect_serial(self.connected_ip, is_tcp=True)
        self.is_suspended = False

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except: pass
        return {}

    def save_config(self):
        config = {"wifi_devices": self.wifi_devices}
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f)
        except: pass

    def start_scan(self):
        self.btn_scan_tcp.configure(text="...", state="disabled")
        threading.Thread(target=self.scan_network_thread, daemon=True).start()

    def scan_network_thread(self):
        found_devices = {} # IP -> Name
        try:
            # Ottieni IP locale per determinare la subnet
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            prefix = ".".join(local_ip.split(".")[:-1]) + "."
            
            threads = []
            def check_ip(ip):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, 9000))
                    if result == 0:
                        # Prova a chiedere il nome
                        sock.sendall(b"AT+NAME?\r\n")
                        # Aspetta una risposta breve (es: "+NAME=PARIS OK")
                        raw_name = sock.recv(64).decode('ascii', errors='ignore').strip()
                        
                        name_resp = ""
                        if "+NAME=" in raw_name:
                            # Estrae la parte dopo "+NAME=" e prende solo fino al primo ritorno a capo
                            name_resp = raw_name.split("+NAME=")[1].split("\r")[0].split("\n")[0].strip()
                        
                        if not name_resp or "AT+" in name_resp:
                            name_resp = "ESP32-Bridge"
                        found_devices[ip] = name_resp
                    sock.close()
                except: pass

            for i in range(1, 255):
                t = threading.Thread(target=check_ip, args=(prefix + str(i),))
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()
                
        except Exception as e:
            print(f"Scan error: {e}")
        
        # Aggiorna UI
        self.after(0, lambda: self.finish_scan(found_devices))

    def finish_scan(self, found_devices):
        self.btn_scan_tcp.configure(text="🔍", state="normal")
        
        # Aggiorniamo wifi_devices in modo non distruttivo (manteniamo quello connesso)
        new_devices = found_devices.copy()
        for ip, name in self.wifi_devices.items():
            if ip not in new_devices:
                # Se è quello a cui siamo connessi, lo teniamo forzatamente
                if ip == self.connected_ip:
                    new_devices[ip] = name
        
        self.wifi_devices = new_devices
        self.wifi_display_list = [f"{name} ({ip})" for ip, name in self.wifi_devices.items()]
        
        if not self.wifi_display_list:
            self.tcp_menu.configure(values=["No devices found"])
            self.tcp_device_var.set("No devices found")
        else:
            self.tcp_menu.configure(values=self.wifi_display_list)
            
            # Manteniamo la selezione sull'IP connesso se possibile
            target_ip = self.connected_ip if self.connected_ip else None
            
            new_selection = None
            for item in self.wifi_display_list:
                if target_ip and f"({target_ip})" in item:
                    new_selection = item
                    break
            
            if new_selection:
                self.tcp_device_var.set(new_selection)
            elif self.wifi_display_list:
                # Altrimenti lasciamo quello che c'era se è ancora valido, o il primo
                curr = self.tcp_device_var.get()
                if curr not in self.wifi_display_list:
                    self.tcp_device_var.set(self.wifi_display_list[0])
        
        self.save_config()

    def open_wifi_setup(self):
        """Apre una finestra popup per configurare un nuovo ESP32 in modalità AP (10.255.255.1)."""
        setup_win = ctk.CTkToplevel(self)
        setup_win.title("ESP32 WiFi Configuration")
        setup_win.geometry("400x480")
        setup_win.attributes("-topmost", True)
        
        ctk.CTkLabel(setup_win, text="Configure ESP32 Bridge", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        ctk.CTkLabel(setup_win, text="Connect to ESP32 AP first (IP: 10.255.255.1)", font=ctk.CTkFont(size=11), text_color="orange").pack(pady=(0, 10))

        # Campi di input
        ctk.CTkLabel(setup_win, text="Device Name:").pack(pady=(10, 0))
        name_entry = ctk.CTkEntry(setup_win, width=300)
        name_entry.pack(pady=5)

        ctk.CTkLabel(setup_win, text="WiFi SSID:").pack(pady=(10, 0))
        ssid_entry = ctk.CTkEntry(setup_win, width=300)
        ssid_entry.insert(0, "jte_production")
        ssid_entry.pack(pady=5)

        ctk.CTkLabel(setup_win, text="WiFi Password:").pack(pady=(10, 0))
        psk_entry = ctk.CTkEntry(setup_win, width=300)
        psk_entry.insert(0, "Jasic@123")
        psk_entry.pack(pady=5)

        status_label = ctk.CTkLabel(setup_win, text="", text_color="gray")
        status_label.pack(pady=10)

        def send_config():
            name = name_entry.get().strip()
            ssid = ssid_entry.get().strip()
            psk = psk_entry.get().strip()
            
            if not name or not ssid or not psk:
                status_label.configure(text="Please fill all fields!", text_color="red")
                return

            def config_thread():
                try:
                    self.after(0, lambda: status_label.configure(text="Connecting to 10.255.255.1...", text_color="orange"))
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5.0)
                    sock.connect(("10.255.255.1", 9000))
                    
                    # Funzione helper per inviare e ricevere conferma
                    def send_at(cmd, desc):
                        self.after(0, lambda: status_label.configure(text=f"Setting {desc}..."))
                        sock.sendall(f"{cmd}\r\n".encode('ascii'))
                        resp = sock.recv(1024).decode('ascii', errors='ignore')
                        return "OK" in resp

                    if not send_at(f"AT+NAME={name}\r\n", "Name"):
                        raise Exception("Failed to set Name")
                    time.sleep(0.5)
                    
                    if not send_at(f"AT+SSID={ssid}\r\n", "SSID"):
                        raise Exception("Failed to set SSID")
                    time.sleep(0.5)
                    
                    if not send_at(f"AT+PSK={psk}\r\n", "PSK"):
                        raise Exception("Failed to set PSK")
                    
                    self.after(0, lambda: status_label.configure(text="Config Saved! ESP32 Rebooting...", text_color="green"))
                    sock.close()
                    # Aggiungi l'IP di default alla lista dopo il setup (presumendo che si sposterà su WiFi locale)
                    # Note: L'IP finale dipenderà dal DHCP, ma salviamo il nome per comodità
                    self.after(2000, setup_win.destroy)
                except Exception as e:
                    self.after(0, lambda: status_label.configure(text=f"Error: {str(e)}", text_color="red"))

            threading.Thread(target=config_thread, daemon=True).start()

        self.btn_save_wifi = ctk.CTkButton(setup_win, text="Save & Reboot ESP32", 
                                          fg_color="#285e28", hover_color="#1e461e",
                                          command=send_config)
        self.btn_save_wifi.pack(pady=20)

    def select_hex_file(self):
        """Apre il selettore file per scegliere un file .hex."""
        path = filedialog.askopenfilename(filetypes=[("HEX files", "*.hex"), ("All files", "*.*")])
        if path:
            self.hex_path_var.set(path)
            self.btn_select_hex.configure(text=os.path.basename(path))

    def start_file_transfer(self, mode="both"):
        """Avvia il trasferimento del file HEX in un thread separato."""
        file_path = self.hex_path_var.get()
        if not file_path:
            self.progress_label.configure(text="Select a file first!", text_color="red")
            return
        
        selection = self.tcp_device_var.get()
        if "(" not in selection:
            self.progress_label.configure(text="Select a WiFi device!", text_color="red")
            return
        
        ip = selection.split("(")[1].split(")")[0]
        
        # Disconnetti la comunicazione attuale ma senza pulire UI
        self.pause_bridge()
        
        self.update_action_buttons_state(loading=True)
        threading.Thread(target=self.file_transfer_thread, args=(ip, file_path, mode), daemon=True).start()

    def file_transfer_thread(self, ip, file_path, mode="both"):
        """Logica di trasferimento file (basata sullo script fornito)."""
        port = 9000
        try:
            file_size = os.path.getsize(file_path)
            filename = os.path.basename(file_path)
            
            self.after(0, lambda: self.progress_label.configure(text="Connecting...", text_color="orange"))
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(20)
                s.connect((ip, port))
                
                # --- PARTE UPLOAD ---
                if mode in ["both", "upload"]:
                    s.sendall(f"AT+FSTART={file_size},{filename}\r".encode())
                    
                    response = s.recv(1024).decode(errors='ignore')
                    if "OK" in response:
                        self.after(0, lambda: self.progress_label.configure(text="Uploading...", text_color="cyan"))
                        bytes_sent = 0
                        
                        with open(file_path, "rb") as f:
                            while True:
                                chunk = f.read(4096)
                                if not chunk:
                                    break
                                s.sendall(chunk)
                                bytes_sent += len(chunk)
                                
                                progress = bytes_sent / file_size
                                self.after(0, lambda p=progress: self.progress_bar.set(p))
                                self.after(0, lambda p=progress: self.progress_label.configure(text=f"Uploading: {p*100:.1f}%"))
                                
                                # Piccola pausa per dare respiro a SPIFFS
                                time.sleep(0.005) 
                        
                        self.after(0, lambda: self.progress_label.configure(text="Finalizing Upload...", text_color="orange"))
                        final_response = s.recv(1024).decode(errors='ignore')
                        
                        if "OK" not in final_response:
                            self.after(0, lambda: self.progress_label.configure(text=f"Upload Error: {final_response.strip()}", text_color="red"))
                            return
                            
                        if mode == "upload":
                            self.after(0, lambda: self.progress_label.configure(text="Upload Success!", text_color="green"))
                            self.after(0, lambda: self.progress_bar.set(1.0))
                            return
                    else:
                        self.after(0, lambda: self.progress_label.configure(text=f"Error: {response.strip()}", text_color="red"))
                        return

                # --- PARTE FLASH ---
                if mode in ["both", "flash"]:
                    model = self.stm32_model_var.get()
                    self.after(0, lambda: self.progress_label.configure(text=f"Flashing {model}...", text_color="yellow"))
                    s.sendall(f"AT+STMFLASH={model},{filename}\r".encode())
                    
                    # Il flash può richiedere tempo, leggiamo i progressi in un loop
                    s.settimeout(120) 
                    buffer = ""
                    while True:
                        try:
                            chunk = s.recv(1024).decode(errors='ignore')
                            if not chunk: break
                            buffer += chunk
                            
                            while "\n" in buffer:
                                line, buffer = buffer.split("\n", 1)
                                line = line.strip()
                                if not line: continue
                                
                                if "+PROGRESS:" in line:
                                    try:
                                        perc = int(line.split(":")[1].replace("%", "").strip())
                                        self.after(0, lambda p=perc: self.progress_bar.set(p/100))
                                        self.after(0, lambda p=perc: self.progress_label.configure(text=f"Flashing: {p}%", text_color="yellow"))
                                    except: pass
                                
                                elif "+ERROR: WRONG CHIP" in line:
                                    self.after(0, lambda l=line: self.progress_label.configure(text=f"Error: {l}", text_color="red"))
                                    return
                                
                                elif "+SUCCESS:" in line:
                                    info = line.split(":", 1)[1].strip()
                                    self.after(0, lambda i=info: self.progress_label.configure(text=f"Success: {i}", text_color="green"))
                                    self.after(0, lambda: self.progress_bar.set(1.0))
                                    return
                                    
                                elif "OK" in line and "+SUCCESS" not in line:
                                    pass
                                    
                        except socket.timeout:
                            self.after(0, lambda: self.progress_label.configure(text="Flash Timeout!", text_color="red"))
                            break
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self.progress_label.configure(text=f"Error: {error_msg}", text_color="red"))
        finally:
            self.after(0, lambda: self.update_action_buttons_state(loading=False))
            self.after(2000, self.resume_bridge)

    def start_format_spiffs(self):
        """Avvia la formattazione SPIFFS in un thread separato."""
        selection = self.tcp_device_var.get()
        if "(" not in selection:
            self.progress_label.configure(text="Select a WiFi device!", text_color="red")
            return
        
        ip = selection.split("(")[1].split(")")[0]
        
        if not messagebox.askyesno("Confirm", "This will ERASE all files on ESP32. Continue?"):
            return

        self.pause_bridge() # Sospende senza pulire UI
        self.update_action_buttons_state(loading=True)
        threading.Thread(target=self.format_spiffs_thread, args=(ip,), daemon=True).start()

    def format_spiffs_thread(self, ip):
        """Logica di formattazione SPIFFS. Usa un socket pulito."""
        try:
            self.after(0, lambda: self.progress_label.configure(text="Formatting SPIFFS (Wait...)", text_color="orange"))
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((ip, 9000))
                s.sendall(b"AT+FFMT\r")
                # Aspetta la conferma OK dall'ESP32 prima di chiudere
                response = s.recv(1024).decode(errors='ignore')
                if "OK" not in response:
                    raise Exception(f"Format rejected: {response}")
                
            self.after(0, lambda: self.progress_label.configure(text="Format command sent", text_color="green"))
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self.progress_label.configure(text=f"Error: {error_msg}", text_color="red"))
        finally:
            self.after(0, lambda: self.update_action_buttons_state(loading=False))
            self.after(0, self.resume_bridge) # Ripristina bridge subito dopo format

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
            if self.is_suspended:
                time.sleep(0.5)
                continue
                
            try:
                if self.jte_comm:
                    # Legge pacchetti in arrivo
                    res = self.jte_comm.sync()
                    
                    if not self.running: break
                    
                    # Se abbiamo finito di caricare le tabelle, resettiamo is_loading
                    # (gestito internamente da sync() per le variabili, ma qui per TABLES_LOADED)
                    if res == "TABLES_LOADED":
                        if self.jte_comm.tables:
                            print("Auto-selezione Tabella 0...")
                            self.after(0, lambda: self.select_table(0))
                        self.jte_comm.is_loading = False # FINE sincronizzazione iniziale
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
                        
                    # 3. KEEP ALIVE (solo se già sincronizzati ma inattivi)
                    elif (not self.jte_comm.is_loading and 
                          self.jte_comm.current_table_index != -1 and 
                          time_since_last_tx > 3.0):
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
