import subprocess
import pexpect
import sys
import os
import time
import re
import pyvisa

# ----------------------------- Configuration -----------------------------
SERIAL_HOST = "10.0.142.108"
SERIAL_PORT = 4027
SMB100B_IP = "10.0.142.183"

LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)

DDR_TIMEOUT = 120  # seconds

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
        timeout=1
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
afe_pwr_callback = None
stress_callback = None
# --------------------------- Global Variables --------------------------
DDR_FPGA_PROGRAMMED = False
NOR_FPGA_PROGRAMMED = False
STRESS_FPGA_PROGRAMMED = False

class SMB100B:
    def __init__(self, resource_name: str):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(resource_name)
        self.inst.timeout = 5000

    def query(self, cmd: str) -> str:
        return self.inst.query(cmd).strip()

    def write(self, cmd: str) -> None:
        self.inst.write(cmd)

    def identify(self) -> str:
        return self.query("*IDN?")

    def reset(self) -> None:
        self.write("*RST")
        self.write("*CLS")

    def set_frequency(self, freq_hz: float) -> None:
        self.write(f"FREQ {freq_hz}")

    def set_power_dbm(self, power_dbm: float) -> None:
        self.write(f"POW {power_dbm}")

    def output_on(self) -> None:
        self.write("OUTP ON")

    def output_off(self) -> None:
        self.write("OUTP OFF")

    def close(self) -> None:
        try:
            self.inst.close()
        finally:
            self.rm.close()
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
                            check=True
                        )
            print("QSPI flash script completed")
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
    "/tools/Xilinx/Vitis/2022.2/bin/xsct",
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
    "/tools/Xilinx/Vitis/2022.2/bin/xsct",
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
    "/tools/Xilinx/Vitis/2022.2/bin/xsct",
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

    try:

        
        env = os.environ.copy()
        env["FWK_VIVADO_JOBS"] = "16"

        if not os.path.exists(fwkProject):
            try: 
                subprocess.run(
                    ["make", "cfg=hw", "project"],
                    cwd=ibert_dir,
                    check=True
                )

                time.sleep(2)  # small delay to ensure build is fully done

                subprocess.run(
                    ["make", "cfg=hw", "build"],
                    cwd=ibert_dir,
                    env=env,
                    check=True
                )

                time.sleep(2) 

                with open(fwkProject, "a") as f:
                    f.write("SUCCESS\n")

            except subprocess.CalledProcessError:
                print("ERROR: IBERT project build failed")
                return False

        write_log(log_file, "Programming FPGA... Please wait a minute...\n")
        
        subprocess.run([
        "vivado",
        "-mode", "batch",
        "-source", "program_ibert.tcl"],
          cwd=ibert_dir,
          check=True
        )

        write_log(log_file, "FPGA programmed with IBERT design\n")
        print("Programming done")

        subprocess.Popen(
            [
                "xterm",
                "-hold",
                "-e",
                f"cd {ibert_dir} && make cfg=hw gui"
            ]
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
    "/tools/Xilinx/Vitis/2022.2/bin/xsct",
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

    SMB100B_RESOURCE = f"TCPIP0::{SMB100B_IP}::inst0::INSTR"
    
    # Timing
    SETTLE_TIME_SEC = 10.0
    RF_OFF_AT_END = True
    
    flush_console(tn)

    
    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running AFE test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting AFE Test for Board {bd_num} ===\n")

    VIVADO_CMD = [
    "/tools/Xilinx/Vitis/2022.2/bin/xsct",
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
    
    powers = [0, 12]

    gen = SMB100B(SMB100B_RESOURCE)

    if NOR_FPGA_PROGRAMMED:
        write_log(log_file, "[PYTHON] FPGA already programmed, skipping boot wait for AFE test.\n")
    else:
        start_time = time.time()
        while True:
            try:
                line = tn.readline().strip()
                if line:
                    write_log(log_file, line + "\n")

                if "FPGA successfully programmed" in line:
                    break

                if time.time() - start_time > DDR_TIMEOUT:
                    write_log(log_file, "\nERROR: AFE boot wait timed out\n")
                    return False

            except pexpect.exceptions.TIMEOUT:
                pass
            except pexpect.exceptions.EOF:
                write_log(log_file, "\nERROR: AFE console closed unexpectedly\n")
                return False

    time.sleep(5)
    
    if afe_callback:
        response = afe_callback()
        gen.set_frequency(200e6)
        gen.set_power_dbm(0.0)
        gen.output_on()

        Pass = True
        for pwr in powers:
            print(f"\nSetting SMB100B power to {pwr:.1f} dBm")
            gen.set_power_dbm(pwr)
            time.sleep(SETTLE_TIME_SEC)


            confirm = afe_pwr_callback(pwr)
            if confirm == "y":
                print("Confirmed channels changed levels.")
            else:
                Pass = False
                print("Channels did NOT change levels. Check connections and settings.")
    else:
            input("Start IOC and open Phoebus GUI. Press Enter to continue...")
            input("Set RF Attenuation to 0 dB in Phoebus. Press Enter to continue...")
            input("Set Trigger source to External and Event Source to EVR in Phoebus. Press Enter to continue...")
            input("View the SA Waveform Data in Phoebus. Press Enter to continue...")
            print("Connected to:", gen.identify())

            # Optional reset
            # gen.reset()
            # time.sleep(1)

            gen.set_frequency(200e6)
            gen.set_power_dbm(0.0)
            gen.output_on()

            Pass = True
            for pwr in powers:
                print(f"\nSetting SMB100B power to {pwr:.1f} dBm")
                gen.set_power_dbm(pwr)
                time.sleep(SETTLE_TIME_SEC)


                confirm = input("Determine if channels changed levels. (y/n): ").strip().lower()
                if confirm == "y":
                    print("Confirmed channels changed levels.")
                else:
                    Pass = False
                    print("Channels did NOT change levels. Check connections and settings.")
            
    if RF_OFF_AT_END:
        try:
            gen.output_off()
        except Exception:
            pass
    gen.close()

    if Pass:
        write_log(log_file, "\n=== AFE TEST PASS ===\n")
        return True
    else:
        write_log(log_file, "\n=== AFE TEST FAIL ===\n")
        return False
#--------------------------- Stress Test Function --------------------------
def stress_test(bd_num, tn):
    global DDR_FPGA_PROGRAMMED, NOR_FPGA_PROGRAMMED, STRESS_FPGA_PROGRAMMED
    flush_console(tn)

    
    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    print(f"\n=== Running Stress test on board {bd_num} ===")
    write_log(log_file, f"\n=== Starting Stress Test for Board {bd_num} ===\n")

    VIVADO_CMD = [
    "/tools/Xilinx/Vitis/2022.2/bin/xsct",
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
        response = input("Open Phoebus GUI and determine if the current for 0.85V rail is above 5 Amps. (y/n): ").strip().lower()

    if response.strip().lower() == "y":
        write_log(log_file, "\n=== STRESS TEST PASS ===\n")
        return True
    else:
        write_log(log_file, "\n=== STRESS TEST FAIL ===\n")
        return False


# ----------------------------- Main Function ----------------------------
def main():
    bd_num = input("Enter the board number: ").strip()
    print(f"Board number entered: {bd_num}")

    log_file = os.path.join(LOG_DIR, f"zudfe_s{bd_num}.log")
    open(log_file, "w").close()  # clear previous log

    tn = open_telnet()
    FAIL = False

    try:
        # DDR_TEST = ddr_test(bd_num, tn)
        # SD_TEST = sd_test(bd_num, tn)
        # TEMP_TEST = temp_test(bd_num, tn)
        # IP_TEST = ip_test(bd_num, tn)
        # IBERT_TEST = ibert_test(bd_num, tn)
        AFE_TEST = afe_test(bd_num, tn)
        # STRESS_TEST = stress_test(bd_num, tn)


        # if not DDR_TEST:
        #     FAIL = True
        # if not TEMP_TEST:
        #     FAIL = True
        # if not IP_TEST:
        #     FAIL = True
        # if not IBERT_TEST:
        #     FAIL = True
        if not AFE_TEST:
            FAIL = True
        # if not STRESS_TEST:
        #     FAIL = True   
    finally:
        print("Closing Telnet connection...")
        tn.close()

    print("\n===== TEST SUMMARY =====")
    print(f"Board Number : {bd_num}")
    # print(f"DDR TEST     : {'PASS' if DDR_TEST else 'FAIL'}")
    # print(f"TEMPERATURE TEST : {'PASS' if TEMP_TEST else 'FAIL'}")
    # print(f"IP TEST      : {'PASS' if IP_TEST else 'FAIL'}")
    # print(f"IBERT TEST    : {'PASS' if IBERT_TEST else 'FAIL'}")

    if not FAIL:
        print("\nALL TESTS PASSED!")
    else:
        print("\nSOME TESTS FAILED. PLEASE REVIEW THE LOGS.")
    
    sys.exit(0 if not FAIL else 1)


# ----------------------------- Entry Point -----------------------------
if __name__ == "__main__":
    main()
