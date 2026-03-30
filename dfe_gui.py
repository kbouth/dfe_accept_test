import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter import messagebox
import threading
import time
from datetime import datetime
import csv
import os

import dfe_test


class TestGUI:
    def __init__(self, root):
        self.root = root
        root.title("ZuDFE Test Station")

        self.data_file = "test_results.csv"
        self.previous_board = None  # Track board changes to reset FPGA state
        self.active_board = None
        self.ip_address = ""
        self.ip_address_var = tk.StringVar(value="ZYNQ+ IP:         -")
        # ---------- Main Layout Frames ----------

        top_frame = tk.Frame(root, pady=5)
        top_frame.pack(fill="x")


        table_frame = tk.Frame(root, pady=5)
        table_frame.pack(fill="both", expand=True)

        log_frame = tk.Frame(root, pady=5)
        log_frame.pack(fill="both", expand=True)

        # ---------- Top Controls ----------

        top_frame.grid_columnconfigure(1, weight=1)

        control_frame = tk.Frame(top_frame)
        control_frame.grid(row=0, column=0, sticky="nw", padx=(8, 12))

        control_frame.grid_columnconfigure(1, weight=1)

        tk.Label(control_frame, text="Board Number").grid(
            row=0, column=0, padx=(0, 8), pady=3, sticky="w"
        )

        self.board = tk.Entry(control_frame, width=18)
        self.board.grid(row=0, column=1, padx=(0, 8), pady=3, sticky="ew")

        tk.Button(
            control_frame, text="RUN ALL", width=10,
            command=self.run_all
        ).grid(row=0, column=2, padx=(0, 4), pady=3, sticky="w")

        tk.Label(control_frame, text="JTAG IP").grid(
            row=1, column=0, padx=(0, 8), pady=3, sticky="w"
        )

        self.jtag_ip = tk.Entry(control_frame, width=18)
        self.jtag_ip.grid(row=1, column=1, padx=(0, 8), pady=3, sticky="ew")
        self._load_jtag_ip()

        tk.Button(
            control_frame, text="Save IP", width=10,
            command=self._save_jtag_ip
        ).grid(row=1, column=2, padx=(0, 4), pady=3, sticky="w")

        tk.Label(control_frame, text="Serial Host").grid(
            row=2, column=0, padx=(0, 8), pady=3, sticky="w"
        )

        self.serial_host = tk.Entry(control_frame, width=18)
        self.serial_host.grid(row=2, column=1, padx=(0, 8), pady=3, sticky="ew")
        self.serial_host.insert(0, dfe_test.SERIAL_HOST)

        tk.Label(control_frame, text="Serial Port").grid(
            row=2, column=2, padx=(8, 8), pady=3, sticky="w"
        )

        self.serial_port = tk.Entry(control_frame, width=8)
        self.serial_port.grid(row=2, column=3, padx=(0, 4), pady=3, sticky="w")
        self.serial_port.insert(0, str(dfe_test.SERIAL_PORT))

        tk.Label(control_frame, text="SMB100B IP").grid(
            row=3, column=0, padx=(0, 8), pady=3, sticky="w"
        )

        self.smb100b_ip = tk.Entry(control_frame, width=18)
        self.smb100b_ip.grid(row=3, column=1, padx=(0, 8), pady=3, sticky="ew")
        self.smb100b_ip.insert(0, dfe_test.SMB100B_IP)

        tk.Label(control_frame, textvariable=self.ip_address_var).grid(
            row=4, column=0, columnspan=4, padx=(0, 0), pady=3, sticky="w"
        )

        # ---------- Buttons + Status Lights (Aligned) ----------

        button_frame = tk.Frame(top_frame)
        button_frame.grid(row=0, column=1, sticky="nw", padx=(8, 10))

        self.status = {}

        buttons = ["DDR","TEMP","IP","IBERT","SD","QSPI","IO","AFE","STRESS"]

        for i, name in enumerate(buttons):

            # Test Button (Row 0)
            tk.Button(
                button_frame,
                text=name,
                width=8,
                command=lambda n=name: self.run_single(n)
            ).grid(row=0, column=i, padx=3)

            # Status Light (Row 1)
            lbl = tk.Label(
                button_frame,
                text=" ",
                bg="gray",
                width=8,
                height=1,
                relief="sunken"
            )
            lbl.grid(row=1, column=i, padx=3, pady=(2,0))

            self.status[name] = lbl

        # ----------------- Results Table -----------------

        columns = (
            "Board",
            "DDR", "TEMP", "IP", "IBERT",
            "SD", "QSPI", "IO", "AFE", "STRESS",
            "ZYNQ_IP", "Overall", "Date", "Time"
        )

        self.table = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=80, anchor="center")

        # ---------- Results Table ----------

        self.table.pack(
            in_=table_frame,
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )


        # Map board number -> row ID
        self.board_rows = {}

        # Store latest results per board
        self.results = {}
        self.detected_ips = {}

        # ----------------- Log Window -----------------

        self.log = scrolledtext.ScrolledText(
            root, width=90, height=16
        )
        # ---------- Log Window ----------

        tk.Label(
            log_frame,
            text="Test Log",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=10)

        self.log.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )


        dfe_test.log_callback = self.append_log
        dfe_test.ip_confirm_callback = self.ask_ip_confirm
        dfe_test.ibert_callback = self.ibert_confirmation
        dfe_test.sd_callback = self.sd_confirmation
        dfe_test.qspi_callback = self.qspi_confirmation
        dfe_test.io_callback = self.io_confirmation
        dfe_test.afe_callback = self.afe_confirmation
        dfe_test.afe_pwr_callback = self.afe_pwr_confirmation
        dfe_test.stress_callback = self.stress_confirmation


        self.load_results()

        # Allow resizing
        root.minsize(1100, 700)



    # --------------------------------------------------

    def append_log(self, text):
        self.root.after(
            0,
            lambda: (
                self.log.insert(tk.END, text),
                self.log.see(tk.END)
            )
        )

    # --------------------------------------------------

    def load_results(self):

        if not os.path.exists(self.data_file):
            return

        with open(self.data_file, newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:

                bd = row["Board"]

                # Restore results dict
                self.results[bd] = {
                    "DDR": row["DDR"] == "PASS",
                    "TEMP": row["TEMP"] == "PASS",
                    "IP": row["IP"] == "PASS",
                    "IBERT": row["IBERT"] == "PASS",
                    "SD": row["SD"] == "PASS",
                    "QSPI": row["QSPI"] == "PASS",
                    "IO": row["IO"] == "PASS",
                    "AFE": row["AFE"] == "PASS",
                    "STRESS": row["STRESS"] == "PASS",
                }

                zynq_ip = row.get("ZYNQ_IP", "")
                if zynq_ip and zynq_ip != "-":
                    self.detected_ips[bd] = zynq_ip



                # Restore table
                vals = (
                    row["Board"],
                    row["DDR"],
                    row["TEMP"],
                    row["IP"],
                    row["IBERT"],
                    row["SD"],
                    row["QSPI"],
                    row["IO"],
                    row["AFE"],
                    row["STRESS"],
                    row.get("ZYNQ_IP", "-"),
                    row["Overall"],
                    row["Date"],
                    row["Time"]
                )



                rid = self.table.insert("", tk.END, values=vals)
                self.board_rows[bd] = rid

# --------------------------------------------------

    def save_results(self):

        with open(self.data_file, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                "Board",
                "DDR", "TEMP", "IP", "IBERT",
                "SD", "QSPI", "IO", "AFE", "STRESS",
                "ZYNQ_IP", "Overall", "Date", "Time"
            ])



            for bd, rid in self.board_rows.items():

                vals = self.table.item(rid)["values"]

                writer.writerow(vals)

    # --------------------------------------------------

    def set_status(self, name, passed):

        color = "green" if passed else "red"

        self.root.after(
            0,
            lambda: self.status[name].config(bg=color)
        )

    # --------------------------------------------------

    def update_table(self, board):

        res = self.results.get(board, {})

        ddr = res.get("DDR")
        temp = res.get("TEMP")
        ip = res.get("IP")
        ibert = res.get("IBERT")
        sd = res.get("SD")
        qspi = res.get("QSPI")
        io = res.get("IO")
        afe = res.get("AFE")
        stress = res.get("STRESS")
        zynq_ip = self.detected_ips.get(board, "-")



        def fmt(v):
            if v is None:
                return "-"
            return "PASS" if v else "FAIL"

        tests = [ddr, temp, ip, ibert, sd, qspi, io, afe, stress]
        
        overall = (
            "PASS"
            if all(v is True for v in tests)
            else "FAIL"
            if any(v is False for v in tests)
            else "-"
        )

        now = datetime.now()

        date = now.strftime("%Y-%m-%d")
        time_s = now.strftime("%H:%M:%S")

        vals = (
            board,
            fmt(ddr),
            fmt(temp),
            fmt(ip),
            fmt(ibert),
            fmt(sd),
            fmt(qspi),
            fmt(io),
            fmt(afe),
            fmt(stress),
            zynq_ip,
            overall,
            date,
            time_s
        )



        def _update():

            if board in self.board_rows:
                rid = self.board_rows[board]
                self.table.item(rid, values=vals)

            else:
                rid = self.table.insert("", tk.END, values=vals)
                self.board_rows[board] = rid

            self.save_results()

        self.root.after(0, _update)

    # --------------------------------------------------

    def _load_jtag_ip(self):
        cfg = os.path.join(os.path.dirname(__file__), "jtag_ip.cfg")
        if os.path.exists(cfg):
            with open(cfg) as f:
                ip = f.read().strip()
            self.jtag_ip.delete(0, tk.END)
            self.jtag_ip.insert(0, ip)

    def _save_jtag_ip(self):
        ip = self.jtag_ip.get().strip()
        if not ip:
            messagebox.showerror("Error", "JTAG IP address cannot be empty.")
            return
        cfg = os.path.join(os.path.dirname(__file__), "jtag_ip.cfg")
        with open(cfg, "w") as f:
            f.write(ip)
        self.append_log(f"JTAG IP saved: {ip}\n")

    def _apply_serial_settings(self):
        host = self.serial_host.get().strip()
        port_text = self.serial_port.get().strip()
        smb100b_ip = self.smb100b_ip.get().strip()

        if not host:
            self.append_log("ERROR: Serial host cannot be empty\n")
            return False

        if not smb100b_ip:
            self.append_log("ERROR: SMB100B IP cannot be empty\n")
            return False

        try:
            port = int(port_text)
        except ValueError:
            self.append_log("ERROR: Serial port must be an integer\n")
            return False

        dfe_test.SERIAL_HOST = host
        dfe_test.SERIAL_PORT = port
        dfe_test.SMB100B_IP = smb100b_ip
        return True

    # --------------------------------------------------

    def reset_status(self):

        for s in self.status.values():
            s.config(bg="gray")

    # --------------------------------------------------

    def get_board(self):

        bd = self.board.get().strip()

        if not bd:
            self.append_log("ERROR: Enter board number\n")
            return None

        if not self._apply_serial_settings():
            return None

        # Reset FPGA programming state only if board number changed
        if bd != self.previous_board:
            dfe_test.DDR_FPGA_PROGRAMMED = False
            dfe_test.NOR_FPGA_PROGRAMMED = False
            dfe_test.STRESS_FPGA_PROGRAMMED = False
            self.previous_board = bd

        return bd

    # --------------------------------------------------

    def run_all(self):

        bd = self.get_board()

        if not bd:
            return

        self.reset_status()
        self.log.delete("1.0", tk.END)

        t = threading.Thread(
            target=self._run_all_tests,
            args=(bd,),
            daemon=True
        )
        t.start()

    # --------------------------------------------------

    def run_single(self, test):

        bd = self.get_board()

        if not bd:
            return

        t = threading.Thread(
            target=self._run_single_test,
            args=(bd, test),
            daemon=True
        )
        t.start()

    # --------------------------------------------------

    def _run_all_tests(self, bd):
        self.active_board = bd

        tn = dfe_test.open_telnet()

        try:
            ddr = dfe_test.ddr_test(bd, tn)
            self.results.setdefault(bd, {})["DDR"] = ddr
            self.set_status("DDR", ddr)

            temp = dfe_test.temp_test(bd, tn)
            self.results.setdefault(bd, {})["TEMP"] = temp
            self.set_status("TEMP", temp)

            ip = dfe_test.ip_test(bd, tn)
            self.results.setdefault(bd, {})["IP"] = ip
            self.set_status("IP", ip)

            ibert = dfe_test.ibert_test(bd, tn)
            self.results.setdefault(bd, {})["IBERT"] = ibert
            self.set_status("IBERT", ibert)

            sd = dfe_test.sd_test(bd, tn)
            self.results.setdefault(bd, {})["SD"] = sd
            self.set_status("SD", sd)

            qspi = dfe_test.qspi_test(bd, tn)
            self.results.setdefault(bd, {})["QSPI"] = qspi
            self.set_status("QSPI", qspi)

            io = dfe_test.io_test(bd, tn)
            self.results.setdefault(bd, {})["IO"] = io
            self.set_status("IO", io)

            afe = dfe_test.afe_test(bd, tn)
            self.results.setdefault(bd, {})["AFE"] = afe
            self.set_status("AFE", afe)

            stress = dfe_test.stress_test(bd, tn)
            self.results.setdefault(bd, {})["STRESS"] = stress
            self.set_status("STRESS", stress)



            self.update_table(bd)

            self.append_log("\nALL TESTS COMPLETE\n")

        finally:
            if self.active_board == bd:
                self.active_board = None
            tn.close()

    # --------------------------------------------------

    def _run_single_test(self, bd, test):
        self.active_board = bd

        tn = dfe_test.open_telnet()

        try:

            if test == "DDR":
                res = dfe_test.ddr_test(bd, tn)

            elif test == "TEMP":
                res = dfe_test.temp_test(bd, tn)

            elif test == "IP":
                res = dfe_test.ip_test(bd, tn)

            elif test == "IBERT":
                res = dfe_test.ibert_test(bd, tn)

            elif test == "SD":
                res = dfe_test.sd_test(bd, tn)

            elif test == "QSPI":
                res = dfe_test.qspi_test(bd, tn)

            elif test == "IO":
                res = dfe_test.io_test(bd, tn)
            
            elif test == "AFE":
                res = dfe_test.afe_test(bd, tn)

            elif test == "STRESS":
                res = dfe_test.stress_test(bd, tn)
            else:
                return

            self.results.setdefault(bd, {})[test] = res

            self.set_status(test, res)

            self.update_table(bd)

            self.append_log(f"\n{test} TEST COMPLETE\n")

        finally:
            if self.active_board == bd:
                self.active_board = None
            tn.close()
    
    def ask_ip_confirm(self, ip):

        done = threading.Event()
        result = {"value": False}

        def show_popup():

            win = tk.Toplevel(self.root)
            win.title("Confirm IP Address")
            win.grab_set()
            win.resizable(False, False)

            tk.Label(
                win,
                text=f"Is this the correct IP address?\n\n{ip}",
                font=("Arial", 12)
            ).pack(padx=20, pady=15)

            btn_frame = tk.Frame(win)
            btn_frame.pack(pady=10)

            def yes():
                result["value"] = True
                self.ip_address = ip
                self.ip_address_var.set(f"ZYNQ+ IP:         {ip}")
                if self.active_board:
                    self.detected_ips[self.active_board] = ip
                    self.update_table(self.active_board)
                done.set()
                win.destroy()

            def no():
                result["value"] = False
                done.set()
                win.destroy()

            tk.Button(
                btn_frame, text="Yes", width=10, command=yes
            ).pack(side="left", padx=10)

            tk.Button(
                btn_frame, text="No", width=10, command=no
            ).pack(side="right", padx=10)

        # Run popup in GUI thread
        self.root.after(0, show_popup)

        # BLOCK test thread until user answers
        done.wait()

        return result["value"]
    
    def ibert_confirmation(self):

        done = threading.Event()
        result = {"value": False}

        steps = [
            "Open Vivado Hardware Manager.",
            "Open the target FPGA.",
            "Create links.",
            "Set Loopback Mode to: Near-End PMA.",
            "Reset all links.",
            "Verify all links are within 2.5 Gbps (±2%)."
        ]

        def show_popup():

            win = tk.Toplevel(self.root)
            win.title("IBERT Test Wizard")
            win.grab_set()
            win.resizable(False, False)

            # Center window
            w, h = 500, 220
            x = (win.winfo_screenwidth() // 2) - (w // 2)
            y = (win.winfo_screenheight() // 2) - (h // 2)
            win.geometry(f"{w}x{h}+{x}+{y}")

            step_index = tk.IntVar(value=0)

            title_lbl = tk.Label(
                win,
                text="IBERT Setup Step",
                font=("Arial", 14, "bold")
            )
            title_lbl.pack(pady=8)

            step_lbl = tk.Label(
                win,
                text="",
                font=("Arial", 12),
                wraplength=460,
                justify="center"
            )
            step_lbl.pack(pady=20)

            nav_frame = tk.Frame(win)
            nav_frame.pack(pady=10)

            def update_step():
                i = step_index.get()

                step_lbl.config(
                    text=f"Step {i+1} of {len(steps)}\n\n{steps[i]}"
                )

                back_btn["state"] = "normal" if i > 0 else "disabled"

                if i == len(steps) - 1:
                    next_btn.pack_forget()
                    pass_btn.pack(side="left", padx=15)
                    fail_btn.pack(side="right", padx=15)
                else:
                    pass_btn.pack_forget()
                    fail_btn.pack_forget()
                    next_btn.pack(side="right", padx=15)

            def next_step():
                step_index.set(step_index.get() + 1)
                update_step()

            def prev_step():
                step_index.set(step_index.get() - 1)
                update_step()

            def pass_test():
                result["value"] = "y"
                done.set()
                win.destroy()

            def fail_test():
                result["value"] = "n"
                done.set()
                win.destroy()

            back_btn = tk.Button(
                nav_frame,
                text="Back",
                width=10,
                command=prev_step
            )

            next_btn = tk.Button(
                nav_frame,
                text="Next",
                width=10,
                command=next_step
            )

            pass_btn = tk.Button(
                nav_frame,
                text="PASS",
                width=10,
                bg="#4CAF50",
                fg="white",
                command=pass_test
            )

            fail_btn = tk.Button(
                nav_frame,
                text="FAIL",
                width=10,
                bg="#F44336",
                fg="white",
                command=fail_test
            )

            back_btn.pack(side="left", padx=15)

            update_step()

            win.protocol("WM_DELETE_WINDOW", fail_test)

        # Run popup in GUI thread
        self.root.after(0, show_popup)

        done.wait()

        return result["value"]
    
    def sd_confirmation(self):

        done = threading.Event()
        result = {"value": False}

        steps = [
            "Insert the SD Card into the empty SD slot (SW1).",
            "Set BOOT Mode () to SD (0101).",
            "Power cycle the FPGA. Press close to continue."
        ]

        def show_popup():

            win = tk.Toplevel(self.root)
            win.title("SD Boot Test Wizard")
            win.grab_set()
            win.resizable(False, False)

            # Center window
            w, h = 500, 220
            x = (win.winfo_screenwidth() // 2) - (w // 2)
            y = (win.winfo_screenheight() // 2) - (h // 2)
            win.geometry(f"{w}x{h}+{x}+{y}")

            step_index = tk.IntVar(value=0)

            title_lbl = tk.Label(
                win,
                text="SD Boot Step",
                font=("Arial", 14, "bold")
            )
            title_lbl.pack(pady=8)

            step_lbl = tk.Label(
                win,
                text="",
                font=("Arial", 12),
                wraplength=460,
                justify="center"
            )
            step_lbl.pack(pady=20)

            nav_frame = tk.Frame(win)
            nav_frame.pack(pady=10)

            def update_step():
                i = step_index.get()

                step_lbl.config(
                    text=f"Step {i+1} of {len(steps)}\n\n{steps[i]}"
                )

                back_btn["state"] = "normal" if i > 0 else "disabled"

                if i == len(steps) - 1:
                    next_btn.pack_forget()
                    close_btn.pack(side="right", padx=15)
                else:
                    close_btn.pack_forget()
                    next_btn.pack(side="right", padx=15)

            def next_step():
                step_index.set(step_index.get() + 1)
                update_step()

            def prev_step():
                step_index.set(step_index.get() - 1)
                update_step()

            def close():
                done.set()
                win.destroy()

            back_btn = tk.Button(
                nav_frame,
                text="Back",
                width=10,
                command=prev_step
            )

            next_btn = tk.Button(
                nav_frame,
                text="Next",
                width=10,
                command=next_step
            )

            close_btn = tk.Button(
                nav_frame,
                text="Close",
                width=10,
                bg="#ACACAC",
                fg="black",
                command=close
            )

            back_btn.pack(side="left", padx=15)

            update_step()

            win.protocol("WM_DELETE_WINDOW", close)

        # Run popup in GUI thread
        self.root.after(0, show_popup)

        done.wait()

        return result["value"]

    def qspi_confirmation(self):

        done = threading.Event()
        result = {"value": False}

        steps = [
            "Switch BOOT Mode to QSPI (0001).",
            "Power cycle the FPGA. Press close to continue."
        ]

        def show_popup():

            win = tk.Toplevel(self.root)
            win.title("QSPI Boot Test Wizard")
            win.grab_set()
            win.resizable(False, False)

            # Center window
            w, h = 500, 220
            x = (win.winfo_screenwidth() // 2) - (w // 2)
            y = (win.winfo_screenheight() // 2) - (h // 2)
            win.geometry(f"{w}x{h}+{x}+{y}")

            step_index = tk.IntVar(value=0)

            title_lbl = tk.Label(
                win,
                text="QSPI Boot Step",
                font=("Arial", 14, "bold")
            )
            title_lbl.pack(pady=8)

            step_lbl = tk.Label(
                win,
                text="",
                font=("Arial", 12),
                wraplength=460,
                justify="center"
            )
            step_lbl.pack(pady=20)

            nav_frame = tk.Frame(win)
            nav_frame.pack(pady=10)

            def update_step():
                i = step_index.get()

                step_lbl.config(
                    text=f"Step {i+1} of {len(steps)}\n\n{steps[i]}"
                )

                back_btn["state"] = "normal" if i > 0 else "disabled"

                if i == len(steps) - 1:
                    next_btn.pack_forget()
                    close_btn.pack(side="right", padx=15)
                else:
                    close_btn.pack_forget()
                    next_btn.pack(side="right", padx=15)

            def next_step():
                step_index.set(step_index.get() + 1)
                update_step()

            def prev_step():
                step_index.set(step_index.get() - 1)
                update_step()

            def close():
                done.set()
                win.destroy()

            back_btn = tk.Button(
                nav_frame,
                text="Back",
                width=10,
                command=prev_step
            )

            next_btn = tk.Button(
                nav_frame,
                text="Next",
                width=10,
                command=next_step
            )

            close_btn = tk.Button(
                nav_frame,
                text="Close",
                width=10,
                bg="#ACACAC",
                fg="black",
                command=close
            )

            back_btn.pack(side="left", padx=15)

            update_step()

            win.protocol("WM_DELETE_WINDOW", close)

        # Run popup in GUI thread
        self.root.after(0, show_popup)

        done.wait()

        return result["value"]

    def io_confirmation(self):
        
        done = threading.Event()
        result = {"value": False}

        def show_popup():

            win = tk.Toplevel(self.root)
            win.title("IO Test Confirmation")
            win.grab_set()
            win.resizable(False, False)

            tk.Label(
                win,
                text="Measure pins with multimeter. Are all pins outputting 1.8 V correctly?",
                font=("Arial", 12),
                wraplength=400,
                justify="center"
            ).pack(padx=20, pady=15)

            btn_frame = tk.Frame(win)
            btn_frame.pack(pady=10)

            def yes():
                result["value"] = "y"
                done.set()
                win.destroy()

            def no():
                result["value"] = "n"
                done.set()
                win.destroy()

            tk.Button(
                btn_frame, text="Yes", width=10, command=yes
            ).pack(side="left", padx=10)

            tk.Button(
                btn_frame, text="No", width=10, command=no
            ).pack(side="right", padx=10)

        # Run popup in GUI thread
        self.root.after(0, show_popup)

        done.wait()

        return result["value"]
    
    def afe_confirmation(self):
        done = threading.Event()
        result = {"value": False}

        # Build steps: first is "open Phoebus", then confirmation for each power level
        steps = [
            "Start IOC and open Phoebus GUI.",
            "Set RF Attenuation to 0 dB in Phoebus.",
            "Set Trigger source to External and Event Source to EVR in Phoebus.",
            "View the SA Waveform Data in Phoebus."
        ]

        def show_popup():

            win = tk.Toplevel(self.root)
            win.title("AFE Test Setup")
            win.grab_set()
            win.resizable(False, False)

            # Center window
            w, h = 500, 220
            x = (win.winfo_screenwidth() // 2) - (w // 2)
            y = (win.winfo_screenheight() // 2) - (h // 2)
            win.geometry(f"{w}x{h}+{x}+{y}")

            step_index = tk.IntVar(value=0)

            title_lbl = tk.Label(
                win,
                text="AFE Test Setup",
                font=("Arial", 14, "bold")
            )
            title_lbl.pack(pady=8)

            step_lbl = tk.Label(
                win,
                text="",
                font=("Arial", 12),
                wraplength=460,
                justify="center"
            )
            step_lbl.pack(pady=20)

            nav_frame = tk.Frame(win)
            nav_frame.pack(pady=10)

            def update_step():
                i = step_index.get()

                step_lbl.config(
                    text=f"Step {i+1} of {len(steps)}\n\n{steps[i]}"
                )

                back_btn["state"] = "normal" if i > 0 else "disabled"

                if i == len(steps) - 1:
                    next_btn.pack_forget()
                    close_btn.pack(side="right", padx=15)
                else:
                    close_btn.pack_forget()
                    next_btn.pack(side="right", padx=15)

            def next_step():
                step_index.set(step_index.get() + 1)
                update_step()

            def prev_step():
                step_index.set(step_index.get() - 1)
                update_step()

            def close():
                done.set()
                win.destroy()

            back_btn = tk.Button(
                nav_frame,
                text="Back",
                width=10,
                command=prev_step
            )

            next_btn = tk.Button(
                nav_frame,
                text="Next",
                width=10,
                command=next_step
            )

            close_btn = tk.Button(
                nav_frame,
                text="Close",
                width=10,
                bg="#ACACAC",
                fg="black",
                command=close
            )

            back_btn.pack(side="left", padx=15)

            update_step()

            win.protocol("WM_DELETE_WINDOW", close)

        # Run popup in GUI thread
        self.root.after(0, show_popup)

        done.wait()

        return result["value"]
    

    def afe_pwr_confirmation(self, pwr):
        done = threading.Event()
        result = {"value": False}

        def show_popup():

            win = tk.Toplevel(self.root)
            win.title("AFE Test Confirmation")
            win.grab_set()
            win.resizable(False, False)

            tk.Label(
                win,
                text=f"Power = {pwr} dBm. Determine if channels changed levels.",
                font=("Arial", 12),
                wraplength=400,
                justify="center"
            ).pack(padx=20, pady=15)

            btn_frame = tk.Frame(win)
            btn_frame.pack(pady=10)

            def yes():
                result["value"] = "y"
                done.set()
                win.destroy()

            def no():
                result["value"] = "n"
                done.set()
                win.destroy()

            tk.Button(
                btn_frame, text="Yes", width=10, command=yes
            ).pack(side="left", padx=10)

            tk.Button(
                btn_frame, text="No", width=10, command=no
            ).pack(side="right", padx=10)

        # Run popup in GUI thread
        self.root.after(0, show_popup)

        done.wait()

        return result["value"]

    
    def stress_confirmation(self):
        
        done = threading.Event()
        result = {"value": False}

        def show_popup():

            win = tk.Toplevel(self.root)
            win.title("Stress Test Confirmation")
            win.grab_set()
            win.resizable(False, False)

            tk.Label(
                win,
                text="Open Phoebus GUI and determine if the current for 0.85V rail is above 5 Amps. (y/n):",
                font=("Arial", 12),
                wraplength=400,
                justify="center"
            ).pack(padx=20, pady=15)

            btn_frame = tk.Frame(win)
            btn_frame.pack(pady=10)

            def yes():
                result["value"] = "y"
                done.set()
                win.destroy()

            def no():
                result["value"] = "n"
                done.set()
                win.destroy()

            tk.Button(
                btn_frame, text="Yes", width=10, command=yes
            ).pack(side="left", padx=10)

            tk.Button(
                btn_frame, text="No", width=10, command=no
            ).pack(side="right", padx=10)

        # Run popup in GUI thread
        self.root.after(0, show_popup)

        done.wait()

        return result["value"]




# ------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    TestGUI(root)

    root.mainloop()
