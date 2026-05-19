import subprocess
import pexpect
import sys
import os
import time
import re
import configparser
import pyvisa
import epics

# ----------------------------- Configuration -----------------------------
SERIAL_HOST = "10.0.142.108"
SERIAL_PORT = 4028
XSCT_BIN = "/tools/Xilinx/Vitis/2022.2/bin/xsct"
VIVADO_BIN = "/tools/Xilinx/Vivado/2022.2/bin/vivado"
VITIS_SETTINGS = "/tools/Xilinx/Vitis/2022.2/settings64.sh"
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "dfe_settings.cfg")

LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)

DDR_TIMEOUT = 120  # seconds

prefix ="DFE{BPM:2}"


def load_runtime_config():
    """Load optional runtime overrides from dfe_settings.cfg."""
    global SERIAL_HOST, SERIAL_PORT, XSCT_BIN, VIVADO_BIN, VITIS_SETTINGS

    if not os.path.exists(SETTINGS_FILE):
        return

    parser = configparser.ConfigParser()
    parser.read(SETTINGS_FILE)

    SERIAL_HOST = parser.get("network", "serial_host", fallback=SERIAL_HOST)
    SERIAL_PORT = parser.getint("network", "serial_port", fallback=SERIAL_PORT)
    XSCT_BIN = parser.get("tools", "xsct_bin", fallback=XSCT_BIN)
    VIVADO_BIN = parser.get("tools", "vivado_bin", fallback=VIVADO_BIN)
    VITIS_SETTINGS = parser.get("tools", "vitis_settings", fallback=VITIS_SETTINGS)


load_runtime_config()

#---------------------------- IP Ping Function --------------------------
def ping_ip(ip, count=3, timeout=3):
    """
    Ping an IP address. Returns True if reachable.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", str(timeout), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False
#--------------------------- Telnet Connection Function --------------------------
def open_telnet():
    print("Opening Serial MOXA connection...")
    tn = pexpect.spawn(
        f"telnet {SERIAL_HOST} {SERIAL_PORT}",
        encoding="utf-8",
        timeout=5
    )
    tn.sendline("")  # wake up console
    return tn
#--------------------------- Console Flush Function --------------------------
def flush_console(tn, duration=1.0):
    """Drain any pending console output."""
    end = time.time() + duration
    while time.time() < end:
        try:
            tn.read_nonblocking(size=4096, timeout=0.1)
        except pexpect.TIMEOUT:
            pass
        except pexpect.EOF:
            break
#--------------------------- DDR Eye Width Parsing Function --------------------------
def parse_eye_width(buffer):
    lines = buffer.splitlines()
    capture = False
    eye_vals = []

    for line in lines:
        if "EYE WIDTH (%)" in line:
            capture = True
            continue

        if capture:
            # Skip separator lines
            if set(line.strip()) <= set("-+ "):
                continue

            nums = re.findall(r"\d+\.\d+", line)
            if nums:
                eye_vals = [float(x) for x in nums]
                break

    if eye_vals:
        avg = sum(eye_vals) / len(eye_vals)
        return eye_vals, avg

    return [], None
# --------------------------- Helper Functions ---------------------------
log_callback = None
ip_confirm_callback = None
ibert_callback = None
sd_callback = None
qspi_callback = None
io_callback = None
afe_callback = None
stress_callback = None
# --------------------------- Global Variables --------------------------
DDR_FPGA_PROGRAMMED = False
NOR_FPGA_PROGRAMMED = False
STRESS_FPGA_PROGRAMMED = False

# --------------------------- Logging Function --------------------------
def write_log(log_file, text):
    print(text, end="")
    sys.stdout.flush()

    with open(log_file, "a") as f:
        f.write(text)

    if log_callback:
        log_callback(text)

#--------------------------- SD Test Function --------------------------
def sd_test(bd_num,tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED
    flush_console(tn)


    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running SD test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting SD Test for Board {bd_num} ===\n")

    DDR_FPGA_PROGRAMMED = False
    NOR_FPGA_PROGRAMMED = False  
    STRESS_FPGA_PROGRAMMED = False

    start_time = time.time()
    sd_test_complete = False

    if sd_callback:
        response = sd_callback()
    else: 
        # 1) Insert SD card
        input("Please insert the SD card and press Enter to continue...")
        input("Set BOOT MODE to SD (0101) and press Enter to continue...")
        #Power cycle the board to ensure SD menu appears
        input("Please power cycle the board now and press Enter to continue...")
        write_log(log_file, "[PYTHON] Waiting for SD menu...\n")

    while True:
        try:
            # Read a line from the console
            line = tn.readline().strip()
            if line:
                write_log(log_file, line + "\n")

            if "FPGA successfully programmed." in line:
                sd_test_complete = True
                break  # SD test done

            # ---- Global timeout ----
            if time.time() - start_time > DDR_TIMEOUT:
                write_log(log_file, "\nERROR: SD test timed out\n")
                tn.close()
                return False

        except pexpect.exceptions.TIMEOUT:
            pass  # keep waiting
        except pexpect.exceptions.EOF:
            write_log(log_file, "\nERROR: SD console closed unexpectedly\n")
            return False
    
    if sd_test_complete:
        write_log(log_file, "\n=== SD TEST PASS ===\n")
        return True
    else:
        write_log(log_file, "\n=== SD TEST FAIL ===\n")
        tn.close()
        return False
#--------------------------- QSPI Test Function --------------------------
def qspi_test(bd_num,tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED
    flush_console(tn)

    DDR_FPGA_PROGRAMMED = False
    NOR_FPGA_PROGRAMMED = False  
    STRESS_FPGA_PROGRAMMED = False

    
    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running QSPI Boot test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting QSPI Boot Test for Board {bd_num} ===\n")

    qspi_dir = "./qspi_dfe"
    QSPIProject = os.path.join(qspi_dir, f"qspi{bd_num}_gen.txt")

    if not os.path.exists(QSPIProject):
        try: 
            subprocess.run(
                            ["./flash_qspi.sh"],
                            cwd="./fpga_boot",
                            env={**os.environ, "VITIS_SETTINGS": VITIS_SETTINGS},
                            check=True
                        )
            print("QSPI flash script completed")

            os.makedirs(qspi_dir, exist_ok=True)
            with open(QSPIProject, "a") as f:
                    f.write("SUCCESS\n")
        except subprocess.CalledProcessError:
            print("ERROR: QSPI flash failed")
            return False
    else: 
        print("QSPI flash already done, skipping flash step")
    
    

    start_time = time.time()
    qspi_test_complete = False

    if qspi_callback:
        response = qspi_callback()
    else:
        input("Set BOOT MODE to QSPI (0001) and press Enter to continue...")
        #Power cycle the board to ensure QSPI boot
        input("Please power cycle the board now and press Enter to continue...")

    while True:
        try:
            # Read a line from the console
            line = tn.readline().strip()
            if line:
                write_log(log_file, line + "\n")

            if "FPGA successfully programmed." in line:
                qspi_test_complete = True
                break  # QSPI test done

            # ---- Global timeout ----
            if time.time() - start_time > DDR_TIMEOUT:
                write_log(log_file, "\nERROR: QSPI test timed out\n")
                tn.close()
                return False

        except pexpect.exceptions.TIMEOUT:
            pass  # keep waiting
        except pexpect.exceptions.EOF:
            write_log(log_file, "\nERROR: QSPI console closed unexpectedly\n")
            return False
    
    if qspi_test_complete:
        write_log(log_file, "\n=== QSPI TEST PASS ===\n")
        return True
    else:
        write_log(log_file, "\n=== QSPI TEST FAIL ===\n")
        tn.close()
        return False
# --------------------------- DDR Test Function --------------------------
def ddr_test(bd_num,tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED
    flush_console(tn)

    VIVADO_CMD = [
    XSCT_BIN,
    "ddr_test/ddr_test.tcl"
    ]

    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running DDR test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting DDR Test for Board {bd_num} ===\n")

    if not DDR_FPGA_PROGRAMMED:
        # 1) Program FPGA
        print("Programming FPGA...")
        try:
            subprocess.run(VIVADO_CMD, check=True)
        except subprocess.CalledProcessError:
            print("ERROR: FPGA programming failed")
            return False
        DDR_FPGA_PROGRAMMED = True
        NOR_FPGA_PROGRAMMED = False  
        STRESS_FPGA_PROGRAMMED = False

    start_time = time.time()
    sent_r = False
    sent_w = False
    r_eye_complete = False
    w_eye_complete = False
    r_avg_eye = 0
    w_avg_eye = 0
    line = ""

    # Already programmed: board is sitting at the DDR menu, nothing more will
    # print on the serial terminal, so send commands immediately before reading.
    if DDR_FPGA_PROGRAMMED:
        write_log(log_file, "[PYTHON] FPGA already programmed, sending 'r' immediately...\n")
        flush_console(tn)
        tn.sendline("r")
        sent_r = True
        write_log(log_file, ">>> SENT: r\n")
    else:
        write_log(log_file, "[PYTHON] Waiting for DDR menu...\n")

    while True:
        # Send 'w' outside try so a TIMEOUT on readline cannot block it.
        # Wait until read-eye results are done first to avoid interleaving.
        if sent_r and r_eye_complete and not sent_w:
            tn.sendline("w")
            sent_w = True
            write_log(log_file, ">>> SENT: w\n")

        try:
            # Read a line from the console
            line = tn.readline().strip()
            if line:
                write_log(log_file, line + "\n")

            # First-run path: send 'r' only after the board starts printing
            # (i.e. the DDR menu has appeared). readline() will succeed here
            # because the board is actively outputting data after programming.
            if not sent_r:
                tn.sendline("r")
                sent_r = True
                write_log(log_file, ">>> SENT: r\n")

            if "Read Eye Test Results :" in line:
                r_eye_buffer = ""
                # Capture the eye test results
                while True:
                    r_eye_line = tn.readline().strip()
                    write_log(log_file, r_eye_line + "\n")
                    if r_eye_line == "":
                        break
                    r_eye_buffer += r_eye_line + "\n"

                eye_vals, avg_eye = parse_eye_width(r_eye_buffer)
                if eye_vals:
                    write_log(log_file, f"\nExtracted Eye Widths: {eye_vals}\n")
                    write_log(log_file, f"Average Eye Width: {avg_eye:.2f}%\n")
                    r_avg_eye = avg_eye
                    r_eye_complete = True
                else:
                    write_log(log_file, "No Eye Width data found.\n")
          
            if "Write Eye Test Results:" in line:
                w_eye_buffer = ""
                # Capture the eye test results
                while True:
                    w_eye_line = tn.readline().strip()
                    write_log(log_file, w_eye_line + "\n")
                    if w_eye_line == "":
                        break
                    w_eye_buffer += w_eye_line + "\n"
                

                eye_vals, avg_eye = parse_eye_width(w_eye_buffer)
                if eye_vals:
                    write_log(log_file, f"\nExtracted Eye Widths: {eye_vals}\n")
                    write_log(log_file, f"Average Eye Width: {avg_eye:.2f}%\n")
                    w_avg_eye = avg_eye
                    w_eye_complete = True
                else:
                    write_log(log_file, "No Eye Width data found.\n")

            if r_eye_complete and w_eye_complete:
                break  # both tests done

            # ---- Global timeout ----
            if time.time() - start_time > DDR_TIMEOUT:
                write_log(log_file, "\nERROR: DDR test timed out\n")
                tn.close()
                return False

        except pexpect.exceptions.TIMEOUT:
            pass  # keep waiting
        except pexpect.exceptions.EOF:
            write_log(log_file, "\nERROR: DDR console closed unexpectedly\n")
            return False
    
    print(f"Read Avg Eye Width: {r_avg_eye:.2f}%, Write Avg Eye Width: {w_avg_eye:.2f}%")
    if r_avg_eye > 70 and w_avg_eye > 70 :
        write_log(log_file, "\n=== DDR TEST PASS ===\n")
        return True
    else:
        write_log(log_file, "\n=== DDR TEST FAIL ===\n")
        tn.close()
        return False
#--------------------------- Temperature Test Function -------------------------- 
def temp_test(bd_num,tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED
    flush_console(tn)

    
    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running Temperature test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting Temperature Test for Board {bd_num} ===\n")
    
    VIVADO_CMD = [
    XSCT_BIN,
    "fpga_boot/fpga_boot.tcl"
    ]

    if not NOR_FPGA_PROGRAMMED:
        # 1) Program FPGA
        print("Programming FPGA...")
        try:
            subprocess.run(VIVADO_CMD, check=True)
        except subprocess.CalledProcessError:
            print("ERROR: FPGA programming failed")
            return False
        DDR_FPGA_PROGRAMMED = False
        NOR_FPGA_PROGRAMMED = True  
        STRESS_FPGA_PROGRAMMED = False

    start_time = time.time()
    temp_test_complete = False
    sent_e = False

    if NOR_FPGA_PROGRAMMED:
        write_log(log_file, "[PYTHON] FPGA already programmed, sending 'E' immediately...\n")
        flush_console(tn)
        tn.sendline("E")
        sent_e = True
        write_log(log_file, ">>> SENT: E\n")
    else:
        write_log(log_file, "[PYTHON] Waiting for Temperature menu...\n")

    while True:
        try:
            # Read a line from the console
            line = tn.readline().strip()
            if line:
                write_log(log_file, line + "\n")

            if (not sent_e) and ("FPGA successfully programmed" in line):
                tn.sendline("E")
                sent_e = True
                write_log(log_file, ">>> SENT: E\n")

            if "DFE Temperature Sensor Readings:" in line:
                temp_buffer = ""
                # Capture the eye test results
                while True:
                    temp_line = tn.readline().strip()
                    write_log(log_file, temp_line + "\n")
                    if temp_line == "DFE temps reading done.":
                        temp_test_complete = True
                        break
                    temp_buffer += temp_line + "\n"

            if temp_test_complete:
                lines = temp_buffer.splitlines()
                dfe_temps = []
                for line in lines:
                    val = re.findall(r"\d+\.\d+", line)
                    if val:
                        dfe_temps.append(float(val[0]))
                
                for temp in dfe_temps:
                    if temp < 20.0 or temp > 60.0:
                        write_log(log_file, f"\nERROR: Temperature {temp}C out of range!\n")
                        temp_test_complete = False
                        break
                break  # Temp test done


            # ---- Global timeout ----
            if time.time() - start_time > DDR_TIMEOUT:
                write_log(log_file, "\nERROR: Temperature test timed out\n")
                tn.close()
                return False

        except pexpect.exceptions.TIMEOUT:
            pass  # keep waiting
        except pexpect.exceptions.EOF:
            write_log(log_file, "\nERROR: Temp console closed unexpectedly\n")
            return False
    
    if temp_test_complete:
        write_log(log_file, "\n=== TEMPERATURE TEST PASS ===\n")
        return True
    else:
        write_log(log_file, "\n=== TEMPERATURE TEST FAIL ===\n")
        tn.close()
        return False
#--------------------------- IP Test Function --------------------------
def ip_test(bd_num, tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED
    flush_console(tn)

    
    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running IP test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting IP Test for Board {bd_num} ===\n")

    VIVADO_CMD = [
    XSCT_BIN,
    "fpga_boot/fpga_boot.tcl"
    ]

    # 1) Program FPGA
    print("Programming FPGA...")
    try:
        subprocess.run(VIVADO_CMD, check=True)
    except subprocess.CalledProcessError:
        print("ERROR: FPGA programming failed")
        return False
    
    DDR_FPGA_PROGRAMMED = False
    NOR_FPGA_PROGRAMMED = True  
    STRESS_FPGA_PROGRAMMED = False

    start_time = time.time()
    ip_test_complete = False
    ip_addr = None

    while True:
        try:
            line = tn.readline().strip()
            if line:
                write_log(log_file, line + "\n")

            # Match DHCP line and extract IP
            if "DHCP address assigned:" in line:
                match = re.search(r"DHCP address assigned:\s+(\d+\.\d+\.\d+\.\d+)", line)
                if match:
                    if ip_confirm_callback:
                        ip_ok = ip_confirm_callback(match.group(1))
                    else:
                        ip_ok = input(
                            f"Is this the correct IP address {match.group(1)}? (y/n): "
                        ).strip().lower() == "y"

                    if ip_ok:
                        ip_addr = match.group(1)
                        write_log(log_file, f"[PYTHON] Extracted IP: {ip_addr}\n")
                        ip_test_complete = True
                        break
                    else:
                        write_log(log_file, "[PYTHON] IP address rejected by user. Try again to assign IP.\n")
                        break
                        

            if "IP TEST FAIL" in line:
                ip_test_complete = False
                break

            if time.time() - start_time > DDR_TIMEOUT:
                write_log(log_file, "\nERROR: IP test timed out\n")
                return False

        except pexpect.exceptions.TIMEOUT:
            pass
        except pexpect.exceptions.EOF:
            write_log(log_file, "\nERROR: IP console closed unexpectedly\n")
            return False

    if not ip_test_complete or not ip_addr:
        write_log(log_file, "\n=== IP TEST FAIL ===\n")
        return False

    # ---- Ping test ----
    write_log(log_file, f"[PYTHON] Pinging {ip_addr}...\n")
    if ping_ip(ip_addr):
        write_log(log_file, f"[PYTHON] Ping successful: {ip_addr}\n")
        write_log(log_file, "\n=== IP TEST PASS ===\n")
        return True
    else:
        write_log(log_file, f"[PYTHON] Ping FAILED: {ip_addr}\n")
        write_log(log_file, "\n=== IP TEST FAIL ===\n")
        return False
#--------------------------- IBERT Test Function --------------------------
def ibert_test(bd_num, tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED

    DDR_FPGA_PROGRAMMED = False
    NOR_FPGA_PROGRAMMED = False  
    STRESS_FPGA_PROGRAMMED = False
    
    flush_console(tn)

    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running IBERT test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting IBERT Test for Board {bd_num} ===\n")

    ibert_dir = "./ibert_dfe"
    fwkProject = os.path.join(ibert_dir, "fwkProject_gen.txt")
    vivado_bin = VIVADO_BIN

    try:

        write_log(log_file, "Programming FPGA... Please wait a minute...\n")
        
        subprocess.run([
        vivado_bin,
        "-mode", "batch",
        "-source", "program_ibert.tcl"],
          cwd=ibert_dir,
          check=True
        )

        write_log(log_file, "FPGA programmed with IBERT design\n")
        print("Programming done")

        subprocess.Popen(
            [vivado_bin, "-mode", "gui"],
            cwd=ibert_dir,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            close_fds=True,
        )
 

        
    except subprocess.CalledProcessError:
        print("ERROR: IBERT project build failed")
        return False

    
    if ibert_callback:
        response = ibert_callback()
    else: 
        input("Open Hardware Manager. Press Enter to continue...")
        input("Open target FPGA and create links. Press Enter to continue...")
        input("Set Loopback mode to Near-End PMA for all links. Press Enter to continue...")
        input("Reset all links. Press Enter to continue...")
        response = input("Are all links within 2.5 Gbps (+/- 2%)? (y/n): ").strip().lower()

    if response == "y":
        write_log(log_file, "\n=== IBERT TEST PASS ===\n")
        return True
    else:        
        write_log(log_file, "\n=== IBERT TEST FAIL ===\n") 
        return False
#--------------------------- IO Test Function --------------------------
def io_test(bd_num, tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED
    flush_console(tn)

    
    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running IO test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting IO Test for Board {bd_num} ===\n")

    VIVADO_CMD = [
    XSCT_BIN,
    "fpga_boot/fpga_boot.tcl"
    ]

    if not NOR_FPGA_PROGRAMMED:
        # 1) Program FPGA
        print("Programming FPGA...")
        try:
            subprocess.run(VIVADO_CMD, check=True)
        except subprocess.CalledProcessError:
            print("ERROR: FPGA programming failed")
            return False
        DDR_FPGA_PROGRAMMED = False
        NOR_FPGA_PROGRAMMED = True  
        STRESS_FPGA_PROGRAMMED = False

    if io_callback:
        response = io_callback()
    else:
        response= input("Measure pins with multimeter. Are all pins outputting 1.8 V correctly? (y/n): ").strip().lower()

    if response == "y":
        write_log(log_file, "\n=== IO TEST PASS ===\n")
        return True
    else:
        write_log(log_file, "\n=== IO TEST FAIL ===\n")
        return False
#--------------------------- AFE Test Function --------------------------
def afe_test(bd_num, tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED

    ADCAPV = prefix + "Live:ADC:A-Wfm"
    ADCBPV = prefix + "Live:ADC:B-Wfm"
    ADCCPV = prefix + "Live:ADC:C-Wfm"
    ADCDPV = prefix + "Live:ADC:D-Wfm"

    mask = 0xFFFF

    PATTERNA = False
    PATTERN5 = False
    skip = False

    flush_console(tn)

    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running AFE test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting AFE Test for Board {bd_num} ===\n")

    VIVADO_CMD = [
    XSCT_BIN,
    "fpga_boot/fpga_boot.tcl"
    ]

    def send_menu_cmd(cmd):
        tn.send(cmd)
        # write_log(log_file, f">>> SENT MENU: {cmd}\n")

    def send_input_cmd(cmd):
        tn.sendline(cmd)
        # write_log(log_file, f">>> SENT INPUT: {cmd}\n")

    def wait_for_text(text, timeout=10):
        idx = tn.expect_exact([text, pexpect.EOF, pexpect.TIMEOUT], timeout=timeout)
        if idx == 0:
            if tn.before:
                write_log(log_file, tn.before)
            write_log(log_file, tn.after)
            return True
        if idx == 1:
            write_log(log_file, "\nERROR: AFE console closed unexpectedly\n")
            return False
        write_log(log_file, f"\nERROR: Timed out waiting for: {text}\n")
        return False

    if NOR_FPGA_PROGRAMMED:
        write_log(log_file, "[PYTHON] FPGA already programmed, skipping boot wait for AFE test.\n")
        skip = True
    else:
        print("Programming FPGA...")
        try:
            subprocess.run(VIVADO_CMD, check=True)
        except subprocess.CalledProcessError:
            print("ERROR: FPGA programming failed")
            return False
        skip = False
        DDR_FPGA_PROGRAMMED = False
        NOR_FPGA_PROGRAMMED = True
        STRESS_FPGA_PROGRAMMED = False
        
    if not skip:
    # Wait for menu/banner to appear at least once after boot.
        if not wait_for_text("FPGA successfully programmed", timeout=DDR_TIMEOUT):
            return False

    
    # Required command sequence:
    # H -> b -> G -> aaaa -> G -> 5555 -> H -> a
    mode_prompt = "Enter a or b (a = Normal Mode, b = Test Mode):"

    if afe_callback:
        response = afe_callback()
    else:
        input("\nStart IOC. Press Enter to continue...")

    
    # Enter ADC output mode selector and choose Test Mode.
    send_menu_cmd("H")
    if not wait_for_text(mode_prompt, timeout=15):
        return False
    
    time.sleep(3)

    send_input_cmd("b")
    if not wait_for_text("LTC2195 ADC Output set to Test Pattern Mode", timeout=15):
        return False

    time.sleep(3)

    # Pattern 1: AAAA
    send_menu_cmd("G")
    if not wait_for_text("Enter a test pattern (hex):", timeout=15):
        return False
    
    time.sleep(3)

    send_input_cmd("aaaa")
    if not wait_for_text("ADC Test Readback done!", timeout=20):
        return False

    time.sleep(3)  # small delay to ensure EPICS PVs are updated before reading

    dataA = epics.caget(ADCAPV, count=10)
    dataB = epics.caget(ADCBPV, count=10)
    dataC = epics.caget(ADCCPV, count=10)
    dataD = epics.caget(ADCDPV, count=10)

    A = hex(int(dataA[0]) & mask)
    B = hex(int(dataB[0]) & mask)
    C = hex(int(dataC[0]) & mask)
    D = hex(int(dataD[0]) & mask)

    write_log(log_file,"\nADC-A = " + A)
    write_log(log_file,"\nADC-B = " + B)
    write_log(log_file,"\nADC-C = " + C)
    write_log(log_file,"\nADC-D = " + D)

    if A == "0xaaaa" and B == "0xaaaa" and C == "0xaaaa" and D == "0xaaaa":
        write_log(log_file, "\nPattern 1 (0xAAAA) readback correct\n")
        PATTERNA = True
    else:
        write_log(log_file, "\nERROR: Pattern 1 (0xAAAA) readback incorrect\n")
        

    # Pattern 2: 5555
    send_menu_cmd("G")
    if not wait_for_text("Enter a test pattern (hex):", timeout=15):
        return False
    
    time.sleep(3)

    send_input_cmd("5555")
    if not wait_for_text("ADC Test Readback done!", timeout=20):
        return False

    time.sleep(3) # small delay to ensure EPICS PVs are updated before reading

    dataA = epics.caget(ADCAPV, count=10)
    dataB = epics.caget(ADCBPV, count=10)
    dataC = epics.caget(ADCCPV, count=10)
    dataD = epics.caget(ADCDPV, count=10)

    A = hex(int(dataA[0]) & mask)
    B = hex(int(dataB[0]) & mask)
    C = hex(int(dataC[0]) & mask)
    D = hex(int(dataD[0]) & mask)

    write_log(log_file,"\nADC-A = " + A)
    write_log(log_file,"\nADC-B = " + B)
    write_log(log_file,"\nADC-C = " + C)
    write_log(log_file,"\nADC-D = " + D)

    if A == "0x5555" and B == "0x5555" and C == "0x5555" and D == "0x5555":
        write_log(log_file, "\nPattern 2 (0x5555) readback correct\n")
        PATTERN5 = True
    else:
        write_log(log_file, "\nERROR: Pattern 2 (0x5555) readback incorrect\n")
    
    # Restore Normal Mode.
    send_menu_cmd("H")
    if not wait_for_text(mode_prompt, timeout=15):
        return False
    
    time.sleep(3)

    send_input_cmd("a")
    if not wait_for_text("LTC2195 ADC Output set to Normal Output Mode", timeout=15):
        return False

    time.sleep(3)

    if PATTERNA and PATTERN5:
        write_log(log_file, "\n=== AFE TEST PASS ===\n")
        return True
    else:
        write_log(log_file, "\n=== AFE TEST FAIL ===\n")
        return False
#--------------------------- Stress Test Function --------------------------
def stress_test(bd_num, tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED
    flush_console(tn)

    Prail_85PV = prefix + "Pwr:V0_85I-I"
    
    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running Stress test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting Stress Test for Board {bd_num} ===\n")

    VIVADO_CMD = [
    XSCT_BIN,
    "stress_test/stress_test.tcl"
    ]


    if not STRESS_FPGA_PROGRAMMED:
        # 1) Program FPGA
        print("Programming FPGA...")
        try:
            subprocess.run(VIVADO_CMD, check=True)
        except subprocess.CalledProcessError:
            print("ERROR: FPGA programming failed")
            return False
        DDR_FPGA_PROGRAMMED = False
        NOR_FPGA_PROGRAMMED = False  
        STRESS_FPGA_PROGRAMMED = True
    
    if stress_callback:
        response = stress_callback()
    else:
        response = input("Start the IOC. Press Enter to continue...").strip().lower()

    time.sleep(3)

    current_prail85 = epics.caget(Prail_85PV, count=10)

    write_log(log_file, f"\nCurrent on 0.85 Power Rail: {current_prail85} A\n")

    if current_prail85 > 5.0:
        write_log(log_file, "\nCurrent on 0.85 rail greater than 5 Amps under stress! Test pass.\n")
        write_log(log_file, "\n=== STRESS TEST PASS ===\n")
        return True
    else:
        write_log(log_file, "\nCurrent on 0.85 rail did not increase under stress. Test fail.\n")
        write_log(log_file, "\n=== STRESS TEST FAIL ===\n")
        return False




# ----------------------------- Main Function ----------------------------
def main():
    # bd_num = input("Enter the board number: ").strip()
    # print(f"Board number entered: {bd_num}")
    bd_num = "01"  # hardcoded for now since we only have one board, can re-enable input later when we have more boards to test

    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    open(log_file, "w").close()  # clear previous log

    tn = open_telnet()
    results = {}

    # Keep default behavior: run AFE only. Add other tests here when needed.
    test_plan = [
        ("AFE TEST", afe_test),
    ]

    try:
        for test_name, test_fn in test_plan:
            try:
                results[test_name] = bool(test_fn(bd_num, tn))
            except Exception as exc:
                results[test_name] = False
                write_log(log_file, f"\nERROR: {test_name} raised exception: {exc}\n")
    finally:
        print("Closing Telnet connection...")
        tn.close()

    print("\n===== TEST SUMMARY =====")
    print(f"Board Number : {bd_num}")

    for test_name, passed in results.items():
        print(f"{test_name:<16}: {'PASS' if passed else 'FAIL'}")

    fail = any(not passed for passed in results.values())

    if not fail:
        print("\nALL TESTS PASSED!")
    else:
        print("\nSOME TESTS FAILED. PLEASE REVIEW THE LOGS.")
    
    sys.exit(0 if not fail else 1)


# ----------------------------- Entry Point -----------------------------
if __name__ == "__main__":
    main()
