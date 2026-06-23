import csv
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak, Preformatted
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
import os

###############################################################################################
# Setup Parameters for ACMI Calibration Report (Adjust these Parameters as Needed)
###############################################################################################

Title = 'Results for ZuBPM DFE Verification Report'
ReportDate = '06/01/2026'
Engineer = 'Kato Bouthsarath'

# File Names from the Data Collection Scripts:

test_results = 'test_results.csv'
pwr_measurements = 'power_measurements.csv'

freport = 'DFE_Verification_Report.pdf'

#TEST_COLUMNS = ["PWR_MEAS", "QSPI", "SD", "IP", "TEMP", "IO", "AFE", "STRESS", "IBERT", "DDR"]
TEST_COLUMNS = ["PWR_MEAS", "SD", "IP", "TEMP", "IO", "AFE", "STRESS", "IBERT", "DDR"]

TEST_DESCRIPTION = ["Correct Power Measurements?",
                # "Boot from QSPI?",  # QSPI disabled
                "Boot from SD?",
                "DFE IP address functions correctly?",
                "DFE temperatures stable?",
                "DFE Debug Header, LEDs, LEMO I/Os functions correctly?",
                "ADC bits toggles?",
                "DFE functions properly under stress?",
                "DFE Transceivers work via IBERT?",
                "DFE DDR works properly?"]

TEST_DESCRIPTION_MAP = dict(zip(TEST_COLUMNS, TEST_DESCRIPTION))

PWR_MEAS_REFS = {
    "C1": 0.90,
    "C2": 1.20,
    "C3": 2.50,
    "C4": 2.50,
    "C211": 0.85,
    "C5": 3.30,
    "C73": 1.80,
    "C74": 1.20,
}

report_callback = None
DDR_TEXT_STYLE = ParagraphStyle(
    "DDRTextStyle",
    fontName="Courier",
    fontSize=7,
    leading=8,
    alignment=TA_CENTER,
    leftIndent=54,
    rightIndent=54,
)


def normalize_status(value):
    status = str(value or "").strip().upper()
    if status in ("PASS", "FAIL"):
        return status
    return "-"


def load_board_results(csv_path):
    board_results = {}
    if not os.path.exists(csv_path):
        return board_results

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            board = str(row.get("Board", "")).strip()
            if not board:
                continue

            board_results[board] = {
                "overall": normalize_status(row.get("Overall")),
                "tests": {test: normalize_status(row.get(test)) for test in TEST_COLUMNS},
                "date": str(row.get("Date", "")).strip(),
                "time": str(row.get("Time", "")).strip(),
                "ip": str(row.get("ZYNQ_IP", "")).strip() or "-",
            }

    return board_results


def load_power_measurements(csv_path):
    power_by_board = {}
    if not os.path.exists(csv_path):
        return power_by_board

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            board = str(row.get("Board", "")).strip()
            if not board:
                continue

            measurements = {}
            for tp in PWR_MEAS_REFS:
                raw = row.get(tp, "")
                try:
                    measurements[tp] = float(raw)
                except (TypeError, ValueError):
                    measurements[tp] = None

            power_by_board[board] = measurements

    return power_by_board


def load_summary_rows(board_results):
    rows = []
    for board, info in board_results.items():
        rows.append([board, info.get("overall", "-")])
    return rows


def get_ddr_result_path(board):
    board_text = str(board).strip()
    board_variants = [board_text]
    if board_text.isdigit():
        board_variants.append(f"{int(board_text):02d}")

    base_dir = os.path.dirname(__file__)
    candidates = []
    for board_value in board_variants:
        filename = f"zudfe_s{board_value}_ddr_results.txt"
        candidates.extend([
            os.path.join(base_dir, "ddr_test", "ddr_test_logs", filename),
            os.path.join(base_dir, "ddr_test", "ddr_test_logs", "ddr_test", "ddr_test_logs", filename),
        ])

    for path in candidates:
        if os.path.exists(path):
            return path

    return None


def load_ddr_result_text(board):
    ddr_path = get_ddr_result_path(board)
    if not ddr_path:
        return None, None

    with open(ddr_path) as f:
        return ddr_path, f.read()


def add_status_color(table, row_idx, col_idx, status):
    if status == "PASS":
        table.setStyle(TableStyle([
            ("TEXTCOLOR", (col_idx, row_idx), (col_idx, row_idx), colors.darkgreen),
        ]))
    elif status == "FAIL":
        table.setStyle(TableStyle([
            ("TEXTCOLOR", (col_idx, row_idx), (col_idx, row_idx), colors.red),
        ]))

def generate_report():
    
    if os.path.exists(freport):
        if callable(report_callback):
            overwrite = bool(report_callback(freport))
        else:
            x = input("\n\nFile Exists! Make sure this file is not in use then\nEnter '1' to overwrite or '0' to abort: ").strip()
            overwrite = x == "1"

        if overwrite:
            try:
                os.rename(freport,freport)
                print("Available!")
            except OSError:
                raise RuntimeError(f"{freport} is in use. Please close the file and try again.")
        else:
            return False

    doc = SimpleDocTemplate(freport, pagesize=letter, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
    elements = []

    board_results = load_board_results(test_results)
    summary_rows = load_summary_rows(board_results)
    power_by_board = load_power_measurements(pwr_measurements)

    title_data = [
        [Title],
        ["Analysis Performed on " + ReportDate + " by " + Engineer],
    ]

    title_table = Table(
        title_data,
        colWidths=[6 * inch],
        rowHeights=[0.4 * inch, 0.25 * inch],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.lemonchiffon),
            ("VALIGN", (0, 0), (0, -1), "MIDDLE"),
            ("LINEABOVE", (0, 1), (0, 1), 2, colors.black),
            ("FONTSIZE", (0, 0), (0, 0), 14),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BOX", (0, 0), (-1, -1), 2, colors.black),
        ]),
    )
    elements.append(title_table)
    elements.append(Spacer(1, 0.25 * inch))

    summary_data = [['Summary of Test Results'],
                    ["Board", "Overall"]]
    if summary_rows:
        summary_data.extend(summary_rows)
    else:
        summary_data.append(["-", "No test results found"])

    summary_table = Table(
        summary_data,
        colWidths=[2.2 * inch, 2.2 * inch],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lemonchiffon),
            ("SPAN", (0, 0), (-1, 0)),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BOX", (0, 0), (-1, -1), 2, colors.black),
        ]),
    )

    for row_idx in range(1, len(summary_data)):
        status = str(summary_data[row_idx][1]).upper()
        add_status_color(summary_table, row_idx, 1, status)

    elements.append(summary_table)

    # One detail page per board
    for board, info in board_results.items():
        elements.append(PageBreak())

        board_header_data = [
            [f"Board {board} - Detailed Results"],
            [f"Overall: {info.get('overall', '-')}   Date: {info.get('date', '-')}   Time: {info.get('time', '-')}   IP: {info.get('ip', '-')}"],
        ]
        board_header = Table(
            board_header_data,
            colWidths=[6 * inch],
            rowHeights=[0.35 * inch, 0.25 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), colors.lemonchiffon),
                ("VALIGN", (0, 0), (0, -1), "MIDDLE"),
                ("FONTSIZE", (0, 0), (0, 0), 13),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BOX", (0, 0), (-1, -1), 2, colors.black),
            ]),
        )
        elements.append(board_header)
        elements.append(Spacer(1, 0.15 * inch))

        # Power measurement table (Measured vs Ref)
        pwr_title = Table(
            [["DFE Regulators Voltage Measurements"]],
            colWidths=[4.6 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), colors.lemonchiffon),
                ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (0, 0), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BOX", (0, 0), (-1, -1), 2, colors.black),
            ]),
        )
        elements.append(pwr_title)

        pwr_rows = [["Test Point", "Measured (V)", "Reference (V)"]]
        measurements = power_by_board.get(board, {})
        for tp, ref_v in PWR_MEAS_REFS.items():
            meas_v = measurements.get(tp)
            pwr_rows.append([
                tp,
                "-" if meas_v is None else f"{meas_v:.3f}",
                f"{ref_v:.3f}",
            ])

        pwr_table = Table(
            pwr_rows,
            colWidths=[1.5 * inch, 1.55 * inch, 1.55 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lemonchiffon),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BOX", (0, 0), (-1, -1), 2, colors.black),
            ]),
        )
        elements.append(pwr_table)

        elements.append(Spacer(1, 0.2 * inch))

        # Test status table
        test_data = [["Test", "Description", "Result"]]
        for test_name in TEST_COLUMNS:
            test_data.append([
                test_name,
                TEST_DESCRIPTION_MAP.get(test_name, "-"),
                info.get("tests", {}).get(test_name, "-"),
            ])

        test_table = Table(
            test_data,
            colWidths=[1.2 * inch, 4 * inch, 1.0 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lemonchiffon),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BOX", (0, 0), (-1, -1), 2, colors.black),
            ]),
        )
        for row_idx in range(1, len(test_data)):
            add_status_color(test_table, row_idx, 2, test_data[row_idx][2])

        elements.append(test_table)

        ddr_status = info.get("tests", {}).get("DDR", "-")
        if ddr_status != "-":
            elements.append(Spacer(1, 0.2 * inch))

            ddr_title = Table(
                [["DDR Detailed Results"]],
                colWidths=[6 * inch],
                style=TableStyle([
                    ("BACKGROUND", (0, 0), (0, 0), colors.lemonchiffon),
                    ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (0, 0), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BOX", (0, 0), (-1, -1), 2, colors.black),
                ]),
            )
            elements.append(ddr_title)

            ddr_path, ddr_text = load_ddr_result_text(board)
            if ddr_text:
                elements.append(Spacer(1, 0.1 * inch))
                elements.append(
                    Preformatted(
                        ddr_text,
                        style=DDR_TEXT_STYLE,
                    )
                )

        

    doc.build(elements)
    return True