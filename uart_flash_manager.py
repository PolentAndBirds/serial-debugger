
import serial
import time
import os

class STM32FlashManager:
    """
    Gestisce la programmazione di MCU STM32 tramite il bootloader UART.
    Mantiene la porta aperta per tutta la durata del processo.
    """
    ACK = 0x79
    NACK = 0x1F

    def __init__(self, port, baudrate=115200, timeout=2.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def _set_signals_boot(self):
        """Sequenza hardware per entrare in bootloader."""
        print("Resetting into Bootloader mode...")
        self.ser.parity = serial.PARITY_NONE
        self.ser.dtr = False # reset high
        self.ser.rts = True  # boot low
        time.sleep(0.1)
        self.ser.dtr = True  # reset low (active)
        time.sleep(0.1)
        self.ser.rts = False # boot high (active)
        time.sleep(0.2)
        self.ser.dtr = False # reset high (released)
        time.sleep(0.2)

    def _set_signals_exit(self):
        """Sequenza hardware per avviare il firmware (normal mode)."""
        print("Resetting into Normal mode...")
        self.ser.parity = serial.PARITY_NONE
        time.sleep(0.1)
        self.ser.rts = True # boot low
        time.sleep(0.1)
        self.ser.dtr = True # reset low
        time.sleep(0.1)
        self.ser.dtr = False # reset high
        time.sleep(0.2)

    def connect(self):
        """Inizializza la comunicazione (Sync byte 0x7F)."""
        # Il bootloader STM32 richiede PARITY EVEN
        self.ser.parity = serial.PARITY_EVEN
        self.ser.rts = False # Mantieni boot high
        self.ser.dtr = False # Inattivo
        time.sleep(0.1)

        for i in range(10):
            self.ser.write(b'\x7F')
            res = self.ser.read(1)
            if res and res[0] == self.ACK:
                print(f"Bootloader connesso (tentativo {i+1})")
                time.sleep(0.1)
                self.ser.rts = True # Rilascia bootlow post-sync per stabilità
                self.get_available_commands()
                self.get_id()
                return True
            elif res:
                print(f"Risposta: {hex(res[0])} - {res}")
            time.sleep(0.2)
        return False

    def get_available_commands(self):
        if self.send_command(0x00):
            n_bytes = self.ser.read(1)
            if not n_bytes: return
            payload = self.ser.read(n_bytes[0] + 1)
            if self.wait_for_ack():
                version = payload[0]
                commands = list(payload[1:])
                print(f"Versione BL: {hex(version)}, Comandi: {[hex(c) for c in commands]}")
                return commands
        return None

    def get_id(self):
        if self.send_command(0x02):
            res = self.ser.read(1)
            if not res or res[0] == self.NACK: return
            payload = self.ser.read(res[0] + 1)
            if self.wait_for_ack():
                print(f"Chip ID: {payload.hex().upper()}")
                return payload
        return None

    def send_command(self, cmd):
        self.ser.write(bytes([cmd, cmd ^ 0xFF]))
        return self.wait_for_ack()

    def wait_for_ack(self):
        res = self.ser.read(1)
        if not res: return False
        if res[0] == self.NACK: return False
        return res[0] == self.ACK

    def read_unprotect(self):
        if self.send_command(0x82):
            return self.wait_for_ack()
        return False

    def write_unprotect(self):
        if self.send_command(0x73):
            return self.wait_for_ack()
        return False

    def erase_all(self):
        print("Inizio cancellazione...")
        old_timeout = self.ser.timeout
        self.ser.timeout = 10.0
        try:
            if self.send_command(0x44):
                for data, cs in [(b'\xFF\xFF', 0x00), (b'\xFF\xFE', 0x01), (b'\xFF\xFD', 0x02)]:
                    self.ser.write(data + bytes([cs]))
                    if self.wait_for_ack(): return True
                    time.sleep(0.1)
            if self.send_command(0x43):
                self.ser.write(b'\xFF\x00')
                return self.wait_for_ack()
        finally:
            self.ser.timeout = old_timeout
        return False

    def write_memory(self, address, data):
        if not self.send_command(0x31): return False
        addr_bytes = address.to_bytes(4, 'big')
        cs = 0
        for b in addr_bytes: cs ^= b
        self.ser.write(addr_bytes + bytes([cs]))
        if not self.wait_for_ack(): return False

        length = len(data) - 1
        cs = length
        for b in data: cs ^= b
        self.ser.write(bytes([length]))
        for i in range(0, len(data), 64):
            self.ser.write(data[i : i+64])
            time.sleep(0.002)
        self.ser.write(bytes([cs]))
        return self.wait_for_ack()

    def flash_hex(self, hex_path, progress_callback=None):
        try:
            data_blocks = self.parse_hex_simple(hex_path)
            if not data_blocks: raise Exception("HEX vuoto")

            # APRIAMO LA PORTA UNA VOLTA SOLA
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            
            # Procedura 1: Entra in bootloader
            self._set_signals_boot()
            
            # Procedura 2: Sincronizzazione
            if not self.connect():
                # Fallback a 57600
                print("Provo fallback a 57600...")
                self.ser.baudrate = 57600
                self._set_signals_boot()
                if not self.connect(): raise Exception("Sync fallito")

            # Procedura 3: Erase
            print("Cancellazione...")
            if not self.erase_all():
                print("Erase fallito. Provo sblocco protezioni...")
                if self.write_unprotect():
                    print("Scrittura sbloccata. Riavvio...")
                    self._set_signals_boot()
                    self.connect()
                    if not self.erase_all(): raise Exception("Erase fallito post-sblocco")
                elif self.read_unprotect():
                    print("Lettura sbloccata. Riavvio...")
                    self._set_signals_boot()
                    self.connect()
                    if not self.erase_all(): raise Exception("Erase fallito post-sblocco")
                else:
                    raise Exception("Impossibile cancellare la flash")

            # Procedura 4: Scrittura
            total_bytes = sum(len(b[1]) for b in data_blocks)
            bytes_written = 0
            for addr, data in data_blocks:
                for i in range(0, len(data), 256):
                    chunk = data[i:i+256]
                    if not self.write_memory(addr + i, chunk):
                        raise Exception(f"Errore scrittura a {hex(addr+i)}")
                    bytes_written += len(chunk)
                    if progress_callback: progress_callback(bytes_written, total_bytes)

            # Procedura 5: Reset finale
            self._set_signals_exit()
            return True
        except Exception as e:
            print(f"Errore: {e}")
            return False
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()

    def parse_hex_simple(self, file_path):
        blocks = []
        base_addr = 0
        ext_addr = 0
        current_data = bytearray()
        with open(file_path, 'r') as f:
            for line in f:
                if not line.startswith(':'): continue
                count = int(line[1:3], 16)
                addr = int(line[3:7], 16)
                rtype = int(line[7:9], 16)
                data = bytes.fromhex(line[9:9+count*2])
                if rtype == 0x04: ext_addr = (int(line[9:13], 16) << 16)
                elif rtype == 0x00:
                    full_addr = ext_addr + addr
                    if not current_data or full_addr == base_addr + len(current_data):
                        if not current_data: base_addr = full_addr
                        current_data.extend(data)
                    else:
                        blocks.append((base_addr, current_data))
                        base_addr = full_addr
                        current_data = bytearray(data)
                elif rtype == 0x01:
                    if current_data: blocks.append((base_addr, current_data))
                    break
        return blocks
