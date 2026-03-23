import serial
import sys
import time
import os

# ANSI colors
GREEN      = '\033[92m'   # logo
ORANGE     = '\033[33m'   # main title
CYAN       = '\033[96m'   # menu options
YELLOW     = '\033[93m'   # menu options
LIGHT_GREY = '\033[90m'   # menu options
WHITE      = '\033[97m'   # context/submenu
RED        = '\033[91m'   # warnings
RESET      = '\033[0m'

# ASCII Logo
logo = r"""
                                          ________ .                          
                          _________.     /'      /'/                          
                          \'      \ \   /       / /                           
██▄  ██  ▄▄▄  ▄▄  ▄▄  ▄▄▄  \       \ \ /       / /  ██▀▀█▄ ▄▄▄▄   ▄▄▄  ▄▄   ▄▄
██▀█▄██ ██ ██ ███ ██ ██ ██  \_ _ _ _\ /_ _ _ _/ /   ██  ██ ██ ██ ██ ██ ███▄███
██  ▀██ ██▄██ ██▀███ ██ ██  /       /\        \ \   ██▄▄█▀ ██▄█▀ ██ ██ ██ ▀ ██
██   ██ ██ ██ ██  ██ ▀█▄█▀ /       / /\        \ \  ██     ██ ██ ▀█▄█▀ ██   ██
                          /       / /  \        \ \                           
                         /_______/ /    \________\'    > Release V0.1 beta    
                         |       |/                                           
 OG XBOX EEPROM Flasher  |_______/  for the Arduino Nano - tim@beepfixer.com 
"""

EEPROM_SIZE = 256

# ---------------- Helper Functions ----------------

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header(context="- MAIN"):
    """Clear screen and show logo + header with dynamic context."""
    clear_screen()
    print(GREEN + logo + RESET)
    print(f"{ORANGE}NanoProm v0.1 beta {WHITE}{context}{RESET}")
    print()

def list_com_ports():
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    LIGHT_GREY = '\033[90m'  # bright black / light grey
    print("Available COM ports:")
    for i, port in enumerate(ports):
        print(f"{LIGHT_GREY}{i}: {port.device} - {port.description}{RESET}")
    return ports

def select_com_port():
    ports = list_com_ports()
    while True:
        print()
        choice = input("Select COM port number (or 'X' to go back): ").strip()
        if choice.lower() == 'x':
            return None
        if choice.isdigit() and int(choice) < len(ports):
            return ports[int(choice)].device
        print("Invalid selection.")

def read_eeprom(com_port):
    """Read 256 bytes from EEPROM; return None if incomplete."""
    ser = serial.Serial(com_port, 9600, timeout=10)
    time.sleep(2)
    ser.write(b'\x00')  # READ command
    data = ser.read(EEPROM_SIZE)
    ser.close()
    
    if len(data) != EEPROM_SIZE:
        print(f"{RED}Error: did not receive 256 bytes from EEPROM (received {len(data)} bytes){RESET}")
        return None
    return data

def read2_eeprom(com_port):
    """Read 256 bytes from standalone EEPROM; return None if incomplete."""
    ser = serial.Serial(com_port, 9600, timeout=10)
    time.sleep(2)  # allow Arduino to settle

    ser.write(b'\x03')  # READ2 command for standalone EEPROM
    data = ser.read(EEPROM_SIZE)
    ser.close()
    
    if len(data) != EEPROM_SIZE:
        print(f"{RED}Error: did not receive 256 bytes from standalone EEPROM (received {len(data)} bytes){RESET}")
        return None
    return data

def write_eeprom(com_port, filename):
    """
    Reliable EEPROM write for current Nano firmware with progress bar.
    Returns True if ACK received, False otherwise.
    """
    import os
    import sys

    if not os.path.exists(filename):
        print(f"{RED}File does not exist.{RESET}")
        return False

    with open(filename, 'rb') as f:
        data = f.read()
    if len(data) < EEPROM_SIZE:
        data += b'\x00' * (EEPROM_SIZE - len(data))
    elif len(data) > EEPROM_SIZE:
        data = data[:EEPROM_SIZE]

    try:
        ser = serial.Serial(com_port, 9600, timeout=20)
        time.sleep(2)
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        # WRITE command
        ser.write(b'\x01')
        ser.flush()

        # Send bytes one by one with tiny delay and progress bar
        for i, b in enumerate(data, 1):
            ser.write(bytes([b]))
            time.sleep(0.002)  # 2ms per byte

            # Progress bar (text)
            done = int(i / EEPROM_SIZE * 30)  # 30-char bar
            sys.stdout.write(f"\rWriting EEPROM: [{'#'*done}{'.'*(30-done)}] {i}/{EEPROM_SIZE}")
            sys.stdout.flush()

        ser.flush()
        print()  # newline after progress bar

        # Wait for ACK (0x00)
        ack = ser.read(1)
        if ack == b'\x00':
            print(f"{GREEN}EEPROM write successful and ACK received!{RESET}")
            success = True
        else:
            print(f"{RED}No ACK from board. Write may have failed.{RESET}")
            success = False

        ser.close()
        return success

    except Exception as e:
        print(f"{RED}Error writing EEPROM: {e}{RESET}")
        if 'ser' in locals() and ser.is_open:
            ser.close()
        return False

def write2_eeprom(com_port, filename):
    """
    Reliable write to standalone EEPROM (EEPROM_ADDR2) with progress bar.
    Returns True if ACK received, False otherwise.
    """
    import os
    import sys

    if not os.path.exists(filename):
        print(f"{RED}File does not exist.{RESET}")
        return False

    with open(filename, 'rb') as f:
        data = f.read()
    if len(data) < EEPROM_SIZE:
        data += b'\x00' * (EEPROM_SIZE - len(data))
    elif len(data) > EEPROM_SIZE:
        data = data[:EEPROM_SIZE]

    try:
        ser = serial.Serial(com_port, 9600, timeout=20)
        time.sleep(2)
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        # WRITE2 command for standalone EEPROM
        ser.write(b'\x04')
        ser.flush()

        # Send bytes one by one with tiny delay and progress bar
        for i, b in enumerate(data, 1):
            ser.write(bytes([b]))
            time.sleep(0.002)  # 2ms per byte

            # Progress bar (text)
            done = int(i / EEPROM_SIZE * 30)  # 30-char bar
            sys.stdout.write(f"\rWriting standalone EEPROM: [{'#'*done}{'.'*(30-done)}] {i}/{EEPROM_SIZE}")
            sys.stdout.flush()

        ser.flush()
        print()  # newline after progress bar

        # Wait for ACK (0x00)
        ack = ser.read(1)
        if ack == b'\x00':
            print(f"{GREEN}Standalone EEPROM write successful and ACK received!{RESET}")
            success = True
        else:
            print(f"{RED}No ACK from board. Write may have failed.{RESET}")
            success = False

        ser.close()
        return success

    except Exception as e:
        print(f"{RED}Error writing standalone EEPROM: {e}{RESET}")
        if 'ser' in locals() and ser.is_open:
            ser.close()
        return False

def erase_eeprom(com_port):
    """Erase the entire EEPROM with 00 or FF, display progress, then read & verify robustly."""
    val = ''
    while val not in ['0','f','x']:
        print()
        print(f"{RED}WARNING - YOU ARE ABOUT TO ERASE YOUR XBOX EEPROM!{RESET}")
        print()
        val = input("Erase with (0) 00 or (F) FF - (X) to go back: ").strip().lower()

    if val == 'x':
        return

    byte_val = b'\x00' if val == '0' else b'\xFF'

    try:
        ser = serial.Serial(com_port, 9600, timeout=10)
        time.sleep(2)  # let Nano settle

        # --- Send ERASE command ---
        print(f"Erasing EEPROM with {'00' if val=='0' else 'FF'}...")
        ser.write(b'\x02')  # ERASE command
        time.sleep(0.1)

        # send bytes one by one with tiny delay + progress bar
        for i in range(EEPROM_SIZE):
            ser.write(byte_val)
            time.sleep(0.002)
            done = int((i+1)/EEPROM_SIZE * 30)
            sys.stdout.write(f"\rProgress: [{'#'*done}{'.'*(30-done)}] {i+1}/{EEPROM_SIZE}")
            sys.stdout.flush()
        ser.flush()
        print()  # newline after progress bar

        # --- Post-erase verification loop ---
        while True:
            print("\nReading EEPROM after erase for verification...")

            # flush input/output buffers before read
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            # --- Visual waiting countdown ---
            for i in range(3, 0, -1):
                sys.stdout.write(f"\rWaiting for Nano to finish internal erase... {i} ")
                sys.stdout.flush()
                time.sleep(1)
            print("\r" + " " * 50, end="\r")  # clear line

            # --- Robust read: discard first read to clear lingering byte ---
            ser.write(b'\x00')
            _ = ser.read(EEPROM_SIZE)  # discard potential incomplete read
            time.sleep(0.05)
            ser.reset_input_buffer()

            # --- Actual read ---
            ser.write(b'\x00')
            data = b''
            start = time.time()
            while len(data) < EEPROM_SIZE and (time.time() - start) < 5:
                data += ser.read(EEPROM_SIZE - len(data))

            # --- Display full EEPROM like normal read ---
            display_eeprom(data, context="- POST-ERASE READ")

            # --- Verify ---
            correct_bytes = sum(1 for b in data if b == byte_val[0])
            wrong_bytes = EEPROM_SIZE - correct_bytes

            if correct_bytes == EEPROM_SIZE:
                print(f"{GREEN}All {EEPROM_SIZE}/{EEPROM_SIZE} bytes match expected value.{RESET}")
                break
            else:
                print(f"{RED}{correct_bytes}/{EEPROM_SIZE} bytes match expected value ({wrong_bytes} wrong).{RESET}")
                choice = input("Retry verification read? (Y/N or X to cancel): ").strip().lower()
                if choice not in ['y']:
                    break

    except Exception as e:
        print(f"{RED}Error during erase: {e}{RESET}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

def erase2_eeprom(com_port):
    """Erase the entire standalone EEPROM (EEPROM_ADDR2) with 00 or FF, display progress, then read & verify."""
    val = ''
    while val not in ['0','f','x']:
        print()
        print(f"{RED}WARNING - YOU ARE ABOUT TO ERASE THE STANDALONE EEPROM!{RESET}")
        print()
        val = input("Erase with (0) 00 or (F) FF - (X) to go back: ").strip().lower()

    if val == 'x':
        return

    byte_val = b'\x00' if val == '0' else b'\xFF'

    try:
        ser = serial.Serial(com_port, 9600, timeout=10)
        time.sleep(2)  # let Nano settle

        # --- Send ERASE2 command ---
        print(f"Erasing standalone EEPROM with {'00' if val=='0' else 'FF'}...")
        ser.write(b'\x05')  # ERASE2 command
        time.sleep(0.1)

        # send bytes one by one with tiny delay + progress bar
        for i in range(EEPROM_SIZE):
            ser.write(byte_val)
            time.sleep(0.002)
            done = int((i+1)/EEPROM_SIZE * 30)
            sys.stdout.write(f"\rProgress: [{'#'*done}{'.'*(30-done)}] {i+1}/{EEPROM_SIZE}")
            sys.stdout.flush()
        ser.flush()
        print()  # newline after progress bar

        # --- Post-erase verification loop ---
        while True:
            print("\nReading standalone EEPROM after erase for verification...")

            # flush input/output buffers before read
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            # --- Visual waiting countdown ---
            for i in range(3, 0, -1):
                sys.stdout.write(f"\rWaiting for Nano to finish internal erase... {i} ")
                sys.stdout.flush()
                time.sleep(1)
            print("\r" + " " * 50, end="\r")  # clear line

            # --- Robust read: discard first read to clear lingering byte ---
            ser.write(b'\x03')
            _ = ser.read(EEPROM_SIZE)  # discard potential incomplete read
            time.sleep(0.05)
            ser.reset_input_buffer()

            # --- Actual read ---
            ser.write(b'\x03')
            data = b''
            start = time.time()
            while len(data) < EEPROM_SIZE and (time.time() - start) < 5:
                data += ser.read(EEPROM_SIZE - len(data))

            # --- Display full EEPROM like normal read ---
            display_eeprom(data, context="- STANDALONE POST-ERASE READ")

            # --- Verify ---
            correct_bytes = sum(1 for b in data if b == byte_val[0])
            wrong_bytes = EEPROM_SIZE - correct_bytes

            if correct_bytes == EEPROM_SIZE:
                print(f"{GREEN}All {EEPROM_SIZE}/{EEPROM_SIZE} bytes match expected value.{RESET}")
                break
            else:
                print(f"{RED}{correct_bytes}/{EEPROM_SIZE} bytes match expected value ({wrong_bytes} wrong).{RESET}")
                choice = input("Retry verification read? (Y/N or X to cancel): ").strip().lower()
                if choice not in ['y']:
                    break

    except Exception as e:
        print(f"{RED}Error during erase of standalone EEPROM: {e}{RESET}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

def display_eeprom(data, context="- MAIN", standalone=False):
    """
    Display EEPROM contents in 16-byte rows.
    If standalone=True, adjusts header to indicate standalone EEPROM.
    """
    eeprom_type = "STANDALONE EEPROM" if standalone else "XBOX ONBOARD EEPROM"
    print(f"\n{CYAN}{eeprom_type} {context}{RESET} (full {len(data)} bytes):")
    
    LIGHT_GREY = '\033[90m'  # light grey for EEPROM bytes
    for i in range(0, len(data), 16):
        line = " ".join(f"{b:02X}" for b in data[i:i+16])
        print(f"{LIGHT_GREY}{line}{RESET}")

def save_eeprom_prompt(data):
    """Prompt the user to save EEPROM data to a .bin file with a unique default name."""
    from datetime import datetime

    # Generate timestamped default filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    default_name = f"xbox_eeprom_{timestamp}.bin"

    print()
    save = input(f"Save read EEPROM to a .bin file? (Y/N): ").strip().lower()
    if save != 'y':
        return
    
    filename = input(f"Enter filename to save (default: {default_name}): ").strip()
    if not filename:
        filename = default_name
    elif not filename.lower().endswith(".bin"):
        filename += ".bin"

    # ensure ../binfiles exists and prepend it to filename
    save_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../binfiles"))
    os.makedirs(save_dir, exist_ok=True)
    full_path = os.path.join(save_dir, filename)

    try:
        with open(full_path, 'wb') as f:
            f.write(data)
        print(f"{GREEN}EEPROM data saved to {full_path}{RESET}")
    except Exception as e:
        print(f"{RED}Error saving file: {e}{RESET}")

def verify_eeprom(com_port, pc_file, context="- VERIFY", standalone=False):
    # Use read2_eeprom if standalone
    eeprom = read2_eeprom(com_port) if standalone else read_eeprom(com_port)
    if eeprom is None:
        return
    with open(pc_file, 'rb') as f:
        file_data = f.read(EEPROM_SIZE)
        if len(file_data) < EEPROM_SIZE:
            file_data += b'\x00' * (EEPROM_SIZE - len(file_data))

    # --- Header ---
    bytes_per_row = 16
    byte_width = 3
    row_width = bytes_per_row * byte_width - 1

    header1 = f"EEPROM {context}".ljust(row_width)
    header2 = f"PC FILE: {os.path.basename(pc_file)}"
    print(f"\n{CYAN}{header1}    {header2}{RESET}\n")

    mismatches = []

    # --- Row by row comparison ---
    for i in range(0, EEPROM_SIZE, 16):
        row_eeprom = eeprom[i:i+16]
        row_file   = file_data[i:i+16]

        line_e, line_f = [], []

        for j, (b_e, b_f) in enumerate(zip(row_eeprom, row_file)):
            if b_e == b_f:
                line_e.append(GREEN + f"{b_e:02X}" + RESET)
                line_f.append(GREEN + f"{b_f:02X}" + RESET)
            else:
                line_e.append(RED + f"{b_e:02X}" + RESET)
                line_f.append(RED + f"{b_f:02X}" + RESET)
                mismatches.append(i + j)

        print(" ".join(line_e) + "    " + " ".join(line_f))

    # --- Summary ---
    if not mismatches:
        print(f"{GREEN}\nVerification OK: EEPROM matches file!{RESET}")
    else:
        print(f"{RED}\nVerification FAILED: {len(mismatches)} mismatch(es) found.{RESET}")
        print(f"{RED}First mismatches:{RESET}")
        for addr in mismatches[:3]:
            print(f"Addr 0x{addr:02X}: EEPROM={eeprom[addr]:02X} File={file_data[addr]:02X}")
        if len(mismatches) > 3:
            print(f"...and {len(mismatches)-3} more mismatches")

        save = input("Save full mismatch report to text file? (Y/N): ").strip().lower()
        if save == 'y':
            filename = input("Enter filename for report (without extension): ").strip()
            if not filename.endswith(".txt"):
                filename += ".txt"

            # ensure ../binfiles exists and prepend it to filename
            save_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../binfiles"))
            os.makedirs(save_dir, exist_ok=True)
            full_path = os.path.join(save_dir, filename)

            with open(full_path, 'w') as f:
                f.write(f"EEPROM {context} vs PC FILE: {pc_file}\n")
                for addr in mismatches:
                    f.write(f"Addr 0x{addr:02X}: EEPROM={eeprom[addr]:02X} File={file_data[addr]:02X}\n")
            print(f"{GREEN}Full report saved to {full_path}{RESET}")

def verify_two_files(file1, file2, context="- VERIFY2"): 
    with open(file1,'rb') as f:
        data1 = f.read(EEPROM_SIZE)
        if len(data1) < EEPROM_SIZE:
            data1 += b'\x00'*(EEPROM_SIZE-len(data1))

    with open(file2,'rb') as f:
        data2 = f.read(EEPROM_SIZE)
        if len(data2) < EEPROM_SIZE:
            data2 += b'\x00'*(EEPROM_SIZE-len(data2))

    # header alignment
    bytes_per_row = 16
    byte_width = 3
    row_width = bytes_per_row * byte_width - 1

    header1 = f"PC FILE: {os.path.basename(file1)}".ljust(row_width)
    header2 = f"PC FILE: {os.path.basename(file2)}"

    print(f"\n{CYAN}{header1}    {header2}{RESET}")

    mismatches = []

    for i in range(0, EEPROM_SIZE, 16):
        row1 = data1[i:i+16]
        row2 = data2[i:i+16]

        line1, line2 = [], []

        for j, (b1, b2) in enumerate(zip(row1, row2)):
            if b1 == b2:
                line1.append(GREEN + f"{b1:02X}" + RESET)
                line2.append(GREEN + f"{b2:02X}" + RESET)
            else:
                line1.append(RED + f"{b1:02X}" + RESET)
                line2.append(RED + f"{b2:02X}" + RESET)
                mismatches.append(i + j)

        print(" ".join(line1) + "    " + " ".join(line2))

    if not mismatches:
        print(f"{GREEN}\nVerification OK: Files match!{RESET}")
    else:
        print(f"{RED}\nVerification FAILED: {len(mismatches)} mismatch(es) found.{RESET}")
        print(f"{RED}First mismatches:{RESET}")
        for addr in mismatches[:3]:
            print(f"Addr 0x{addr:02X}: FILE1={data1[addr]:02X} FILE2={data2[addr]:02X}")
        if len(mismatches) > 3:
            print(f"...and {len(mismatches)-3} more mismatches")

        # save full mismatch report
        save = input("Save full mismatch report to text file? (Y/N): ").strip().lower()
        if save == 'y':
            filename = input("Enter filename for report (without extension): ").strip()
            if not filename.endswith(".txt"):
                filename += ".txt"
            
            # ensure ../binfiles exists and prepend it to filename
            save_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../binfiles"))
            os.makedirs(save_dir, exist_ok=True)
            full_path = os.path.join(save_dir, filename)

            with open(full_path, 'w') as f:
                f.write(f"PC FILES {context}: {file1} vs {file2}\n")
                for addr in mismatches:
                    f.write(f"Addr 0x{addr:02X}: FILE1={data1[addr]:02X} FILE2={data2[addr]:02X}\n")

            print(f"{GREEN}Full report saved to {full_path}{RESET}")

# ---------------- Main Menu ----------------

def main_menu(context="- MAIN"):
    show_header(context)
    print(CYAN + "[ 1 ] XBOX EEPROM - Read - save to PC (as a .bin file)" + RESET)
    print(CYAN + "[ 2 ] XBOX EEPROM - Flash - from a PC .bin file" + RESET)
    print(CYAN + "[ 3 ] XBOX EEPROM - Erase - fill with 00 or FF" + RESET)
    print(CYAN + "[ 4 ] XBOX EEPROM - Compare - with a PC .bin file" + RESET)
    print()
    print(ORANGE + "[ 5 ] PC ONLY - Compare - two .bin files" + RESET)
    print()
    print(LIGHT_GREY + "[ 6 ] STANDALONE EEPROM - Read - save to PC (as a .bin file)" + RESET)
    print(LIGHT_GREY + "[ 7 ] STANDALONE EEPROM - Flash - from a PC .bin file" + RESET)
    print(LIGHT_GREY + "[ 8 ] STANDALONE EEPROM - Erase - fill with 00 or FF" + RESET)
    print(LIGHT_GREY + "[ 9 ] STANDALONE EEPROM - Compare - with a PC .bin file" + RESET)
    print()
    print(YELLOW + "[ X ] Exit" + RESET)
    print()
    return input("Select option: ").strip()

# ---------------- Main Loop ----------------

if __name__ == "__main__":
    while True:
        choice = main_menu(context="- MAIN")

        if choice.lower() == 'x':
            print("Exiting...")
            break

        elif choice == '1':  # READ EEPROM
            show_header("- READ")  # redraw first
            port = select_com_port()
            if port:
                data = read_eeprom(port)
                if data:
                    display_eeprom(data, context="- READ")
                    save_eeprom_prompt(data)
                else:
                    # EEPROM read failed, show message and pause
                    input(f"\n{RED}Failed to read EEPROM!{RESET}\nPress Enter to return to main menu...")
                input("\nPress Enter to return to main menu...")

        elif choice == '2':  # WRITE EEPROM
            show_header("- WRITE")  # redraw first
            port = select_com_port()
            if port:
                while True:
                    fname = input("Enter filename to write from (.bin file) or 'X' to go back: ").strip()
                    if fname.lower() == 'x':
                        break
                    if not fname:
                        print(f"{RED}Please provide a filename!{RESET}")
                        continue

                    # prepend ../binfiles if not absolute
                    if not os.path.isabs(fname):
                        fname = os.path.abspath(os.path.join(os.path.dirname(__file__), "../binfiles", fname))

                    if not os.path.exists(fname):
                        print(f"{RED}File does not exist: {fname}{RESET}")
                        continue

                    # file exists, perform write
                    success = write_eeprom(port, fname)  # confirmation inside function

                    # --- Post-write verification ---
                    if success:
                        verify_choice = input(f"\nDo you want to verify the EEPROM write against '{fname}'? (Y/N): ").strip().lower()
                        if verify_choice == 'y':
                            print("\nVerifying EEPROM write...")
                            verify_eeprom(port, fname, context="- POST-WRITE VERIFY")
                    break  # exit loop after valid write attempt

                input("\nPress Enter to return to main menu...")
     
        elif choice == '3':  # ERASE EEPROM
            show_header("- ERASE")  # redraw first
            port = select_com_port()
            if port:
                erase_eeprom(port)
                input("\nPress Enter to return to main menu...")

        elif choice == '4':  # VERIFY EEPROM
            show_header("- VERIFY")  # redraw first
            port = select_com_port()
            print()
            if port:
                while True:
                    fname = input("Enter PC .bin filename (file name or full path, or 'X' to go back): ").strip()
                    if fname.lower() == 'x':
                        break
                    if not fname:
                        print(f"{RED}Please provide a filename!{RESET}")
                        continue

                    # prepend ../binfiles if not absolute
                    if not os.path.isabs(fname):
                        fname = os.path.abspath(os.path.join(os.path.dirname(__file__), "../binfiles", fname))

                    if not os.path.exists(fname):
                        print(f"{RED}File does not exist: {fname}{RESET}")
                        continue

                    # file exists, proceed
                    verify_eeprom(port, fname, context="- VERIFY")
                    break
                input("\nPress Enter to return to main menu...")

        elif choice == '5':  # VERIFY TWO FILES
            show_header("- COMPARE 2 .BIN FILES")  # redraw first
            
            # file1 prompt
            while True:
                f1 = input("Enter first PC .bin filename (or 'X' to go back): ").strip()
                if f1.lower() == 'x':
                    break

                # prepend ../binfiles if not absolute
                if not os.path.isabs(f1):
                    f1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "../binfiles", f1))

                if os.path.exists(f1):
                    break
                print(f"{RED}File does not exist.{RESET}")
            if f1.lower() == 'x':
                continue

            # file2 prompt
            while True:
                f2 = input("Enter second PC .bin filename (or 'X' to go back): ").strip()
                if f2.lower() == 'x':
                    break

                # prepend ../binfiles if not absolute
                if not os.path.isabs(f2):
                    f2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "../binfiles", f2))

                if os.path.exists(f2):
                    break
                print(f"{RED}File does not exist.{RESET}")

            if f2.lower() == 'x':
                continue

            verify_two_files(f1, f2, context="- VERIFY2")
            input("\nPress Enter to return to main menu...")

        elif choice == '6':  # STANDALONE READ
            show_header("- STANDALONE READ")  # redraw first
            port = select_com_port()
            if port:
                data = read2_eeprom(port)  # use the new read2 function
                if data:
                    display_eeprom(data, context="- STANDALONE READ", standalone=True)
                    save_eeprom_prompt(data)
                else:
                    # Standalone EEPROM read failed
                    input(f"\n{RED}Failed to read standalone EEPROM!{RESET}\nPress Enter to return to main menu...")
                input("\nPress Enter to return to main menu...")

        elif choice == '7':  # STANDALONE FLASH
            show_header("- STANDALONE WRITE")  # redraw first
            port = select_com_port()
            if port:
                while True:
                    fname = input("Enter filename to write from (.bin file) or 'X' to go back: ").strip()
                    if fname.lower() == 'x':
                        break
                    if not fname:
                        print(f"{RED}Please provide a filename!{RESET}")
                        continue

                    # prepend ../binfiles if not absolute
                    if not os.path.isabs(fname):
                        fname = os.path.abspath(os.path.join(os.path.dirname(__file__), "../binfiles", fname))

                    if not os.path.exists(fname):
                        print(f"{RED}File does not exist: {fname}{RESET}")
                        continue

                    # file exists, perform write to standalone EEPROM
                    success = write2_eeprom(port, fname)  # use the v2 write function

                    # --- Post-write verification ---
                    if success:
                        verify_choice = input(f"\nDo you want to verify the standalone EEPROM write against '{fname}'? (Y/N): ").strip().lower()
                        if verify_choice == 'y':
                            print("\nVerifying standalone EEPROM write...")
                            data = read2_eeprom(port)  # read back using v2
                            if data:
                                display_eeprom(data, context="- STANDALONE POST-WRITE VERIFY", standalone=True)
                                save_eeprom_prompt(data)
                            else:
                                print(f"{RED}Verification read failed!{RESET}")
                    break  # exit loop after valid write attempt

                input("\nPress Enter to return to main menu...")

        elif choice == '8':  # STANDALONE ERASE
            show_header("- STANDALONE ERASE")  # redraw first
            port = select_com_port()
            if port:
                erase2_eeprom(port)  # use v2 erase function
                input("\nPress Enter to return to main menu...")

        elif choice == '9':  # STANDALONE VERIFY
            show_header("- STANDALONE VERIFY")  # redraw first
            port = select_com_port()
            print()
            if port:
                while True:
                    fname = input("Enter PC .bin filename to compare with (or 'X' to go back): ").strip()
                    if fname.lower() == 'x':
                        break
                    if not fname:
                        print(f"{RED}Please provide a filename!{RESET}")
                        continue

                    # prepend ../binfiles if not absolute
                    if not os.path.isabs(fname):
                        fname = os.path.abspath(os.path.join(os.path.dirname(__file__), "../binfiles", fname))

                    if not os.path.exists(fname):
                        print(f"{RED}File does not exist: {fname}{RESET}")
                        continue

                    # file exists, proceed
                    verify_eeprom(port, fname, context="- STANDALONE VERIFY", standalone=True)
                    break
                input("\nPress Enter to return to main menu...")

        else:
            print("Invalid selection.")
            input("\nPress Enter to return to main menu...")