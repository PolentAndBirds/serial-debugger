import os
import socket
import time
import threading

class FileManager:
    """
    Gestisce il trasferimento di file HEX e la formattazione SPIFFS su ESP32.
    """
    def __init__(self, app_callback):
        self.app = app_callback

    def file_transfer_thread(self, ip, file_path, mode, stm32_model, format_after_flash=False):
        """Logica di trasferimento file (basata sullo script fornito)."""
        port = 9000
        try:
            file_size = os.path.getsize(file_path)
            filename = os.path.basename(file_path)
            
            self.app.after(0, lambda: self.app.progress_label.configure(text="Connecting...", text_color="orange"))
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(20)
                s.connect((ip, port))
                
                # --- PARTE UPLOAD ---
                if mode in ["both", "upload"]:
                    s.sendall(f"AT+FSTART={file_size},{filename}\r".encode())
                    
                    response = s.recv(1024).decode(errors='ignore')
                    print(f"RX -> {response}")
                    if "OK" in response:
                        self.app.after(0, lambda: self.app.progress_label.configure(text="Uploading...", text_color="cyan"))
                        bytes_sent = 0
                        
                        with open(file_path, "rb") as f:
                            while True:
                                chunk = f.read(4096)
                                if not chunk:
                                    break
                                s.sendall(chunk)
                                bytes_sent += len(chunk)
                                
                                progress = bytes_sent / file_size
                                self.app.after(0, lambda p=progress: self.app.progress_bar.set(p))
                                self.app.after(0, lambda p=progress: self.app.progress_label.configure(text=f"Uploading: {p*100:.1f}%"))
                                
                                time.sleep(0.005) 
                        
                        self.app.after(0, lambda: self.app.progress_label.configure(text="Finalizing Upload...", text_color="orange"))
                        final_response = s.recv(1024).decode(errors='ignore')
                        print(f"RX -> {final_response}")
                        
                        if "OK" not in final_response:
                            self.app.after(0, lambda: self.app.progress_label.configure(text=f"Upload Error: {final_response.strip()}", text_color="red"))
                            return
                            
                        if mode == "upload":
                            self.app.after(0, lambda: self.app.progress_label.configure(text="Upload Success!", text_color="green"))
                            self.app.after(0, lambda: self.app.progress_bar.set(1.0))
                            return
                    else:
                        self.app.after(0, lambda: self.app.progress_label.configure(text=f"Error: {response.strip()}", text_color="red"))
                        return

                # --- PARTE FLASH ---
                if mode in ["both", "flash"]:
                    model = stm32_model
                    self.app.after(0, lambda: self.app.progress_label.configure(text=f"Flashing {model}...", text_color="yellow"))
                    suffix = ",1" if format_after_flash else ""
                    s.sendall(f"AT+STMFLASH={model},{filename}{suffix}\r".encode())
                    
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
                                        self.app.after(0, lambda p=perc: self.app.progress_bar.set(p/100))
                                        self.app.after(0, lambda p=perc: self.app.progress_label.configure(text=f"Flashing: {p}%", text_color="yellow"))
                                    except: pass
                                
                                elif "+ERROR: WRONG CHIP" in line:
                                    self.app.after(0, lambda l=line: self.app.progress_label.configure(text=f"Error: {l}", text_color="red"))
                                    return
                                
                                elif "+ERROR:" in line:
                                    self.app.after(0, lambda l=line: self.app.progress_label.configure(text=f"Error: {l}", text_color="red"))
                                    return
                                
                                elif "+SUCCESS:" in line:
                                    info = line.split(":", 1)[1].strip()
                                    self.app.after(0, lambda i=info: self.app.progress_label.configure(text=f"Success: {i}", text_color="green"))
                                    self.app.after(0, lambda: self.app.progress_bar.set(1.0))
                                    return
                                    
                        except socket.timeout:
                            self.app.after(0, lambda: self.app.progress_label.configure(text="Flash Timeout!", text_color="red"))
                            break
        except Exception as e:
            error_msg = str(e)
            self.app.after(0, lambda: self.app.progress_label.configure(text=f"Error: {error_msg}", text_color="red"))
        finally:
            self.app.after(0, lambda: self.app.update_action_buttons_state(loading=False))
            self.app.after(2000, self.app.resume_bridge)

    def format_spiffs_thread(self, ip):
        """Logica di formattazione SPIFFS."""
        try:
            self.app.after(0, lambda: self.app.progress_label.configure(text="Formatting SPIFFS (Wait...)", text_color="orange"))
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((ip, 9000))
                s.sendall(b"AT+FFMT\r")
                response = s.recv(1024).decode(errors='ignore')
                print(f"RX -> {response}")
                if "OK" not in response:
                    raise Exception(f"Format rejected: {response}")
                
            self.app.after(0, lambda: self.app.progress_label.configure(text="Format command sent", text_color="green"))
        except Exception as e:
            error_msg = str(e)
            self.app.after(0, lambda: self.app.progress_label.configure(text=f"Error: {error_msg}", text_color="red"))
        finally:
            self.app.after(0, lambda: self.app.update_action_buttons_state(loading=False))
            self.app.after(0, self.app.resume_bridge)
