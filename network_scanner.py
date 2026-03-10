import socket
import threading

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
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, 9000))
                    if result == 0:
                        sock.sendall(b"AT+NAME?\r\n")
                        raw_name = sock.recv(64).decode('ascii', errors='ignore').strip()
                        
                        name_resp = ""
                        if "+NAME=" in raw_name:
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
        
        self.app.after(0, lambda: self.app.finish_scan(found_devices))
