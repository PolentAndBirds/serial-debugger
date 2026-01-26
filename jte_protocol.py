
import serial
import time
import threading

class JTEProtocol:
    """
    Gestisce la comunicazione seriale con il firmware JTE su STM32.
    Implementa un protocollo personalizzato basato su pacchetti binari per la gestione
    di tabelle di parametri e variabili in tempo reale.
    """
    def __init__(self, port, baudrate=19200, timeout=1):
        """
        Inizializza la connessione seriale.
        Parametri:
            port: Nome della porta seriale (es. 'COM3' o '/dev/ttyUSB0')
            baudrate: Velocità di trasmissione (default 19200)
            timeout: Tempo limite per le operazioni di lettura
        """
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        # Segnali di controllo necessari per la board STM32
        self.ser.dtr = False
        self.ser.rts = True
        self.ser.open()
        
        # Lock per garantire l'accesso thread-safe alla porta seriale
        self.lock = threading.Lock()
        self.machine_name = ""
        self.version = ""
        self.tables = [] # Elenco delle tabelle disponibili
        self.current_table_index = -1
        self.variables = [] # Variabili della tabella attualmente selezionata
        self.connected = True
        self.is_loading = False # Flag attivato durante l'aggiornamento dei nomi
        self.last_tx_time = time.time()
        self._temp_variables = [] # Buffer temporaneo per i nomi delle variabili in arrivo

    def close(self):
        """Chiude la connessione seriale in modo sicuro."""
        with self.lock:
            if self.ser.is_open:
                self.ser.close()
        self.connected = False

    def send_raw(self, data):
        """
        Invia dati grezzi sulla seriale.
        Può accettare sia stringhe che array di byte.
        """
        with self.lock:
            print(f"TX -> {data}")
            self.last_tx_time = time.time()
            if isinstance(data, str):
                self.ser.write(data.encode('ascii'))
            else:
                self.ser.write(data)

    def read_packet(self):
        """
        Legge un pacchetto in arrivo dalla board.
        Il protocollo prevede un header (0xf0-0xf4), un payload e un terminatore (0xff).
        
        Tipi di pacchetti:
        0xf0: Nome di una variabile
        0xf1: Valore di una variabile
        0xf2: Versione del firmware
        0xf3: Nome di una tabella
        0xf4: Stringa di debug
        """
        with self.lock:
            if not self.ser.in_waiting:
                return None
            
            # Legge il primo byte (header del pacchetto)
            header = self.ser.read(1)
            if not header: return None
            
            type_byte = header[0]
            if type_byte not in [0xf0, 0xf1, 0xf2, 0xf3, 0xf4]:
                return None # Ignora byte spuri o non riconosciuti
            
            # Legge il payload fino al terminatore 0xff
            payload = bytearray()
            start_wait = time.time()
            while time.time() - start_wait < 1.0: # Timeout di sicurezza per il singolo pacchetto
                b = self.ser.read(1)
                if not b: continue
                if b[0] == 0xff:
                    break
                payload.append(b[0])
            else:
                return None # Timeout durante la ricezione del pacchetto completo
            #debug dati ricevuti(commento per disabilitare)
            #print(f"RX -> {hex(type_byte)} Payload: {payload.hex(' ')}") 
                
            # Gestione dei vari tipi di pacchetti ricevuti
            if type_byte == 0xf2: # Pacchetto Versione
                self.version = payload.decode('ascii', errors='ignore').strip()
                return {'type': 0xf2, 'version': self.version}
                
            elif type_byte == 0xf3: # Pacchetto Nome Tabella
                if not payload: return {'type': 0xf3, 'index': -1, 'name': None}
                idx = payload[0]
                # I nomi sono strighe ASCII, l'ultimo byte indica se la tabella ha punti o meno
                name = payload[1:-1].decode('ascii', errors='ignore').strip()
                with_points = payload[-1]
                return {'type': 0xf3, 'index': idx, 'name': name, 'with_points': with_points}
                
            elif type_byte == 0xf0: # Pacchetto Nome Variabile
                if not payload: return {'type': 0xf0, 'index': -1, 'name': None}
                idx = payload[0]
                name = payload[1:-1].decode('ascii', errors='ignore').strip()
                step_type = chr(payload[-1]) # Tipo di incremento della variabile
                return {'type': 0xf0, 'index': idx, 'name': name, 'step_type': step_type}
                
            elif type_byte == 0xf1: # Pacchetto Valore Variabile
                if not payload: return {'type': 0xf1, 'end': True}
                idx = payload[0]
                if idx > 100: return {'type': 0xf1, 'end': True}
                val_str = payload[1:].decode('ascii', errors='ignore').strip()
                return {'type': 0xf1, 'index': idx, 'value': val_str}
                
            elif type_byte == 0xf4: # Pacchetto Debug (Messaggi generici)
                val_str = payload.decode('ascii', errors='ignore').strip()
                return {'type': 0xf4, 'value': val_str}
                
            return None

    def select_table(self, index):
        """
        Invia il comando per cambiare tabella (#Tx) e richiede nomi e valori (#.).
        Parametri:
            index: Indice della tabella da selezionare.
        """
        self.current_table_index = index
        self.is_loading = True
        # Invia il comando di selezione tabella seguito dalla richiesta di sincronizzazione totale
        self.send_raw(f"#T{index}#.")
        # Pulisce la lista temporanea delle variabili, che verrà riempita dai pacchetti 0xf0 in arrivo
        self._temp_variables = [] 

    def sync(self):
        """
        Legge e processa un singolo pacchetto dal buffer seriale, aggiornando lo stato interno.
        Questa funzione viene solitamente chiamata in un loop.
        """
        packet = self.read_packet()
        if not packet:
            return False
            
        if packet['type'] == 0xf0: # Ricezione elenco Nomi Variabile
            if packet['name'] is None: # Segnala la fine dell'elenco nomi
                self.variables = self._temp_variables
                self._temp_variables = []
                self.is_loading = False
                # Una volta completati i nomi, richiede il refresh dei valori
                self.request_values()
                return "TABLE_UPDATED"
            else:
                # Aggiunge la variabile all'elenco temporaneo
                self._temp_variables.append({
                    'index': packet['index'],
                    'name': packet['name'],
                    'step_type': packet['step_type'],
                    'value': ""
                })
                
        elif packet['type'] == 0xf1: # Ricezione Valore Variabile
            if 'end' in packet:
                return "VALUES_UPDATED"
            # Aggiorna il valore della variabile corrispondente nell'elenco attuale
            for var in self.variables:
                if var['index'] == packet['index']:
                    var['value'] = packet['value']
                    break
        
        elif packet['type'] == 0xf2: # Ricezione Versione
            self.version = packet['version']
            return "VERSION_UPDATED"
            
        elif packet['type'] == 0xf3: # Ricezione Nomi Tabelle (Fase di inizializzazione)
            if packet['name'] is not None:
                # Evita di aggiungere tabelle duplicate
                if not any(t['index'] == packet['index'] for t in self.tables):
                    self.tables.append(packet)
                    return "NEW_TABLE"
            else:
                # Ricezione di un pacchetto 0xf3 vuoto indica che tutte le tabelle sono state trasmesse
                print("--- FINE CARICAMENTO TABELLE ---")
                return "TABLES_LOADED"

        return True

    def request_values(self):
        """Richiede l'invio immediato dei valori attuali di tutte le variabili."""
        self.send_raw("#.")

    def modify_var(self, var_idx, action):
        """
        Invia un comando di modifica per una specifica variabile.
        Parametri:
            var_idx: Indice della variabile (0-99).
            action: Operazione da eseguire ('+', '-', '*', '/').
        """
        idx_str = f"{var_idx:02d}" # Formato a due cifre (es. 01, 05, 12)
        self.send_raw(f"#{action}{idx_str}")

    def wake_up(self):
        """
        Invia una sequenza di risveglio se la board non risponde da tempo.
        Riautorizza la comunicazione e risincronizza lo stato.
        """
        print("--- WAKE UP STM32 ---")
        self.send_raw("#$") # Sblocco
        time.sleep(0.1)
        self.send_raw("#:") # Richiesta Info/Versione
        time.sleep(0.1)
        if self.current_table_index != -1:
            # Se eravamo in una tabella, la riselezioniamo
            self.send_raw(f"#T{self.current_table_index}#.")

    def init_comm(self):
        """
        Esegue l'inizializzazione completa della comunicazione.
        Svuota i buffer e invia la sequenza di 'handshake' #$#:.
        """
        with self.lock:
            self.ser.reset_input_buffer()
        
        print("Invio sequenza sblocco e inizializzazione #$#:")
        self.send_raw("#$#:") # #$ sblocca, #: richiede nomi tabelle e versione
        self.tables = []
        self._temp_variables = []
        self.current_table_index = -1

    def hard_reset(self):
        """
        Esegue un reset hardware della board agendo sul segnale DTR (connesso al pin RESET).
        Dopo il reset attende il riavvio della board e reinizializza la comunicazione.
        """
        print("--- ESECUZIONE HARD RESET (DTR TOGGLE) ---")
        self.ser.dtr = True
        time.sleep(0.2)
        self.ser.dtr = False
        time.sleep(1.5) # Attesa per il bootloader/startup firmware
        self.init_comm() # Rimette l'STM32 in stato di ascolto attivo
