
import serial
import time

def debug_raw_serial(port, baudrate=19200):
    try:
        print(f"Tentativo di connessione su {port} a {baudrate} baud...")
        ser = serial.Serial(port, baudrate, timeout=1)
        ser.setDTR(False) # boot a zero

        print("Invio comando di reset: #$")
        ser.write(b"#$")
        time.sleep(0.1)
        print("Invio comando di inizializzazione: #:")
        ser.write(b"#:")
        
        print("In attesa di dati per 5 secondi...")
        start_time = time.time()
        while time.time() - start_time < 5:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting)
                print(f"Ricevuto ({len(data)} byte): {data.hex(' ')}")
                # Prova a stampare anche come stringa se leggibile
                try:
                    print(f"Come stringa: {data.decode('ascii', errors='replace')}")
                except:
                    pass
            time.sleep(0.1)
            ser.write(b"#T0#.")
            
        ser.close()
        print("\nSessione di debug terminata.")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    import serial.tools.list_ports
    ports = [p.device for p in serial.tools.list_ports.comports()]
    if ports:
        # Selezioniamo COM9 se presente, altrimenti la prima disponibile
        target = "COM9" if "COM9" in ports else ports[0]
        debug_raw_serial(target)
    else:
        print("Nessuna porta seriale trovata.")
