
import serial
import time
import os

class STM32FlashManager:
    """
    Gestisce la programmazione di MCU STM32 tramite il bootloader UART integrato.
    Ottimizzato per STM32G4 e gestione protezioni.
    """
    ACK = 0x79
    NACK = 0x1F

    def __init__(self, port, baudrate=115200, timeout=2.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def enter_bootloader(self):
        """Sequenza RESET/BOOT0 con logica invertita dell'utente."""
        print("Configurazione segnali BOOT0 (RTS) e RESET (DTR)...")
        try:
            s = serial.Serial()
            s.port = self.port
            s.baudrate = 115200
            s.dsrdtr = False
            s.rtscts = False
            s.dtr = False # reset high (inactive)
            s.rts = True  # boot low (inactive)
            s.open()
            time.sleep(0.1)

            s.dtr = True  # reset low (active)
            time.sleep(0.1)
            s.rts = False # boot high (active)
            time.sleep(0.2)
            s.dtr = False # reset high (released)
            time.sleep(0.2)
            print("Reset rilasciato con BOOT0 attivo.")
            s.close()
        except Exception as e:
            print(f"Errore durante enter_bootloader: {e}")

    def exit_bootloader(self):
        """Reset hardware normale."""
        try:
            with serial.Serial(self.port, 115200) as s:
                s.rts = True # boot low
                s.dtr = True # reset low
                time.sleep(0.1)
                s.dtr = False # reset high
        except: pass

    def connect(self):
        """Inizializza la comunicazione con il bootloader (Sync byte 0x7F)."""
        if self.ser and self.ser.is_open:
            self.ser.close()
        
        try:
            self.ser = serial.Serial(self.port, self.baudrate, parity=serial.PARITY_EVEN, timeout=self.timeout)
            self.ser.rts = False # Mantieni boot high
            self.ser.dtr = False # Mantieni reset released
            time.sleep(0.1)

            for i in range(10):
                self.ser.write(b'\x7F')
                res = self.ser.read(1)
                if res and res[0] == self.ACK:
                    print(f"Bootloader connesso (tentativo {i+1})")
                    self.get_version()
                    self.get_id()
                    return True
                time.sleep(0.2)
            return False
        except Exception as e:
            print(f"Errore apertura: {e}")
            return False

    def get_version(self):
        if self.send_command(0x01):
            res = self.ser.read(1)
            if not res: return
            payload = self.ser.read(res[0] + 1)
            if self.wait_for_ack():
                print(f"Versione Bootloader: {hex(payload[0])}")
                return payload
        return None

    def get_id(self):
        if self.send_command(0x02):
            res = self.ser.read(1)
            if not res: return
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
        if res[0] == self.NACK:
             print("Ricevuto NACK")
             return False
        return res[0] == self.ACK

    def read_unprotect(self):
        print("Invio comando Read Unprotect (0x82)...")
        if self.send_command(0x82):
            return self.wait_for_ack()
        return False

    def write_unprotect(self):
        print("Invio comando Write Unprotect (0x73)...")
        if self.send_command(0x73):
            return self.wait_for_ack()
        return False

    def erase_all(self):
        print("Tentativo cancellazione (Erase 0x43)...")
        if self.send_command(0x43):
            self.ser.write(b'\xFF\x00')
            if self.wait_for_ack(): return True
        
        print("Tentativo Extended Erase (0x44)...")
        if self.send_command(0x44):
            self.ser.write(b'\xFF\xFF\x00')
            return self.wait_for_ack()
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
        self.ser.write(bytes([length]) + data + bytes([cs]))
        return self.wait_for_ack()

    def flash_hex(self, hex_path, progress_callback=None):
        try:
            data_blocks = self.parse_hex_simple(hex_path)
            if not data_blocks: raise Exception("HEX vuoto")

            self.enter_bootloader()
            if not self.connect(): raise Exception("Sync bootloader fallito")

            print("Inizio cancellazione...")
            if not self.erase_all():
                print("Erase fallito. Provo Write Unprotect...")
                if self.write_unprotect():
                    print("Scrittura sbloccata. Riconnessione...")
                    if self.ser: self.ser.close()
                    time.sleep(1.5)
                    self.enter_bootloader()
                    if not self.connect(): raise Exception("Riconnessione fallita")
                    if self.erase_all(): goto_write = True
                    else: goto_write = False
                else: goto_write = False

                if not goto_write:
                    print("Erase fallito. Provo Read Unprotect...")
                    if self.read_unprotect():
                        print("Chip sbloccato. Riconnessione...")
                        if self.ser: self.ser.close()
                        time.sleep(1.5)
                        self.enter_bootloader()
                        if not self.connect(): raise Exception("Riconnessione fallita")
                        if not self.erase_all(): raise Exception("Erase fallito post-unprotect")
                    else:
                        raise Exception("Impossibile cancellare la flash")

            total_bytes = sum(len(b[1]) for b in data_blocks)
            bytes_written = 0
            print(f"Scrittura in corso ({total_bytes} byte)...")

            for addr, data in data_blocks:
                for i in range(0, len(data), 256):
                    chunk = data[i:i+256]
                    if not self.write_memory(addr + i, chunk):
                        raise Exception(f"Errore scrittura a {hex(addr+i)}")
                    bytes_written += len(chunk)
                    if progress_callback: progress_callback(bytes_written, total_bytes)

            self.exit_bootloader()
            return True
        except Exception as e:
            print(f"Errore flash: {e}")
            return False
        finally:
            if self.ser: self.ser.close()

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
