import socket
import threading
import time

class NetworkScanner:
    """
    Gestisce la scansione della rete locale per trovare bridge ESP32.
    """
    def __init__(self, app_callback):
        self.app = app_callback

    def scan_network_thread(self):
        found_devices = {} # IP -> Name
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            prefix = ".".join(local_ip.split(".")[:-1]) + "."
            
            threads = []
            def check_ip(ip):
                try:
                    # Collegamento 1: Recupero Nome
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.8)
                    if sock.connect_ex((ip, 9000)) == 0:
                        sock.sendall(b"AT+NAME?\r\n")
                        time.sleep(0.1)
                        raw_name = sock.recv(512).decode('ascii', errors='ignore').strip()
                        sock.close()
                        
                        name_resp = "ESP32-Bridge"
                        if "+NAME=" in raw_name:
                            try:
                                core_name = raw_name.split("+NAME=")[1].split("\r")[0].split("\n")[0].strip()
                                name_resp = f"JWI-{core_name}"
                            except: pass
                        
                        found_devices[ip] = name_resp
                        
                        # Collegamento 2: Recupero Tipo Macchina (Sessione separata per stabilità)
                        try:
                            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock2.settimeout(0.8)
                            if sock2.connect_ex((ip, 9000)) == 0:
                                sock2.sendall(b"AT+MACHINE=?\r\n")
                                time.sleep(0.1)
                                raw_type = sock2.recv(512).decode('ascii', errors='ignore').strip()
                                if "+MACHINE=" in raw_type:
                                    try:
                                        type_resp = raw_type.split("+MACHINE=")[1].split("\r")[0].split("\n")[0].strip()
                                        found_devices[ip] = f"{name_resp} | {type_resp}"
                                    except: pass
                            sock2.close()
                        except:
                            pass
                            
                        print(f"Scanned {ip}: {found_devices.get(ip)}")
                except: pass

            for i in range(1, 255):
                t = threading.Thread(target=check_ip, args=(prefix + str(i),))
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()
                
        except Exception as e:
            print(f"Scan error: {e}")
        
        self.app.after(0, lambda: self.app.finish_scan(found_devices))
