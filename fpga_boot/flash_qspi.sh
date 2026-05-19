#!/bin/bash
set -e
set -o pipefail

# --------------------------------------------------
# Source Xilinx Vitis environment
# --------------------------------------------------
VITIS_SETTINGS="${VITIS_SETTINGS:-/tools/Xilinx/Vitis/2022.2/settings64.sh}"

if [[ -f "$VITIS_SETTINGS" ]]; then
  source "$VITIS_SETTINGS"
else
  echo "ERROR: Vitis settings file not found at $VITIS_SETTINGS"
  exit 1
fi

# Optional sanity check
if ! command -v program_flash >/dev/null 2>&1; then
  echo "ERROR: program_flash not found even after sourcing Vitis environment"
  exit 1
fi

# --------------------------------------------------
# Existing script logic
# --------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CFG_FILE="${SCRIPT_DIR}/../jtag_ip.cfg"

if [[ ! -f "${CFG_FILE}" ]]; then
  echo "ERROR: Missing JTAG config file: ${CFG_FILE}" >&2
  exit 1
fi

JTAG_IP="$(tr -d '[:space:]' < "${CFG_FILE}")"
if [[ -z "${JTAG_IP}" ]]; then
  echo "ERROR: JTAG IP is empty in ${CFG_FILE}" >&2
  exit 1
fi

program_flash \
  -f "${SCRIPT_DIR}/BOOT.bin" \
  -offset 0 \
  -flash_type qspi-x4-dual_stacked \
  -fsbl "${SCRIPT_DIR}/fsbl.elf" \
  -url "TCP:${JTAG_IP}:3121"
