
import serial.tools.list_ports

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("Nessuna porta seriale trovata.")
        return
    
    print("Porte seriali disponibili:")
    for port in ports:
        print(f"- {port.device}: {port.description}")

if __name__ == "__main__":
    list_serial_ports()
