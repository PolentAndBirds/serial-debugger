import customtkinter as ctk
import socket
import threading
import time
import os

class WiFiSetupDialog(ctk.CTkToplevel):
    """
    Finestra popup per configurare un nuovo ESP32 in modalità AP (10.255.255.1).
    Include funzionalità di scansione WiFi automatica all'apertura.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("ESP32 WiFi Configuration")
        self.geometry("450x700")
        self.attributes("-topmost", True)
        
        # Imposta Icona
        if os.path.exists("icon.ico"):
            self.after(200, lambda: self.iconbitmap("icon.ico"))
        
        ctk.CTkLabel(self, text="Configure ESP32 Bridge", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self, text="Connect to ESP32 AP first (IP: 10.255.255.1)", font=ctk.CTkFont(size=11), text_color="orange").pack(pady=(0, 15))

        # --- Sezione Scansione ---
        scan_frame = ctk.CTkFrame(self, fg_color="transparent")
        scan_frame.pack(fill="x", padx=20)
        
        ctk.CTkLabel(scan_frame, text="Available Networks:", font=ctk.CTkFont(weight="bold")).pack(side="left")
        self.scan_status = ctk.CTkLabel(scan_frame, text="Scanning...", text_color="orange", font=ctk.CTkFont(size=11))
        self.scan_status.pack(side="right")
        
        self.networks_frame = ctk.CTkScrollableFrame(self, width=380, height=180, fg_color="gray20")
        self.networks_frame.pack(pady=5, padx=20)
        
        self.btn_rescan = ctk.CTkButton(self, text="Scan Again", height=24, width=100, font=ctk.CTkFont(size=11),
                                      command=self.start_scan)
        self.btn_rescan.pack(pady=(0, 10))

        # --- Campi di configurazione ---
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=40, pady=10)

        ctk.CTkLabel(form_frame, text="Device Name:", anchor="w").pack(fill="x", pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="es. Bridge-Lab")
        self.name_entry.pack(pady=5)

        ctk.CTkLabel(form_frame, text="WiFi SSID:", anchor="w").pack(fill="x", pady=(10, 0))
        self.ssid_entry = ctk.CTkEntry(form_frame, width=300)
        self.ssid_entry.insert(0, "jte_production")
        self.ssid_entry.pack(pady=5)

        ctk.CTkLabel(form_frame, text="WiFi Password:", anchor="w").pack(fill="x", pady=(10, 0))
        self.psk_entry = ctk.CTkEntry(form_frame, width=300)
        self.psk_entry.insert(0, "Jasic@123")
        self.psk_entry.pack(pady=5)

        self.status_label = ctk.CTkLabel(self, text="", text_color="gray", wraplength=350)
        self.status_label.pack(pady=10)

        self.btn_save_wifi = ctk.CTkButton(self, text="Save & Reboot ESP32", 
                                          fg_color="#285e28", hover_color="#1e461e", height=40,
                                          font=ctk.CTkFont(weight="bold"),
                                          command=self.send_config)
        self.btn_save_wifi.pack(pady=20)

        # Avvio scansione automatica
        self.after(500, self.start_scan)

    def start_scan(self):
        self.scan_status.configure(text="Scanning...", text_color="orange")
        for widget in self.networks_frame.winfo_children():
            widget.destroy()
        threading.Thread(target=self._scan_thread, daemon=True).start()

    def _scan_thread(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect(("10.255.255.1", 9000))
            
            sock.sendall(b"AT+SCAN\r\n")
            
            networks = []
            start_time = time.time()
            buffer = ""
            while time.time() - start_time < 5.0:
                try:
                    data = sock.recv(1024).decode('ascii', errors='ignore')
                    if not data: break
                    buffer += data
                    if "OK" in buffer or "ERROR" in buffer:
                        break
                except socket.timeout:
                    break
            
            sock.close()
            
            # Parsing dei risultati (atteso formato +SCAN:SSID)
            for line in buffer.splitlines():
                if "+SCAN:" in line:
                    ssid = line.split("+SCAN:")[1].strip()
                    if ssid and ssid not in networks:
                        networks.append(ssid)
            
            self.after(0, lambda: self._update_networks_list(networks))
            
        except Exception as e:
            self.after(0, lambda: self.scan_status.configure(text="Device not found (10.255.255.1)", text_color="red"))

    def _update_networks_list(self, networks):
        if not self.winfo_exists(): return
        
        self.scan_status.configure(text=f"Found {len(networks)} networks", text_color="gray")
        
        if not networks:
            ctk.CTkLabel(self.networks_frame, text="No networks found").pack(pady=20)
            return
            
        for ssid in networks:
            btn = ctk.CTkButton(self.networks_frame, text=f"📡 {ssid}", 
                                fg_color="gray25", text_color="white",
                                hover_color="#3a3a3a", anchor="w", height=32,
                                command=lambda s=ssid: self._on_network_selected(s))
            btn.pack(fill="x", padx=5, pady=2)

    def _on_network_selected(self, ssid):
        self.ssid_entry.delete(0, 'end')
        self.ssid_entry.insert(0, ssid)
        # La richiesta dell'utente: "collega con password uguale a SSID"
        self.psk_entry.delete(0, 'end')
        self.psk_entry.insert(0, ssid)
        self.status_label.configure(text=f"Ready to connect to: {ssid}", text_color="green")

    def send_config(self):
        name = self.name_entry.get().strip()
        ssid = self.ssid_entry.get().strip()
        psk = self.psk_entry.get().strip()
        
        if not name or not ssid or not psk:
            self.status_label.configure(text="Please fill all fields or select a network!", text_color="red")
            return

        threading.Thread(target=self._config_thread, args=(name, ssid, psk), daemon=True).start()

    def _config_thread(self, name, ssid, psk):
        try:
            self.after(0, lambda: self.status_label.configure(text="Connecting to 10.255.255.1...", text_color="orange"))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect(("10.255.255.1", 9000))
            
            def send_at(cmd, desc):
                self.after(0, lambda: self.status_label.configure(text=f"Setting {desc}..."))
                sock.sendall(f"{cmd}\r\n".encode('ascii'))
                resp = ""
                start = time.time()
                while time.time() - start < 2.0:
                    try:
                        chunk = sock.recv(1024).decode('ascii', errors='ignore')
                        if not chunk: break
                        resp += chunk
                        if "OK" in resp or "ERROR" in resp: break
                    except: break
                return "OK" in resp

            if not send_at(f"AT+NAME={name}", "Name"):
                raise Exception("Failed to set Name")
            time.sleep(0.5)
            
            if not send_at(f"AT+SSID={ssid}", "SSID"):
                raise Exception("Failed to set SSID")
            time.sleep(0.5)
            
            if not send_at(f"AT+PSK={psk}", "PSK"):
                raise Exception("Failed to set PSK")
            
            self.after(0, lambda: self.status_label.configure(text="Config Saved! ESP32 Rebooting...", text_color="green"))
            
            # Comando di riavvio opzionale se supportato, altrimenti chiudiamo e basta
            sock.sendall(b"AT+RST\r\n") 
            time.sleep(0.5)
            
            sock.close()
            self.after(2000, self.destroy)
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}", text_color="red"))

