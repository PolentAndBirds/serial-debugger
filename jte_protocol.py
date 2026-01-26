
import serial
import time
import threading

class JTEProtocol:
    def __init__(self, port, baudrate=19200, timeout=1):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.ser.dtr = False
        self.ser.rts = True
        self.ser.open()
        
        self.lock = threading.Lock()
        self.machine_name = ""
        self.version = ""
        self.tables = []
        self.current_table_index = -1
        self.variables = []
        self.connected = True
        self.is_loading = False
        self.last_tx_time = time.time()
        self._temp_variables = []

    def close(self):
        with self.lock:
            if self.ser.is_open:
                self.ser.close()
        self.connected = False

    def send_raw(self, data):
        with self.lock:
            print(f"TX -> {data}")
            self.last_tx_time = time.time()
            if isinstance(data, str):
                self.ser.write(data.encode('ascii'))
            else:
                self.ser.write(data)

    def read_packet(self):
        with self.lock:
            if not self.ser.in_waiting:
                return None
            
            header = self.ser.read(1)
            if not header: return None
            
            type_byte = header[0]
            if type_byte not in [0xf0, 0xf1, 0xf2, 0xf3, 0xf4]:
                return None # Ignora byte spuri
            
            payload = bytearray()
            start_wait = time.time()
            while time.time() - start_wait < 1.0:
                b = self.ser.read(1)
                if not b: continue
                if b[0] == 0xff:
                    break
                payload.append(b[0])
            else:
                return None # Timeout pacchetto
                
            #print(f"RX -> {hex(type_byte)} Payload: {payload.hex(' ')}")
            
            if type_byte == 0xf2: # Version
                self.version = payload.decode('ascii', errors='ignore').strip()
                return {'type': 0xf2, 'version': self.version}
                
            elif type_byte == 0xf3: # Table Name
                if not payload: return {'type': 0xf3, 'index': -1, 'name': None}
                idx = payload[0]
                name = payload[1:-1].decode('ascii', errors='ignore').strip()
                with_points = payload[-1]
                return {'type': 0xf3, 'index': idx, 'name': name, 'with_points': with_points}
                
            elif type_byte == 0xf0: # Variable Name
                if not payload: return {'type': 0xf0, 'index': -1, 'name': None}
                idx = payload[0]
                name = payload[1:-1].decode('ascii', errors='ignore').strip()
                step_type = chr(payload[-1])
                return {'type': 0xf0, 'index': idx, 'name': name, 'step_type': step_type}
                
            elif type_byte == 0xf1: # Variable Value
                if not payload: return {'type': 0xf1, 'end': True}
                idx = payload[0]
                if idx > 100: return {'type': 0xf1, 'end': True}
                val_str = payload[1:].decode('ascii', errors='ignore').strip()
                return {'type': 0xf1, 'index': idx, 'value': val_str}
                
            elif type_byte == 0xf4: # Debug String
                val_str = payload.decode('ascii', errors='ignore').strip()
                return {'type': 0xf4, 'value': val_str}
                
            return None

    def select_table(self, index):
        """Invia il comando per cambiare tabella e richiedere i nomi + valori."""
        self.current_table_index = index
        self.is_loading = True
        # Inviamo #T0 e subito dopo #. per avere nomi e primi valori
        self.send_raw(f"#T{index}#.")
        # Non puliamo la lista variabili qui, aspettiamo che arrivi il pacchetto 0xf0
        self._temp_variables = [] 

    def sync(self):
        """Legge un singolo pacchetto dal buffer e aggiorna lo stato interno."""
        packet = self.read_packet()
        if not packet:
            return False
            
        if packet['type'] == 0xf0: # Nome Variabile
            if packet['name'] is None: # Fine elenco nomi
                self.variables = self._temp_variables
                self._temp_variables = []
                self.is_loading = False
                # Quando finiscono i nomi, chiediamo di nuovo i valori per sicurezza
                self.request_values()
                return "TABLE_UPDATED"
            else:
                self._temp_variables.append({
                    'index': packet['index'],
                    'name': packet['name'],
                    'step_type': packet['step_type'],
                    'value': ""
                })
                
        elif packet['type'] == 0xf1: # Valore Variabile
            if 'end' in packet:
                return "VALUES_UPDATED"
            for var in self.variables:
                if var['index'] == packet['index']:
                    var['value'] = packet['value']
                    break
        
        elif packet['type'] == 0xf2:
            self.version = packet['version']
            return "VERSION_UPDATED"
            
        elif packet['type'] == 0xf3:
            if packet['name'] is not None:
                # Evitiamo duplicati nelle tabelle
                if not any(t['index'] == packet['index'] for t in self.tables):
                    self.tables.append(packet)
                    return "NEW_TABLE"
            else:
                # Se riceve 0xf3 con nome nullo, le tabelle sono finite
                print("--- FINE CARICAMENTO TABELLE ---")
                return "TABLES_LOADED"

        return True

    def request_values(self):
        self.send_raw("#.")

    def modify_var(self, var_idx, action):
        # action: '+', '-', '*', '/'
        # var_idx should be 01..99
        idx_str = f"{var_idx:02d}"
        self.send_raw(f"#{action}{idx_str}")

    def wake_up(self):
        """Risveglia l'STM32 se è andato in timeout (oltre i 3 secondi)."""
        print("--- WAKE UP STM32 ---")
        self.send_raw("#$")
        time.sleep(0.1)
        self.send_raw("#:")
        time.sleep(0.1)
        if self.current_table_index != -1:
            self.send_raw(f"#T{self.current_table_index}#.")

    def init_comm(self):
        # Svuota buffer residui
        with self.lock:
            self.ser.reset_input_buffer()
        
        # Sblocco e Inizializzazione in un unico colpo come chiesto
        print("Invio sequenza sblocco e inizializzazione #$#:")
        self.send_raw("#$#:")
        self.tables = []
        self._temp_variables = []
        self.current_table_index = -1

    def hard_reset(self):
        """Esegue un reset fisico della board tramite DTR e reinizializza."""
        print("--- ESECUZIONE HARD RESET (DTR TOGGLE) ---")
        self.ser.dtr = True
        time.sleep(0.2)
        self.ser.dtr = False
        time.sleep(1.5) # Tempo per il boot
        self.init_comm() # Essenziale per rimettere STM32 in stato di ascolto (#$#:)
