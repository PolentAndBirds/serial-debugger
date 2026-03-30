import customtkinter as ctk 
import serial.tools.list_ports
import threading
import time
import os
from tkinter import filedialog, messagebox

# Import moduli estratti
from jte_protocol import JTEProtocol
from tcp_serial_bridge import TCPSerialBridge
from ui_widgets import VariableRow
from wifi_setup import WiFiSetupDialog
from file_manager import FileManager
from plot_manager import PlotManager
from network_scanner import NetworkScanner
from app_config import load_config, save_config

class JTEApp(ctk.CTk):
    """
    Classe principale dell'applicazione.
    """
    def __init__(self):
        super().__init__()

        self.title("JTE Serial Debugger")
        self.geometry("1400x900")
        
        # Configurazione griglia
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(1, weight=1)

        # Stato applicazione
        self.jte_comm = None
        self.running = False
        self.is_suspended = False
        self.connected_ip = None
        self.var_rows = {}
        self.current_table_idx = -1

        # Setup Managers
        self.file_manager = FileManager(self)
        self.network_scanner = NetworkScanner(self)
        
        self.setup_ui()
        
        # Inizializza Plot Manager dopo che plot_container è stato creato
        self.plot_manager = PlotManager(self.plot_container, self)
        self.plot_manager.update_plot()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update_action_buttons_state()

    def setup_ui(self):
        # Sidebar
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        
        self.version_label = ctk.CTkLabel(self.navigation_frame, text="Not connected", font=ctk.CTkFont(size=12))
        self.version_label.pack(pady=(0, 10))

        # --- CONNECTION & CONTROL ---
        ctk.CTkLabel(self.navigation_frame, text="Connection", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0))
        
        # Seriale
        serial_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        serial_frame.pack(pady=5, padx=10, fill="x")
        
        self.port_var = ctk.StringVar(value="Serial port")
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu = ctk.CTkOptionMenu(serial_frame, variable=self.port_var, 
                                          values=ports if ports else ["Nessuna Porta"],
                                          width=100)
        self.port_menu.pack(side="left", padx=(0, 2))

        self.btn_connect_serial = ctk.CTkButton(serial_frame, text="▶", width=35, 
                                               command=lambda: self.connect_serial(self.port_var.get()))
        self.btn_connect_serial.pack(side="left", padx=(0, 2))

        self.btn_refresh_ports = ctk.CTkButton(serial_frame, text="↻", width=30, command=self.refresh_ports)
        self.btn_refresh_ports.pack(side="left")

        # WiFi
        self.config_file = "config.json"
        config = load_config(self.config_file)
        self.wifi_devices = config.get("wifi_devices", {"192.168.50.100": "Default"})
        
        self.wifi_display_list = [f"{name} ({ip})" for ip, name in self.wifi_devices.items()]
        self.tcp_device_var = ctk.StringVar(value=self.wifi_display_list[0] if self.wifi_display_list else "")
        
        wifi_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        wifi_frame.pack(pady=5, padx=10, fill="x")
        
        self.tcp_menu = ctk.CTkOptionMenu(wifi_frame, variable=self.tcp_device_var, 
                                         values=self.wifi_display_list if self.wifi_display_list else ["No devices"],
                                         command=self.on_connect_wifi_click, width=140)
        self.tcp_menu.pack(side="left", padx=(0, 5))
        self.tcp_menu.bind("<Button-1>", lambda e: self.start_scan())

        self.btn_scan_tcp = ctk.CTkButton(wifi_frame, text="Scan", width=30, command=self.start_scan)
        self.btn_scan_tcp.pack(side="left")

        self.btn_setup_wifi = ctk.CTkButton(wifi_frame, text="Setup Bridge", width=85, command=self.open_wifi_setup)
        self.btn_setup_wifi.pack(side="right", padx=(0, 5))

        # System Actions (Setup, Reset, Close)
        sys_actions_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        sys_actions_frame.pack(pady=5, padx=10, fill="x")

        

        self.btn_reset = ctk.CTkButton(sys_actions_frame, text="Reset", fg_color="#A02020", hover_color="#801010", 
                                      command=self.perform_reset, width=40)
        self.btn_reset.pack(side="left", padx=(0, 5), expand=True, fill="x")

        self.btn_disconnect = ctk.CTkButton(sys_actions_frame, text="Close", fg_color="gray30", hover_color="gray20",
                                           command=self.disconnect, width=40)
        self.btn_disconnect.pack(side="left", expand=True, fill="x")

        # --- FIRMWARE ---
        ctk.CTkLabel(self.navigation_frame, text="Firmware Update", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(15, 0))
        
        self.hex_path_var = ctk.StringVar(value="")
        self.btn_select_hex = ctk.CTkButton(self.navigation_frame, text="Select HEX File", 
                                           fg_color="gray25", hover_color="gray20", command=self.select_hex_file)
        self.btn_select_hex.pack(pady=5, padx=10, fill="x")
        
        # Opzioni Firmware Row
        fw_opts_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        fw_opts_frame.pack(pady=2, padx=10, fill="x")

        self.stm32_model_var = ctk.StringVar(value="F3")
        self.stm32_model_menu = ctk.CTkOptionMenu(fw_opts_frame, variable=self.stm32_model_var,
                                                 values=["F3", "G4"], width=60)
        self.stm32_model_menu.pack(side="left", padx=(0, 10))

        self.format_after_flash_var = ctk.BooleanVar(value=False)
        self.cb_format_after_flash = ctk.CTkCheckBox(fw_opts_frame, text="Format FS", 
                                                    variable=self.format_after_flash_var,
                                                    font=ctk.CTkFont(size=11), width=20)
        self.cb_format_after_flash.pack(side="left")

        # Main Flash Actions
        self.btn_flash = ctk.CTkButton(self.navigation_frame, text="FLASH (Upload + Write)", 
                                      font=ctk.CTkFont(weight="bold"), command=self.start_file_transfer)
        self.btn_flash.pack(pady=(10, 5), padx=10, fill="x")

        # Extra Flash Actions Row
        extra_fw_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        extra_fw_frame.pack(pady=0, padx=10, fill="x")

        self.btn_upload_only = ctk.CTkButton(extra_fw_frame, text="Upload", height=24, font=ctk.CTkFont(size=11),
                                            fg_color="gray30", command=lambda: self.start_file_transfer(mode="upload"))
        self.btn_upload_only.pack(side="left", padx=(0, 2), expand=True, fill="x")

        self.btn_flash_only = ctk.CTkButton(extra_fw_frame, text="Write Only", height=24, font=ctk.CTkFont(size=11),
                                           fg_color="gray30", command=lambda: self.start_file_transfer(mode="flash"))
        self.btn_flash_only.pack(side="left", padx=(2, 2), expand=True, fill="x")

        self.btn_format = ctk.CTkButton(extra_fw_frame, text="Format", height=24, font=ctk.CTkFont(size=11),
                                       fg_color="gray30", command=self.start_format_spiffs)
        self.btn_format.pack(side="left", padx=(2, 0), expand=True, fill="x")
        
        self.progress_bar = ctk.CTkProgressBar(self.navigation_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(10, 2), padx=10, fill="x")
        self.progress_label = ctk.CTkLabel(self.navigation_frame, text="Idle", font=ctk.CTkFont(size=10))
        self.progress_label.pack(pady=(0, 10))

        self.table_buttons = []
        self.table_btns_frame = ctk.CTkScrollableFrame(self.navigation_frame, fg_color="transparent", label_text="Tables")
        self.table_btns_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Main Home
        self.home_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew")

        # Plot
        self.plot_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        self.plot_container.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    def refresh_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu.configure(values=ports if ports else ["No Serial Port"])

    def on_connect_wifi_click(self, selection):
        if "(" in selection and ")" in selection:
            ip = selection.split("(")[1].split(")")[0]
            self.connected_ip = ip
            self.connect_serial(ip, is_tcp=True)

    def connect_serial(self, port, is_tcp=False):
        if not port or port in ["Nessuna Porta", "No Serial Port", "No devices", "Serial port"]: 
            print(f"Skipping connection for invalid port: {port}")
            return
        self.disconnect()
        
        try:
            self.version_label.configure(text=f"Connecting {'TCP' if is_tcp else 'Serial'}...", text_color="orange")
            if is_tcp:
                bridge = TCPSerialBridge(port, port=9000)
                if not bridge.open():
                    raise Exception(f"Unable to connect to {port}:9000")
                self.jte_comm = JTEProtocol(bridge)
            else:
                self.jte_comm = JTEProtocol(port)
                
            self.jte_comm.init_comm()
            self.update_table_buttons()
            self.running = True
            threading.Thread(target=self.comm_thread, daemon=True).start()
            self.update_action_buttons_state()
        except Exception as e:
            self.version_label.configure(text=f"Error: {str(e)}", text_color="red")
            self.running = False
            self.update_action_buttons_state()

    def disconnect(self):
        self.running = False
        if self.jte_comm:
            self.jte_comm.close()
            self.jte_comm = None
        
        self.version_label.configure(text="Disconnected", text_color="gray")
        self.current_table_idx = -1
        self.table_buttons = []
        for child in self.table_btns_frame.winfo_children(): child.destroy()
        for child in self.home_frame.winfo_children(): child.destroy()
        self.var_rows = {}
        if hasattr(self, 'plot_manager'): self.plot_manager.clear_data()
        self.update_action_buttons_state()

    def update_action_buttons_state(self, loading=False):
        state = "normal" if self.running and not loading else "disabled"
        for btn in [self.btn_disconnect, self.btn_flash, self.btn_format, self.btn_reset, self.btn_upload_only, self.btn_flash_only]:
            btn.configure(state=state)
        # Abilita Connetti solo se non siamo già in corsa
        if hasattr(self, 'btn_connect_serial'):
            self.btn_connect_serial.configure(state="disabled" if self.running else "normal")

    def pause_bridge(self):
        self.is_suspended = True
        if self.jte_comm: self.jte_comm.close()

    def resume_bridge(self):
        if self.connected_ip: self.connect_serial(self.connected_ip, is_tcp=True)
        self.is_suspended = False

    def start_scan(self):
        self.btn_scan_tcp.configure(text="...", state="disabled")
        threading.Thread(target=self.network_scanner.scan_network_thread, daemon=True).start()

    def finish_scan(self, found_devices):
        self.btn_scan_tcp.configure(text="Rescan", state="normal")
        new_devices = found_devices.copy()
        for ip, name in self.wifi_devices.items():
            if ip not in new_devices and ip == self.connected_ip:
                new_devices[ip] = name
        
        self.wifi_devices = new_devices
        self.wifi_display_list = [f"{name} ({ip})" for ip, name in self.wifi_devices.items()]
        
        if not self.wifi_display_list:
            self.tcp_menu.configure(values=["No devices found"])
            self.tcp_device_var.set("No devices found")
        else:
            self.tcp_menu.configure(values=self.wifi_display_list)
            target_ip = self.connected_ip if self.connected_ip else None
            new_selection = next((item for item in self.wifi_display_list if target_ip and f"({target_ip})" in item), None)
            
            if new_selection: self.tcp_device_var.set(new_selection)
            elif self.wifi_display_list and self.tcp_device_var.get() not in self.wifi_display_list:
                self.tcp_device_var.set(self.wifi_display_list[0])
        
        save_config({"wifi_devices": self.wifi_devices}, self.config_file)

    def open_wifi_setup(self):
        WiFiSetupDialog(self)

    def select_hex_file(self):
        path = filedialog.askopenfilename(filetypes=[("HEX files", "*.hex"), ("BIN files", "*.bin"), ("All files", "*.*")])
        if path:
            self.hex_path_var.set(path)
            self.btn_select_hex.configure(text=os.path.basename(path))

    def start_file_transfer(self, mode="both"):
        file_path = self.hex_path_var.get()
        if not file_path:
            self.progress_label.configure(text="Select a file first!", text_color="red")
            return
        
        selection = self.tcp_device_var.get()
        if "(" not in selection:
            self.progress_label.configure(text="Select a WiFi device!", text_color="red")
            return
        
        ip = selection.split("(")[1].split(")")[0]
        self.pause_bridge()
        self.update_action_buttons_state(loading=True)
        threading.Thread(target=self.file_manager.file_transfer_thread, 
                         args=(ip, file_path, mode, self.stm32_model_var.get(), self.format_after_flash_var.get()), 
                         daemon=True).start()

    def start_format_spiffs(self):
        selection = self.tcp_device_var.get()
        if "(" not in selection:
            self.progress_label.configure(text="Select a WiFi device!", text_color="red")
            return
        
        ip = selection.split("(")[1].split(")")[0]
        if not messagebox.askyesno("Confirm", "This will ERASE all files on ESP32. Continue?"):
            return

        self.pause_bridge()
        self.update_action_buttons_state(loading=True)
        threading.Thread(target=self.file_manager.format_spiffs_thread, args=(ip,), daemon=True).start()

    def select_table(self, idx):
        if not self.jte_comm: return
        self.var_rows = {}
        for child in self.home_frame.winfo_children(): child.destroy()
        ctk.CTkLabel(self.home_frame, text="Loading variables...").pack(pady=20)
        
        self.jte_comm.select_table(idx)
        self.update_table_buttons()
        self.plot_manager.clear_data()

    def perform_reset(self):
        if not self.jte_comm: return
        self.version_label.configure(text="Resetting...", text_color="orange")
        for child in self.home_frame.winfo_children(): child.destroy()
        self.var_rows = {}
        self.jte_comm.hard_reset()
        self.update_table_buttons()
        self.plot_manager.clear_data()

    def toggle_plot_variable(self, idx, is_active):
        self.plot_manager.toggle_variable(idx, is_active)

    def on_closing(self):
        self.running = False
        if self.jte_comm: self.jte_comm.close()
        self.quit()
        try: self.destroy()
        except: pass

    def modify_variable(self, idx, action):
        if self.jte_comm: self.jte_comm.modify_var(idx, action)

    def comm_thread(self):
        last_request_time = 0
        last_values_time = 0
        waiting_for_values = False
        
        while self.running:
            if self.is_suspended:
                time.sleep(0.5)
                continue
                
            try:
                if self.jte_comm:
                    res = self.jte_comm.sync()
                    if not self.running: break
                    
                    if res == "TABLES_LOADED":
                        if self.jte_comm.tables: self.after(0, lambda: self.select_table(0))
                        self.jte_comm.is_loading = False
                    elif res == "TABLE_UPDATED":
                        self.after(0, self.rebuild_ui)
                        waiting_for_values = False
                    elif res == "VALUES_UPDATED":
                         self.after(0, self.update_ui_values)
                         last_values_time = time.time()
                         waiting_for_values = False
                    elif res == "NEW_TABLE" or res == "VERSION_UPDATED":
                        self.after(0, self.update_table_buttons)
                    elif res == "DEBUG_MESSAGE":
                        print(f"DEBUG FROM MCU: {self.jte_comm.last_debug_msg}")
                    
                    now = time.time()
                    time_since_last_tx = now - self.jte_comm.last_tx_time
                    
                    if time_since_last_tx > 2.8:
                        self.jte_comm.wake_up()
                        waiting_for_values = False
                    elif (self.jte_comm.current_table_index != -1 and not self.jte_comm.is_loading):
                        timeout_per_sicurezza = (now - last_request_time > 1.0)
                        ritardo_post_ricezione = (now - last_values_time > 0.1)
                        if (not waiting_for_values or timeout_per_sicurezza) and ritardo_post_ricezione:
                            self.jte_comm.request_values()
                            last_request_time = now
                            waiting_for_values = True
                        
                time.sleep(0.01)
            except Exception as e:
                print(f"Comm error: {e}")
                break

    def update_table_buttons(self):
        if not self.jte_comm or not self.winfo_exists(): return
        for btn in self.table_buttons: btn.destroy()
        self.table_buttons = []
        for table in self.jte_comm.tables:
            is_active = (table['index'] == self.jte_comm.current_table_index)
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
        if not self.jte_comm or not self.winfo_exists(): return
        for child in self.home_frame.winfo_children(): child.destroy()
        self.var_rows = {}
        for var in self.jte_comm.variables:
            is_plotted = var['index'] in self.plot_manager.plotted_indices
            row = VariableRow(self.home_frame, var, self.modify_variable, self.toggle_plot_variable, 
                             is_plotted=is_plotted, fg_color="transparent")
            row.pack(fill="x", padx=5, pady=0)
            self.var_rows[var['index']] = row
            separator = ctk.CTkFrame(self.home_frame, height=2, fg_color="gray25", border_width=0)
            separator.pack(fill="x", padx=20, pady=(0, 2))

    def update_ui_values(self):
        if not self.jte_comm or not self.winfo_exists(): return
        for var in self.jte_comm.variables:
            idx = var['index']
            val_str = var['value']
            row = self.var_rows.get(idx)
            if row: row.update_value(val_str)
            if idx in self.plot_manager.plotted_indices:
                self.plot_manager.add_value(idx, val_str)

if __name__ == "__main__":
    app = JTEApp()
    app.mainloop()
