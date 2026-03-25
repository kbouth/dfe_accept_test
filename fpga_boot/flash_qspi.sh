#!/bin/bash
set -e
set -o pipefail

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
