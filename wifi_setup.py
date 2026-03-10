import customtkinter as ctk
import socket
import threading
import time

class WiFiSetupDialog(ctk.CTkToplevel):
    """
    Finestra popup per configurare un nuovo ESP32 in modalità AP (10.255.255.1).
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("ESP32 WiFi Configuration")
        self.geometry("400x480")
        self.attributes("-topmost", True)
        
        ctk.CTkLabel(self, text="Configure ESP32 Bridge", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Connect to ESP32 AP first (IP: 10.255.255.1)", font=ctk.CTkFont(size=11), text_color="orange").pack(pady=(0, 10))

        # Campi di input
        ctk.CTkLabel(self, text="Device Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(self, width=300)
        self.name_entry.pack(pady=5)

        ctk.CTkLabel(self, text="WiFi SSID:").pack(pady=(10, 0))
        self.ssid_entry = ctk.CTkEntry(self, width=300)
        self.ssid_entry.insert(0, "jte_production")
        self.ssid_entry.pack(pady=5)

        ctk.CTkLabel(self, text="WiFi Password:").pack(pady=(10, 0))
        self.psk_entry = ctk.CTkEntry(self, width=300)
        self.psk_entry.insert(0, "Jasic@123")
        self.psk_entry.pack(pady=5)

        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.pack(pady=10)

        self.btn_save_wifi = ctk.CTkButton(self, text="Save & Reboot ESP32", 
                                          fg_color="#285e28", hover_color="#1e461e",
                                          command=self.send_config)
        self.btn_save_wifi.pack(pady=20)

    def send_config(self):
        name = self.name_entry.get().strip()
        ssid = self.ssid_entry.get().strip()
        psk = self.psk_entry.get().strip()
        
        if not name or not ssid or not psk:
            self.status_label.configure(text="Please fill all fields!", text_color="red")
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
                resp = sock.recv(1024).decode('ascii', errors='ignore')
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
            sock.close()
            self.after(2000, self.destroy)
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}", text_color="red"))
