
import socket
import time
import threading

class TCPSerialBridge:
    """
    Simulation of a serial port over a TCP socket.
    Used to connect to ESP32 serial-wifi bridges.
    """
    def __init__(self, host, port=9000, timeout=1.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.in_waiting = 0
        self._read_buffer = bytearray()
        self.is_open = False
        self._lock = threading.Lock()
        
        # Stubs for compatibility with pyserial
        self.dtr = False
        self.rts = False
        self.baudrate = 0
        self.port_name = f"tcp://{host}:{port}"

    def open(self):
        """Connects to the ESP32 and sends AT+BYPASS=1."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.host, self.port))
            self.is_open = True
            
            # Send the bypass command as requested by the user
            print(f"Connecting to {self.host} and sending AT+BYPASS=1...")
            self.sock.sendall(b"AT+BYPASS=1\r\n")
            time.sleep(0.1) # Give it a moment to switch modes
            
            # Start a background thread to read from the socket
            self._running = True
            self._thread = threading.Thread(target=self._recv_loop, daemon=True)
            self._thread.start()
            
            return True
        except Exception as e:
            print(f"TCP Connection error: {e}")
            self.is_open = False
            return False

    def _recv_loop(self):
        while self._running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    self.is_open = False
                    self._running = False
                    break
                with self._lock:
                    self._read_buffer.extend(data)
                    self.in_waiting = len(self._read_buffer)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"TCP Receive error: {e}")
                self.is_open = False
                self._running = False
                break

    def read(self, size=1):
        with self._lock:
            if not self._read_buffer:
                return b""
            data = self._read_buffer[:size]
            self._read_buffer = self._read_buffer[size:]
            self.in_waiting = len(self._read_buffer)
            return bytes(data)

    def write(self, data):
        if not self.is_open:
            return 0
        if isinstance(data, str):
            data = data.encode('ascii')
        try:
            self.sock.sendall(data)
            return len(data)
        except Exception as e:
            print(f"TCP Write error: {e}")
            self.is_open = False
            return 0

    def close(self):
        self._running = False
        self.is_open = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass

    def reset_input_buffer(self):
        with self._lock:
            self._read_buffer.clear()
            self.in_waiting = 0

    def send_at_command(self, command, timeout=5.0):
        """
        Sends an AT command directly to the ESP32 and waits for a response.
        This is useful for commands like AT+FFMT while the bridge is active.
        """
        if not self.is_open:
            return "Error: Not connected"
            
        print(f"Sending AT command through bridge: {command}")
        if isinstance(command, str):
            command = command.encode('ascii')
            
        # Clear buffer before sending to avoid old data
        self.reset_input_buffer()
        self.sock.sendall(command)
        
        # Wait for a line containing OK or ERROR
        start_time = time.time()
        response = ""
        while time.time() - start_time < timeout:
            chunk = self.read(1024).decode('ascii', errors='ignore')
            if chunk:
                response += chunk
                if "OK" in response or "ERROR" in response:
                    return response.strip()
            time.sleep(0.1)
            
        return response.strip() if response else "Error: Timeout"

    def flush(self):
        pass # Not applicable for TCP in the same way, but needed for compatibility
