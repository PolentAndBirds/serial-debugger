
import serial
import time
import sys

def debug_step_by_step(port, baudrate=19200):
    try:
        print(f"--- DEBUG STEP-BY-STEP SU {port} ({baudrate} baud) ---")
        ser = serial.Serial(port, baudrate, timeout=0.1)
        ser.dtr = False # boot a zero
        
        # Svuota buffer
        ser.reset_input_buffer()
        
        print("\n1. Invio '#$'...")
        ser.write(b"#$")
        time.sleep(0.5) # Piccolo delay
        
        print("2. Invio '#:'...")
        ser.write(b"#:")
        time.sleep(0.5) # Piccolo delay
        

        
        print("3. In attesa di intestazione e tabelle...")
        start_time = time.time()
        captured_data = bytearray()
        
        while time.time() - start_time < 5:
            if ser.in_waiting:
                chunk = ser.read(ser.in_waiting)
                captured_data.extend(chunk)
                print(f"Ricevuti {len(chunk)} byte: {chunk.hex(' ')}")
            time.sleep(0.1)
            
        if not captured_data:
            print("\nERRORE: Nessuna risposta dall'STM32.")
            print("Verifica:")
            print(" - I collegamenti TX/RX")
            print(" - Che run_jte_interface() sia effettivamente chiamata ogni 1ms")
            print(" - Che il baudrate sia corretto (ora impostato a 19200)")
        else:
            print(f"\nTOTALE RICEVUTO: {captured_data.hex(' ')}")
            
        ser.close()
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    target = "COM9" # Modifica se necessario
    debug_step_by_step(target)
